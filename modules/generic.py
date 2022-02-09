import os
import pynini
from pynini.lib import pynutil
from typing import List
from .constants import Constants

class GenericITN:
    lang = None
    zero_digit = None

    def __init__(self):
        self.__load_data()

    def __remove_starting_zeros(self, word):
        if word[0] in self.__class__.zero_digit and len(word) > 1:
            first_non_zero_num = min([pos for pos, word in enumerate(list(word)) if word != self.__class__.zero_digit])
            word = word[first_non_zero_num:]
        return word
    
    def __load_data(self):
        data_dir_path = os.path.join(Constants.DATA_PATH, self.__class__.lang)
        
        digit_file = os.path.join(data_dir_path, 'digit.tsv')
        with open(digit_file) as f:
            self.digits = f.readlines()
        self.digits = ''.join([line.split()[-1] for line in self.digits])
        self.digits_with_zero = self.__class__.zero_digit + self.digits
        self.digits = pynini.union(*self.digits).optimize()
        self.digits_with_zero = pynini.union(*self.digits_with_zero).optimize()
        self.graph_zero = pynini.string_file(os.path.join(data_dir_path, "zero.tsv"))
        self.graph_digit = pynini.string_file(os.path.join(data_dir_path, "digit.tsv"))
        self.graph_tens = pynini.string_file(os.path.join(data_dir_path, "tens.tsv"))
        
        with open(os.path.join(data_dir_path, "hundred.tsv")) as f:
            self.hundred = f.read().strip()
        
        self.graph_hundred = pynini.cross(self.hundred, "")

        graph_zero_insert = pynutil.insert(self.__class__.zero_digit)

        self.graph_hundred_component = pynini.union(
            self.graph_digit + Constants.delete_space + self.graph_hundred, 
            graph_zero_insert,
        )
        self.graph_hundred_component += Constants.delete_space
        self.graph_hundred_component += pynini.union(
            self.graph_tens, 
            graph_zero_insert + (self.graph_digit | graph_zero_insert),
        )

        self.graph_hundred_component_at_least_one_none_zero_digit = self.graph_hundred_component @ (
                pynini.closure(self.digits) + (self.digits - self.__class__.zero_digit) + pynini.closure(self.digits)
        )

        with open(os.path.join(data_dir_path,"thousands.tsv")) as f:
            self.thousands = f.readlines()

        thousands_sum = pynutil.delete(self.thousands[0])

        for th in self.thousands[1:]:
            thousands_sum += pynutil.delete(th)

        self.graph_thousands = pynini.union(
            self.graph_hundred_component + Constants.delete_space + thousands_sum,
            pynutil.insert(self.__class__.zero_digit * 3, weight=0.1)
        )

        self.fst = pynini.union(
            self.graph_thousands
            + Constants.delete_space
            + self.graph_hundred_component,
            self.graph_zero,
        )

        self.word = pynini.closure(pynutil.add_weight(Constants.NOT_SPACE, weight=0.1), 1)

        self.word_fst = self.word.optimize()

        self.fst = pynini.cdrewrite(self.fst, "", "", Constants.SIGMA).optimize()

        self.final_graph = (pynutil.add_weight(self.fst, 1.1) | pynutil.add_weight(self.word_fst, 100)).optimize()

    
    def execute(self, inp):
        s = pynini.escape(inp.strip())
        ans = s @ self.final_graph
        astr = pynini.shortestpath(ans).string()
        astr = ' '.join([self.__remove_starting_zeros(word) for word in astr.split()])
        return s, astr
