import os
import shutil
import pytest
from pathlib import Path

from src.chunker.chunk_manager import ChunkManager

# A dummy splitter to bypass actual splitting logic.
class DummySplitManager:
    def split_text(self, text: str):
        # For testing, simply return the text in a list.
        return [text]

@pytest.fixture(scope="module")
def test_config(tmp_path_factory):
    # Use a fixed output path as required.
    output_path = "./data/test/output"
    os.makedirs(output_path, exist_ok=True)
    
    # Create a temporary config file with the desired output folder.
    config_content = f"""
file_io:
  input_path: "data/test/input"
  output_path: "{output_path}"

logging:
  enabled: true
  level: "INFO"
  format: "%(asctime)s - %(levelname)s - %(message)s"
  handlers:
    - type: "stream"

splitter:
  method: "fixed"
  fixed:
    size: 100
"""
    config_dir = tmp_path_factory.mktemp("config")
    config_file = config_dir / "config.yaml"
    config_file.write_text(config_content)
    yield config_file, output_path
    # Cleanup test output folder after tests complete.
    if os.path.exists("./data/test"):
        shutil.rmtree("./data/test")

# Fixture for ChunkManager that uses the temporary config file.
@pytest.fixture
def chunk_manager(test_config, monkeypatch):
    config_file, output_path = test_config
    # Monkeypatch the SplitManager in the ChunkManager module to use our DummySplitManager.
    monkeypatch.setattr("src.chunker.chunk_manager.SplitManager", lambda config_path: DummySplitManager())
    cm = ChunkManager(config_path=str(config_file))
    return cm

class TestChunkManager:
    def test_save_chunks(self, chunk_manager):
        # Prepare a list of markdown chunks.
        chunks = [
            "# Chunk 1\nContent for chunk 1",
            "# Chunk 2\nContent for chunk 2",
            "# Chunk 3\nContent for chunk 3"
        ]
        base_filename = "test_file"
        saved_files = chunk_manager.save_chunks(chunks, base_filename)
        
        # Verify that files are saved in the output folder "./data/test/output"
        output_folder = chunk_manager.output_path
        for i, filepath in enumerate(saved_files, start=1):
            expected_filename = f"{base_filename}_chunk_{i}.md"
            expected_filepath = os.path.join(output_folder, expected_filename)
            assert filepath == expected_filepath, f"Expected {expected_filepath}, got {filepath}"
            assert os.path.exists(filepath), f"File {filepath} was not created."
            
            # Verify that the file content matches the corresponding chunk.
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            assert content == chunks[i - 1], f"File {filepath} content mismatch."

    def test_process_file_invalid_format(self, tmp_path, test_config):
        config_file, output_path = test_config
        
        # Create an invalid (binary) file that cannot be read as UTF-8 text.
        invalid_file = tmp_path / "invalid.bin"
        invalid_file.write_bytes(b"\xff\xfe\xfd\xfc")
        
        # Instantiate ChunkManager; let it use the real SplitManager.
        cm = ChunkManager(config_path=str(config_file))
        
        # Calling process_file on an invalid file should trigger error handling and return an empty list.
        result = cm.process_file(str(invalid_file))
        assert result == [], "Expected an empty list when processing an invalid file format."
