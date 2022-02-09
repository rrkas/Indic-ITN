from modules.constants import Constants
from modules.generic import GenericITN


class Hi(GenericITN):
    # lang = "hi"

    def remove_starting_zeros(self, word, zero_digits):
        if word[0] in zero_digits and len(word) > 1:
            first_non_zero_num = min([pos for pos, word in enumerate(list(word)) if word != "०"])
            word = word[first_non_zero_num:]
        return word
