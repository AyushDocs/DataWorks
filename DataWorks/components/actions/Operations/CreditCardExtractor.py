from DataWorks.logger import logging
import os
import base64
import requests
import re

class CreditCardExtractor:
    def __init__(self,input_file,output_file):
        self.input_file = input_file
        self.output_file = output_file
        pass
    def extract(self):
        input_file = self.input_file
        output_file = self.output_file
        logging.info(f"USER trying to extract credit card number from {input_file} and put it to {output_file}")
        with open(input_file if os.path.exists(input_file) else input_file.replace('-','_'), "rb") as f:
            image_data = f.read()
        response_text=self.get_credit_card_text(input_file,image_data)

        logging.info(f"USER trying to extract credit card number text of file loaded,{response_text}")
        cc_regex = r"\b(?:\d{4}[- ]?){3}\d{4}|\b\d{13,19}\b"
        credit_card_numbers = re.findall(cc_regex, response_text)[0]
        logging.info("credit card number found")
        with open(output_file, "w") as f:
            f.write(credit_card_numbers)
        logging.info("Extracted credit card number successfully")
    
    def get_credit_card_text(input_file:str,image_data:bytes)->str:
        ext = os.path.splitext(input_file)[1][1:]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}",
        }
        base64_image = base64.b64encode(image_data).decode("utf-8")
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract the text in this image"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "detail": "low",
                                "url": f"data:image/{ext};base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
        }
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        response_text = response.json()["choices"][0]["message"]["content"]