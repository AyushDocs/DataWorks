from DataWorks.components.actions.Buisness import (
    clone_repo_and_commit,
    compress_or_resize_image,
    convert_markdown_to_html,
    fetch_data_from_api,
    filter_csv,
    run_sql_query_on_db,
    scrape_website,
    transcribe_audio_openai,
)

BUISNESS_TASKS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_data_from_api",
            "description": "Fetch data from a given API URL (must NOT be a Python script URL, especially not from GitHub).",
            "parameters": {
                "type": "object",
                "properties": {
                    "api_url": {
                        "type": "string",
                        "description": "API URL to fetch data from. This must NOT be a Python script URL.",
                    },
                    "headers": {
                        "type": "object",
                        "description": "Optional headers for the request",
                    },
                    "params": {
                        "type": "object",
                        "description": "Optional parameters to pass in the API request",
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Path to save the output data",
                    },
                },
                "required": ["api_url", "output_file"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clone_repo_and_commit",
            "description": "Clone a Git repository and make a commit",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "Git repository URL"},
                    "commit_message": {
                        "type": "string",
                        "description": "Message for the commit",
                    },
                    "branch": {
                        "type": "string",
                        "description": "Branch name to check out",
                    },
                },
                "required": ["repo_url", "commit_message", "branch"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_sql_query_on_db",
            "description": "Run a SQL query on a specified database",
            "parameters": {
                "type": "object",
                "properties": {
                    "db_type": {
                        "type": "string",
                        "description": "Type of database (sqlite or duckdb)",
                    },
                    "query": {"type": "string", "description": "SQL query to execute"},
                    "db_connection": {
                        "type": "string",
                        "description": "SQL connection string",
                    },
                },
                "required": ["db_type", "query", "db_connection"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_website",
            "description": "Scrape data from a website",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the website to scrape",
                    }
                },
                "required": ["url"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compress_or_resize_image",
            "description": "Compress or resize an image file",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Path to the input image file",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where the processed image will be saved",
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["compress", "resize", "compress_and_resize"],
                        "description": "Operation to perform on the image",
                    },
                    "quality": {
                        "type": "integer",
                        "description": "Quality level for image compression (1-100)",
                    },
                },
                "required": ["input_path", "output_path", "operation", "quality"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "transcribe_audio_openai",
            "description": "Transcribe audio from an MP3 file using OpenAI's Whisper API",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Path to the audio file to transcribe",
                    },
                    "output_text_path": {
                        "type": "string",
                        "description": "Path to save the transcribed text",
                    }
                },
                "required": ["input_path", "output_text_path"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_markdown_to_html",
            "description": "Convert a Markdown file to HTML",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Path to the Markdown file",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path to save the generated HTML file",
                    },
                },
                "required": ["input_path", "output_path"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "filter_csv",
            "description": "Filter rows from a CSV file based on a column value",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "CSV file path"},
                    "filter_column": {
                        "type": "string",
                        "description": "Column name to filter by",
                    },
                    "filter_value": {
                        "type": "string",
                        "description": "Value to match in the filter column",
                    },
                },
                "required": ["file", "filter_column", "filter_value"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]
BUISNESS_TASK_MAPPINGS = {
    "fetch_data_from_api": fetch_data_from_api,
    "clone_repo_and_commit": clone_repo_and_commit,
    "run_sql_query_on_db": run_sql_query_on_db,
    "scrape_website": scrape_website,
    "compress_or_resize_image": compress_or_resize_image,
    "transcribe_audio_openai": transcribe_audio_openai,
    "convert_markdown_to_html": convert_markdown_to_html,
    "filter_csv": filter_csv,  # Direct function from Flask app
}
