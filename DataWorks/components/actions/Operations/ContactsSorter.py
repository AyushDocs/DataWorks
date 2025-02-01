from dataclasses import dataclass
from DataWorks.logger import logging
import json


@dataclass
class ContactsSorter:
    input_file:str
    output_file:str
    sort_keys:str
    def sort(self):
        with open(self.input_file, "r") as f:
            contacts = json.load(f)
        contacts_sorted = sorted(contacts, key=lambda x: tuple(x[key] for key in self.sort_keys))
        with open(self.output_file, "w") as f:
            json.dump(contacts_sorted, f, indent=4)
        logging.info("Sorted contacts successfully")