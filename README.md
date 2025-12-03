# Apostles Prophet-ability Calculator

An interactive R Shiny application that calculates and visualizes the probability of each apostle of The Church of Jesus Christ of Latter-day Saints becoming prophet, based on actuarial life expectancy data and succession order.

## Overview

This app uses Monte Carlo simulation (100,000 runs) to estimate the probability that each apostle will eventually become prophet by outliving those senior to them in the Quorum of the Twelve. The simulation is based on:

- Current ages of apostles
- Ordination dates (which determine succession order)
- Weibull distribution fitted to CDC mortality data

## Features

- **Interactive visualizations**: Click on any apostle's bar to highlight them across both charts and see detailed information
- **Current age chart**: Shows the current age of each apostle, ordered by seniority
- **Succession probability chart**: Displays the estimated probability of becoming prophet
- **Detailed information panel**: Shows birth date, ordination date, years in quorum, seniority, and Wikipedia link for selected apostles

## Project Structure

```
├── app.R                  # Main Shiny application (interactive UI)
├── run_all.R             # Master script to regenerate all derived data
├── raw_data/
│   ├── apostles.csv      # List of apostles with birth and ordination dates
│   └── Table05.csv       # CDC life table mortality data
├── src/
│   ├── 1_load_apostles.R          # Load and process apostle data
│   ├── 2_fit_death_curve.R        # Fit Weibull distribution to mortality data
│   ├── 3_calculate_prophet.R     # Run Monte Carlo simulations
│   └── 4_make_plots.R            # Create plotting functions
└── derived_data/         # Generated files (RDS format)
```

## Installation

### Prerequisites

You need R (version 4.0+) with the following packages:

```r
install.packages(c(
  "shiny",
  "bslib",
  "tidyverse",
  "scales",
  "plotly",
  "glue",
  "MASS"
))
```

### Setup

1. Clone this repository
2. Navigate to the project directory
3. Run the data processing pipeline:

```bash
Rscript run_all.R
```

This will:
- Load apostle data from `raw_data/apostles.csv`
- Fit a Weibull distribution to CDC mortality data
- Run 100,000 Monte Carlo simulations
- Generate derived data files needed by the app

## Usage

### Running the App Locally

```bash
Rscript app.R
```

The app will start on `http://0.0.0.0:8080` and can be accessed from your web browser.

### Updating Apostle Data

To update the list of apostles:

1. Edit `raw_data/apostles.csv` to add/update apostle information
2. Re-run the data processing pipeline:

```bash
Rscript run_all.R
```

3. Restart the Shiny app

The CSV format is:
```csv
Name,Birth Date,Ordained Apostle
First Middle Last,YYYY-MM-DD,YYYY-MM-DD
```

## Methodology

### Mortality Modeling

The app uses CDC life table data (Table05.csv) to fit a Weibull distribution that models mortality rates. This distribution is then used to simulate life expectancy for each apostle based on their current age.

### Succession Probability Calculation

For each of 100,000 simulations:
1. A death age is sampled for each apostle using the Weibull distribution
2. The simulation determines which apostle becomes prophet by checking who outlives all those senior to them
3. Results are aggregated to calculate the probability for each apostle

The probability shown represents the percentage of simulations in which each apostle becomes prophet.

## Data Sources

- **Apostle Information**: Publicly available data from The Church of Jesus Christ of Latter-day Saints
- **Mortality Data**: CDC National Vital Statistics Reports life tables

## Deployment

### Shiny Server / shinyapps.io

The app is configured to run on port 8080. For deployment to ShinyApps.io or other hosting platforms:

1. Ensure all derived data files are generated (`run_all.R`)
2. Deploy using the `rsconnect` package or ShinyApps.io interface

## License

This project is for educational and informational purposes only. Succession probabilities are statistical estimates based on actuarial data and do not represent official predictions or doctrine.

## Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Updates

Last data update: Run `Rscript run_all.R` to regenerate with current dates

## Author

Created with Claude Code
