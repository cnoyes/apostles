#!/usr/bin/env Rscript
# Load and process apostles data from CSV
# Calculates current age based on birth date

library('readr')
library('tidyr')
library('dplyr')

# Load apostles data and calculate ages
apostles <- read_csv('raw_data/apostles.csv') %>%
  separate_wider_delim(Name, delim = " ", names = c('First', 'Middle', 'Last')) %>%
  mutate(Age = as.numeric(difftime(Sys.Date(), `Birth Date`, units = "days")) / 365.25)

# Preserve original order by last name
apostles$Last <- factor(apostles$Last, levels = apostles$Last)

# Save processed data
saveRDS(apostles, 'derived_data/apostles.rds')
message("✓ Loaded ", nrow(apostles), " apostles and saved to derived_data/apostles.rds")
