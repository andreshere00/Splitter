import unittest
from src.services.fixed_splitter import FixedSplitter

# The sample text to be used in tests.
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

class TestFixedSplitter(unittest.TestCase):
    def test_split_into_100_character_chunks(self):
        splitter = FixedSplitter(size=100)
        chunks = splitter.split(SAMPLE_TEXT)
        
        # Verify that every chunk except possibly the last one is exactly 100 characters.
        for chunk in chunks[:-1]:
            self.assertEqual(len(chunk), 100, "Chunk length is not 100 characters.")
        
        # Reassemble and check that the result matches the original text.
        reconstructed = "".join(chunks)
        self.assertEqual(reconstructed, SAMPLE_TEXT, "Reconstructed text does not match the original.")

    def test_split_into_single_character_chunks(self):
        splitter = FixedSplitter(size=1)
        chunks = splitter.split(SAMPLE_TEXT)
        
        # Every chunk should be exactly 1 character.
        for chunk in chunks:
            self.assertEqual(len(chunk), 1, "Chunk length is not 1 character.")
        
        # Reassemble and check.
        reconstructed = "".join(chunks)
        self.assertEqual(reconstructed, SAMPLE_TEXT, "Reconstructed text does not match the original.")

    def test_split_with_zero_chunk_size_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            FixedSplitter(size=0)
        self.assertEqual(str(context.exception), "Chunk size must be greater than 0")

    def test_split_with_negative_chunk_size_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            FixedSplitter(size=-1)
        self.assertEqual(str(context.exception), "Chunk size must be greater than 0")

    def test_split_into_large_chunk(self):
        # When chunk size is larger than the text length, we expect one chunk equal to the entire text.
        splitter = FixedSplitter(size=10000)
        chunks = splitter.split(SAMPLE_TEXT)
        # According to the specification, the text length is 2786 characters.
        self.assertEqual(len(chunks), 1, "Expected one chunk when chunk size is larger than text length.")
        self.assertEqual(len(chunks[0]), len(SAMPLE_TEXT), "The single chunk should be 2786 characters long.")

    def test_print_chunks(self):
        # For debugging: print chunks from splitting into 100-character pieces.
        splitter = FixedSplitter(size=100)
        chunks = splitter.split(SAMPLE_TEXT)
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i + 1}:\n{chunk}\n{'-'*40}")
