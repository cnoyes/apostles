#!/usr/bin/env Rscript
# Calculate succession probabilities for each apostle
# Uses Monte Carlo simulation (100,000 runs) to estimate the probability
# that each apostle becomes prophet by outliving those senior to them

library('dplyr')

# Function to calculate death age based on current age and
# fitted Weibull death curve
get_death_age <- function(age, fit.shape, fit.scale) {
  
  # get density of current age
  p1 <- pweibull(age, fit.shape, fit.scale)
  
  # take random sample (will be probability sample)
  n <- runif(length(age))
  
  # shift probability sample to be greater than current density
  p2 <- n * (1-p1) + p1
  
  # calculate death age based on sampled probability
  death_age <- qweibull(p2, fit.shape, fit.scale)
  return(death_age)
}

apostles <- readRDS('derived_data/apostles.rds')
fit <- readRDS('derived_data/fit.rds')
fit.shape <- fit$estimate[['shape']]
fit.scale <- fit$estimate[['scale']]
num_apostles <- nrow(apostles)
num_sims <- 100000

# Repeat each row 100,000 times and simulate a new "Death Date" for each apostle
simulation_df <- apostles %>% mutate(Position = row_number()) %>%
  uncount(num_sims, .id = 'Sim Number') %>%
  arrange(`Sim Number`, Position) %>%
  mutate(`Death Age` = get_death_age(Age, fit.shape, fit.scale)) %>%
  mutate(`Death Date` = `Birth Date` + `Death Age` * 365.25)

# Transform "Death Date" into matrix where each row represents
# one simulation and each column represents one of the apostles
death_date_matrix <- matrix(simulation_df$`Death Date`,
                            ncol = num_apostles, byrow = T)

# create "prophet" matrix where each row represents
# one simulation and each column is T/F for whether that apostle became prophet
prophet_matrix <- matrix(NA, nrow = nrow(death_date_matrix),
                         ncol = ncol(death_date_matrix))

# compare each column to see if apostle outlives higher ranking apostles
prophet_matrix[, 2] <- death_date_matrix[, 2] > death_date_matrix[, 1]
for (i in 3:num_apostles) prophet_matrix[, i] <- apply(death_date_matrix[, i] > death_date_matrix[, 1:(i-1)], 1, all)

# convert results back to simulation data frame
simulation_df$Prophet <- c(t(prophet_matrix))

rm(death_date_matrix)
rm(prophet_matrix)

# summarize simulation results
apostles_with_prob <- simulation_df %>%
  group_by(Position, First, Middle, Last, `Birth Date`, `Ordained Apostle`, `Age`) %>%
  summarize(Prob = sum(Prophet) / num_sims) %>%
  ungroup() %>%
  arrange(Position) %>%
  dplyr::select(-Position)

saveRDS(apostles_with_prob, 'derived_data/apostles_with_prob.rds')

last_update <- Sys.Date()
saveRDS(last_update, 'derived_data/last_update.rds')

message("✓ Completed ", format(num_sims, big.mark = ","), " simulations for ",
        num_apostles, " apostles")
message("✓ Results saved to derived_data/apostles_with_prob.rds")
