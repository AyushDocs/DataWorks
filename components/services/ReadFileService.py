import os

class ReadFileService:
    @staticmethod
    def read_file(file_path):
        abs_file_path = os.path.abspath(file_path)
        abs_parent_directory = os.path.abspath('/data')
        if not os.path.commonpath([abs_file_path, abs_parent_directory]) == abs_parent_directory:
            return "Error file requested is outside of data directory",401

        if not os.path.exists(file_path):
            return "", 404

        with open(file_path, 'r') as file:
            return file.read(),200

    