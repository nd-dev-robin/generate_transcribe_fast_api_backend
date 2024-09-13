

import os
import math
from pydub import AudioSegment
import openai
from config import OPENAI_KEY
from response.responses import HTTP_200,HTTP_400,HTTP_401,HTTP_404,HTTP_500
import json

# Set your OpenAI API key

openai.api_key = OPENAI_KEY


# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    print(f"open ai key ==================================== {OPENAI_KEY}")
    try:
        with open(file_path, 'rb') as audio_file:
            response = openai.audio.transcriptions.create(
                model='whisper-1',                                      
                file=audio_file,
                response_format='srt'
            )
            return response if isinstance(response, str) else response.get('text')
    except Exception as e:
        raise ValueError(f"An error occurred during transcription: {e}")
        # return HTTP_500(str(e))
        # return HTTP_400(details={"transcribe_audio":f"An error occurred during transcription: {e}"})

# Function to identify speakers and format conversation
def identify_speakers(transcribed_text):
    if not transcribed_text:
        print("No transcribed text available for speaker identification.")
        return None

    prompt = (
        "The following is a transcription of a conversation between multiple speakers. "
        "you will always respond in JSON."
        "Identify each speaker and format the text as a dialogue with speaker labels and timestamps.\n\n"
        f"Transcribed Text:\n{transcribed_text}\n\nFormatted Conversation:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that can identify speakers in a conversation and format the text with speaker labels and you will always respond in JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.5,
            # response_format={ "type": "json_object" }
           
        )
        formatted_conversation = response.choices[0].message.content.strip()
        return formatted_conversation
    except Exception as e:
        return HTTP_400(details={"identify_speakers"f"An error occurred during speaker identification: {e}"})

# Function to split audio if larger than 20 MB
def split_audio_if_large(file_path, chunk_size_mb=20):
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
    if file_size <= chunk_size_mb:
        return [file_path]  # No need to split

    # Load audio with pydub
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)  # Get the duration in milliseconds

    # Calculate how many chunks are needed based on the file size
    total_chunks = math.ceil(file_size / chunk_size_mb)
    chunk_duration_ms = duration_ms / total_chunks  # Duration per chunk

    # Split the audio into smaller chunks
    audio_chunks = []
    for i in range(total_chunks):
        start_time = i * chunk_duration_ms
        end_time = (i + 1) * chunk_duration_ms
        chunk = audio[start_time:end_time]
        chunk_path = f"chunk_{i + 1}.mp3"
        chunk.export(chunk_path, format="mp3")
        audio_chunks.append(chunk_path)

    return audio_chunks


def transcribe_audio_with_openai(file_path):
    audio_file_path = file_path

    # Step 1: Split the audio if needed
    audio_chunks = split_audio_if_large(audio_file_path, chunk_size_mb=20)

    full_transcription = ""

    # Step 2: Transcribe each chunk
    for chunk_path in audio_chunks:
        transcribed_text = transcribe_audio(chunk_path)
        if transcribed_text:
            full_transcription += transcribed_text
        else:
            return HTTP_400(details={"non_binary_error":f"Failed to transcribe chunk: {chunk_path}"})


    # Step 3: Identify speakers and format conversation
    if full_transcription:
        formatted_conversation = identify_speakers(full_transcription)
        if formatted_conversation:
            data = {"transcribed_text":transcribed_text,"chat":formatted_conversation}
            return data
        else:
            return HTTP_400(details={"non_binary_error":"Failed to identify speakers."})
    else:
        return HTTP_400(details={"non_binary_error":"No transcription available."})

    
    