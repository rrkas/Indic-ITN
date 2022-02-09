class GenericITN:
    lang = NotImplementedError

    def remove_starting_zeros(self, word, zero_digits):
        """
        args:
        word            str     word to be cleaned
        zero_digits     list    digits considered as ZERO in the language

        returns         str     cleaned word
        """
        raise NotImplementedError
    
    def load_data(self):
        pass