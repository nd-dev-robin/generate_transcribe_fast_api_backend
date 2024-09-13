
from config import s3_client,aws_bucket
from fastapi import HTTPException
import os

def download_audio_from_s3(file_key):
    print(f"file name ============= {file_key}")
    try:
        # Define the local path where the file will be saved
        local_path = os.path.join('audio', file_key.split('/')[-1])
        
        # Ensure the 'audio' directory exists
        os.makedirs('audio', exist_ok=True)
        print("//////////////////////////////")
        # Download the file from S3
        bucket_name = aws_bucket
        s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_stream = s3_response['Body'].read()
        
        # Save the file to the local directory
        with open(local_path, 'wb') as f:
            f.write(file_stream)
        
        # Return a success message with the local path
        return local_path
        
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

