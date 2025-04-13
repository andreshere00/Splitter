import json

import pytest
import yaml

from src.domain.splitter.splitters.schema_based_splitter import SchemaBasedSplitter


class TestSchemaBasedSplitter:
    @pytest.fixture
    def csv_text(self):
        # CSV-like input; first line is header, then three rows.
        return (
            "col1,col2\nrow1_val1,row1_val2\nrow2_val1,row2_val2\nrow3_val1,row3_val2"
        )

    @pytest.fixture
    def json_text(self):
        # JSON input as a list of registers.
        sample = [
            {"a": "A1", "b": "B1"},
            {"a": "A2", "b": "B2"},
            {"a": "A3", "b": "B3"},
            {"a": "A4", "b": "B4"},
            {"a": "A5", "b": "B5"},
        ]
        return json.dumps(sample)

    @pytest.fixture
    def yaml_text(self):
        # YAML input that is equivalent to the JSON above.
        sample = [
            {"a": "A1", "b": "B1"},
            {"a": "A2", "b": "B2"},
            {"a": "A3", "b": "B3"},
            {"a": "A4", "b": "B4"},
            {"a": "A5", "b": "B5"},
        ]
        return yaml.dump(sample, default_flow_style=False)

    @pytest.fixture
    def splitter(self):
        return SchemaBasedSplitter(max_num_rows=2, header_lines=1, max_chunk_size=300)

    def test_csv_fallback(self, splitter, csv_text):
        # Expect CSV mode: The header is the first line, then rows split by max_num_rows.
        chunks = splitter.split(csv_text)
        # Given 1 header and 3 rows with max_num_rows=2, we expect two chunks.
        assert len(chunks) == 2
        # First chunk should contain header + first 2 rows.
        assert "col1,col2" in chunks[0]
        assert "row1_val1,row1_val2" in chunks[0]
        assert "row2_val1,row2_val2" in chunks[0]
        # Second chunk should contain header + remaining row.
        assert "row3_val1,row3_val2" in chunks[1]

    def test_json_structured(self, splitter, json_text):
        # Test structured splitting for JSON input
        chunks = splitter.split(json_text)
        # Since RecursiveJsonSplitter splits based on character count,
        # we expect several chunks (at least one) and each chunk should be valid JSON.
        assert len(chunks) >= 1
        for chunk in chunks:
            # Validate that each chunk can be loaded as JSON.
            try:
                parsed = json.loads(chunk)
            except Exception as e:
                pytest.fail(f"Chunk is not valid JSON: {e}")
            # Optionally, check for expected keys like "header" and "rows".
            # Some behavior depends on the RecursiveJsonSplitter implementation.
            assert isinstance(parsed, dict) or isinstance(parsed, list)

    def test_yaml_structured(self, splitter, yaml_text):
        # Test structured splitting for YAML input by converting YAML to JSON and splitting
        chunks = splitter.split(yaml_text)
        # Validate that we received at least one chunk and each chunk is valid JSON.
        assert len(chunks) >= 1
        for chunk in chunks:
            try:
                parsed = json.loads(chunk)
            except Exception as e:
                pytest.fail(f"Chunk from YAML is not valid JSON: {e}")
            assert isinstance(parsed, dict) or isinstance(parsed, list)
