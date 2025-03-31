from src.domain.splitter.base_splitter import BaseSplitter

# from src.domain.splitter.splitters.semantic_splitter import SemanticSplitter
# TODO: Semantic Splitter implementation
from src.domain.splitter.splitters.fixed_splitter import FixedSplitter
from src.domain.splitter.splitters.paragraph_splitter import ParagraphSplitter

# from src.domain.splitter.splitters.paged_splitter import PagedSplitter TODO:
# Paged Splitter implementation
from src.domain.splitter.splitters.recursive_splitter import RecursiveSplitter
from src.domain.splitter.splitters.sentence_splitter import SentenceSplitter
from src.domain.splitter.splitters.word_splitter import WordSplitter

# from src.domain.splitter.splitters.row_column_splitter import RowColumnSplitter
# TODO: Row-Column Splitter implementation
# from src.domain.splitter.splitters.schema_based_splitter import SchemaBasedSplitter
# TODO: Schema-based Splitter implementation
# from src.domain.splitter.splitters.auto_splitter import AutoSplitter
# TODO: Auto
# Splitter implementation

__all__ = [
    BaseSplitter,
    WordSplitter,
    SentenceSplitter,
    ParagraphSplitter,
    # SemanticSplitter, TODO: Semantic Splitter implementation
    FixedSplitter,
    # PagedSplitter, TODO: Paged Splitter implementation
    RecursiveSplitter,
    # RowColumnSplitter, TODO: Row-Column Splitter implementation
    # SchemaBasedSplitter, TODO: Schema-based Splitter implementation
    # AutoSplitter TODO: Auto Splitter implementation
]
