class Formatter:
    """
    Inherit this class and override format function
    """

    def format(self, text: str):
        """Override this function in inherited subclass. return text after formatting"""
        return text

    @property
    def name(self):
        return self.__class__.__name__

    @classmethod
    def get_all(cls):
        """
        returns all subclasses inherited from Formatter

        >>> formatters = Formatter.get_all()
        >>> Extractor.from_yaml_file('a.yaml', formatters=formatters)
        """
        return cls.__subclasses__()


class Integer(Formatter):
    def format(self, text):
        return int(text)


class Decimal(Formatter):
    def format(self, text):
        return float(text)
