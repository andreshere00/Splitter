import unittest
from src.services.fixed_splitter import FixedSplitter
from src.components.read_manager import ReadManager

class TestFixedSplitter(unittest.TestCase):
    def setUp(self):
        # List of test file names for different formats.
        self.test_files = [
            "test_1.docx",
            "test_1.md",
            "test_1.pdf",
            "test_1.txt",
        ]
        # Use a fixed chunk size for the test.
        self.fixed_size = 100
        self.splitter = FixedSplitter(size=self.fixed_size)
        # Initialize the ReadManager from our project.
        self.read_manager = ReadManager("src/config.yaml")
        # Override the input_path to point to our test files directory.
        self.read_manager.input_path = "data/test"

    def test_fixed_splitter_on_files(self):
        for file_name in self.test_files:
            with self.subTest(file=file_name):
                # Read file content using the appropriate file reader.
                content = self.read_manager.read_file(file_name)
                # Ensure the content was read successfully.
                self.assertTrue(content, f"Content for {file_name} should not be empty")
                
                # Use FixedSplitter to split the content.
                chunks = self.splitter.split(content)
                
                # Print each chunk for inspection.
                for i, chunk in enumerate(chunks):
                    print(f"Chunk {i + 1} for {file_name}:\n{chunk}\n{'-'*40}")
                
                # Reassemble the chunks.
                reconstructed = "".join(chunks)
                self.assertEqual(
                    reconstructed,
                    content,
                    f"Reconstructed text does not match original for {file_name}"
                )
                
                # Check that each chunk (except possibly the last one) is exactly fixed_size characters.
                for chunk in chunks[:-1]:
                    self.assertEqual(
                        len(chunk),
                        self.fixed_size,
                        f"Chunk length is not {self.fixed_size} for {file_name}"
                    )