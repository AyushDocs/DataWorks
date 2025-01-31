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
        logging.info(f"Received user input: {user_input}")

        try:
            response = requests.post(
                "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.environ.get('AI_API_KEY', '')}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": user_input}],
                    "tools": OPERATION_TASKS + BUISNESS_TASKS,
                },
                timeout=10  # Prevent hanging requests
            )

            # Log response status
            logging.info(f"API response status: {response.status_code}")

            # Handle API response errors
            if response.status_code != 200:
                logging.error(f"API request failed: {response.text}")
                return formatter({"error": "AI service request failed"}), 500

            response_data = response.json()
            logging.debug(f"API response data: {json.dumps(response_data, indent=2)}")

            if "choices" not in response_data or not response_data["choices"]:
                logging.error("Invalid API response: Missing 'choices'")
                return formatter({"error": "Unexpected API response format"}), 500

            function = response_data["choices"][0].get("message", {})

            if "tool_calls" in function:
                function_call = function["tool_calls"][0].get("function", {})

                TASKS = OPERATION_TASK_MAPPINGS | BUISNESS_TASK_MAPPINGS
                func_name = function_call.get("name")
                args = json.loads(function_call.get("arguments", "{}"))

                if func_name in TASKS:
                    logging.info(f"Executing task: {func_name} with args: {args}")
                    TASKS[func_name](args)
                    return formatter(
                        {"message": "Task executed successfully", "input": user_input}
                    ), 200

            logging.info(f"Default AI response sent: {function.get('content', 'No response')}")
            return formatter({"message": function.get("content", "No response"), "input": user_input}), 200

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {str(e)}")
            return formatter({"error": "Failed to connect to AI service"}), 500
        except KeyError as e:
            logging.error(f"Missing key in API response: {str(e)}")
            return formatter({"error": "Unexpected API response format"}), 500
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing error: {str(e)}")
            return formatter({"error": "Invalid JSON format in response"}), 500
        except Exception as e:
            logging.exception("Unexpected error occurred")
            return formatter({"error": str(e)}), 500
