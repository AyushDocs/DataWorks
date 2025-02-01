import requests
import os
from dataclasses import dataclass
from typing import List,Any
from DataWorks.logger import logging
import json

@dataclass
class FunctionDecider:
    user_input: str
    tasks: List
    formatter:Any

    def decide(self):
        response= requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": self.user_input}],
                "tools": self.tasks,
            },
            timeout=10,
        )
        logging.info(f"API response status: {response.status_code}")

        if response.status_code != 200:
            logging.error(f"API request failed: {response.text}")
            return self.formatter({"error": "AI service request failed"}), 500

        response_data = response.json()
        logging.debug(f"API response data: {json.dumps(response_data, indent=2)}")
        if "choices" not in response:
            logging.error("Invalid API response: Missing 'choices'")
            raise Exception('invalid api response')
        
        function = response_data["choices"][0].get("message")
        
        if "tool_calls" in function:
            function_call = function["tool_calls"][0].get("function", {})
            func_name = function_call.get("name")
            args = json.loads(function_call.get("arguments", "{}"))
            return False,func_name,args,None
        else:
            content=function.get('content', 'No response')
            return True,None,None,content