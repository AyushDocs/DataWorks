from dataclasses import dataclass
from DataWorks.logger import logging
import os
import json

@dataclass
class MarkdownIndexer:
    input_directory:str
    output_file:str
    file_extension:str
    header_prefix:str
    def index(self):
        logging.info(f"Indexing markdown headers in directory: {self.input_directory}")
        index = {}
        markdown_files = [
            f for f in os.listdir(self.input_directory) if f.endswith(self.file_extension)
        ]
        logging.info(f"Found {len(markdown_files)} markdown files to process")
        for file in markdown_files:
            file_path = os.path.join(self.input_directory, file)
            with open(file_path, "r") as f:
                for line in f:
                    if line.startswith(self.header_prefix):
                        title = line.strip().lstrip("#").strip()
                        index[file] = title
                        logging.info(f"Indexed file: {file} with header: {title}")
                        break

        # Write the index to the output file
        with open(self.output_file, "w") as out_f:
            json.dump(index, out_f, indent=4)

        logging.info(f"Index successfully written to {self.output_file}")
        return True