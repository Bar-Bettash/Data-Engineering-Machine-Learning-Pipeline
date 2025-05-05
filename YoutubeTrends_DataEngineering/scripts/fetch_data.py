import os
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

def fetch_trending_data():
    # Ensure the destination directory exists
    os.makedirs("data", exist_ok=True)

    # Set the Kaggle config path to use your .kaggle folder
    os.environ['KAGGLE_CONFIG_DIR'] = "/root/.kaggle"



    # Authenticate and initialize the Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Download and unzip the YouTube trending dataset
    api.dataset_download_files('datasnaek/youtube-new', path='data', unzip=True)

    # Load a specific country's file — e.g., US trending videos
    df = pd.read_csv('data/USvideos.csv')

    # Save it as a standardized file name
    df.to_csv('data/youtube_trending.csv', index=False)

    print("✅ Trending data fetched and saved to 'data/youtube_trending.csv'")

if __name__ == "__main__":
    fetch_trending_data()
