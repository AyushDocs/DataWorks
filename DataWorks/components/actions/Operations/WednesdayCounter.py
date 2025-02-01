from dataclasses import dataclass
from DataWorks.logger import logging
from dateutil.parser import parse


@dataclass
class WednesdayCounter:
    input_file: str
    output_file: str

    def count(self):
        with open(self.input_file, "r") as f:
            dates = f.readlines()
        wednesdays_count = sum(
            1 for date in dates if parse(date).strftime("%A") == "Wednesday"
        )
        with open(self.output_file, "w") as f:
            f.write(str(wednesdays_count))
        logging.info(f"Counted {wednesdays_count} Wednesdays")
