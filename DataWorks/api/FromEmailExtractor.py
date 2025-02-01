import requests
from dataclasses import dataclass
import os
import json


@dataclass
class FromEmailExtractor:
    email_text: str

    def extract_from_email(self):
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
                    {"role": "user", "content": self.email_text},
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
        return json.loads(result["choices"][0]["message"]["content"])["email_address"]
