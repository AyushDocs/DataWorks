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

def run_script(params: dict):
    try:
        script_url = params["python_script_url"]
        if not script_url.endswith(".py"):
            logging.error("Invalid script URL: Not a Python file")
            return
        logging.info("Running script %s", script_url)
        logging.warning("Running script %s which may potentially harm the system", script_url)
        subprocess.run(
            f"uv run {script_url} 24f2004275@ds.study.iitm.ac.in",
            shell=True,
            check=True
        )
        logging.info("Ran script {script_url}")

    except Exception as e:
        logging.error("Error running script: %s", str(e))

def format_markdown(params: dict):
    try:
        input_file = params["input_file"]
        formatter = params["formatter"].lower()
        logging.info("Formatting markdown file %s with formatter %s", input_file, formatter)
        subprocess.run(rf"{formatter} --write {input_file}", shell=True, check=True)
    except Exception as e:
        logging.error("Error formatting markdown file: %s", str(e))

def count_wednesdays(params: dict):
    try:
        input_file = params["input_file"]
        output_file = params["output_file"]
        with open(input_file, "r") as f:
            dates = f.readlines()
        wednesdays_count = sum(
            1 for date in dates if parse(date).strftime("%A") == "Wednesday"
        )
        with open(output_file, "w") as f:
            f.write(str(wednesdays_count))
        logging.info/("Counted %d Wednesdays", wednesdays_count)
    except Exception as e:
        logging.error("Error counting Wednesdays: %s", str(e))

def sort_contacts(params: dict):
    try:
        input_file = params["input_file"]
        output_file = params["output_file"]
        sort_keys = params["sort_keys"]
        with open(input_file, "r") as f:
            contacts = json.load(f)
        contacts_sorted = sorted(contacts, key=lambda x: tuple(x[key] for key in sort_keys))
        with open(output_file, "w") as f:
            json.dump(contacts_sorted, f, indent=4)
        logging.info("Sorted contacts successfully")
    except Exception as e:
        logging.error("Error sorting contacts: %s", str(e))

def recent_logs(params: dict):
    try:
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
    except Exception as e:
        logging.error("Error retrieving recent logs: %s", str(e))

def extract_credit_card_number(params: dict):
    try:
        input_file = params["input_file"]
        output_file = params["output_file"]
        with open(input_file if os.path.exists(input_file) else input_file.replace('-','_'), "rb") as f:
            image_data = f.read()
        ext = os.path.splitext(input_file)[1][1:]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('AI_API_KEY')}",
        }
        base64_image = base64.b64encode(image_data).decode("utf-8")
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract the text in this image"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "detail": "low",
                                "url": f"data:image/{ext};base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
        }
        response = requests.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        response_text = response.json()["choices"][0]["message"]["content"]
        cc_regex = r"\b(?:\d{4}[- ]?){3}\d{4}|\b\d{13,19}\b"
        credit_card_numbers = re.findall(cc_regex, response_text)[0]
        with open(output_file, "w") as f:
            f.write(credit_card_numbers)
        logging.info("Extracted credit card number successfully")
    except Exception as e:
        logging.error("Error extracting credit card number: %s", str(e))

def find_similar_comments(params: dict):
    try:
        input_file = params["input_file"]
        output_file = params["output_file"]
        with open(input_file, "r") as f:
            comments = f.readlines()
        url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {os.environ.get('AI_API_KEY')}",
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
    except Exception as e:
        logging.error("Error finding similar comments: %s", str(e))


def extract_sender_email(params: dict):
    try:
        input_file = params["input_file"]
        output_file = params["output_file"]

        with open(input_file, "r") as f:
            email_text = f.read()

        response = requests.post(
            url="https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ.get('AI_API_KEY')}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Identify the sender of email from the following text"},
                    {"role": "user", "content": email_text},
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "email",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {"email_address": {"type": "string"}},
                            "required": ["email_address"],
                            "additionalProperties": False,
                        },
                    },
                },
            },
        )
        response.raise_for_status()

        result = response.json()
        sender_email = json.loads(result["choices"][0]["message"]["content"])["email_address"]

        with open(output_file, "w") as f:
            f.write(sender_email)

        logging.info(f"Successfully extracted sender email: {sender_email}")
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Failed to parse response JSON: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
def index_markdown_headers(params: dict):
    try:
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
            try:
                with open(file_path, "r") as f:
                    for line in f:
                        if line.startswith(header_prefix):
                            title = line.strip().lstrip("#").strip()
                            index[file] = title
                            logging.info(f"Indexed file: {file} with header: {title}")
                            break
            except Exception as e:
                logging.error(f"Failed to process file {file}: {e}")
                continue  # Skip to the next file if an error occurs

        # Write the index to the output file
        with open(output_file, "w") as out_f:
            json.dump(index, out_f, indent=4)
        
        logging.info(f"Index successfully written to {output_file}")
        return True

    except Exception as e:
        logging.error(f"An error occurred during markdown header indexing: {e}")
        raise

def calculate_gold_ticket_sales(params: dict):
    try:
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
    except sqlite3.DatabaseError as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        conn.close()
