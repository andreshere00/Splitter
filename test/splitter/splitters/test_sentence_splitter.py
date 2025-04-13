import re

import pytest

from src.domain.splitter.splitters.sentence_splitter import SentenceSplitter

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


def test_split_into_chunks_of_5():
    splitter = SentenceSplitter(num_sentences=5)
    groups = splitter.split(SAMPLE_TEXT)

    print("\n--- Split into chunks of 5 sentences ---")
    for i, group in enumerate(groups, 1):
        print(f"Chunk {i}: {group}\n")

    # Count sentences in the original text
    sentences = re.split(r"(?<=[.!?])\s+", SAMPLE_TEXT)
    sentences = [s.strip() for s in sentences if s.strip()]
    expected_num_groups = (len(sentences) + 4) // 5  # Ceiling division

    assert len(groups) == expected_num_groups

    # Verify that all groups except possibly the last one have exactly 5 sentences.
    for group in groups[:-1]:
        sub_sentences = re.split(r"(?<=[.!?])\s+", group)
        sub_sentences = [s.strip() for s in sub_sentences if s.strip()]
        assert len(sub_sentences) == 5


def test_split_into_chunks_of_1000():
    splitter = SentenceSplitter(num_sentences=1000)
    groups = splitter.split(SAMPLE_TEXT)

    print("\n--- Split into chunks of 1000 sentences ---")
    for i, group in enumerate(groups, 1):
        print(f"Chunk {i}: {group}\n")

    # With 1000 sentences per group and fewer than 1000 sentences in the text,
    # we expect a single group containing all sentences.
    assert len(groups) == 1


def test_split_into_chunks_of_0():
    with pytest.raises(ValueError, match="num_sentences must be greater than 0"):
        SentenceSplitter(num_sentences=0)


def test_split_into_chunks_of_negative():
    with pytest.raises(ValueError, match="num_sentences must be greater than 0"):
        SentenceSplitter(num_sentences=-3)
