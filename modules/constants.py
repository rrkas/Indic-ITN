import os
import pynini
import string
from pynini.lib import byte, pynutil, utf8
from pynini.examples import plurals


class Constants:
    ROOT_PATH = os.sep.join(os.path.normpath(__file__).split(os.sep)[:-2])
    DATA_PATH = os.path.join(ROOT_PATH, "data")

    CHAR = utf8.VALID_UTF8_CHAR

    DIGIT = byte.DIGIT
    LOWER = pynini.union(*string.ascii_lowercase).optimize()
    UPPER = pynini.union(*string.ascii_uppercase).optimize()
    ALPHA = pynini.union(LOWER, UPPER).optimize()
    ALNUM = pynini.union(DIGIT, ALPHA).optimize()
    HEX = pynini.union(*string.hexdigits).optimize()
    NON_BREAKING_SPACE = u"\u00A0"
    SPACE = " "
    WHITE_SPACE = pynini.union(" ", "\t", "\n", "\r", u"\u00A0").optimize()
    NOT_SPACE = pynini.difference(CHAR, WHITE_SPACE).optimize()
    NOT_QUOTE = pynini.difference(CHAR, r'"').optimize()

    PUNCT = pynini.union(*map(pynini.escape, string.punctuation)).optimize()
    GRAPH = pynini.union(ALNUM, PUNCT).optimize()

    SIGMA = pynini.closure(CHAR)

    delete_space = pynutil.delete(pynini.closure(WHITE_SPACE))
    insert_space = pynutil.insert(" ")
    delete_extra_space = pynini.cross(pynini.closure(WHITE_SPACE, 1), " ")


    _v = pynini.union("a", "e", "i", "o", "u")
    _c = pynini.union(
        "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"
    )
    _ies = SIGMA + _c + pynini.cross("y", "ies")
    _es = SIGMA + pynini.union("s", "sh", "ch", "x", "z") + pynutil.insert("es")
    _s = SIGMA + pynutil.insert("s")

    # graph_plural = plurals._priority_union(
    #     suppletive, plurals._priority_union(_ies, plurals._priority_union(_es, _s, SIGMA), SIGMA), SIGMA
    # ).optimize()

    # SINGULAR_TO_PLURAL = graph_plural
    # PLURAL_TO_SINGULAR = pynini.invert(graph_plural)

print(Constants.ROOT_PATH)