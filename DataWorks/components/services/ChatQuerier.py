import json
import requests
import os
from DataWorks.components.services.OperationsTaskHandler import (
    OPERATION_TASK_MAPPINGS,
    OPERATION_TASKS,
)
from DataWorks.components.services.BuisnessTaskHandler import (
    BUISNESS_TASKS,
    BUISNESS_TASK_MAPPINGS,
)
from DataWorks.logger import logging


class ChatQuerier:
    @staticmethod
    def query_gpt(user_input: str, formatter) -> dict:
        # try:
        response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('AI_API_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": user_input}],
                "tools": OPERATION_TASKS + BUISNESS_TASKS,
                # "tool_choice": "required",
            },
        )
        function = response.json()["choices"][0]["message"]
        if "tool_calls" in function:
            function = function["tool_calls"][0]["function"]
            TASKS = OPERATION_TASK_MAPPINGS | BUISNESS_TASK_MAPPINGS
            func_name = function["name"]
            args = json.loads(function["arguments"])
            func = TASKS[func_name]
            func(args)
            logging.info(f'Task is one of the default tasks: {user_input}, {func_name}, {args}')
            return (
                formatter(
                    {"message": "Task executed successfully", "input": user_input}
                ),
                200,
            )
        logging.info(f"Task is not one of the 18 standard operations. Default Open Ai response is being sent {user_input},{function['content']}")
        return formatter({"message": function["content"], "input": user_input}), 200

    # except Exception as e:
    # return formatter({"error": str(e)}), 500
