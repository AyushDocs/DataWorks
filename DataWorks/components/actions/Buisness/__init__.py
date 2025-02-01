from DataWorks.components.actions.Buisness.ApiDataFetcher import ApiDataFetcher
from DataWorks.components.actions.Buisness.GitRepoManager import GitRepoManager
from DataWorks.components.actions.Buisness.SQLQueryRunner import SQLQueryRunner
from DataWorks.components.actions.Buisness.WebsiteScraper import WebsiteScraper
from DataWorks.components.actions.Buisness.ImageProcessor import ImageProcessor
from DataWorks.components.actions.Buisness.OpenAITranscriber import OpenAITranscriber
from DataWorks.components.actions.Buisness.MarkdownConverter import MarkdownConverter
from DataWorks.components.actions.Buisness.CSVFilter import CSVFilter


def fetch_data_from_api(data: dict):
    return ApiDataFetcher(**data).fetch()

def clone_repo_and_commit(data: dict):
    return GitRepoManager(**data).clone_and_commit()

def run_sql_query_on_db(data: dict):
    return SQLQueryRunner(**data).run()

def scrape_website(data: dict) -> str:
    return WebsiteScraper(**data).scrape()

def compress_or_resize_image(data: dict):
    return ImageProcessor(**data).process()

def transcribe_audio_openai(data: dict):
    return OpenAITranscriber(**data).transcribe()

def convert_markdown_to_html(data: dict):
    return MarkdownConverter(**data).convert()

def filter_csv(data: dict) -> dict:
    return CSVFilter(**data).filter()
