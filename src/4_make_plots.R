#!/usr/bin/env Rscript
# Create plotting functions and format labels for the Shiny app

library(ggplot2)
library(dplyr)
library(scales)

PlotAge <- function(apostles_with_labels) {
  
  ggplot(apostles_with_labels, aes(x = Last, y = Age, label = `Age Label`)) +
    geom_bar(stat = "identity", fill = 'darkblue') +
    geom_text(nudge_y = 2) +
    labs(x = "", y = "Age", title = "Ages of the Apostles") +
    coord_cartesian(ylim = c(50, 105)) +
    theme_minimal(base_size = 14) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          axis.text.y = element_blank(),
          panel.grid = element_blank())
}

PlotProb <- function(apostles_with_labels) {
  
  ggplot(apostles_with_labels,
         aes(x = Last, y = Prob, label = `Prob Label`)) +
    geom_bar(stat = "identity", fill = 'darkblue') +
    geom_text(nudge_y = .02) +
    labs(x = "", y = "Probability", title = "Probability of Becoming Prophet") +
    scale_y_continuous(labels = scales::percent) +
    theme_minimal(base_size = 14) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          axis.text.y = element_blank(),
          panel.grid = element_blank())
}

apostles_with_labels <- readRDS('derived_data/apostles_with_prob.rds') %>%
  mutate(`Age Label` = floor(Age),
         `Prob Label` = scales::percent(round(Prob, 2)))
apostles_with_labels$Last <- factor(apostles_with_labels$Last,
                                    levels = apostles_with_labels$Last)

saveRDS(apostles_with_labels, 'derived_data/apostles_with_labels.rds')
saveRDS(PlotAge, 'derived_data/PlotAge.rds')
saveRDS(PlotProb, 'derived_data/PlotProb.rds')

message("✓ Created plot functions and labels")
