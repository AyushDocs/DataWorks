import json
import requests
import os
from DataWorks.logger import logging
from dataclasses import dataclass

@dataclass
class SenderEmailExtractor:
    input_file:str
    output_file:str

    def extract(self):
        with open(self.input_file, "r") as f:
            email_text = f.read()

        sender_email = self.get_email_from_file(email_text)

        with open(self.output_file, "w") as f:
            f.write(sender_email)

        logging.info(f"Successfully extracted sender email: {sender_email}")

    def get_email_from_file(self, email_text):
        response = requests.post(
            url="https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "Identify the sender of email from the following text",
                    },
                    {"role": "user", "content": email_text},
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "email",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {"email_address": {"type": "string"}},
                            "required": ["email_address"],
                            "additionalProperties": False,
                        },
                    },
                },
            },
        )
        response.raise_for_status()

        result = response.json()
        sender_email = json.loads(result["choices"][0]["message"]["content"])[
            "email_address"
        ]
        
        return sender_email
