from DataWorks.logger import logging
from dataclasses import dataclass
from DataWorks.api.FromEmailExtractor import FromEmailExtractor
@dataclass
class SenderEmailExtractor:
    input_file:str
    output_file:str

    def extract(self):
        with open(self.input_file, "r") as f:
            email_text = f.read()

        sender_email = FromEmailExtractor(email_text).extract_from_email()

        with open(self.output_file, "w") as f:
            f.write(sender_email)

        logging.info(f"Successfully extracted sender email: {sender_email}")
