# Splitter

## Overview

The **Splitter** application aims to convert documents into markdown format, and split them into **chunks** using various splitting strategies. The architecture consists of three main pieces: the `ReadManager`, the `SplitManager` and the `ChunkManager`. Observe the following diagram:

![Splitter architecture diagram](./docs/assets/splitter.drawio.svg)

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
  - REST API
  - CLI

### API

The API is accessed through a FastAPI application. This application can be launched executing:

```bash
make serve
```

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
- `split_method := str`.
- `metadata := list[str]`.

### CLI

The application is accessible through Command Line Interface (CLI) using the following command:

```bash
make run
```

### Docker

> Comming soon!

---

## Project scenario

This application compose a piece of an ambicious project named **"MultiRAG"**. This system aims to be a super modullarizable and open-source RAG system which is fully customizable piece by piece. Observe the following architecture diagram:

[MultiRAG architecture](docs/assets/MultiRAG.drawio.svg)

## Project Structure
```bash
.
├── Makefile
├── README.md
├── data
│   ├── output
│   └── test
│       ├── input
│       │   ├── test_1.docx
│       │   ├── test_1.md
│       │   ├── test_1.pdf
│       │   └── test_1.txt
│       └── output
├── docs
│   ├── assets
│   │   └── splitter.drawio.svg
│   ├── chunker
│   │   └── docs.md
│   ├── index.md
│   ├── reader
│   │   └── docs.md
│   └── splitter
│       └── docs.md
├── mkdocs.yml
├── pyproject.toml
├── requirements.txt
├── scripts
│   ├── conftest.py
│   └── validate_commit_msg.py
├── src
│   ├── __init__.py
│   ├── application
│   │   ├── api
│   │   │   ├── app.py
│   │   │   ├── config.py
│   │   │   ├── models.py
│   │   │   └── routers
│   │   │       └── split.py
│   │   └── cli.py
│   ├── chunker
│   │   ├── __init__.py
│   │   └── chunk_manager.py
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
│       └── logging_manager.py
├── test
│   ├── chunker
│   │   ├── __init__.py
│   │   └── test_chunk_manager.py
│   ├── reader
│   │   ├── __init__.py
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
│       └── __init__.py
└── uv.lock
```

## Contact

If you like to contribute to my project, please, send an e-mail to [andresherencia2000@gmail.com](mailto:andresherencia2000@gmail.com)