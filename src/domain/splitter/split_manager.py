import logging
from typing import Dict, List, Optional, Union

from src.domain.splitter.base_splitter import BaseSplitter
from src.domain.splitter.splitters import (
    FixedSplitter,
    ParagraphSplitter,
    RecursiveSplitter,
    SchemaBasedSplitter,
    SentenceSplitter,
    WordSplitter,
)


class SplitManager:
    """
    Picks the right splitter class according to the YAML config
    and exposes `split_text(...)`.
    """

    def __init__(
        self,
        config: Optional[Dict] = None,
        *,
        split_method: Optional[str] = None,
    ) -> None:
        # Build a tiny config if none given
        if config is None:
            config = {"splitter": {"default": split_method or "auto"}}

        self.config = config
        self.splitter: BaseSplitter = self._create_splitter()

    def _create_splitter(self) -> BaseSplitter:
        splitter_cfg = self.config.get("splitter", {})

        # Accept both YAML-style `default` and API-style `method`
        method = splitter_cfg.get("default") or splitter_cfg.get("method") or "auto"

        mapping = {
            "word": WordSplitter,
            "sentence": SentenceSplitter,
            "paragraph": ParagraphSplitter,
            "fixed": FixedSplitter,
            "recursive": RecursiveSplitter,
            "schema-based": SchemaBasedSplitter,
            # "auto": AutoSplitter,
        }
        cls = mapping.get(method)
        if cls is None:
            raise ValueError(f"Invalid splitting method: {method}")

        raw_params: Union[Dict, List[Dict]] = splitter_cfg.get("methods", {}).get(
            method, {}
        )

        # Convert list-of-dicts (recursive) → single dict
        if isinstance(raw_params, list):
            params: Dict = {}
            for piece in raw_params:
                if isinstance(piece, dict):
                    params.update(piece)
        else:
            params = raw_params

        return cls(**(params or {}))

    def split_text(self, text: str) -> List[str]:
        if not text.strip():
            logging.warning("Empty text provided for splitting.")
            return []
        try:
            return self.splitter.split(text)
        except Exception as exc:
            logging.error(f"Error during text splitting: {exc}")
            return []
