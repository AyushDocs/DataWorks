from flask import Flask, request, jsonify, render_template
from DataWorks.components.services.ReadFileService import ReadFileService
from DataWorks.components.services.ChatQuerier import ChatQuerier
from DataWorks.logger import logging
from dotenv import load_dotenv


def get_app(name):

    load_dotenv()
    __app = Flask(name)

    @__app.route("/")
    def index():
        logging.info("USER visited home page")
        return render_template("home.html")

    @__app.route("/run", methods=["POST"])
    def run_task():
        task_description = request.args.get("task")
        logging.info("user has ran the command %s", task_description)
        return ChatQuerier.query_gpt(task_description, formatter=jsonify)

    @__app.route("/read", methods=["GET"])
    def read_file():
        file_path = request.args.get("path")
        logging.info("USER wishes to read file %s", file_path)
        return ReadFileService.read_file(file_path)

    return __app
