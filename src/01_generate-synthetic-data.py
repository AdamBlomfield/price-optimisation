# 01_data-generation.py
"""
Script for generating synthetic pricing and sales data for the price optimization project.
"""

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Library Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from utils import create_logger

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dynamically get the script name using Path
SCRIPT_NAME = Path(__file__).stem

# Create logger for this script
log = create_logger(SCRIPT_NAME)

# Ensure reproducibility
np.random.seed(1)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_output_directories():
    """
    Create necessary directories for saving data and visualizations.
    """
    try:
        log.info("Creating output directories")
        os.makedirs('data/raw', exist_ok=True)
        os.makedirs('artifacts/charts', exist_ok=True)
        log.info("\tOutput directories created successfully")
    except Exception as e:
        log.error(f"\tFailed to create output directories: {e}")
        raise

def generate_synthetic_data():
    """
    Generate synthetic pricing and sales data.
    """
    try:
        log.info(f"Generating synthetic data")
        
        # Set parameters
        # Create exponential distribution of prices
        n = 100
        price = np.sort(
            np.random.exponential(
                scale=100, 
                size=n)
            )
        
        # Create linear relationship between price and quantity
        #   quantity = 1000 - 5 * price + noise
        #   noise is normally distributed with mean 0 and standard deviation 50
        quantity = 1000 - 5 * price + np.random.normal(loc=0, 
                                                        scale=50, 
                                                        size=n)
        # clip the noise to make sure it's never negative
        quantity = quantity.clip(min=0)

        # Add outliers
        n_outliers = 10
        outlier_prices = np.random.uniform(low=5, high=50, size=n_outliers) # Prices between 5 and 50
        outlier_quantity = 1100 + np.random.normal(loc=0, scale=50, size=n_outliers)
        price = np.concatenate([price, outlier_prices])
        quantity = np.concatenate([quantity, outlier_quantity])

        # Add outliers
        n_outliers = 10
        outlier_prices = np.random.uniform(low=51, high=100, size=n_outliers)
        outlier_quantity = 900 + np.random.normal(loc=0, scale=50, size=n_outliers)
        price = np.concatenate([price, outlier_prices])
        quantity = np.concatenate([quantity, outlier_quantity])

        # Create DataFrame
        df = pd.DataFrame({'Price': price, 'Quantity': quantity})

        # Filter out prices < 5
        df = df[df['Price'] >= 5]
        
        log.info("\tSynthetic data generation completed")
        return df
    except Exception as e:
        log.error(f"\tError in generating synthetic data: {e}")
        raise

def visualize_data_distribution(df):
    """
    
    """
    try:
        log.info("Creating data distribution visualizations")

        # Visualize data distribution
        plt.figure(figsize=(12, 6))
        plt.scatter(df['Price'], df['Quantity'], alpha=0.5)
        plt.xlabel('Price')
        plt.ylabel('Quantity')
        plt.title('Data Distribution')
        fig_filepath='artifacts/charts/raw_data_distribution.png'
        plt.savefig(fig_filepath)
        
        log.info(f"\tData distribution visualizations saved to {fig_filepath}")
    except Exception as e:
        log.error(f"\tError in creating visualizations: {e}")
        raise

def save_generated_data(df):
    """
    Save the generated dataset to a CSV file.
    
    Args:
    df (pandas.DataFrame): Dataset to be saved
    """
    try:
        # Save to CSV
        output_path = 'data/raw/synthetic_pricing_data.csv'
        df.to_csv(output_path, index=False)
        log.info(f"Data saved to {output_path}")
    except Exception as e:
        log.error(f"Error saving data: {e}")
        raise

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Execution Block
if __name__ == '__main__':
    try:
        # Log start of script
        log.info("Starting data generation script")
        
        # Set up output directories
        create_output_directories()
        
        # Generate synthetic data
        synthetic_data = generate_synthetic_data()
        
        # Visualize data distribution
        visualize_data_distribution(synthetic_data)
        
        # Save generated data
        save_generated_data(synthetic_data)
        
        log.info("Data generation completed successfully")
    except Exception as e:
        log.critical(f"Script execution failed: {e}")