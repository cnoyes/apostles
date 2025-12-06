#!/usr/bin/env Rscript
# Fit a Weibull distribution to CDC mortality data
# This is used to simulate life expectancy for apostles

library('MASS')
library('ggplot2')
library('dplyr')

# Load CDC life table data
data <- read.csv(file = "raw_data/Table05.csv", stringsAsFactors = F)

death_df <- tibble(`Death Age` = rep(data$Age..years. + 0.5,
                                     data$Number.dying.between.ages.x.and.x...1))

ggplot(data, aes(x = `Age..years.`, y = `Number.dying.between.ages.x.and.x...1`)) +
  geom_bar(stat = 'identity')

ggplot(death_df, aes(x = `Death Age`)) + geom_density()

min <- 50
max <- 101
age <- data[, 1] + .5
deaths <- data[, 4]
raw <- rep(age, deaths)
ind <- age > min & age < max
fit.age <- age[ind]
fit.deaths <- deaths[ind]
fit.raw <- raw[raw > min & raw < max]

fit <- fitdistr(fit.raw, "weibull")
fit.shape <- fit$estimate['shape']
fit.scale <- fit$estimate['scale']

plot(age, dweibull(age, fit.shape, fit.scale), col = 'blue',
     type = 'l', ylab = "Probability Density",
     main = "Mortality Curve\nCDC Life Table and Weibull Fit")
lines(density(raw), col = 'black')

saveRDS(fit, 'derived_data/fit.rds')
message("✓ Fitted Weibull distribution to mortality data (shape=",
        round(fit.shape, 2), ", scale=", round(fit.scale, 2), ")")

