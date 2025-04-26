from pathlib import Path

import pytest

from src.infrastructure.converter.convert_manager import ConvertManager


class DummyPDF:
    calls = []

    def __init__(self):
        pass

    def convert(self, src, dst):
        DummyPDF.calls.append((Path(src), Path(dst)))


class DummyJSON:
    calls = []

    def __init__(self):
        pass

    def convert(self, src, dst):
        DummyJSON.calls.append((Path(src), Path(dst)))


class DummyPNG:
    calls = []

    def __init__(self):
        pass

    def convert(self, src, dst):
        DummyPNG.calls.append((Path(src), Path(dst)))


@pytest.fixture(autouse=True)
def clear_dummy_calls():
    # reset between tests
    DummyPDF.calls.clear()
    DummyJSON.calls.clear()
    DummyPNG.calls.clear()
    yield
    DummyPDF.calls.clear()
    DummyJSON.calls.clear()
    DummyPNG.calls.clear()


def test_convert_folder_redirects_to_correct_converters(monkeypatch, tmp_path):
    # 1) point ConvertManager at your real config.yaml
    project_root = Path(__file__).parents[3]
    config_path = (
        project_root / "config_tmp.yaml"
    )  # TODO: Change to actual config.yaml path
    cm = ConvertManager(config_path)

    # 2) monkey-patch the internal mapping so real converters are replaced by our dummies
    monkeypatch.setattr(
        cm,
        "_CREATORS",
        {
            "pdf": DummyPDF,
            "json": DummyJSON,
            "png": DummyPNG,
        },
    )

    # 3) run on your test inputs
    input_dir = project_root / "data" / "test" / "input"
    output_dir = tmp_path / "out"
    cm.convert_folder(input_dir, output_dir)

    # 4) for each file in input_dir, check that:
    #    - if converter == "none", we just copied it,
    #    - otherwise we called the right dummy and produced a file.ext
    for src in sorted(input_dir.iterdir()):
        ext = src.suffix.lstrip(".")
        conv_name = cm._get_conversion_name(src.suffix)
        # expected destination path
        out_name = (
            src.name if conv_name == "none" else src.with_suffix(f".{conv_name}").name
        )
        dst = output_dir / out_name

        # file must exist in output
        assert dst.exists(), f"{dst} was not created"

        if conv_name == "none":
            # none of our dummy converters should have seen this file
            all_calls = DummyPDF.calls + DummyJSON.calls + DummyPNG.calls
            assert not any(
                c[0] == src for c in all_calls
            ), f"{src.name} should have been copied but converter was called"
        else:
            # ensure exactly one call to the right dummy
            if conv_name == "pdf":
                assert (src, dst) in DummyPDF.calls
            elif conv_name == "json":
                assert (src, dst) in DummyJSON.calls
            elif conv_name == "png":
                assert (src, dst) in DummyPNG.calls
            else:
                pytest.skip(f"No dummy converter for '{conv_name}'")
