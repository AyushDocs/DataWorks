from DataWorks.logger import logging
from DataWorks.api.OCR import OCR
import os
import re
from dataclasses import dataclass


@dataclass
class CreditCardExtractor:
    input_file: str
    output_file: str

    def extract(self):
        input_file = self.input_file
        output_file = self.output_file
        logging.info(
            f"USER trying to extract credit card number from {input_file} and put it to {output_file}"
        )
        with open(
            input_file if os.path.exists(input_file) else input_file.replace("-", "_"),
            "rb",
        ) as f:
            image_data = f.read()
        response_text = OCR(input_file, image_data).extract_text()

        logging.info(
            f"USER trying to extract credit card number text of file loaded,{response_text}"
        )
        credit_card_numbers = self.extract_credit_card_from_text(response_text)
        logging.info("credit card number found")
        with open(output_file, "w") as f:
            f.write(credit_card_numbers)
        logging.info("Extracted credit card number successfully")

    def extract_credit_card_from_text(self, response_text):
        cc_regex = r"\b(?:\d{4}[- ]?){3}\d{4}|\b\d{13,19}\b"
        credit_card_numbers = re.findall(cc_regex, response_text)[0]
        return credit_card_numbers
