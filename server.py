from flask import Flask, request, jsonify, render_template
from components.services.ReadFileService import ReadFileService
from components.services.OperationsTaskHandler import GPTQuerier
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/run", methods=["POST"])
def run_task():
    task_description = request.args.get("task")
    return GPTQuerier.query_gpt(task_description, formatter=jsonify)


@app.route("/read", methods=["GET"])
def read_file():
    file_path = request.args.get("path")
    return ReadFileService.read_file(file_path)


if __name__ == "__main__":
    app.run(debug=True)
