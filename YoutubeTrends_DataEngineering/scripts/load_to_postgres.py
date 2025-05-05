import pandas as pd
from sqlalchemy import create_engine

# Load the cleaned CSV
df = pd.read_csv("data/youtube_trending.csv")

# Create a SQLAlchemy engine
engine = create_engine("postgresql://user:password@localhost:5432/youtube")

# Load into PostgreSQL
df.to_sql("trending_videos", engine, if_exists="replace", index=False)

print("✅ Data loaded into PostgreSQL.")
