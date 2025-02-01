import os
import requests
import logging
from dataclasses import dataclass

@dataclass
class OpenAITranscriber:
    input_path: str
    output_text_path: str
    api_key: str = os.environ.get("AIPROXY_TOKEN")

    def transcribe(self) -> bool:
        logging.info(f"Transcribing audio file: {self.input_path}")

        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        with open(self.input_path, "rb") as audio_file:
            files = {"file": audio_file, "model": "whisper-1"}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()

        transcription = response.json().get("text", "")
        with open(self.output_text_path, "w") as output_file:
            output_file.write(transcription)

        logging.info(f"Audio transcribed and saved to {self.output_text_path}")
        return True
