# Splitter

## Overview

The **Splitter** application aims to convert documents into markdown format, and split them into **chunks** using various splitting strategies. The architecture consists of three main pieces: the `ReadManager`, the `SplitManager` and the `ChunkManager`. Observe the following diagram:

![Splitter architecture diagram](./assets/splitter.drawio.svg)

## How to launch the application

The application is exposed via:

- **REST API**
- **CLI**

### Pre-requisites

The following tools and packages are needed to execute the application:

- [Python](https://www.python.org/) with `make`. `$PYTHONPATH` may be set in the `.env` file.
- [Docker](https://www.docker.com/).

To install all the dependencies, you can use `make install`.

```bash
make install
```

This application uses `uv` as dependency management tool, if not installed, use the following command:

```sh
make install-uv
```

### API

The API is accessed through a FastAPI application. This application can be launched executing:

```bash
make serve
```

### **API Definition**

#### **Input**

Object: `class <ChunkRequest>`

```python
document_name: Optional[str] = None
document_path: str
document_id: Optional[str] = None
split_method: str
split_params: Optional[Dict[str, Any]] = None
metadata: Optional[List[str]] = []
```


#### **Output**

Object: `class <ChunkResponse>`

```python
chunks: List[str]
chunk_id: List[str]
chunk_path: str
document_id: str
document_name: Optional[str] = None
split_method: str
split_params: Optional[Dict[str, Any]] = None
metadata: Optional[List[str]] = []
```

### CLI

The application is accessible through Command Line Interface (CLI) using the following command:

```bash
make run
```

### Docker

The API-interface can be launched using Docker with the following Make commands:

Build the image:

```sh
make docker-api-build # build the image
```

Run the image:

```sh
make docker-api-run # run the image
```

Application will be accessible through the browser at the host `0.0.0.0:8080/docs`. 

These values are configurable through the following environment variables:

```sh
PORT=8080
HOST=0.0.0.0
LOG_LEVEL=info
```

## Configuration 

File handling, splitting methods and application settings can be modified using a [configuration file](src/config.yaml). This file is provided in `src/config.yaml` file. Otherwise, parameters can be passed as API parameters. The config file has the following structure by default:

```yaml
# 1. File I/O Configuration
file_io:
  input_path: "data/input"     # Where the application reads files from
  output_path: "data/output"   # Where the application saves the results

# 2. Logging Configuration
logging:
  enabled: true                # Set to false to disable logging
  level: "INFO"                # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "%(asctime)s - %(levelname)s - %(message)s"
  handlers:
    - type: "stream"
    - type: "file"
      filename: "logs/app.log"
      mode: "a"

# 3. Splitting Methods Configuration
splitter:
  method: "recursive"

  methods:
    word:
      num_words: 100  # Number of words in each chunk

    sentence:
      num_sentences: 5  # Number of sentences in each chunk

    paragraph:
      num_paragraphs: 3  # Number of paragraphs in each chunk

    semantic:
      language_model: "bert-base-uncased"  # For semantic similarity
      overlap: 0.2                         # Overlap ratio between chunks

    fixed:
      size: 100  # Number of characters per chunk

    paged:
      num_pages: 1  # Number of pages in each chunk
      overlap: 0.1  # Overlap (in pages) between chunks

    recursive:
      size: 10000     # Characters per chunk
      overlap: 1000   # Overlapping characters

    row-column:
      num_columns: 2
      column_names: ["Column1", "Column2"]
      num_rows: 5
      row_names: ["Row1", "Row2"]

    schema-based:
      num_registers: 50  # Number of registers (or rows) per chunk
      overlap: 5         # Overlapping registers

    auto:
      fallback_method: "paragraph"
      chunk_size: 500
      overlap: 100
```

---

## Architecture

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

## Project scenario

This application compose a piece of an ambicious project named **"MultiRAG"**. This system aims to be a super modullarizable and open-source RAG system which is fully customizable piece by piece. Observe the following architecture diagram:

[MultiRAG architecture](assets/MultiRAG.drawio.svg)

## Project Structure
```bash
.
├── CHANGELOG.md
├── Dockerfile.api
├── Makefile
├── README.md
├── data
│   ├── input
│   │   └── andres_herencia_TFM_TECI.pdf
│   ├── output
│   └── test
│       ├── input
│       │   ├── test_1.docx
│       │   ├── test_1.md
│       │   ├── test_1.pdf
│       │   └── test_1.txt
│       └── output
├── docker-compose.yaml
├── docs
│   ├── assets
│   │   ├── MultiRAG.drawio.svg
│   │   ├── splitter.drawio.svg
│   │   └── splitter.drawio_v0.1.0.drawio.svg
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
│   ├── __pycache__
│   │   └── __init__.cpython-312.pyc
│   ├── application
│   │   ├── api
│   │   │   ├── __pycache__
│   │   │   │   ├── app.cpython-312.pyc
│   │   │   │   └── models.cpython-312.pyc
│   │   │   ├── app.py
│   │   │   ├── config.py
│   │   │   ├── models.py
│   │   │   └── routers
│   │   │       ├── __pycache__
│   │   │       │   └── split.cpython-312.pyc
│   │   │       └── split.py
│   │   └── cli.py
│   ├── chunker
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── chunk_manager.cpython-312.pyc
│   │   └── chunk_manager.py
│   ├── config.yaml
│   ├── main.py
│   ├── reader
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── read_manager.cpython-312.pyc
│   │   └── read_manager.py
│   ├── splitter
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── base_splitter.cpython-312.pyc
│   │   │   └── split_manager.cpython-312.pyc
│   │   ├── base_splitter.py
│   │   ├── split_manager.py
│   │   └── splitters
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-312.pyc
│   │       │   ├── fixed_splitter.cpython-312.pyc
│   │       │   ├── paragraph_splitter.cpython-312.pyc
│   │       │   ├── recursive_splitter.cpython-312.pyc
│   │       │   ├── sentence_splitter.cpython-312.pyc
│   │       │   └── word_splitter.cpython-312.pyc
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
│       ├── __pycache__
│       │   └── logging_manager.cpython-312.pyc
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