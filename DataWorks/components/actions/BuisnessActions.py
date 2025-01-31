import os
import requests
import pandas as pd
from enum import Enum
from PIL import Image
import markdown
import sqlite3
import duckdb
import io
import logging
import shutil
from urllib.parse import urlparse
class ImageOperation(Enum):
    COMPRESS = "compress"
    RESIZE = "resize"
    COMPRESS_AND_RESIZE = "compress_and_resize"


def fetch_data_from_api(data: dict) -> dict:
    try:
        api_url = data.get("api_url")
        headers = data.get("headers", None)
        params = data.get("params", None)
        output_file = data.get("output_file")
        
        logging.info(f"Fetching data from API: {api_url}")
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        with open(output_file, "w") as f:
            f.write(response.text)
        
        logging.info(f"Data successfully fetched and saved to {output_file}")
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from API: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def clone_repo_and_commit(data: dict) -> bool:
    try:
        repo_url = data.get("repo_url")
        commit_message = data.get("commit_message", "DataWorks commit")
        branch = data.get("branch", "main")
        
        if not repo_url:
            raise ValueError("Repo URL must be specified")
        
        GITHUB_TOKEN = os.environ.get("PAT_TOKEN_GITHUB")

        if not GITHUB_TOKEN:
            logging.error("Error: GITHUB_TOKEN is not set!")
        repo_name = os.path.basename(repo_url).replace(".git", "")

        # Remove existing repo folder if it exists
        if os.path.exists(repo_name):
            shutil.rmtree(repo_name)

        # Format authenticated URL
        parsed_url = urlparse(repo_url)
        auth_url = f"https://{GITHUB_TOKEN}@{parsed_url.netloc}{parsed_url.path}"

        logging.info(f"Cloning repository: {auth_url}")
        os.system(f"git clone {auth_url}")
        
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        os.chdir(repo_name)
        os.system("git checkout " + branch)
        os.system(f"echo {commit_message} > random_.txt")
        os.system("git add .")
        os.system(f'git commit -am "{commit_message}"')
        os.system("git push -u origin main")
        
        logging.info(f"{repo_url} cloned and changes committed successfully")
        return True
    
    except Exception as e:
        logging.error(f"Failed to clone repository or commit changes: {e}")
        raise


def run_sql_query_on_db(data: dict) -> pd.DataFrame:
    try:
        db_type = data.get("db_type")
        query = data.get("query")
        db_connection_string = data.get("db_connection")
        
        logging.info(f"Running SQL query on {db_type} database")
        
        if db_type == "sqlite":
            conn = sqlite3.connect(db_connection_string)
        elif db_type == "duckdb":
            conn = duckdb.connect(db_connection_string)
        else:
            raise ValueError("Unsupported database type. Use 'sqlite' or 'duckdb'.")
        
        result = pd.read_sql_query(query, conn)
        conn.close()
        
        logging.info("SQL query executed successfully")
        return result
    
    except Exception as e:
        logging.error(f"Failed to run SQL query: {e}")
        raise


def scrape_website(data: dict) -> str:
    try:
        url = data.get("url")
        
        logging.info(f"Scraping website: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        logging.info("Website scraped successfully")
        return response.text if response.status_code == 200 else ""
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to scrape website: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def compress_or_resize_image(data: dict) -> bool:
    try:
        input_path = data.get("input_path")
        output_path = data.get("output_path")
        operation = ImageOperation(data.get("operation", "compress"))
        quality = data.get("quality", 85)
        
        logging.info(f"Processing image: {input_path}")
        
        with Image.open(input_path) as img:
            if operation in {ImageOperation.RESIZE, ImageOperation.COMPRESS_AND_RESIZE}:
                img.thumbnail((img.width, img.height))
            if operation in {ImageOperation.COMPRESS, ImageOperation.COMPRESS_AND_RESIZE}:
                img.save(output_path, quality=quality, optimize=True)
        
        logging.info(f"Image processed and saved to {output_path}")
        return True
    
    except Exception as e:
        logging.error(f"Failed to process image: {e}")
        raise


def transcribe_audio_openai(data: dict) -> bool:
    try:
        input_path = data.get("input_path")
        output_text_path = data.get("output_text_path")
        openai_api_key = data.get("openai_api_key")
        
        logging.info(f"Transcribing audio file: {input_path}")
        
        url = "https://api.openai.com/v1/audio/transcriptions"
        with open(input_path, "rb") as audio_file:
            files = {"file": audio_file, "model": "whisper-1"}
            headers = {"Authorization": f"Bearer {openai_api_key}"}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
        
        if response.status_code == 200:
            transcription = response.json().get("text", "")
            with open(output_text_path, "w") as output_file:
                output_file.write(transcription)
            
            logging.info(f"Audio transcribed and saved to {output_text_path}")
            return True
        
        return False
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to transcribe audio: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def convert_markdown_to_html(data: dict) -> bool:
    try:
        input_path = data.get("input_path")
        output_path = data.get("output_path")
        
        logging.info(f"Converting markdown file: {input_path}")
        
        with open(input_path, "r") as md_file:
            md_content = md_file.read()
        
        html_content = markdown.markdown(md_content)
        with open(output_path, "w") as html_file:
            html_file.write(html_content)
        
        logging.info(f"Markdown converted to HTML and saved to {output_path}")
        return True
    
    except Exception as e:
        logging.error(f"Failed to convert markdown to HTML: {e}")
        raise


def filter_csv(input_data: dict) -> dict:
    try:
        file_content = input_data.get("file_content")
        filter_column = input_data.get("filter_column")
        filter_value = input_data.get("filter_value")
        
        logging.info("Filtering CSV data")
        
        if not file_content:
            return {"error": "file_content is required"}
        if not filter_column or not filter_value:
            return {"error": "filter_column and filter_value are required"}
        
        df = pd.read_csv(io.StringIO(file_content))
        if filter_column not in df.columns:
            return {"error": f"Column '{filter_column}' not found in the CSV file"}
        
        filtered_df = df[df[filter_column] == filter_value]
        filtered_data = filtered_df.to_dict(orient="records")
        
        logging.info("CSV data filtered successfully")
        return {"filtered_data": filtered_data}
    
    except Exception as e:
        logging.error(f"Failed to filter CSV data: {e}")
        return {"error": f"An error occurred: {str(e)}"}