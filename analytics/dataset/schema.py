# schema.py
# by James Fulford

from editor_extractor import *


class Schema():
    def __init__(self, dictionary, error_path="Schema Errors"):
        from copy import deepcopy
        from utils import Logger

        diction = dictionary
        if isinstance(dictionary, Schema):
            diction = dictionary.dictionary

        self.dictionary = deepcopy(diction)
        self.declarations = {}
        self.accessors = {}
        self.editors = {}
        self.logger = Logger(error_path + ".json")
        self.make_schema()

    def make_schema(self, decl=Extractor("Declaration"), acs=Extractor("Data"), edt=Editor("Data")):
        """
        Parses schema. Makes accessors and declarations.
        """
        from copy import deepcopy as dc

        level = decl(self.dictionary)  # what schema looks like below here?
        dt = type(acs(self.dictionary))  # what does the data look like here?

        # LIST
        if(type(level) is list):
            decl_list = Extractor(decl.name, decl.code + "[0]")
            access = Extractor(acs.name, acs.code)

            path = dc(edt.path)
            path.append([])
            editor = Editor(edt.name, path=path)

            self.make_schema(decl=decl_list, acs=access, edt=editor)  # Recursion!

        # DICT
        elif(type(level) is dict):
            # VARIABLE DECLARATION:
            if self._is_var_decl(level):
                self._is_valid_var_decl(level)  # Error logging
                self.declarations[decl.name] = dc(level)  # Copies declaration
                self.accessors[acs.name] = dc(acs)  # Keeps accessor
                self.editors[acs.name] = dc(edt)  # yes, uses acs.name!
            # OTHERWISE, RECURSE ON EACH KEY
            else:
                for key in map(str, level.keys()):
                    # ACCESSOR
                    if dt is list:
                        acs_code = "map(lambda y: y[\"" + key + "\"], " + acs.code + ")"
                    else:
                        acs_code = acs.code + "[\"" + key + "\"]"
                    access = Extractor(key, code=acs_code)
                    self.accessors[acs.name] = access  # add it to list
                    # DECLARATION
                    decl_code = decl.code + "[\"" + key + "\"]"
                    decl_key = Extractor(key, code=decl_code)
                    # EDITOR
                    edit_path = dc(edt.path)
                    edit_path.append(key)
                    editor = Editor(key, path=edit_path)

                    self.make_schema(decl=decl_key, acs=access, edt=editor)

        # NOT DICT OR LIST
        else:
            if(isinstance(level, Schema)):  # one always manages to sneak in
                pass
            else:  # logs error
                error = {
                    "location": "schema.Schema.make_schema",
                    "description": "Field is not properly formed.",
                    "name": decl.name,
                    "level": level
                }
                self.logger.log(error, "SchemaParse BadField")


    def validate(self, data):
        """
        Checks that all accessors give values.
        Checks that each value are correct datatype.
        """
        for key in self.accessors.keys():
            try:
                ty = type(self.accessors[key](data))
            except KeyError:
                print data
            except AssertionError:
                print data

    def __getitem__(self, key):
        return self.dictionary[key]

    def __setitem__(self, key, value):
        self.dictionary[key] = value

        # TODO: have it make just the new key
        self.declarations = {}
        self.accessors = {}
        self.make_schema()

    def remove_attr(self, attr):
        del self.dictionary[attr]
        del self.accessors[attr]
        del self.declarations[attr]

    import declarations
    _is_var_decl = declarations._is_var_decl
    _is_valid_var_decl = declarations._is_valid_var_decl
