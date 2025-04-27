FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=on

WORKDIR /app

# ------------------------------------------------------------------------
# OS-level deps for conversions
# ------------------------------------------------------------------------
RUN set -e; apt-get update && \
    apt-get install -y --no-install-recommends \
        libreoffice \
        tesseract-ocr \
        poppler-utils \
        ghostscript \
        libpangocairo-1.0-0 libcairo2 \
        fonts-dejavu-core \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml README.md ./
COPY src src
RUN pip install --upgrade pip setuptools wheel \
 && pip install .
COPY config.yaml config.yaml
COPY data data

LABEL org.opencontainers.image.title="Splitter" \
      org.opencontainers.image.description="Convert & split documents into LLM-friendly chunks" \
      org.opencontainers.image.version="0.4.0"

ENTRYPOINT ["python", "-m", "src.application.cli"]
CMD ["config.yaml"]
