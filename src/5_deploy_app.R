#!/usr/bin/env Rscript

source('~/detachAllPackages.R')

setwd('~/Projects/apostles/')

library('rsconnect')

files <- c('app.R', 'run.R', 'raw_data/apostles.csv', 'raw_data/Table05.csv',
           'src/1_load_apostles.R', 'src/2_fit_death_curve.R',
           'src/3_calculate_prophet.R', 'src/4_make_plots.R',
           'src/5_deploy_app.R', 'derived_data/')

deployApp(launch.browser = F, forceUpdate = T, appFiles = files)

