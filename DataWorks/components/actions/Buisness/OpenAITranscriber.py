import logging
from dataclasses import dataclass
from DataWorks.api.AudioTranscriber import AudioTranscriber


@dataclass
class OpenAITranscriber:
    input_path: str
    output_text_path: str

    def transcribe(self) -> bool:
        logging.info(f"Transcribing audio file: {self.input_path}")

        with open(self.input_path, "rb") as audio_file:
            transcription = AudioTranscriber(audio_file).transcribe()
            with open(self.output_text_path, "w") as output_file:
                output_file.write(transcription)

        logging.info(f"Audio transcribed and saved to {self.output_text_path}")
        return True
