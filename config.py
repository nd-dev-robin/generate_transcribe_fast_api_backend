from dotenv import load_dotenv
import os
import boto3
# Load environment variables from .env file
load_dotenv()

OPENAI_KEY=os.getenv("OPENAI_KEY")

# Get AWS credentials and region from environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
aws_bucket=os.getenv("AUDIO_FILES_BUCKET")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Open api key file

