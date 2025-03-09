import pytest
from src.services.word_splitter import WordSplitter

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

class TestWordSplitter:
    def test_split_chunks_of_10(self):
        """
        Test splitting the text into chunks of 10 words.
        Prints each chunk for context.
        """
        splitter = WordSplitter(num_words=10)
        groups = splitter.split(SAMPLE_TEXT)
        
        print("\n--- Test Split in Chunks of 10 Words ---")
        for idx, group in enumerate(groups, start=1):
            print(f"Chunk {idx}: {group}")
        
        # Verify that all groups except possibly the last one have exactly 10 words.
        for group in groups[:-1]:
            word_count = len(group.split())
            assert word_count == 10, f"Expected 10 words, got {word_count}"
        # The last group may have fewer than 10 words.
        last_count = len(groups[-1].split())
        assert last_count <= 10, f"Expected last chunk to have <= 10 words, got {last_count}"

    def test_split_chunks_of_10000(self):
        """
        Test splitting the text into chunks of 10000 words.
        Since the text has fewer words than 10000, it should return a single chunk.
        """
        splitter = WordSplitter(num_words=10000)
        groups = splitter.split(SAMPLE_TEXT)
        
        print("\n--- Test Split in Chunks of 10000 Words ---")
        print("Output groups:", groups)
        
        # Expect one group containing the entire text.
        assert len(groups) == 1
        
        # Ensure the output chunk equals the original text (after normalizing whitespace).
        assert groups[0].split() == SAMPLE_TEXT.split()

    def test_split_chunks_of_0(self):
        """
        Test that splitting with 0 words per chunk raises an Exception.
        """
        with pytest.raises(ValueError, match="num_words must be greater than 0"):
            WordSplitter(num_words=0)

    def test_split_chunks_of_negative(self):
        """
        Test that splitting with a negative number of words per chunk raises an Exception.
        """
        with pytest.raises(ValueError, match="num_words must be greater than 0"):
            WordSplitter(num_words=-3)
