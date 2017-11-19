# editor_extractor.py
# by James Fulford

class Extractor():
    def __init__(self, name, code="x"):
        self.name = name  # str, not needed
        self.code = code  # str

    def __call__(self, x):
        try:
            return eval(self.code)
        except KeyError:
            print("ERROR: " + str(self))
            raise

    def __str__(self):
        return "lambda x: " + str(self.code)

    __repr__ = __str__

class Editor():
    def __init__(self, name, path=[]):
        self.name = name
        self.path = path


    # TODO: def read(self, data_element) to replace Extractor class
    def write(self, data_element, content):
        # this function writes and then executes code.
        # as a result, it may have side-effects on global variables.
        # that is why weird strings are attached to each var -
        # reduces chances of overwriting other variables by a lot.
        tabs = 0  # how many indents do we have to write?
        itr = "iter"  # makes iterating variable different
        varsity = map(chr, range(65, 65+26))
        varsity = map(lambda x: x + "", varsity)
        var = 0  # indicates which variable we are using in varsity
        code = varsity[var] + " = data_element"
        looped = False
        for lvl in self.path[:-1]:
            code += "\n" + "\t" * tabs  # new line



            if type(lvl) is list:
                code += "for " + itr + varsity[var] + " in " + varsity[var] + ":"
                tabs = tabs + 1
                var = var + 1
                assert var < len(varsity)  # run out of variables!
                looped = True
            else:
                if looped:
                    code += varsity[var] + " = " + itr + varsity[var - 1] + "[\"" + lvl + "\"]"
                    looped = False
                else:
                    code += varsity[var] + " = " + varsity[var] + "[\"" + lvl + "\"]"

        code += "\n" + "\t" * tabs  # new line

        this_var = varsity[var - 1]
        if var is 0:
            this_var = varsity[0]
        if looped:
            this_var = itr + this_var


        # find value to assign
        if type(content) is dict:
            code += "try:"
            code += "\n" + "\t" * (tabs + 1)  # new line
            code += this_var + "[\"" + self.path[-1] + "\"] = "
            code += "content[" + this_var + "[\"" + self.path[-1] + "\"]]"
            code += "\n" + "\t" * tabs  # new line
            code += "except KeyError:"
            code += "\n" + "\t" * (tabs + 1)  # new line
            code += "pass"  # if it isn't in the dictionary, don't worry about it.
        else:
            code += this_var + "[\"" + self.path[-1] + "\"] = content"
            if callable(content):
                code += "(" + this_var + ")"

        # run the code!
        try:
            exec(code)
        except:
            print(code)  # incredibly useful, this line
            raise

    def __str__(self):
        label = self.name + ": "
        # I can't believe this worked more/less first try:
        return reduce(lambda x, y: str(x) + "/" + str(y), self.path, label)
