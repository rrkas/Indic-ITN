from abc import abstractmethod
import os
import pynini
from pynini.lib import pynutil
from typing import List
from .constants import Constants


class GenericITN:
    lang = NotImplementedError()
    zero_digit = NotImplementedError()

    def __init__(self) -> None:
        self.data_dir_path = os.path.join(Constants.DATA_PATH, self.__class__.lang)

    def optimize_zeros(self, inp: str, line: str):
        # remove spaces
        line.replace(" ", "")

        def strip_zeros(s: str):
            return s.strip().lstrip(self.__class__.zero_digit)

        out = ""

        i = 0
        while i < len(inp):
            line = strip_zeros(line)

            if len(line) == 0:
                break

            if inp[i] == " ":
                # check extra spaces
                if out[-1] != " ":
                    out += " "
            else:
                if line.startswith(inp[i]):
                    out += inp[i]
                    if len(line):
                        line = line[1:]
                    else:
                        break
                elif line[0] in self.numbers:
                    num = ""
                    while len(line) and line[0] in self.numbers:
                        num += line[0]

                        if len(line):
                            line = line[1:]
                        else:
                            break
                    out += num

            i += 1

        return out

    @abstractmethod
    def prepare_fst(self):
        raise NotImplementedError()

    def load_numbers(self):
        data = {}
        with open(os.path.join(self.data_dir_path, "numbers_en.tsv")) as f:
            for line in f.readlines():
                kv = line.split("\t")
                if len(kv) == 2:
                    data[kv[0].strip()] = kv[1].strip()
        self.numbers = data

    def set_final_graph_fst(self, fst):
        self.final_graph = fst

    def replace_numbers_en(self, inp: str):
        for k in self.numbers:
            inp = inp.replace(k, self.numbers[k])
        return inp

    def execute(self, inp, to_eng=False):
        self.prepare_fst()
        self.load_numbers()
        s = pynini.escape(inp.strip())
        ans = s @ self.final_graph
        astr = pynini.shortestpath(ans).string()
        astr = self.optimize_zeros(inp, astr)
        astr = self.replace_numbers_en(astr)
        return s, astr
