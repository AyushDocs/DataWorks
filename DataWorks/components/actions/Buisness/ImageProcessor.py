import logging
from enum import Enum
from dataclasses import dataclass
from PIL import Image

class ImageOperation(Enum):
    COMPRESS = "compress"
    RESIZE = "resize"
    COMPRESS_AND_RESIZE = "compress_and_resize"

@dataclass
class ImageProcessor:
    input_path: str
    output_path: str
    operation: ImageOperation = ImageOperation.COMPRESS
    quality: int = 85

    def process(self) -> bool:
        logging.info(f"Processing image: {self.input_path}")

        with Image.open(self.input_path) as img:
            if self.operation in {ImageOperation.RESIZE, ImageOperation.COMPRESS_AND_RESIZE}:
                img.thumbnail((img.width, img.height))

            if self.operation in {ImageOperation.COMPRESS, ImageOperation.COMPRESS_AND_RESIZE}:
                img.save(self.output_path, quality=self.quality, optimize=True)

        logging.info(f"Image processed and saved to {self.output_path}")
        return True
