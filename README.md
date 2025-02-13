# Splitter

## Overview

The **Splitter** system is responsible for processing documents and dividing them into **chunks** using various splitting strategies. The architecture consists of multiple managers and services working together to read, split, process, and save chunks.

![Splitter architecture diagram](./assets/splitter.drawio.svg)

## Components

### **1. Read Manager**
- Responsible for reading input documents.
- Supports local file formats: `txt`, `md`, `doc`, `docx`, `xls`, `xlsx`, `pdf`, `ppt`, `pptx`, `json`, `yaml`.
- If required, **OCR** can be applied to extract text from scanned documents.

### **2. Split Manager**
- Splits text into meaningful chunks based on different strategies.
- Includes the following methods:

| Splitter Name          | Description | Parameters | Compatible Formats |
|------------------------|-------------|------------|---------------------|
| **Word Splitter**      | Splits text into words. | Input data, number of words in each chunk. | `txt`, `markdown`, `doc`, `docx`, `pdf`, `ppt`, `pptx` |
| **Sentence Splitter**  | Splits text into sentences. | Input data, number of sentences in each chunk. | `txt`, `markdown`, `doc`, `docx`, `pdf`, `ppt`, `pptx` |
| **Paragraph Splitter** | Splits text into paragraphs. | Input data, number of paragraphs in each chunk. | `txt`, `markdown`, `doc`, `docx`, `pdf`, `ppt`, `pptx` |
| **Semantic Splitter**  | Splits text based on semantic similarity, using a language model. | Input data, language model, overlap. | `txt`, `markdown`, `doc`, `docx`, `pdf`, `ppt`, `pptx` |
| **Fixed Splitter**     | Splits text into a fixed number of words or characters. | Input data, number of characters in each chunk. | `txt`, `markdown`, `doc`, `docx`, `pdf`, `ppt`, `pptx` |
| **Paged Splitter**     | Splits text into pages. | Input data, number of pages in each chunk, overlap. | `doc`, `docx`, `pdf`, `xls`, `xlsx`, `ppt`, `pptx` |
| **Recursive Splitter** | Splits based on a specified chunk size with overlap. | Input data, number of characters in each chunk, overlap parameter. | `txt`, `markdown`, `doc`, `docx`, `pdf`, `ppt`, `pptx` |
| **Row-Column Splitter** | Splits table content by rows or columns. | Input data, number of columns, column names, number of rows, row names. | `xlsx`, `xls`, `json`, `yaml` |
| **Schema-based Splitter** | Splits a hierarchical schema while preserving headers. | Input data, number of registers, overlap. | `json`, `yaml`, `xml`, `ppt`, `pptx` |
| **Auto Splitter**      | Combines multiple splitting methods based on document content. | Input data, number of characters in each chunk, overlap. | All formats |

### **3. Chunk Manager**
- Organizes and processes the chunks created by the **Split Manager**.
- Features:
  - **Aggregator**: Groups related chunks.
  - **Markdown conversion**: Converts text into Markdown format.
  - **Error handling**: Ensures smooth chunking.

### **4. Save Manager**
- Saves the generated chunks from **Chunk Manager**.
- Supports saving in structured formats.

## Application Interfaces

- The application is exposed via:
  - **FastAPI** (REST API)
  - **CLI** (Command Line Interface)

### **API Definition**
#### **Input**
- `document_name`
- `document_path`
- `document_id`
- `metadata` (dummy)

#### **Output**
- `chunk_id`
- `path`
- `document_id`
- `document_name`
- `conversion_method`
- `metadata` (dummy)

---

## **Project Structure**
```bash
.
├── README.md
├── assets
│   └── splitter.drawio.svg
├── path
│   └── to
│       └── data
│           ├── aliases
│           │   └── data.json
│           ├── collections
│           └── raft_state.json
├── requirements.txt
├── setup.py
├── src
│   ├── __init__.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── chunk_manager.py
│   │   ├── read_manager.py
│   │   ├── save_manager.py
│   │   └── split_manager.py
│   ├── config.py
│   ├── config.yaml
│   ├── main.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── auto_splitter.py
│   │   ├── fixed_splitter.py
│   │   ├── paged_splitter.py
│   │   ├── paragraph_splitter.py
│   │   ├── recursive_splitter.py
│   │   ├── semantic_splitter.py
│   │   ├── sentence_splitter.py
│   │   └── word_splitter.py
│   └── utils
│       ├── __init__.py
│       ├── file_reader.py
│       └── text_utils.py
└── tests
```