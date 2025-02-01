import base64
import requests
from dataclasses import dataclass
import os

@dataclass
class OCR:
    input_file:str
    image_data:str
    def extract_text(self):
        ext = os.path.splitext(self.input_file)[1][1:]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}",
        }
        base64_image = base64.b64encode(self.image_data).decode("utf-8")
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
        return response.json()["choices"][0]["message"]["content"]