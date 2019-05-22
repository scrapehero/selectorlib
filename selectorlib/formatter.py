import abc


class Format(abc.ABC):
    @abc.abstractmethod
    def format(self, text: str):
        """return text after formatting"""

    @property
    def name(self):
        return self.__class__.__name__


class Integer(Format):
    def format(self, text):
        return int(text)
