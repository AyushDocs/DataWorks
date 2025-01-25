import os
import requests
import pandas as pd
from enum import Enum
from PIL import Image
import markdown
import sqlite3
import duckdb


class ImageOperation(Enum):
    COMPRESS = "compress"
    RESIZE = "resize"
    COMPRESS_AND_RESIZE = "compress_and_resize"


def fetch_data_from_api(data: dict) -> dict:
    api_url = data.get("api_url")
    headers = data.get("headers", None)
    params = data.get("params", None)

    response = requests.get(api_url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else {}


def clone_repo_and_commit(data: dict) -> bool:
    repo_url = data.get("repo_url")
    commit_message = data.get("commit_message")
    branch = data.get("branch", "main")

    os.system(f"git clone {repo_url}")
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    os.chdir(repo_name)
    os.system("git checkout " + branch)
    os.system(f'git commit -am "{commit_message}"')
    os.system("git push")
    return True


def run_sql_query_on_db(data: dict) -> pd.DataFrame:
    db_type = data.get("db_type")
    query = data.get("query")

    if db_type == "sqlite":
        conn = sqlite3.connect("database.db")
    elif db_type == "duckdb":
        conn = duckdb.connect("database.duckdb")
    else:
        raise ValueError("Unsupported database type. Use 'sqlite' or 'duckdb'.")

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def scrape_website(data: dict) -> str:
    url = data.get("url")
    response = requests.get(url)
    return response.text if response.status_code == 200 else ""


def compress_or_resize_image(data: dict) -> bool:
    input_path = data.get("input_path")
    output_path = data.get("output_path")
    operation = ImageOperation(data.get("operation", "compress"))
    quality = data.get("quality", 85)

    with Image.open(input_path) as img:
        if operation in {ImageOperation.RESIZE, ImageOperation.COMPRESS_AND_RESIZE}:
            img.thumbnail((img.width, img.height))
        if operation in {ImageOperation.COMPRESS, ImageOperation.COMPRESS_AND_RESIZE}:
            img.save(output_path, quality=quality, optimize=True)
    return True


def transcribe_audio_openai(data: dict) -> bool:
    input_path = data.get("input_path")
    output_text_path = data.get("output_text_path")
    openai_api_key = data.get("openai_api_key")

    url = "https://api.openai.com/v1/audio/transcriptions"
    with open(input_path, "rb") as audio_file:
        files = {"file": audio_file, "model": "whisper-1"}
        headers = {"Authorization": f"Bearer {openai_api_key}"}
        response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        transcription = response.json().get("text", "")
        with open(output_text_path, "w") as output_file:
            output_file.write(transcription)
        return True
    return False


def convert_markdown_to_html(data: dict) -> bool:
    input_path = data.get("input_path")
    output_path = data.get("output_path")

    with open(input_path, "r") as md_file:
        md_content = md_file.read()
    html_content = markdown.markdown(md_content)
    with open(output_path, "w") as html_file:
        html_file.write(html_content)
    return True
