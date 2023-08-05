from .lex_attrs import LEX_ATTRS
from .punctuation import TOKENIZER_INFIXES, TOKENIZER_SUFFIXES, TOKENIZER_PREFIXES
from .stop_words import STOP_WORDS
from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS
from ...language import Language, BaseDefaults


class SlovenianDefaults(BaseDefaults):
    stop_words = STOP_WORDS
    tokenizer_exceptions = TOKENIZER_EXCEPTIONS
    prefixes = TOKENIZER_PREFIXES
    infixes = TOKENIZER_INFIXES
    suffixes = TOKENIZER_SUFFIXES
    lex_attr_getters = LEX_ATTRS


class Slovenian(Language):
    lang = "sl"
    Defaults = SlovenianDefaults


__all__ = ["Slovenian"]
