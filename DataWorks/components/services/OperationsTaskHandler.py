from DataWorks.components.actions.Operations import (
    calculate_gold_ticket_sales,
    count_wednesdays,
    extract_credit_card_number,
    extract_sender_email,
    find_similar_comments,
    format_markdown,
    index_markdown_headers,
    recent_logs,
    run_script,
    sort_contacts,
)

OPERATION_TASKS = [
    {
        "type": "function",
        "function": {
            "name": "run_script",
            "description": "Run a Python script from a given URL (usually a GitHub link) and execute it locally.",
            "parameters": {
                "type": "object",
                "properties": {
                    "python_script_url": {
                        "type": "string",
                        "description": "The URL of the Python script to download and run.",
                    }
                },
                "required": ["python_script_url"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "format_markdown",
            "description": "Format a markdown file using a specified formatter like Prettier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "The path to the markdown file to format.",
                    },
                    "formatter_version": {
                        "type": "string",
                        "description": "The version of prettier to use, if not given supply a default prettier version",
                    },
                },
                "required": ["input_file"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "count_wednesdays",
            "description": "Count the number of Wednesdays in a file containing dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "The path to the file containing dates.",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The path to the output file where the count will be saved.",
                    },
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sort_contacts",
            "description": "Sort contacts from a JSON file based on specified keys.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "The path to the JSON file containing contacts.",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The path to the output file to store sorted contacts.",
                    },
                    "sort_keys": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The keys to sort the contacts by (e.g., ['name', 'email']).",
                    },
                },
                "required": ["input_file", "output_file", "sort_keys"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recent_logs",
            "description": "Retrieve the most recent logs from a specified directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_directory": {
                        "type": "string",
                        "description": "The directory containing log files.",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The path to the output file to store the log entries.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The maximum number of log entries to retrieve.",
                    },
                },
                "required": ["input_directory", "output_file", "limit"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "index_markdown_headers",
            "description": "Create an index of headers from markdown files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_directory": {
                        "type": "string",
                        "description": "The directory containing markdown files.",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The path to the output file to store the index.",
                    },
                    "file_extension": {
                        "type": "string",
                        "description": "The file extension of markdown files (e.g., '.md').",
                    },
                    "header_prefix": {
                        "type": "string",
                        "description": "The prefix of the headers to index (e.g., '# ').",
                    },
                },
                "required": [
                    "input_directory",
                    "output_file",
                    "file_extension",
                    "header_prefix",
                ],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "extract_credit_card_number",
            "description": "Extract the credit card number from an image file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "The path to the image file containing the credit card number.",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The path to the output file to store the extracted number.",
                    },
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_similar_comments",
            "description": "Find the most similar comments from a list of comments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "The path to the input file containing comments.",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The path to the output file to store similar comments.",
                    },
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "extract_sender_email",
            "description": "Extract the sender's email address from the provided email text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "The path to the email text file.",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The path to the output file to store the sender's email.",
                    },
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_gold_ticket_sales",
            "description": "Calculate total sales of 'Gold' tickets from a database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "database_file": {
                        "type": "string",
                        "description": "The path to the SQLite database file.",
                    },
                    "table": {
                        "type": "string",
                        "description": "The name of the table containing ticket sales data.",
                    },
                    "columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The columns to select in the query (e.g., ['ticket_type', 'sales_amount']).",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The path to the output file to store the total sales.",
                    },
                },
                "required": ["database_file", "table", "columns", "output_file"],
                "additionalProperties": False,
            },
        },
    },
]

OPERATION_TASK_MAPPINGS = {
    "run_script": run_script,
    "format_markdown": format_markdown,
    "count_wednesdays": count_wednesdays,
    "sort_contacts": sort_contacts,
    "recent_logs": recent_logs,
    "index_markdown_headers": index_markdown_headers,
    "extract_credit_card_number": extract_credit_card_number,
    "find_similar_comments": find_similar_comments,
    "extract_sender_email": extract_sender_email,
    "calculate_gold_ticket_sales": calculate_gold_ticket_sales,
}
