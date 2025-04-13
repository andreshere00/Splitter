import os

import pytest

from src.domain.chunker.chunk_manager import ChunkManager


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

    # Create a configuration dictionary with the desired settings.
    config_data = {
        "file_io": {
            "input_path": "data/test/input",
            "output_path": output_path,
        },
        "logging": {
            "enabled": True,
            "level": "INFO",
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "handlers": [{"type": "stream"}],
        },
        "splitter": {
            "method": "fixed",
            "fixed": {"size": 100},
        },
    }

    print(f"[test_config fixture] Using config: {config_data}")
    print(f"[test_config fixture] Output path set to: {output_path}")

    yield config_data, output_path


# Fixture for ChunkManager that uses the temporary configuration dictionary.
@pytest.fixture
def chunk_manager(test_config, monkeypatch):
    config_data, output_path = test_config
    # Monkeypatch the SplitManager in the ChunkManager module to use our DummySplitManager.
    monkeypatch.setattr(
        "src.domain.chunker.chunk_manager.SplitManager",
        lambda config: DummySplitManager(),
    )
    cm = ChunkManager(config=config_data)
    print(
        f"[chunk_manager fixture] Initialized ChunkManager with config: {config_data}"
    )
    return cm


class TestChunkManager:
    def test_save_chunks(self, chunk_manager):
        print("[test_save_chunks] Starting test for save_chunks.")
        # Prepare a list of markdown chunks.
        chunks = [
            "# Chunk 1\nContent for chunk 1",
            "# Chunk 2\nContent for chunk 2",
            "# Chunk 3\nContent for chunk 3",
        ]
        base_filename = "test_file"
        original_extension = ".md"
        splitter_method = "fixed"
        saved_files = chunk_manager.save_chunks(
            chunks, base_filename, original_extension, splitter_method
        )
        print(f"[test_save_chunks] Saved files: {saved_files}")

        # Verify that each file exists and follows the naming convention.
        for i, filepath in enumerate(saved_files, start=1):
            expected_chunk_filename = f"{base_filename}_chunk_{i}.md"
            # Check that the filepath ends with the expected chunk file name.
            assert filepath.endswith(
                expected_chunk_filename
            ), f"File {filepath} does not end with expected chunk filename {expected_chunk_filename}"
            assert os.path.exists(filepath), f"File {filepath} was not created."

            # Verify that the file content matches the corresponding chunk.
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"[test_save_chunks] Content of {filepath}: {content}")
            assert content == chunks[i - 1], f"File {filepath} content mismatch."
        print("[test_save_chunks] Test completed successfully.")

    def test_process_file_invalid_format(self, test_config):
        config_data, _ = test_config
        print(
            "[test_process_file_invalid_format] Starting test for process_file invalid call."
        )

        # Instantiate ChunkManager with the config dictionary.
        cm = ChunkManager(config=config_data)
        print(
            f"[test_process_file_invalid_format] Initialized ChunkManager with config: {config_data}"
        )

        # Calling process_file should raise an AttributeError, as it doesn't exist.
        with pytest.raises(AttributeError):
            _ = cm.process_file("dummy_path")
        print("[test_process_file_invalid_format] Test completed successfully.")
