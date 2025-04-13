import os

import pdfplumber

from src.domain.reader.base_reader import BaseReader


class PDFPlumberReader(BaseReader):
    """
    Reader implementation using pdfplumber for PDF files.
    It extracts text lines and tables, then returns a Markdown
    representation of the PDF content.
    """

    def convert(self, file_path: str) -> str:
        """
        Converts the provided PDF file to Markdown text by extracting
        text lines and tables.

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

                # Extract tables from the page.
                tables = page.find_tables()
                for idx, table in enumerate(tables):
                    try:
                        table_data = table.extract()
                    except Exception as e:
                        print(
                            f"Error extracting table on page {page.page_number} of {document_name}: {e}"  # noqa: E501
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
