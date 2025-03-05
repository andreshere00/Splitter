import unittest
from src.services.paragraph_splitter import ParagraphSplitter

# The sample text to be used in tests.
SAMPLE_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eget purus non est porta rutrum. Suspendisse euismod lectus laoreet sem pellentesque egestas et et sem. Pellentesque ex felis, cursus eget ornare eu, posuere vitae ante. Nam et hendrerit neque, sed ornare tortor. Quisque sodales scelerisque odio ut sodales. Suspendisse efficitur ante non ante pellentesque, ac consequat tellus mattis. Phasellus blandit risus tortor, nec tempor tellus accumsan eu.\n\n"
    "Aliquam semper eu orci ut pretium. Nulla a tempor ligula. Vestibulum vel metus efficitur, tincidunt erat quis, dapibus nisi. Donec finibus odio vitae tortor elementum efficitur. Nunc non eros erat. Suspendisse potenti. Etiam magna orci, egestas vitae diam in, fermentum eleifend orci. Sed ligula dolor, euismod a efficitur sit amet, suscipit vitae tellus. Etiam et purus viverra, pulvinar dui vitae, euismod dolor. In venenatis quam et tortor semper, quis dapibus arcu volutpat. Vivamus urna orci, aliquet id nisl in, volutpat luctus enim.\n\n"
    "Duis accumsan diam tristique mattis bibendum. Pellentesque a justo non augue dignissim hendrerit id eget nisl. Morbi commodo scelerisque justo, at varius purus varius fringilla. Sed in nunc est. Sed elementum urna in ligula placerat hendrerit. Nullam tempus a metus sed suscipit. Quisque nec erat gravida lacus auctor sodales. Maecenas placerat viverra mauris lacinia eleifend. Etiam gravida orci vitae fermentum tempor. Aliquam erat volutpat. In id malesuada elit, id ornare enim. Sed sodales mi risus, eget lacinia nisi blandit ut. Donec interdum venenatis sagittis.\n\n"
    "Suspendisse ac turpis tellus. Phasellus iaculis lacus ante, et rutrum tortor semper at. Aliquam molestie, ante eget viverra volutpat, ligula ante cursus magna, vel suscipit dui felis et tellus. Cras urna quam, molestie blandit aliquet quis, consequat in urna. Duis ac feugiat nisl. Proin gravida dolor mi, eget imperdiet eros elementum quis. Vivamus justo quam, finibus vitae accumsan id, dignissim luctus mauris. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.\n\n"
    "Maecenas in egestas neque. Duis eu sapien sed nunc imperdiet dignissim. Duis maximus, lacus nec eleifend pretium, lectus neque elementum augue, sit amet convallis justo sem et felis. Integer elementum, mauris non cursus porta, tortor tellus accumsan odio, eget sollicitudin ligula quam et erat. Aliquam erat volutpat. Ut pellentesque cursus rhoncus. Suspendisse a mollis elit, in rhoncus felis. Aliquam vel leo vel nulla imperdiet sodales vitae id leo. Pellentesque auctor sollicitudin rhoncus. Nullam egestas risus vel quam efficitur pellentesque. Maecenas commodo justo ligula, at scelerisque elit venenatis sit amet. Etiam tincidunt neque elit, fringilla hendrerit orci fermentum et. In pretium ac purus in iaculis."
)

class TestParagraphSplitter(unittest.TestCase):

    def test_split_into_single_paragraph_chunks(self):
        """Splitting into chunks of 1 paragraph should return each paragraph separately."""
        splitter = ParagraphSplitter(num_paragraphs=1)
        chunks = splitter.split(SAMPLE_TEXT)
        # Expected: each non-empty paragraph as a separate chunk.
        paragraphs = [p.strip() for p in SAMPLE_TEXT.split("\n") if p.strip()]
        self.assertEqual(chunks, paragraphs)

    def test_split_into_max_paragraph_chunks(self):
        """
        Splitting into chunks of 100 paragraphs should return a single chunk 
        containing all paragraphs (since the sample text contains fewer paragraphs).
        """
        splitter = ParagraphSplitter(num_paragraphs=100)
        chunks = splitter.split(SAMPLE_TEXT)
        paragraphs = [p.strip() for p in SAMPLE_TEXT.split("\n") if p.strip()]
        expected = "\n\n".join(paragraphs)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], expected)

    def test_split_into_zero_paragraphs_raises_exception(self):
        """Splitting into chunks of 0 paragraphs should raise a ValueError."""
        with self.assertRaises(ValueError) as context:
            ParagraphSplitter(num_paragraphs=0)
        self.assertEqual(str(context.exception), "Number of paragraphs must be greater than 0")

    def test_split_into_negative_paragraphs_raises_exception(self):
        """Splitting into chunks of negative paragraphs should raise a ValueError."""
        with self.assertRaises(ValueError) as context:
            ParagraphSplitter(num_paragraphs=-3)
        self.assertEqual(str(context.exception), "Number of paragraphs must be greater than 0")