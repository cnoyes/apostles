#!/usr/bin/env Rscript
# Master script to run all data processing steps
# Run this script from the project root directory to regenerate all derived data

cat("\n========================================\n")
cat("Apostles Prophet-ability Calculator\n")
cat("Data Processing Pipeline\n")
cat("========================================\n\n")

# Ensure we're in the project root directory
# (assumes script is run from project root)

# Step 1: Load apostles data
cat("Step 1/4: Loading apostles data...\n")
source("src/1_load_apostles.R")

cat("\n")

# Step 2: Fit mortality curve
cat("Step 2/4: Fitting mortality curve to CDC data...\n")
source("src/2_fit_death_curve.R")

cat("\n")

# Step 3: Calculate succession probabilities (this takes ~30 seconds)
cat("Step 3/4: Running Monte Carlo simulations...\n")
cat("(This may take 30-60 seconds)\n")
source("src/3_calculate_prophet.R")

cat("\n")

# Step 4: Create plots
cat("Step 4/4: Creating plot functions...\n")
source("src/4_make_plots.R")

cat("\n========================================\n")
cat("✓ All processing complete!\n")
cat("Run the Shiny app with: Rscript app.R\n")
cat("========================================\n\n")
