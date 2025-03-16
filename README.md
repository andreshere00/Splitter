# Splitter

## Overview

The **Splitter** system is responsible for processing documents and dividing them into **chunks** using various splitting strategies. The architecture consists of multiple managers and services working together to read, split, process, and save chunks.

![Splitter architecture diagram](./data/assets/splitter.drawio.svg)

## Components

### **1. Read Manager**
- Responsible for reading input documents.
- Supports local file formats: `txt`, `md`, `docx`, `xls`, `xlsx`, `pdf`, `ppt`, `pptx`, `json`, `yaml`.
- If required, **OCR** can be applied to extract text from scanned documents.

### **2. Split Manager**
- Splits text into meaningful chunks based on different strategies.
- Includes the following methods:

| Splitter Name          | Description | Parameters | Compatible Formats |
|------------------------|-------------|------------|--------------------|
| **Word Splitter**      | Splits text into words. | Input data, number of words in each chunk. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx` |
| **Sentence Splitter**  | Splits text into sentences. | Input data, number of sentences in each chunk. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx` |
| **Paragraph Splitter** | Splits text into paragraphs. | Input data, number of paragraphs in each chunk. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx` |
| **Semantic Splitter**  | Splits text based on semantic similarity, using a language model. | Input data, language model, overlap. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx` |
| **Fixed Splitter**     | Splits text into a fixed number of words or characters. | Input data, number of characters in each chunk. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx` |
| **Paged Splitter**     | Splits text into pages. | Input data, number of pages in each chunk, overlap. | `docx`, `pdf`, `xls`, `xlsx`, `ppt`, `pptx` |
| **Recursive Splitter** | Splits based on a specified chunk size with overlap. | Input data, number of characters in each chunk, overlap parameter. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx` |
| **Row-Column Splitter** | Splits table content by rows or columns. | Input data, number of columns, column names, number of rows, row names. | `xlsx`, `xls`, `json`, `yaml` |
| **Schema-based Splitter** | Splits a hierarchical schema while preserving headers. | Input data, number of registers, overlap. | `json`, `yaml`, `xml`, `xls`, `xlsx`, `ppt`, `pptx` |
| **Auto Splitter**      | Combines multiple splitting methods based on document content. | Input data, number of characters in each chunk, overlap. | All formats |

### **3. Chunk Manager**
- Saves the generated chunks from **Chunk Manager**.
- Features:
  - **Aggregator**: Groups related chunks.
  - **Markdown conversion**: Converts text into Markdown format.
  - **Error handling**: Ensures smooth chunking.

## Application Interfaces

- The application is exposed via:
  - **FastAPI** (REST API)
  - **CLI** (Command Line Interface)

### **API Definition**
#### **Input**

- `document_name := str`.
- `document_path := str`.
- `document_id := str`.
- `split_method := str`. 
- `metadata := list[str]`.

#### **Output**
- `chunks := list[str]`.
- `chunk_id := str`.
- `chunk_path := str`.
- `document_id := str`.
- `document_name := str`.
- `conversion_method := str`.
- `metadata := list[str]`.

---

## **Project Structure**
```bash
.
├── Makefile
├── README.md
├── assets
│   └── splitter.drawio.svg
├── conftest.py
├── data
│   ├── input
│   ├── output
│   └── test
│       ├── input
│       │   ├── test_1.docx
│       │   ├── test_1.md
│       │   ├── test_1.pdf
│       │   └── test_1.txt
│       └── output
├── main.py
├── pyproject.toml
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── application
│   │   └── cli.py
│   ├── chunker
│   │   ├── __init__.py
│   │   └── chunk_manager.py
│   ├── config.py
│   ├── config.yaml
│   ├── main.py
│   ├── reader
│   │   ├── __init__.py
│   │   └── read_manager.py
│   ├── splitter
│   │   ├── __init__.py
│   │   ├── base_splitter.py
│   │   ├── split_manager.py
│   │   └── splitters
│   │       ├── __init__.py
│   │       ├── auto_splitter.py
│   │       ├── fixed_splitter.py
│   │       ├── paged_splitter.py
│   │       ├── paragraph_splitter.py
│   │       ├── recursive_splitter.py
│   │       ├── row_column_splitter.py
│   │       ├── schema_based_splitter.py
│   │       ├── semantic_splitter.py
│   │       ├── sentence_splitter.py
│   │       └── word_splitter.py
│   └── utils
│       └── splitter.py
├── test
│   ├── chunker
│   │   └── test_chunk_manager.py
│   ├── reader
│   │   └── test_read_manager.py
│   ├── splitter
│   │   ├── __init__.py
│   │   └── splitters
│   │       ├── __init__.py
│   │       ├── test_fixed_splitter.py
│   │       ├── test_paragraph_splitter.py
│   │       ├── test_recursive_splitter.py
│   │       ├── test_sentence_splitter.py
│   │       └── test_word_splitter.py
│   └── utils
└── uv.lock
```

## Contact

If you like to contribute to my project, please, send an e-mail to [andresherencia2000@gmail.com](mailto:andresherencia2000@gmail.com)