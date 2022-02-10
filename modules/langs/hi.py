import os
import pynini
from pynini.lib import pynutil
from modules.constants import Constants
from modules.generic import GenericITN


class Hi(GenericITN):
    lang = "hi"
    zero_digit = "०"

    def prepare_fst(self):
        digit_file = os.path.join(self.data_dir_path, "digit.tsv")
        with open(digit_file) as f:
            digits = f.readlines()
        digits = "".join([line.split()[-1] for line in digits])
        digits_with_zero = __class__.zero_digit + digits
        digits = pynini.union(*digits).optimize()
        digits_with_zero = pynini.union(*digits_with_zero).optimize()
        graph_zero = pynini.string_file(os.path.join(self.data_dir_path, "zero.tsv"))
        graph_digit = pynini.string_file(os.path.join(self.data_dir_path, "digit.tsv"))
        graph_tens = pynini.string_file(os.path.join(self.data_dir_path, "tens.tsv"))

        with open(os.path.join(self.data_dir_path, "hundred.tsv")) as f:
            hundred = f.read().strip()

        graph_hundred = pynini.cross(hundred, "")

        graph_zero_insert = pynutil.insert(__class__.zero_digit)

        graph_hundred_component = pynini.union(
            graph_digit + Constants.delete_space + graph_hundred,
            graph_zero_insert,
        )
        graph_hundred_component += Constants.delete_space
        graph_hundred_component += pynini.union(
            graph_tens,
            graph_zero_insert + (graph_digit | graph_zero_insert),
        )

        graph_hundred_component_at_least_one_none_zero_digit = (
            graph_hundred_component
            @ (
                pynini.closure(digits)
                + (digits - __class__.zero_digit)
                + pynini.closure(digits)
            )
        )

        with open(os.path.join(self.data_dir_path, "thousands.tsv")) as f:
            thousands = f.readlines()

        thousands_sum = pynutil.delete(thousands[0].strip())

        for th in thousands[1:]:
            thousands_sum += pynutil.delete(th.strip())

        graph_thousands = pynini.union(
            graph_hundred_component + Constants.delete_space + thousands_sum,
            pynutil.insert(__class__.zero_digit * 3, weight=0.1),
        )

        fst = pynini.union(
            graph_thousands + Constants.delete_space + graph_hundred_component,
            graph_zero,
        )

        word = pynini.closure(pynutil.add_weight(Constants.NOT_SPACE, weight=0.1), 1)
        word_fst = word.optimize()
        fst = pynini.cdrewrite(fst, "", "", Constants.SIGMA).optimize()
        final_graph = (
            pynutil.add_weight(fst, 1.1) | pynutil.add_weight(word_fst, 100)
        ).optimize()

        self.set_final_graph_fst(final_graph)
