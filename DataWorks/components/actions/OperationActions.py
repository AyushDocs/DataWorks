import os
import json
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
from DataWorks.components.actions.Operations.GoldTicketSalesCalculator import GoldTicketSalesCalculator
from DataWorks.components.actions.Operations.MarkdownIndexer import MarkdownIndexer
from DataWorks.components.actions.Operations.ContactsSorter import ContactsSorter

def run_script(params: dict):
    PythonScriptRunner(**params).execute()


def format_markdown(params: dict):
    MarkdownFormatter(**params).format()


def count_wednesdays(params: dict):
    WednesdayCounter(**params).count()


def sort_contacts(params: dict):
    ContactsSorter(**params).sort()


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
    MarkdownIndexer(**params).index()


def calculate_gold_ticket_sales(params: dict):
    GoldTicketSalesCalculator(**params).calculate()
