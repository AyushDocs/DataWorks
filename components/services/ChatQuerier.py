import json
import requests
import os
from components.services.OperationsTaskHandler import (
    OPERATION_TASK_MAPPINGS,
    OPERATION_TASKS,
)
from components.services.BuisnessTaskHandler import (
    BUISNESS_TASKS,
    BUISNESS_TASK_MAPPINGS,
)


class ChatQuerier:
    @staticmethod
    def query_gpt(user_input: str, formatter) -> dict:
        # try:
            response = requests.post(
                "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('AI_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": user_input}],
                    "tools": OPERATION_TASKS+BUISNESS_TASKS,
                    # "tool_choice": "required",
                },
            )
            function = response.json()["choices"][0]["message"]
            if "tool_calls" in function:
                function=function["tool_calls"][0]["function"]
                TASKS = OPERATION_TASK_MAPPINGS|BUISNESS_TASK_MAPPINGS
                func_name = function["name"]
                args = json.loads(function["arguments"])
                func = TASKS[func_name]
                func(args)
                return formatter({"message": "Task executed successfully","input":user_input}), 200
            return formatter({"message": function["content"],"input":user_input}), 200
            
        # except Exception as e:
            # return formatter({"error": str(e)}), 500
