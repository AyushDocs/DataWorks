from DataWorks.components.services.OperationsTaskHandler import (
    OPERATION_TASK_MAPPINGS,
    OPERATION_TASKS,
)
from DataWorks.components.services.BuisnessTaskHandler import (
    BUISNESS_TASKS,
    BUISNESS_TASK_MAPPINGS,
)
from DataWorks.logger import logging
from DataWorks.exception import SignException
import sys
from DataWorks.api.FunctionDecider import FunctionDecider

class ChatQuerier:
    @staticmethod
    def query_gpt(user_input: str, formatter) -> dict:
        logging.info(f"Received user input: {user_input}")
        mappings=OPERATION_TASK_MAPPINGS|BUISNESS_TASK_MAPPINGS
        tasks = OPERATION_TASKS+BUISNESS_TASKS
        try:
            is_default_response,function_name,function_args,default_content = FunctionDecider(user_input,tasks,formatter)

            if is_default_response:
                logging.info(f"Default AI response sent: {default_content}")
                return formatter({"message": default_content, "input": user_input}), 200
            else:
                if(function_name in mappings):
                    if function_name in BUISNESS_TASKS:
                        response=mappings[function_name](function_args)
                        return formatter({"message": "Task executed successfully", "input": user_input,"response": response}), 200
                    else:
                        return formatter({"message": "Task executed successfully", "input": user_input}), 200

        except Exception as e:
            raise SignException(e,sys)
