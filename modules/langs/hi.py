import os
import pynini
from pynini.lib import pynutil
from modules.constants import Constants
from modules.generic import GenericITN


class ITN(GenericITN):
    lang = "hi"
    zero_digit = "०"

    def prepare_fst(self):
        # digits
        digit_file = os.path.join(self.data_dir_path, "digit.tsv")
        with open(digit_file) as f:
            digits = f.readlines()
        digits = "".join([line.split()[-1] for line in digits])
        digits_with_zero = __class__.zero_digit + digits
        digits = pynini.union(*digits).optimize()
        digits_with_zero = pynini.union(*digits_with_zero).optimize()

        # zero graph
        graph_zero = pynini.string_file(os.path.join(self.data_dir_path, "zero.tsv"))

        # digit graph
        graph_digit = pynini.string_file(os.path.join(self.data_dir_path, "digit.tsv"))

        # tens graph
        graph_tens = pynini.string_file(os.path.join(self.data_dir_path, "tens.tsv"))
        graph_zero_insert = pynutil.insert(__class__.zero_digit)

        # hundred graph
        with open(os.path.join(self.data_dir_path, "hundred.tsv")) as f:
            hundred = f.read().strip()
        graph_hundred = pynini.cross(hundred, "")
        graph_hundred_component = (
            pynini.union(
                graph_digit + Constants.delete_space + graph_hundred,
                graph_zero_insert,
            )
            + Constants.delete_space
            + pynini.union(
                graph_tens,
                graph_zero_insert + (graph_digit | graph_zero_insert),
            )
        )

        # thousand graph
        with open(os.path.join(self.data_dir_path, "thousands.tsv")) as f:
            thousand = f.read().strip()
        thousand = pynini.cross(thousand, "")
        graph_thousand = pynini.union(
            graph_hundred_component + Constants.delete_space + thousand,
            pynutil.insert(__class__.zero_digit * 3),
        )
        # graph_thousand_component = (
        #     pynini.union(
        #         graph_hundred_component + Constants.delete_space + graph_thousand,
        #         graph_zero_insert + (graph_digit | graph_zero_insert),
        #         graph_zero_insert,
        #     )
        #     + Constants.delete_space
        # )

        # lakh
        # with open(os.path.join(self.data_dir_path, "lakh.tsv")) as f:
        #     lakh = f.read().strip()
        # lakh = pynini.cross(lakh, "")
        # graph_lakh = pynini.union(
        #     graph_thousand_component + Constants.delete_space + lakh,
        #     pynutil.insert(__class__.zero_digit * 5),
        # )

        fst = pynini.union(
            graph_thousand + Constants.delete_space + graph_hundred_component,
            graph_zero,
        )

        word = pynini.closure(pynutil.add_weight(Constants.NOT_SPACE, weight=0.1), 1)
        word_fst = word.optimize()
        fst = pynini.cdrewrite(fst, "", "", Constants.SIGMA).optimize()
        final_graph = (
            pynutil.add_weight(fst, 1.1) | pynutil.add_weight(word_fst, 100)
        ).optimize()

        self.set_final_graph_fst(final_graph)
