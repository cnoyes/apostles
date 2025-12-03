#!/usr/bin/env Rscript

library('shiny')
library('ggplot2')
library('tidyverse')

PlotAge <- readRDS('derived_data/PlotAge.rds')
PlotProb <- readRDS('derived_data/PlotProb.rds')
apostles_with_labels <- readRDS('derived_data/apostles_with_labels.rds')
last_update <- readRDS('derived_data/last_update.rds')

ui <- fluidPage(
  titlePanel("Prophet-ability Calculator"),
  h3("Probability of Becoming Prophet Based on Apostle Age"),
  mainPanel(
    h3(paste0("Current Apostles as of ", format(last_update, '%b %d, %Y'))),
    plotOutput("plot_age"),
    plotOutput("plot_prob")
  )
)

server <- function(input, output) {
  
  output$plot_age <- renderPlot({
    PlotAge(apostles_with_labels)
  })
  
  output$plot_prob<- renderPlot({
    PlotProb(apostles_with_labels)
  })
}

shinyApp(ui = ui, server = server)
