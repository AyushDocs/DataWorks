import logging
import markdown
from dataclasses import dataclass

@dataclass
class MarkdownConverter:
    input_path: str
    output_path: str

    def convert(self) -> bool:
        logging.info(f"Converting markdown file: {self.input_path}")

        with open(self.input_path, "r") as md_file:
            md_content = md_file.read()

        html_content = markdown.markdown(md_content)

        with open(self.output_path, "w") as html_file:
            html_file.write(html_content)

        logging.info(f"Markdown converted to HTML and saved to {self.output_path}")
        return True
