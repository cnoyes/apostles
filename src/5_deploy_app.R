#!/usr/bin/env Rscript
# Deploy app to shinyapps.io
# Ensure you have run run_all.R before deploying to generate derived data

library('rsconnect')

cat("========================================\n")
cat("Deploying to shinyapps.io\n")
cat("========================================\n\n")

# Check that derived data exists
if (!dir.exists('derived_data')) {
  stop("derived_data/ directory not found! Run 'Rscript run_all.R' first.")
}

required_files <- c(
  'derived_data/apostles_with_labels.rds',
  'derived_data/last_update.rds'
)

for (f in required_files) {
  if (!file.exists(f)) {
    stop("Required file not found: ", f, "\nRun 'Rscript run_all.R' first.")
  }
}

# Deploy app with all necessary files
deployApp(
  launch.browser = FALSE,
  forceUpdate = TRUE,
  appFiles = c('app.R', 'derived_data/')
)

cat("\n✓ Deployment complete!\n")
cat("Visit: https://claynoyes.shinyapps.io/apostles/\n")

