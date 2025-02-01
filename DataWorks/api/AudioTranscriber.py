from dataclasses import dataclass
from io import BufferedReader
import requests
import os

@dataclass
class AudioTranscriber:
    audio_file:BufferedReader
    def transcribe(self):
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}"}

        files = {"file": self.audio_file, "model": "whisper-1"}
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()

        return response.json().get("text", "")