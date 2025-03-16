import unittest

from src.splitter.splitters.recursive_splitter import RecursiveSplitter

# Sample text for testing.
SAMPLE_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eget purus non est porta rutrum. "
    "Suspendisse euismod lectus laoreet sem pellentesque egestas et et sem. Pellentesque ex felis, cursus "
    "eget ornare eu, posuere vitae ante. Nam et hendrerit neque, sed ornare tortor. Quisque sodales "
    "scelerisque odio ut sodales. Suspendisse efficitur ante non ante pellentesque, ac consequat tellus "
    "mattis. Phasellus blandit risus tortor, nec tempor tellus accumsan eu.\n\n"
    "Aliquam semper eu orci ut pretium. Nulla a tempor ligula. Vestibulum vel metus efficitur, tincidunt "
    "erat quis, dapibus nisi. Donec finibus odio vitae tortor elementum efficitur. Nunc non eros erat. "
    "Suspendisse potenti. Etiam magna orci, egestas vitae diam in, fermentum eleifend orci. Sed ligula dolor, "
    "euismod a efficitur sit amet, suscipit vitae tellus. Etiam et purus viverra, pulvinar dui vitae, "
    "euismod dolor. In venenatis quam et tortor semper, quis dapibus arcu volutpat. Vivamus urna orci, aliquet "
    "id nisl in, volutpat luctus enim.\n\n"
    "Duis accumsan diam tristique mattis bibendum. Pellentesque a justo non augue dignissim hendrerit id "
    "eget nisl. Morbi commodo scelerisque justo, at varius purus varius fringilla. Sed in nunc est. Sed "
    "elementum urna in ligula placerat hendrerit. Nullam tempus a metus sed suscipit. Quisque nec erat "
    "gravida lacus auctor sodales. Maecenas placerat viverra mauris lacinia eleifend. Etiam gravida orci vitae "
    "fermentum tempor. Aliquam erat volutpat. In id malesuada elit, id ornare enim. Sed sodales mi risus, eget "
    "lacinia nisi blandit ut. Donec interdum venenatis sagittis.\n\n"
    "Suspendisse ac turpis tellus. Phasellus iaculis lacus ante, et rutrum tortor semper at. Aliquam molestie, "
    "ante eget viverra volutpat, ligula ante cursus magna, vel suscipit dui felis et tellus. Cras urna quam, "
    "molestie blandit aliquet quis, consequat in urna. Duis ac feugiat nisl. Proin gravida dolor mi, eget "
    "imperdiet eros elementum quis. Vivamus justo quam, finibus vitae accumsan id, dignissim luctus mauris. Orci "
    "varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.\n\n"
    "Maecenas in egestas neque. Duis eu sapien sed nunc imperdiet dignissim. Duis maximus, lacus nec eleifend "
    "pretium, lectus neque elementum augue, sit amet convallis justo sem et felis. Integer elementum, mauris "
    "non cursus porta, tortor tellus accumsan odio, eget sollicitudin ligula quam et erat. Aliquam erat volutpat. "
    "Ut pellentesque cursus rhoncus. Suspendisse a mollis elit, in rhoncus felis. Aliquam vel leo vel nulla "
    "imperdiet sodales vitae id leo. Pellentesque auctor sollicitudin rhoncus. Nullam egestas risus vel quam "
    "efficitur pellentesque. Maecenas commodo justo ligula, at scelerisque elit venenatis sit amet. Etiam "
    "tincidunt neque elit, fringilla hendrerit orci fermentum et. In pretium ac purus in iaculis."
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
        self.assertEqual(
            str(context.exception),
            "Chunk size and overlap parameters should be greater than 0",
        )

    def test_invalid_overlap_raises_exception(self):
        """Test that a non-positive overlap value raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            RecursiveSplitter(size=100, overlap=0)
        self.assertEqual(
            str(context.exception),
            "Chunk size and overlap parameters should be greater than 0",
        )
