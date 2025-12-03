#!/usr/bin/env Rscript

source('~/detachAllPackages.R')

setwd('~/Projects/apostles/')

library('tidyverse')
library('ggplot2')
library('plotly')

fit.shape <- readRDS('derived_data/fit.rds')$estimate[['shape']]
fit.scale <- readRDS('derived_data/fit.rds')$estimate[['scale']]

df <- read_csv('raw_data/apostles_all.csv')

dates <- c(seq(as.Date(paste0(year(min(df$dateOrdained)) + 1, '-01-01')),
               as.Date(paste0(year(Sys.Date()), '-01-01')), by = 'year'),
           unique(df$dateCalled), unique(df$outDate), unique(df$deathDate),
           unique(df$outDate - 1), unique(df$deathDate - 1),
           Sys.Date()) %>% sort %>% unique

all <- df %>%
  mutate(dummy = 1,
         dateRelease = as.Date(ifelse(!is.na(outDate), outDate,
                               ifelse(!is.na(deathDate), deathDate,
                               Sys.Date())))) %>%
  left_join(tibble(d = dates, dummy = 1), by = c('dummy')) %>%
  arrange(seniority, d) %>%
  mutate(active = dateCalled <= d & dateRelease > d) %>%
  select(-dummy) %>% filter(active) %>% arrange(d, seniority) %>%
  mutate(age = as.numeric(difftime(d, birthDate, units = 'days') / 365.25)) %>%
  select(name, birthDate, dateCalled, d, age, seniority) %>%
  arrange(d, seniority) %>%
  group_by(d) %>%
  mutate(position = row_number()) %>%
  ungroup()

slots <- expand_grid(d = unique(all$d), position = unique(all$position))

all <- slots %>% left_join(all, by = c('d', 'position'))

get_death_age <- function(age, fit.shape, fit.scale) {
  p1 <- pweibull(age, fit.shape, fit.scale)
  n <- runif(length(age))
  p2 <- n * (1-p1) + p1
  death_age <- qweibull(p2, fit.shape, fit.scale)
  return(death_age)
}

temp_df <- all %>% filter(d >= '1800-01-01') %>%
  uncount(10000, .id = 'sim_number') %>%
  arrange(d, sim_number, position) %>%
  mutate(death_age = get_death_age(age, fit.shape, fit.scale)) %>%
  mutate(death_date = birthDate + death_age * 365.25)

x <- matrix(temp_df$death_date, ncol = 17, byrow = T)
y <- matrix(T, nrow = nrow(x), ncol = ncol(x))
y[, 2] <- x[, 2] > x[, 1]
for (i in 3:17) y[, i] <- apply(x[, i] > x[, 1:(i-1)], 1, all)

temp_df$prophet <- c(t(y))

rm(x)
rm(y)

temp_df <- temp_df %>%
  group_by(d, position, name, birthDate, dateCalled, age, seniority) %>%
  summarize(death_age = mean(death_age),
            prophet_prob = sum(prophet) / 10000) %>%
  ungroup()

p <- ggplot(temp_df, aes(x = d, y = prophet_prob, group = name, color = name)) +
  geom_line() +
  scale_x_date(date_labels = '%Y') +
  scale_y_continuous(labels = scales::percent) +
  labs(x = 'Year', y = 'Prophet Probability') +
  theme_light() +
  theme(legend.position = "none")
ggplotly(p)
