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
from DataWorks.components.actions.Operations.RecentLogsWriter import RecentLogsWriter

def run_script(params: dict):
    PythonScriptRunner(**params).execute()


def format_markdown(params: dict):
    MarkdownFormatter(**params).format()


def count_wednesdays(params: dict):
    WednesdayCounter(**params).count()


def sort_contacts(params: dict):
    ContactsSorter(**params).sort()


def recent_logs(params: dict):
    RecentLogsWriter(**params).write()


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
