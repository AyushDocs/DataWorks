import requests
import os
from components.actions.index import calculate_gold_ticket_sales,count_wednesdays,extract_credit_card_number,extract_sender_email,find_similar_comments,format_markdown,index_markdown_headers,recent_logs,run_script,sort_contacts
ALL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_script",
            "description": "Run a script from a given URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_url": {"type": "string", "description": "URL of the script to run"}
                },
                "required": ["script_url"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "format_markdown",
            "description": "Format a markdown file using the specified formatter",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the markdown file to format"},
                    "formatter": {"type": "string", "description": "Formatter to use (e.g., Prettier)"}
                },
                "required": ["input_file", "formatter"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_wednesdays",
            "description": "Count the number of Wednesdays in a file of dates",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the file containing dates"},
                    "output_file": {"type": "string", "description": "Path to the output file where the count will be saved"}
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sort_contacts",
            "description": "Sort contacts from a JSON file based on specified keys",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the contacts file"},
                    "output_file": {"type": "string", "description": "Path to the output file to store sorted contacts"},
                    "sort_keys": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Keys to sort by"
                    }
                },
                "required": ["input_file", "output_file", "sort_keys"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recent_logs",
            "description": "Retrieve the most recent logs from a specified directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_directory": {"type": "string", "description": "Directory containing log files"},
                    "output_file": {"type": "string", "description": "Path to the output file to store log entries"},
                    "limit": {"type": "integer", "description": "Limit to the number of logs to retrieve"}
                },
                "required": ["input_directory", "output_file", "limit"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "index_markdown_headers",
            "description": "Create an index of headers from markdown files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_directory": {"type": "string", "description": "Directory containing markdown files"},
                    "output_file": {"type": "string", "description": "Path to the output file to store the index"},
                    "file_extension": {"type": "string", "description": "File extension of markdown files (e.g., .md)"},
                    "header_prefix": {"type": "string", "description": "Prefix of the headers to index (e.g., '# ')"}
                },
                "required": ["input_directory", "output_file", "file_extension", "header_prefix"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_credit_card_number",
            "description": "Extract the credit card number from an image file",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the image file containing the credit card number"},
                    "output_file": {"type": "string", "description": "Path to the output file to store the extracted number"}
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_similar_comments",
            "description": "Find the most similar comments from a list of comments",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the input file containing comments"},
                    "output_file": {"type": "string", "description": "Path to the output file to store similar comments"}
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_sender_email",
            "description": "Extract the sender's email address from the provided email text",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the email text file"},
                    "output_file": {"type": "string", "description": "Path to the output file to store the sender's email"}
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_gold_ticket_sales",
            "description": "Calculate total sales of 'Gold' tickets from a database",
            "parameters": {
                "type": "object",
                "properties": {
                    "database_file": {"type": "string", "description": "Path to the SQLite database file"},
                    "table": {"type": "string", "description": "Name of the table containing ticket sales data"},
                    "columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Columns to select in the query"
                    },
                    "output_file": {"type": "string", "description": "Path to the output file to store the total sales"}
                },
                "required": ["database_file", "table", "columns", "output_file"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

mappings={
    "run_script":run_script,
    "format_markdown":format_markdown,
    "count_wednesdays":count_wednesdays,
    "sort_contacts":sort_contacts,
    "recent_logs":recent_logs,
    "index_markdown_headers":index_markdown_headers,
    "extract_credit_card_number":extract_credit_card_number,
    "find_similar_comments":find_similar_comments,
    "extract_sender_email":extract_sender_email,
    "calculate_gold_ticket_sales":calculate_gold_ticket_sales
}

def query_gpt(user_input: str) -> dict:
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('AI_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_input}],
            "tools": ALL_TOOLS,
            "tool_choice": "required",
        },
    )
    d= response.json()["choices"][0]["message"]["function_call"]
    mappings[d["name"]](d["argument"])