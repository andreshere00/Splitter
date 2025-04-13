import json

import pytest

from src.domain.reader.readers.pandas_reader import PandasReader


class TestPandasReader:
    @pytest.fixture
    def csv_file(self, tmp_path):
        content = "col1,col2\nval1,val2\nval3,val4"
        file_path = tmp_path / "test.csv"
        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    def test_csv_reading(self, csv_file):
        reader = PandasReader()
        data = reader.convert(csv_file)
        # Expect a list of dictionaries with keys 'col1' and 'col2'
        assert isinstance(data, list)
        assert data == [
            {"col1": "val1", "col2": "val2"},
            {"col1": "val3", "col2": "val4"},
        ]

    @pytest.fixture
    def json_file(self, tmp_path):
        # Create a simple JSON file that is tabular
        content = json.dumps([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        file_path = tmp_path / "test.json"
        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    def test_json_reading(self, json_file):
        reader = PandasReader()
        data = reader.convert(json_file)
        # Pandas reading for JSON returns a list of dicts.
        assert isinstance(data, list)
        assert data == [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
