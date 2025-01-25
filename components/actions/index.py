import base64
import requests
import os
import json
import os
import json
import subprocess
import datetime
import csv
from sklearn.metrics.pairwise import cosine_similarity
import re
import sqlite3
import numpy as np
from typing import List
import requests
from dateutil.parser import parse

def run_script(script_url: str):
    subprocess.run([f"uv run {script_url} 24f2004275@ds.study.iitm.ac.in"],shell=True)

def format_markdown(input_file: str, formatter: str):
    print(f'{formatter} --write {input_file}')
    subprocess.run(rf'{formatter} --write {input_file}',shell=True)

def count_wednesdays(input_file: str, output_file: str):
    with open(input_file, 'r') as f:
        dates = f.readlines()
    wednesdays_count = sum(1 for date in dates if parse(date).strftime('%A')=='Wednesday')
    with open(output_file, 'w') as f:
        f.write(str(wednesdays_count))

def sort_contacts(input_file: str, output_file: str, sort_keys: List[str]):
    with open(input_file, 'r') as f:
        (contacts := json.load(f))
    contacts_sorted = sorted(contacts, key=lambda x: (x[key] for key in sort_keys))
    with open(output_file, 'w') as f:
        json.dump(contacts_sorted, f, indent=4)

def recent_logs(input_directory: str, output_file: str, limit: int):
    log_files = [f for f in os.listdir(input_directory) if f.endswith('.log')]
    log_files.sort(key=lambda f: os.path.getmtime(os.path.join(input_directory, f)), reverse=True)
    with open(output_file, 'w') as out_f:
        for log_file in log_files[:limit]:
            with open(os.path.join(input_directory, log_file), 'r') as f:
                first_line = f.readline().strip()
                out_f.write(first_line + "\n")

def index_markdown_headers(input_directory: str, output_file: str, file_extension: str, header_prefix: str):
    index = {}
    markdown_files = [f for f in os.listdir(input_directory) if f.endswith(file_extension)]
    for file in markdown_files:
        with open(os.path.join(input_directory, file), 'r') as f:
            for line in f:
                if line.startswith(header_prefix):
                    title = line.strip().lstrip('#').strip()
                    index[file] = title
                    break

    # Write the index to the output file
    with open(output_file, 'w') as out_f:
        json.dump(index, out_f, indent=4)

def extract_credit_card_number(input_file: str, output_file: str):
    with open(input_file, 'rb') as f:
        image_data = f.read()
        ext=os.path.splitext(image_data)[1][1:]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get("AI_API_KEY")}"
    }
    base64_image = base64.b64encode(image_data).decode('utf-8')
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the text in this image"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "detail": "low",
                            "url": f"data:image/{ext};base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/chat/completions", headers=headers, json=data)

    if not response.status_code == 200:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        return
    
    response_text = response.json()["choices"][0]["message"]["content"]
    response = requests.post(
        url="https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ.get('AI_API_KEY')}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "get the credit card number from the following text"},
                {"role": "user", "content": response_text}
            ]
        }
    )
    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    with open(output_file, 'w') as f:
        f.write(answer)

def find_similar_comments(input_file: str, output_file: str):
    with open(input_file, 'r') as f:
        comments = f.readlines()
    url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {os.environ("AI_API_KEY")}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "text-embedding-ada-002",  # Use OpenAI's Ada embedding model
        "input": comments  # List of comments to get embeddings for
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        embeddings = [item['embedding'] for item in response_json['data']]
        if len(embeddings) == 0:
            return None, None, None
        similarity_matrix = cosine_similarity(embeddings)
        np.fill_diagonal(similarity_matrix, -np.inf)
        i, j = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
        with open(output_file, 'w') as f:
            f.write(f"Comment 1: {comments[i]}\nComment 2: {comments[j]}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

def extract_sender_email(input_file:str,output_file:str):
    with open(input_file, 'r') as f:
        email_text = f.read()
    response = requests.post(
        url="https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ.get("AI_API_KEY")}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Identify the sender of email from the following text"},
                {"role": "user", "content": email_text}
            ]
        }
    )
    result = response.json()
    sender_email = result["choices"][0]["message"]["content"]
    with open(output_file, 'w') as f:
        f.write(sender_email)

def calculate_gold_ticket_sales(database_file: str,table:str,columns:List[str],output_file: str):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute(f"SELECT SUM(units * price) FROM {table} WHERE type = Gold")
    total_sales = cursor.fetchone()[0] or 0
    with open(output_file, 'w') as f:
        f.write(str(total_sales))

    conn.close()

script_directory = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_directory, "format.md")
print(input_file)