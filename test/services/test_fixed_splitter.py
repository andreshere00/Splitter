import unittest
import os
from src.services.fixed_splitter import FixedSplitter

class TestFixedSplitter(unittest.TestCase):
    def setUp(self):
        # Directory where the test files are located.
        self.test_dir = os.path.join("data", "test")
        # List of test file names.
        self.test_files = [
            "test_1.doc",
            "test_1.txt",
            "test_1.pdf",
            "test_1.md",
            "test_1.docx"
        ]
        # Use a fixed chunk size for the test.
        self.fixed_size = 100
        self.splitter = FixedSplitter(size=self.fixed_size)

    def test_fixed_splitter_on_files(self):
        for file_name in self.test_files:
            file_path = os.path.join(self.test_dir, file_name)
            with self.subTest(file=file_name):
                try:
                    # Read file content as text.
                    # For simplicity, assume test files are plain text.
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    self.fail(f"Failed to read {file_path}: {e}")

                # Use FixedSplitter to split the content.
                chunks = self.splitter.split(content)
                
                # Reassemble the chunks.
                reconstructed = "".join(chunks)
                self.assertEqual(
                    reconstructed,
                    content,
                    f"Reconstructed text does not match original for {file_name}"
                )
                
                # Check that each chunk (except possibly the last one) is exactly fixed_size long.
                for chunk in chunks[:-1]:
                    self.assertEqual(
                        len(chunk),
                        self.fixed_size,
                        f"Chunk length is not {self.fixed_size} for {file_name}"
                    )