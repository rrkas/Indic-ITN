import os
import pynini
from pynini.lib import pynutil
from modules.constants import Constants
from modules.generic import GenericITN


class HindiITN(GenericITN):
    lang = "hi"
    zero_digit = "०"

    def prepare_fst(self):
        digit_file = os.path.join(self.data_dir_path, "digit.tsv")
        with open(digit_file) as f:
            digits = f.readlines()
        digits = "".join([line.split()[-1] for line in digits])
        digits = pynini.union(*digits).optimize()

        graph_zero = pynini.string_file(os.path.join(self.data_dir_path, "zero.tsv"))
        graph_digit = pynini.string_file(os.path.join(self.data_dir_path, "digit.tsv"))
        graph_tens = pynini.string_file(os.path.join(self.data_dir_path, "tens.tsv"))
        insert_zero = pynutil.insert(__class__.zero_digit)

        # hundred graph
        with open(os.path.join(self.data_dir_path, "hundred.tsv")) as f:
            hundred = f.read().strip()
        graph_hundred_component = (
            pynini.union(
                graph_digit + " "
                # + Constants.delete_space
                + pynutil.delete(hundred),
                insert_zero,
            )
            # + Constants.delete_space
            + pynini.union(
                graph_tens,
                insert_zero + (graph_digit | insert_zero),
            )
        )

        # graph_hundred_component = graph_hundred_component @ (
        #     pynini.closure(digits)
        #     + (digits - __class__.zero_digit)
        #     + pynini.closure(digits)
        # )

        # thousand graph
        with open(os.path.join(self.data_dir_path, "thousands.tsv")) as f:
            thousand = f.read().strip()
        graph_thousand = pynini.union(
            graph_hundred_component
            # + Constants.delete_space
            + pynutil.delete(thousand),
            pynutil.insert(__class__.zero_digit * 3),
        )

        # lakh
        with open(os.path.join(self.data_dir_path, "lakh.tsv")) as f:
            lakh = f.read().strip()
        graph_lakh = pynini.union(
            graph_hundred_component
            # + Constants.delete_space
            + pynutil.delete(lakh),
            pynutil.insert(__class__.zero_digit * 5),
        )

        fst = pynini.union(
            graph_lakh
            # + Constants.delete_space
            + graph_thousand
            # + Constants.delete_space
            + graph_hundred_component,
            graph_zero,
        )

        # fst = fst @ pynini.union(
        #     pynutil.delete(pynini.closure(__class__.zero_digit))
        #     + pynini.difference(digits, __class__.zero_digit)
        #     + pynini.closure(digits),
        #     __class__.zero_digit,
        # )

        word = pynini.closure(pynutil.add_weight(Constants.NOT_SPACE, weight=0.1), 1)
        word_fst = word.optimize()
        fst = pynini.cdrewrite(fst, "", "", Constants.SIGMA).optimize()
        final_graph = (
            pynutil.add_weight(fst, 1.1) | pynutil.add_weight(word_fst, 100)
        ).optimize()

        self.set_final_graph_fst(final_graph)
