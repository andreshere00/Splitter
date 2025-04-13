import os

import pytest
import yaml

from src.domain.reader.readers.yaml_reader import YAMLReader


class TestYamlReader:
    @pytest.fixture
    def yaml_file(self, tmp_path):
        # Create a YAML file with some structured data.
        data = {"key1": "value1", "key2": [1, 2, 3]}
        content = yaml.dump(data, default_flow_style=False)
        file_path = tmp_path / "test.yaml"
        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    def test_yaml_reading(self, yaml_file):
        reader = YAMLReader()
        data = reader.convert(yaml_file)
        # Expect the parsed YAML data to equal the original data.
        expected = {"key1": "value1", "key2": [1, 2, 3]}
        assert data == expected

    def test_yaml_file_not_found(self, tmp_path):
        reader = YAMLReader()
        non_existent = os.path.join(str(tmp_path), "nonexistent.yaml")
        with pytest.raises(FileNotFoundError):
            reader.convert(non_existent)
