import unittest
from src.services.recursive_splitter import RecursiveSplitter

# Sample text for testing.
SAMPLE_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Suspendisse euismod lectus laoreet sem pellentesque egestas et et sem. "
    "Pellentesque ex felis, cursus eget ornare eu, posuere vitae ante. "
    "Nam et hendrerit neque, sed ornare tortor. Quisque sodales scelerisque odio ut sodales. "
    "Suspendisse efficitur ante non ante pellentesque, ac consequat tellus mattis. "
    "Phasellus blandit risus tortor, nec tempor tellus accumsan eu. "
    "Aliquam semper eu orci ut pretium. Nulla a tempor ligula. "
    "Vestibulum vel metus efficitur, tincidunt erat quis, dapibus nisi."
)

class TestRecursiveSplitter(unittest.TestCase):
    def test_empty_text_returns_empty_list(self):
        """Test that splitting an empty text returns an empty list."""
        splitter = RecursiveSplitter(size=100, overlap=25)
        self.assertEqual(splitter.split(""), [])

    def test_valid_text_splits_into_chunks(self):
        """Test that a valid text is split into a list of non-empty string chunks."""
        splitter = RecursiveSplitter(size=100, overlap=25)
        chunks = splitter.split(SAMPLE_TEXT)
        # Print each chunk for debugging purposes.
        print("\n--- RecursiveSplitter Chunks ---")
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}:\n{chunk}\n{'-'*40}")
        # Check that we have at least one chunk.
        self.assertTrue(chunks, "Expected non-empty list of chunks.")
        # Ensure that each chunk is a non-empty string.
        for chunk in chunks:
            self.assertIsInstance(chunk, str)
            self.assertTrue(len(chunk) > 0)

    def test_invalid_size_raises_exception(self):
        """Test that a non-positive chunk size raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            RecursiveSplitter(size=0, overlap=25)
        self.assertEqual(str(context.exception), "Chunk size and overlap parameters should be greater than 0")

    def test_invalid_overlap_raises_exception(self):
        """Test that a non-positive overlap value raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            RecursiveSplitter(size=100, overlap=0)
        self.assertEqual(str(context.exception), "Chunk size and overlap parameters should be greater than 0")
        