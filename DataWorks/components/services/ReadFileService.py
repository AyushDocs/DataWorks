import os
from DataWorks.logger import logging

class ReadFileService:
    @staticmethod
    def read_file(file_path):
        abs_file_path = os.path.realpath(file_path)
        abs_parent_directory = os.path.abspath("/data")
        logging.info('USER requested file path: %s', abs_file_path)
        if (
            not os.path.commonpath([abs_file_path, abs_parent_directory])
            == abs_parent_directory
        ):
            logging.error('USER requested file path: %s', abs_file_path,'is outside of /data directory')
            return {"error": "File requested is outside of data directory"}, 401
        if not os.path.exists(abs_file_path):
            logging.error('USER requested file path: %s', abs_file_path,'does not exist')
            return {"error": "File not found", "path": abs_file_path}, 404

        try:
            with open(abs_file_path, "r", encoding="utf-8") as file:
                content = file.read()
                logging.info('USER requested file path: %s', abs_file_path,'has been read successfully')
                if not content:  # Check if the file is empty
                    return "", 204  # No Content
                return content, 200
        except UnicodeDecodeError:
            logging.error('Unable to decode file %s', abs_file_path)
            return {"error": "File contains non-UTF-8 characters"}, 415
        except OSError:
            logging.error('Error reading file %s', abs_file_path)
            return {"error": "Error reading file"}, 500
