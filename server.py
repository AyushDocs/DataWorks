from flask import Flask, request, jsonify,render_template
from components.services.ReadFileService import ReadFileService
from dotenv import load_dotenv
from tools import query_gpt
load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')
    try:
        query_gpt(task_description)
        return jsonify({"message": "Task executed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/read', methods=['GET'])
def read_file():
    file_path=request.args.get('path')
    return ReadFileService.read_file(file_path)

if __name__ == '__main__':
    app.run(debug=True)
