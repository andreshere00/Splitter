from src.domain.reader.readers.markitdown_reader import MarkItDownReader


# Dummy class to replace MarkItDown.
class DummyMarkItDown:
    def __init__(self, llm_client=None, llm_model=None):
        self.llm_client = llm_client
        self.llm_model = llm_model

    def convert(self, file_path: str):
        # Create a dummy result with a text_content attribute.
        class DummyResult:
            text_content = f"converted: {file_path}"

        return DummyResult()


def test_markitdown_converter(monkeypatch):
    """
    Test that MarkItDownReader stores provided llm parameters and uses
    the MarkItDown (monkey-patched) conversion method.
    """
    # Monkey-patch the MarkItDown class in the module with our dummy.
    monkeypatch.setattr(
        "src.domain.reader.readers.markitdown_reader.MarkItDown", DummyMarkItDown
    )

    dummy_client = "dummy_client"
    dummy_model = "dummy_model"
    converter = MarkItDownReader(llm_client=dummy_client, llm_model=dummy_model)

    # Verify that the llm parameters are correctly stored.
    assert converter.llm_client == dummy_client
    assert converter.llm_model == dummy_model

    # Test that the convert method returns the expected dummy result.
    result = converter.convert("test_file.txt")
    expected = "converted: test_file.txt"
    assert result == expected
