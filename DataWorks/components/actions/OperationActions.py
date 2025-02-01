import os
import json
import sqlite3
from DataWorks.logger import logging
from DataWorks.components.actions.Operations.CreditCardExtractor import (
    CreditCardExtractor,
)
from DataWorks.components.actions.Operations.SenderEmailExtractor import (
    SenderEmailExtractor,
)
from DataWorks.components.actions.Operations.SimilarCommentFinder import (
    SimilarCommentFinder,
)
from DataWorks.components.actions.Operations.MarkdownFormatter import MarkdownFormatter
from DataWorks.components.actions.Operations.PythonScriptRunner import (
    PythonScriptRunner,
)
from DataWorks.components.actions.Operations.WednesdayCounter import WednesdayCounter


def run_script(params: dict):
    PythonScriptRunner(**params).execute()


def format_markdown(params: dict):
    MarkdownFormatter(**params).format()


def count_wednesdays(params: dict):
    WednesdayCounter(**params).count()


def sort_contacts(params: dict):
    input_file = params["input_file"]
    output_file = params["output_file"]
    sort_keys = params["sort_keys"]
    with open(input_file, "r") as f:
        contacts = json.load(f)
    contacts_sorted = sorted(contacts, key=lambda x: tuple(x[key] for key in sort_keys))
    with open(output_file, "w") as f:
        json.dump(contacts_sorted, f, indent=4)
    logging.info("Sorted contacts successfully")


def recent_logs(params: dict):
    input_directory = params["input_directory"]
    output_file = params["output_file"]
    limit = params["limit"]
    log_files = [f for f in os.listdir(input_directory) if f.endswith(".log")]
    log_files.sort(
        key=lambda f: os.path.getmtime(os.path.join(input_directory, f)), reverse=True
    )
    with open(output_file, "w") as out_f:
        for log_file in log_files[:limit]:
            with open(os.path.join(input_directory, log_file), "r") as f:
                first_line = f.readline().strip()
                out_f.write(first_line + "\n")
    logging.info("Extracted recent logs successfully")


def extract_credit_card_number(params: dict):
    CreditCardExtractor(**params).extract_credit_card_number()


def find_similar_comments(params: dict):
    SimilarCommentFinder(**params).find_comments()


def extract_sender_email(params: dict):
    SenderEmailExtractor(**params).extract()


def index_markdown_headers(params: dict):
    # Extract parameters
    input_directory = params.get("input_directory")
    output_file = params.get("output_file")
    file_extension = params.get("file_extension")
    header_prefix = params.get("header_prefix")

    # Validate required parameters
    if not all([input_directory, output_file, file_extension, header_prefix]):
        raise ValueError("Missing required parameters in 'params' dictionary")

    logging.info(f"Indexing markdown headers in directory: {input_directory}")

    # Initialize index dictionary
    index = {}

    # Find all markdown files in the input directory
    markdown_files = [
        f for f in os.listdir(input_directory) if f.endswith(file_extension)
    ]
    logging.info(f"Found {len(markdown_files)} markdown files to process")

    # Process each markdown file
    for file in markdown_files:
        file_path = os.path.join(input_directory, file)
        with open(file_path, "r") as f:
            for line in f:
                if line.startswith(header_prefix):
                    title = line.strip().lstrip("#").strip()
                    index[file] = title
                    logging.info(f"Indexed file: {file} with header: {title}")
                    break

    # Write the index to the output file
    with open(output_file, "w") as out_f:
        json.dump(index, out_f, indent=4)

    logging.info(f"Index successfully written to {output_file}")
    return True


def calculate_gold_ticket_sales(params: dict):
    database_file = params["database_file"]
    table = params["table"]
    output_file = params["output_file"]

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    query = f"SELECT SUM(units * price) FROM {table} WHERE type = 'Gold'"
    logging.info(f"Executing query: {query}")
    cursor.execute(query)
    total_sales = cursor.fetchone()[0] or 0

    with open(output_file, "w") as f:
        f.write(str(total_sales))

    logging.info(f"Successfully calculated gold ticket sales: {total_sales}")
    conn.close()
