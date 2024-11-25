# Bayesian Analysis of F1 Driver Positions (2022-2024 Hybrid Era)

## Project Overview

This project aims to conduct a Bayesian analysis of Formula 1 driver positions during the 2022-2024 hybrid era. Using advanced statistical models, we predict race outcomes by analyzing factors such as qualifying performance, weather conditions, and car/team contributions. This provides insights into driver and constructor performance, while identifying trends in this highly competitive sport.

## Goals and Use Cases

- **Analysis and Prediction**: Identify key factors affecting driver performance and predict future race results.
- **Team Strategy**: Enhance team preparation and decision-making for upcoming races.
- **Education**: Aid new team members and enthusiasts in understanding race dynamics.
- **Betting**: Provide accurate predictions to assist betting strategies.
- **Regulation Impact**: Evaluate how FIA regulations influence race outcomes and improve fan experiences.

## Data

The dataset integrates:
- **Race Results (2022-2024)**: Driver positions, times, and points.
- **Qualifying and Practice Sessions**: Session results, times, and gaps.
- **Weather Data**: Metrics such as temperature, rainfall, and wind conditions.

Data sources include the official Formula 1 website and the FastF1 API.

### Selected Features
Key features for the analysis:
- Year, race, driver, car/team.
- Final race position, qualifying position.
- Weather variables: average track temperature, rainfall.

## Models

We developed three Bayesian models to analyze race results:

1. **Model 1**: Baseline model considering driver and constructor performance.
2. **Model 2**: Adds weather factors (e.g., rainfall, track temperature).
3. **Model 3**: Incorporates qualifying positions and their impact on race outcomes.

### Model Comparison

- **Model 1**: Best predictive performance (based on WAIC).
- **Model 2**: Improved accuracy in variable conditions (e.g., wet weather).
- **Model 3**: Most comprehensive, including qualifying dynamics, but slightly less precise than Model 1.

## Libraries and Tools

The project employs:
- **Statistical Framework**: `cmdstanpy`, `arviz`, `numpy`, and `scipy`.
- **Data Manipulation and Visualization**: `pandas`, `matplotlib`, `seaborn`.
- **APIs**: Data retrieval from FastF1.

## Results

- Drivers with high skill coefficients: Lewis Hamilton, George Russell, Charles Leclerc, Max Verstappen.
- Top-performing constructors: Red Bull Racing RBPT, Ferrari, McLaren Mercedes.
- Model 3 effectively captures qualifying's influence but is slightly outperformed by Model 1 in predictive accuracy.

## Usage

1. Install dependencies listed in `requirements.txt`.
2. Prepare data using the provided preprocessing scripts.
3. Run Bayesian models using `cmdstanpy` scripts for posterior analysis.
4. Visualize results with the included plotting utilities.

## Future Work

- Extend analysis to include post-2024 seasons.
- Refine models to better handle outlier performances.
- Explore additional data sources for richer context.

## Authors

Andrzej Janik, Łukasz Gakan  
*Data Analytics 2024, Automatic Control and Robotics - Computer Science in Control and Management*
