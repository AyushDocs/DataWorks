import base64
import requests
import os
import json
import subprocess
from sklearn.metrics.pairwise import cosine_similarity
import re
import sqlite3
import numpy as np
from dateutil.parser import parse
from DataWorks.logger import logging
import sys
from DataWorks.exception import SignException
from DataWorks.components.actions.Operations.CreditCardExtractor import CreditCardExtractor
from DataWorks.components.actions.Operations.SenderEmailExtractor import SenderEmailExtractor

def run_script(params: dict):
    script_url = params["python_script_url"]
    if not script_url.endswith(".py"):
        logging.error("Invalid script URL: Not a Python file")
        return
    logging.info(f"Running script {script_url}")
    logging.warning(f"Running script {script_url} which may potentially harm the system")
    subprocess.run(
        f"uv run {script_url} 24f2004275@ds.study.iitm.ac.in",
        shell=True,
        check=True
    )
    logging.info(f"Ran script {script_url}")

def format_markdown(params: dict):
    input_file = params["input_file"]
    prettier_version = params["prettier_version"]
    logging.info(f"Formatting markdown file {input_file} with formatter prettier@{prettier_version}")
    subprocess.run(f" npx prettier@{prettier_version} --write {input_file}", shell=True, check=True)
    logging.info(f"Successfully formatted markdown file {input_file} with formatter prettier@{prettier_version}")

def count_wednesdays(params: dict):
    input_file = params["input_file"]
    output_file = params["output_file"]
    with open(input_file, "r") as f:
        dates = f.readlines()
    wednesdays_count = sum(
        1 for date in dates if parse(date).strftime("%A") == "Wednesday"
    )
    with open(output_file, "w") as f:
        f.write(str(wednesdays_count))
    logging.info(f"Counted {wednesdays_count} Wednesdays")

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
    input_file = params["input_file"]
    output_file = params["output_file"]
    CreditCardExtractor(input_file, output_file).extract_credit_card_number()
    
def find_similar_comments(params: dict):
    input_file = params["input_file"]
    output_file = params["output_file"]
    with open(input_file, "r") as f:
        comments = f.readlines()
    url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}",
        "Content-Type": "application/json",
    }
    data = {"model": "text-embedding-3-small", "input": comments}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    response_json = response.json()
    embeddings = [item["embedding"] for item in response_json["data"]]
    if not embeddings:
        return None, None, None
    similarity_matrix = cosine_similarity(embeddings)
    np.fill_diagonal(similarity_matrix, -np.inf)
    i, j = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
    with open(output_file, "w") as f:
        f.write(f"{comments[i]}{comments[j]}")
    logging.info("Found and wrote most similar comments")

def extract_sender_email(params: dict):
    input_file = params["input_file"]
    output_file = params["output_file"]
    SenderEmailExtractor(input_file,output_file).extract()


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
