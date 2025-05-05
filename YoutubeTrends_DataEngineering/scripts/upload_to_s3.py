import boto3
import os

# Load AWS credentials from environment or ~/.aws/credentials
s3 = boto3.client('s3')

# Upload local file to S3 bucket
s3.upload_file(
    Filename='data/youtube_trending.csv',
    Bucket='youtube-trending-data-pipeline',
    Key='youtube_trending.csv'
)

print("✅ Uploaded to S3.")

