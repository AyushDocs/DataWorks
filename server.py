import os
import json
from flask import Flask, request, jsonify,render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')
    
    try:
        return jsonify({"message": "Task executed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path')
    abs_file_path = os.path.abspath(file_path)
    abs_parent_directory = os.path.abspath('data')
    if not os.path.commonpath([abs_file_path, abs_parent_directory]) == abs_parent_directory:
        return "Error file requested is outside of data directory",401

    if not os.path.exists(file_path):
        return "", 404
    
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    return file_content, 200

if __name__ == '__main__':
    app.run(debug=True)
