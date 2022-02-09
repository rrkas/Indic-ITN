import os
import pynini
from pynini.lib import utf8


class Constants:
    ROOT_PATH = os.sep.join(os.path.normpath(__file__).split(os.sep)[:-2])
    DATA_PATH = os.path.join(ROOT_PATH, "data")

    CHAR = utf8.VALID_UTF8_CHAR
    SIGMA = pynini.closure(CHAR)
    SPACE = " "
    WHITE_SPACE = pynini.union(" ", "\t", "\n", "\r", u"\u00A0").optimize()
    NOT_SPACE = pynini.difference(CHAR, WHITE_SPACE).optimize()
    NON_BREAKING_SPACE = u"\u00A0"

print(Constants.ROOT_PATH)