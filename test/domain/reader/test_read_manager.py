"""
test/domain/reader/test_read_manager.py

Integrated tests for ReadManager → ConvertManager → AnalyzeManager → Readers.
All heavy I/O and external deps are stubbed out with monkeypatch.
"""

import io
import os
import shutil
from pathlib import Path

import pytest
from fastapi import UploadFile

from src.domain.reader.read_manager import ReadManager
from src.domain.reader.readers.markitdown_reader import MarkItDownReader

# Path to the shipped test inputs
TEST_INPUT = Path("data/test/input")


@pytest.fixture
def dummy_config():
    """
    Minimal config dict: input_path → data/test/input,
    reader → markitdown, ocr → none.
    """
    return {
        "file_io": {"input_path": str(TEST_INPUT)},
        "reader": {"method": "markitdown"},
        "ocr": {"method": "none"},
    }


@pytest.fixture(autouse=True)
def speed_up_pipeline(monkeypatch):
    """
    0) Stub load_config so both managers see keys 'converter' and 'analyzer'.
    1) Patch ConvertManager.convert_file → simple copy.
    2) Patch AnalyzeManager.get_analyzer → (None, 'none').
    3) Patch Reader.convert methods → return dummy text or raise on .exe.
    """
    # 0) stub load_config for both modules
    fake_full_cfg = {
        "converter": {"default": "none", "override": {}},
        "analyzer": {"default": "none", "override": {}},
    }
    monkeypatch.setattr(
        "src.infrastructure.converter.convert_manager.load_config",
        lambda path: fake_full_cfg,
        raising=True,
    )
    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyze_manager.load_config",
        lambda path: fake_full_cfg,
        raising=True,
    )

    # 1) ConvertManager.convert_file just copies into dst_folder
    def fake_convert(self, src, dst_folder):
        dst = Path(dst_folder) / Path(src).name
        shutil.copy(src, dst)
        return dst

    monkeypatch.setattr(
        "src.infrastructure.converter.convert_manager.ConvertManager.convert_file",
        fake_convert,
        raising=True,
    )

    # 2) AnalyzeManager.get_analyzer always returns no-op
    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyze_manager.AnalyzeManager.get_analyzer",
        lambda self, ext: (None, "none"),
        raising=True,
    )

    # 3) Patch Reader.convert implementations
    def fake_md_convert(self, path):
        if Path(path).suffix.lower() == ".exe":
            from markitdown._markitdown import UnsupportedFormatException

            raise UnsupportedFormatException("Extension not supported")
        return f"# DUMMY MARKDOWN from {Path(path).name}\n"

    monkeypatch.setattr(
        "src.domain.reader.readers.markitdown_reader.MarkItDownReader.convert",
        fake_md_convert,
        raising=True,
    )
    monkeypatch.setattr(
        "src.domain.reader.readers.pdfplumber_reader.PDFPlumberReader.convert",
        lambda self, p: f"# DUMMY PDF TEXT from {Path(p).name}",
        raising=True,
    )
    monkeypatch.setattr(
        "src.domain.reader.readers.docling_reader.DoclingReader.convert",
        lambda self, p: f"# DUMMY DOCLING TEXT from {Path(p).name}",
        raising=True,
    )

    yield


@pytest.fixture
def read_manager(dummy_config):
    return ReadManager(config=dummy_config)


# ---------------------- TESTS ---------------------- #


@pytest.mark.parametrize("fname", ["test_1.md", "test_1.pdf", "test_1.txt"])
def test_read_valid_files(read_manager, fname):
    """Any supported file returns non-empty markdown text."""
    result = read_manager.read_file(fname)
    assert isinstance(result, str)
    assert result.strip() != ""


def test_read_file_not_found(read_manager):
    """Nonexistent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_manager.read_file("does_not_exist.md")


def test_read_empty_file(tmp_path, dummy_config):
    """Empty file raises ValueError."""
    empty = tmp_path / "empty.txt"
    empty.write_text("", encoding="utf-8")
    rm = ReadManager(config=dummy_config)
    with pytest.raises(ValueError, match="is empty"):
        rm.read_file(str(empty))


def test_read_invalid_extension_raises(read_manager):
    """Unsupported extension raises UnsupportedFormatException."""
    from markitdown._markitdown import UnsupportedFormatException

    with pytest.raises(UnsupportedFormatException):
        read_manager.read_file("malicious.exe")


def test_read_from_uploadfile(read_manager):
    """Reading via UploadFile yields the same dummy markdown."""
    file_path = TEST_INPUT / "test_1.pdf"
    data = file_path.read_bytes()
    upload = UploadFile(filename="test_1.pdf", file=io.BytesIO(data))
    text = read_manager.read_file_object(upload)
    assert text.strip().startswith("# DUMMY")


def test_reader_receives_client_and_model(monkeypatch, dummy_config):
    """
    Ensure that _make_reader is invoked with the (client, model)
    tuple returned by AnalyzeManager.get_analyzer.
    """
    # Have AnalyzeManager.get_analyzer return dummy client/model
    monkeypatch.setattr(
        "src.infrastructure.analyzer.analyze_manager.AnalyzeManager.get_analyzer",
        lambda self, ext: ("CLIENT_X", "MODEL_Y"),
        raising=True,
    )

    captured = {}

    def spy_init(self, client, model):
        captured["client"] = client
        captured["model"] = model
        # do not call super; we only need to capture args

    monkeypatch.setattr(
        "src.domain.reader.readers.markitdown_reader.MarkItDownReader.__init__",
        spy_init,
        raising=True,
    )

    rm = ReadManager(config=dummy_config)
    rm.read_file("test_1.md")

    assert captured["client"] == "CLIENT_X"
    assert captured["model"] == "MODEL_Y"
