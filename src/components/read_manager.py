import logging
import yaml
from abc import ABC, abstractmethod
import markdown
import pandas as pd
import PyPDF2
import docx
import os
from PIL import Image, UnidentifiedImageError
from bs4 import BeautifulSoup
import pytesseract

class ReadManager:
    def __init__(self, config_path="config.yaml"):
        """Initialize ReadManager with configurations and logging."""
        self.config = self.load_config(config_path)
        self.readers = self._initialize_readers()
        self._configure_logging()

    def load_config(self, config_path):
        """Load configuration from a YAML file."""
        with open(config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _initialize_readers(self):
        """Dynamically load all available file readers."""
        return {
            ".txt": TextFileReader(),
            ".md": MarkdownFileReader(),
            ".pdf": PdfFileReader(),
            ".docx": WordFileReader(),
            ".xlsx": ExcelFileReader(),
            ".csv": CsvFileReader(),
            ".png": ImageFileReader(),
            ".svg": SvgFileReader(),
        }

    def _configure_logging(self):
        """Set up logging configuration based on config file."""
        log_config = self.config.get('logging', {})
        log_level = log_config.get('level', 'ERROR').upper()
        log_format = log_config.get('format', '%(asctime)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(level=log_level, format=log_format)

        # Add handlers from the config (stream and file)
        for handler_config in log_config.get('handlers', []):
            if handler_config['type'] == 'stream':
                stream_handler = logging.StreamHandler()
                logging.getLogger().addHandler(stream_handler)
            elif handler_config['type'] == 'file':
                file_handler = logging.FileHandler(handler_config['filename'], mode=handler_config.get('mode', 'a'))
                logging.getLogger().addHandler(file_handler)

    def read_file(self, file_path):
        """Determine the file type and call the appropriate reader."""
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return ""
        
        ext = os.path.splitext(file_path)[1].lower()
        reader = self.readers.get(ext)

        if not reader:
            logging.error(f"Unsupported file type: {ext} for file {file_path}")
            return ""

        return reader.read(file_path)

# File Reader Classes (No Change in Structure)
class FileReader(ABC):
    """Abstract class for file readers."""
    
    @abstractmethod
    def read(self, file_path):
        pass

class TextFileReader(FileReader):
    def read(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"Text file not found: {file_path}")
        except Exception as e:
            logging.error(f"Error reading text file {file_path}: {e}")
        return ""

class MarkdownFileReader(FileReader):
    def read(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return markdown.markdown(file.read())
        except FileNotFoundError:
            logging.error(f"Markdown file not found: {file_path}")
        except Exception as e:
            logging.error(f"Error reading markdown file {file_path}: {e}")
        return ""

class PdfFileReader(FileReader):
    def read(self, file_path):
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except FileNotFoundError:
            logging.error(f"PDF file not found: {file_path}")
        except Exception as e:
            logging.error(f"Error reading PDF file {file_path}: {e}")
        return ""

class WordFileReader(FileReader):
    def read(self, file_path):
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except FileNotFoundError:
            logging.error(f"Word document not found: {file_path}")
        except Exception as e:
            logging.error(f"Error reading Word document {file_path}: {e}")
        return ""

class ExcelFileReader(FileReader):
    def read(self, file_path):
        try:
            df = pd.read_excel(file_path, sheet_name=None)
            return "\n".join([df[sheet].to_string() for sheet in df])
        except FileNotFoundError:
            logging.error(f"Excel file not found: {file_path}")
        except Exception as e:
            logging.error(f"Error reading Excel file {file_path}: {e}")
        return ""

class CsvFileReader(FileReader):
    def read(self, file_path):
        try:
            df = pd.read_csv(file_path)
            return df.to_string()
        except FileNotFoundError:
            logging.error(f"CSV file not found: {file_path}")
        except Exception as e:
            logging.error(f"Error reading CSV file {file_path}: {e}")
        return ""

class ImageFileReader(FileReader):
    def read(self, file_path):
        try:
            img = Image.open(file_path)
            return pytesseract.image_to_string(img)
        except FileNotFoundError:
            logging.error(f"Image file not found: {file_path}")
        except UnidentifiedImageError:
            logging.error(f"Invalid image format: {file_path}")
        except ImportError:
            logging.error("Install pytesseract for OCR support.")
        except Exception as e:
            logging.error(f"Error reading image file {file_path}: {e}")
        return ""

class SvgFileReader(FileReader):
    def read(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "xml")
                return " ".join([text.get_text() for text in soup.find_all("text")])
        except FileNotFoundError:
            logging.error(f"SVG file not found: {file_path}")
        except Exception as e:
            logging.error(f"Error reading SVG file {file_path}: {e}")
        return ""
