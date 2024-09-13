from fastapi import APIRouter,HTTPException,Path
from fastapi.responses import StreamingResponse
import boto3
import os
from dotenv import load_dotenv
from routers.utils.download_audio import download_audio_from_s3
from routers.utils.transcribe_audio import transcribe_audio_with_openai
from response.responses import HTTP_200,HTTP_400,HTTP_404,HTTP_401,HTTP_500


# Load environment variables from .env file
load_dotenv()

router = APIRouter()

@router.post("/generate_transcribe/{file_key}/{identifier}/")
def download_file(
    file_key: str = Path(..., description="The key of the file to be downloaded from S3"),
    identifier: str = Path(..., description="The identifier for the file, e.g., aws/openai")
):
    """
    # Generate Transcribe
    ## Description:
    * This endpoint is used to download a file from S3 bucket and generate  a transcription.
    ## Request and Response: 
    * Request: Handle a POST method to ownload a file from S3 bucket and transcribe the auido to text.
    * Response: Return a StreamingResponse object with the downloaded file.
    ## Parameters:
    ### - Path Parameters:  
    * file_key: The key of the file in the S3 bucket.
    ### - Body Parameters:  
    * NA.
    
    """
    
    # Checking file key is present in path params
    if not file_key:
        return HTTP_404(details={"file_key":"File key is missing."})
    
    # Checking  identifier is present in path params
    if not identifier:
        return HTTP_404(details={"identifier":"Identifier is missing."})
    
    
    
    identifier_list = ["aws","openai"]
    if identifier not in identifier_list:
        return HTTP_404(details={"identifier":"Invalid identifier,identifiers must be 'openai' or 'aws'."})
    
    print("??????????????????????????????????????????????")
    
    # Download file from s3 bucket and return file path
    if identifier  == "openai":
        try:
            file_path = download_audio_from_s3(file_key)
        except Exception as e:
            raise HTTPException(status_code=404, detail=e)
        chat_response = transcribe_audio_with_openai(file_path)
        
    if identifier == "aws":
        chat_response = "Integration of aws is not done yet.Please try with  openai until we finish  the integration."
    return HTTP_200(data=chat_response)


    

    
    
    
