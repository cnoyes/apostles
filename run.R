#!/usr/bin/env Rscript

source('~/detachAllPackages.R')

setwd('~/Projects/apostles/')

source('src/1_load_apostles.R')
source('src/2_fit_death_curve.R')
source('src/3_calculate_prophet.R')
source('src/4_make_plots.R')
source('src/5_deploy_app.R')

