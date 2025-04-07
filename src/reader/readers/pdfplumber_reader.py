import io
import os

import pdfplumber
from markitdown import MarkItDown
from PIL import Image

from src.reader.base_reader import BaseReader


class PDFPlumberReader(BaseReader):
    """
    Reader implementation using pdfplumber for PDF files.
    It extracts text lines, images, and tables, then returns a Markdown
    representation of the PDF content.
    """

    def __init__(self, llm_client=None, llm_model=None):
        """
        Initializes the PDFPlumberReader.
        Based on the provided llm_method configuration, this reader will load
        the corresponding LLM client (Azure OpenAI or OpenAI) and use it in MarkItDown.

        Args:
            llm_method (str): The LLM method to use ("azure", "openai", or "none").
                              Defaults to "azure".
        """
        # Use the LLMClient factory to load the appropriate model.
        self.llm_client = llm_client
        self.llm_model = llm_model
        self.md = MarkItDown(llm_client=llm_client, llm_model=llm_model)

    def convert(self, file_path: str) -> str:
        """
        Converts the provided PDF file to Markdown text by extracting
        text lines, images (with descriptions), and tables.

        Args:
            file_path (str): The full path to the PDF file.

        Returns:
            str: A Markdown string representing the PDF content.
        """
        markdown_content = ""
        document_name = os.path.basename(file_path)
        markdown_content += f"# Document: {document_name}\n\n"

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                markdown_content += f"## Page {page.page_number}\n\n"
                all_objects = []

                # Extract text lines from the page.
                text_lines = page.extract_text_lines(
                    layout=True, strip=True, return_chars=False
                )
                for line in text_lines:
                    line["object_type"] = "text_line"
                    all_objects.append(line)

                # Include graphic objects if needed.
                for line in page.lines:
                    line["object_type"] = "line"
                    all_objects.append(line)
                for rect in page.rects:
                    rect["object_type"] = "rect"
                    all_objects.append(rect)
                for curve in page.curves:
                    curve["object_type"] = "curve"
                    all_objects.append(curve)

                header_threshold = page.height * 0.1
                footer_threshold = page.height * 0.1

                # Process images within the page.
                for idx, image in enumerate(page.images):
                    if image["top"] < header_threshold or image["bottom"] > (
                        page.height - footer_threshold
                    ):
                        continue
                    image["object_type"] = "image"
                    try:
                        image_data = image["stream"].get_data()
                        image_obj = Image.open(io.BytesIO(image_data))
                        image_file_name = f"{os.path.splitext(document_name)[0]}_page{page.page_number}_img{idx}.png"  # noqa: E501
                        image_file_path = os.path.join(
                            self.output_images_path, image_file_name
                        )
                        image_obj.save(image_file_path)
                        image["extracted_image"] = image_file_name
                        # Use MarkItDown to obtain an image description.
                        image["description"] = self.md.convert(
                            image_file_path
                        ).text_content
                    except Exception as e:
                        print(
                            f"Error processing image on page {page.page_number} of \
                                {document_name}: {e}"
                        )
                    all_objects.append(image)

                # Extract tables from the page.
                tables = page.find_tables()
                for idx, table in enumerate(tables):
                    try:
                        table_data = table.extract()
                    except Exception as e:
                        print(
                            f"Error extracting table on page {page.page_number} of \
                                {document_name}: {e}"
                        )
                        table_data = None
                    table_obj = {
                        "object_type": "table",
                        "bbox": table.bbox,
                        "table_data": table_data,
                        "table_index": idx,
                    }
                    all_objects.append(table_obj)

                def get_vertical_position(obj):
                    """
                    Returns the vertical position for sorting objects.
                    """
                    if obj.get("object_type") == "table":
                        return obj.get("bbox", [0, 0, 0, 0])[1]
                    elif obj.get("object_type") == "text_line":
                        return obj.get("top", 0)
                    else:
                        return obj.get("doctop", obj.get("y0", 0))

                sorted_objects = sorted(all_objects, key=get_vertical_position)

                # Build the markdown content for this page.
                for obj in sorted_objects:
                    obj_type = obj.get("object_type")
                    if obj_type == "text_line":
                        text = obj.get("text", "").strip()
                        if text:
                            markdown_content += f"{text}\n\n"
                    elif obj_type == "image":
                        img_name = obj.get("extracted_image", "Unnamed_Image")
                        description = obj.get("description", "").strip()
                        markdown_content += f"![{img_name}]({img_name})\n\n"
                        if description:
                            markdown_content += f"**Description:** {description}\n\n"
                    elif obj_type == "table":
                        table_data = obj.get("table_data")
                        if table_data and len(table_data) > 0:
                            header_row = [str(cell).strip() for cell in table_data[0]]
                            markdown_content += "| " + " | ".join(header_row) + " |\n"
                            markdown_content += (
                                "| " + " | ".join(["---"] * len(header_row)) + " |\n"
                            )
                            for row in table_data[1:]:
                                row_cells = [str(cell).strip() for cell in row]
                                markdown_content += (
                                    "| " + " | ".join(row_cells) + " |\n"
                                )
                            markdown_content += "\n"
        return markdown_content
