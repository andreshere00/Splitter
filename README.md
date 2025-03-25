# Splitter

## Overview

The **Splitter** application aims to convert documents into markdown format, and split them into **chunks** using various splitting strategies. The architecture consists of three main pieces: the `ReadManager`, the `SplitManager` and the `ChunkManager`. Observe the following diagram:

![Splitter architecture diagram](./docs/assets/splitter.drawio.svg)

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

Many other commands are available (use `make help` to consult):

```sh
  make docs             - Run the documentation server.
  make install          - Install application dependencies using uv.
  make install-uv       - Install uv CLI (OS-specific).
  make run              - Execute the application using uv.
  make serve            - Serve the FastAPI application.
  make docker-api-build - Build the API dockerized application.
  make docker-api-run   - Run the API dockerized application.
  make test             - Run tests using uv and pytest.
  make shell            - Run a uv shell.
  make pre-commit       - Install pre-commit hooks.
  make format           - Run pyupgrade, isort, black and flake8 for code style.
  make clean            - Clean output, cache and log files.
  make clean-cache      - Clean cache files.
  make clean-data       - Clean output data files.
  make clean-log        - Clean log files.
  make remove-data      - Remove data presented in the output folder.
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

    # semantic:
    #   language_model: "bert-base-uncased"  # For semantic similarity
    #   overlap: 0.2                         # Overlap ratio between chunks

    fixed:
      size: 100  # Number of characters per chunk

    # paged:
    #   num_pages: 1  # Number of pages in each chunk
    #   overlap: 0.1  # Overlap (in pages) between chunks

    recursive:
      size: 10000     # Characters per chunk
      overlap: 1000   # Overlapping characters

    # row-column:
    #   num_columns: 2
    #   column_names: ["Column1", "Column2"]
    #   num_rows: 5
    #   row_names: ["Row1", "Row2"]

    # schema-based:
    #   num_registers: 50  # Number of registers (or rows) per chunk
    #   overlap: 5         # Overlapping registers

    # auto:
    #   fallback_method: "paragraph"
    #   chunk_size: 500
    #   overlap: 100

# 4. OCR configuration
ocr:
  method: "azure"  # Options: openai, textract, huggingface, none
  include_image_blobs: false
  include_json_structure: false

```

---

## Architecture

### **1. Read Manager**
- Responsible for reading input documents.
- Supports local file formats: `txt`, `md`, ~~'doc'~~, `docx`, ~~`xls`~~, `xlsx`, `pdf`, ~~`ppt`~~, `pptx`, ~~`json`~~, ~~`yaml`~~.
- If required, **OCR** can be applied to extract text from scanned documents (OpenAI, AzureOpenAI, ~~Textract~~, ~~Mistral~~, ~~Custom~~). 

### **2. Split Manager**
- Splits text into meaningful chunks based on different strategies.
- Includes the following methods:

| Splitter Name          | Description | Parameters | Compatible Formats |
|------------------------|-------------|------------|--------------------|
| **Word Splitter**      | Splits text into words. | Input data, number of words in each chunk. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx`, `.jpg`, `.png` |
| **Sentence Splitter**  | Splits text into sentences. | Input data, number of sentences in each chunk. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx`, `.jpg`, `.png` |
| **Paragraph Splitter** | Splits text into paragraphs. | Input data, number of paragraphs in each chunk. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx`, `.jpg`, `.png` |
| **Semantic Splitter**  | Splits text based on semantic similarity, using a language model. | Input data, language model, overlap. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx`, `.jpg`, `.png` |
| **Fixed Splitter**     | Splits text into a fixed number of words or characters. | Input data, number of characters in each chunk. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx`, `.jpg`, `.png` |
| **Paged Splitter**     | Splits text into pages. | Input data, number of pages in each chunk, overlap. | `docx`, `pdf`, `xls`, `xlsx`, `ppt`, `pptx` |
| **Recursive Splitter** | Splits based on a specified chunk size with overlap. | Input data, number of characters in each chunk, overlap parameter. | `txt`, `markdown`, `docx`, `pdf`, `ppt`, `pptx`, `.jpg`, `.png` |
| **Row-Column Splitter** | Splits table content by rows or columns. | Input data, number of columns, column names, number of rows, row names. | `xlsx`, `xls`, `json`, `yaml` |
| **Schema-based Splitter** | Splits a hierarchical schema while preserving headers. | Input data, number of registers, overlap. | `json`, `yaml`, `xml`, `xls`, `xlsx`, `ppt`, `pptx` |
| **Auto Splitter**      | Combines multiple splitting methods based on document content. | Input data, number of characters in each chunk, overlap. | All formats |

### **3. Chunk Manager**
- Saves the generated chunks from **Chunk Manager**.
- Features:
  - **Aggregator**: Groups related chunks.
  - **Markdown conversion**: Converts text into Markdown format.
  - **Error handling**: Ensures smooth chunking.


## Scenario

This application compose a piece of an ambicious project named **"MultiRAG"**. This system aims to be a super modullarizable and open-source RAG system which is fully customizable piece by piece. Observe the following architecture diagram:

[MultiRAG architecture](docs/assets/MultiRAG.drawio.svg)


## Project Structure
```bash
.
├── CHANGELOG.md
├── Dockerfile.api
├── Makefile
├── README.md
├── data
│   ├── input
│   │   └── image.jpg
│   ├── output
│   └── test
│       ├── input
│       │   ├── test_1.docx
│       │   ├── test_1.md
│       │   ├── test_1.pdf
│       │   ├── test_1.pptx
│       │   ├── test_1.txt
│       │   └── test_1.xlsx
│       └── output
├── docker-compose.yaml
├── docs
│   ├── assets
│   │   ├── MultiRAG.drawio.svg
│   │   ├── splitter.drawio.svg
│   │   ├── splitter.drawio_v0.1.0.drawio.svg
│   │   └── splitter_v0.3.0.drawio.svg
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
│   │   │       ├── health.py
│   │   │       └── split.py
│   │   └── cli.py
│   ├── chunker
│   │   ├── __init__.py
│   │   └── chunk_manager.py
│   ├── config.yaml
│   ├── main.py
│   ├── model
│   │   ├── base_client.py
│   │   ├── llm_client.py
│   │   └── models
│   │       ├── azure_client.py
│   │       ├── openai_client.py
│   │       └── textract_client.py
│   ├── reader
│   │   ├── __init__.py
│   │   ├── base_reader.py
│   │   ├── read_manager.py
│   │   └── readers
│   │       ├── custom_reader.py
│   │       ├── docling_reader.py
│   │       ├── markitdown_reader.py
│   │       ├── ocr_reader.py
│   │       ├── pdfplumber_reader.py
│   │       └── textract_reader.py
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
│       ├── config_loader.py
│       └── logging_manager.py
├── test
│   ├── application
│   │   ├── __init__.py
│   │   └── api
│   │       ├── __init__.py
│   │       ├── routers
│   │       │   ├── __init__.py
│   │       │   ├── test_health.py
│   │       │   └── test_split.py
│   │       └── test_app.py
│   ├── chunker
│   │   ├── __init__.py
│   │   └── test_chunk_manager.py
│   ├── model
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── test_azure_client.py
│   │   │   └── test_openai_client.py
│   │   └── test_llm_client.py
│   ├── reader
│   │   ├── __init__.py
│   │   ├── readers
│   │   │   ├── __init__.py
│   │   │   └── test_markitdown_reader.py
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

- E-mail: [andresherencia2000@gmail.com](mailto:andresherencia2000@gmail.com).
- LinkedIn: [link](https://linkedin.com/in/andres-herencia)
