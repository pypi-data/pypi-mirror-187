from typing import (
    Callable,
    Protocol,
    Iterator,
    Optional,
    Union,
    Tuple,
    Any,
)
from thinc.types import Floats1d, FloatsXd
from .doc import Doc
from .span import Span
from .morphanalysis import MorphAnalysis
from ..lexeme import Lexeme
from ..vocab import Vocab
from .underscore import Underscore

class TokenMethod(Protocol):
    def __call__(self: Token, *args: Any, **kwargs: Any) -> Any: ...  # type: ignore[misc]

class Token:
    i: int
    doc: Doc
    vocab: Vocab
    @classmethod
    def set_extension(
        cls,
        name: str,
        default: Optional[Any] = ...,
        getter: Optional[Callable[[Token], Any]] = ...,
        setter: Optional[Callable[[Token, Any], None]] = ...,
        method: Optional[TokenMethod] = ...,
        force: bool = ...,
    ) -> None: ...
    @classmethod
    def get_extension(
        cls, name: str
    ) -> Tuple[
        Optional[Any],
        Optional[TokenMethod],
        Optional[Callable[[Token], Any]],
        Optional[Callable[[Token, Any], None]],
    ]: ...
    @classmethod
    def has_extension(cls, name: str) -> bool: ...
    @classmethod
    def remove_extension(
        cls, name: str
    ) -> Tuple[
        Optional[Any],
        Optional[TokenMethod],
        Optional[Callable[[Token], Any]],
        Optional[Callable[[Token, Any], None]],
    ]: ...
    def __init__(self, vocab: Vocab, doc: Doc, offset: int) -> None: ...
    def __hash__(self) -> int: ...
    def __len__(self) -> int: ...
    def __unicode__(self) -> str: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: Token, op: int) -> bool: ...
    @property
    def _(self) -> Underscore: ...
    def nbor(self, i: int = ...) -> Token: ...
    def similarity(self, other: Union[Doc, Span, Token, Lexeme]) -> float: ...
    def has_morph(self) -> bool: ...
    morph: MorphAnalysis
    @property
    def lex(self) -> Lexeme: ...
    @property
    def lex_id(self) -> int: ...
    @property
    def rank(self) -> int: ...
    @property
    def text(self) -> str: ...
    @property
    def text_with_ws(self) -> str: ...
    @property
    def prob(self) -> float: ...
    @property
    def sentiment(self) -> float: ...
    @property
    def lang(self) -> int: ...
    @property
    def idx(self) -> int: ...
    @property
    def cluster(self) -> int: ...
    @property
    def orth(self) -> int: ...
    @property
    def lower(self) -> int: ...
    @property
    def norm(self) -> int: ...
    @property
    def shape(self) -> int: ...
    @property
    def prefix(self) -> int: ...
    @property
    def suffix(self) -> int: ...
    lemma: int
    pos: int
    tag: int
    dep: int
    @property
    def has_vector(self) -> bool: ...
    @property
    def vector(self) -> Floats1d: ...
    @property
    def vector_norm(self) -> float: ...
    @property
    def tensor(self) -> Optional[FloatsXd]: ...
    @property
    def n_lefts(self) -> int: ...
    @property
    def n_rights(self) -> int: ...
    @property
    def sent(self) -> Span: ...
    sent_start: bool
    is_sent_start: Optional[bool]
    is_sent_end: Optional[bool]
    @property
    def lefts(self) -> Iterator[Token]: ...
    @property
    def rights(self) -> Iterator[Token]: ...
    @property
    def children(self) -> Iterator[Token]: ...
    @property
    def subtree(self) -> Iterator[Token]: ...
    @property
    def left_edge(self) -> Token: ...
    @property
    def right_edge(self) -> Token: ...
    @property
    def ancestors(self) -> Iterator[Token]: ...
    def is_ancestor(self, descendant: Token) -> bool: ...
    def has_head(self) -> bool: ...
    head: Token
    @property
    def conjuncts(self) -> Tuple[Token]: ...
    ent_type: int
    ent_type_: str
    @property
    def ent_iob(self) -> int: ...
    @classmethod
    def iob_strings(cls) -> Tuple[str]: ...
    @property
    def ent_iob_(self) -> str: ...
    ent_id: int
    ent_id_: str
    ent_kb_id: int
    ent_kb_id_: str
    @property
    def whitespace_(self) -> str: ...
    @property
    def orth_(self) -> str: ...
    @property
    def lower_(self) -> str: ...
    norm_: str
    @property
    def shape_(self) -> str: ...
    @property
    def prefix_(self) -> str: ...
    @property
    def suffix_(self) -> str: ...
    @property
    def lang_(self) -> str: ...
    lemma_: str
    pos_: str
    tag_: str
    def has_dep(self) -> bool: ...
    dep_: str
    @property
    def is_oov(self) -> bool: ...
    @property
    def is_stop(self) -> bool: ...
    @property
    def is_alpha(self) -> bool: ...
    @property
    def is_ascii(self) -> bool: ...
    @property
    def is_digit(self) -> bool: ...
    @property
    def is_lower(self) -> bool: ...
    @property
    def is_upper(self) -> bool: ...
    @property
    def is_title(self) -> bool: ...
    @property
    def is_punct(self) -> bool: ...
    @property
    def is_space(self) -> bool: ...
    @property
    def is_bracket(self) -> bool: ...
    @property
    def is_quote(self) -> bool: ...
    @property
    def is_left_punct(self) -> bool: ...
    @property
    def is_right_punct(self) -> bool: ...
    @property
    def is_currency(self) -> bool: ...
    @property
    def like_url(self) -> bool: ...
    @property
    def like_num(self) -> bool: ...
    @property
    def like_email(self) -> bool: ...
