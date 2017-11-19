# datapoint.py
# by James Fulford
# defines a class representing a single record in dataset.data
# allows for easier access of and writing to variables

class Datapoint():
    def __init__(self, dictionary, declarations, accessors, editors):
        self.dictionary = dictionary
        self.declarations = declarations
        self.accessors = accessors
        self.editors = editors

    def access(self, variable):
        return self.accessors[variable](self.dictionary)

    __getitem__ = access

    def write(self, variable, content):
        edt = self.editors[variable]
        edt.write(self.dictionary, content)

    # __assignitem__ = write
