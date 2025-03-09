from urllib.parse import quote_plus
from dotenv import load_dotenv
import requests
import os

load_dotenv() # Access .env file

URL_ENDPOINT = "http://api.voicerss.org/?"
API_KEY = os.getenv("API_Key")
FILE_PATH = "../voiceover.mp3"

def voice_2_text(input_text, language):
    encoded_text = quote_plus(input_text) # URL encode the text to ensure it's safe for use in the URL
    url = f"{URL_ENDPOINT}key={API_KEY}&hl={language}&c=MP3&src={encoded_text}"
    response = requests.get(url)

    # If the response is successful, receive an audio file in MP3 format
    if response.status_code == 200:

        # Check if the response is an MP3 file by looking at the Content-Type header
        if 'audio/mpeg' not in response.headers['Content-Type']:
            raise Exception("Received file is not a valid MP3.")

        # Save the audio response as a file
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)  # Remove the old file if it exists

        with open(FILE_PATH, "wb") as file:
            file.write(response.content)

        return FILE_PATH

    else:
        raise Exception("API request failed")