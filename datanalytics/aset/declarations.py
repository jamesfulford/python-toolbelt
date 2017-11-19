# declarations.py
# by James Fulford


import utils

# list of valid datatypes
data_types = map(str, utils.load("/Users/jamesfulford/Python/Python Utilities/analytics/dataset/supported_data_types.json"))


def _is_var_decl(self, decl):
        """
        Checks if decl is a variable declaration.
            Has "data_type" as keys.
            Or, has "__decl__" or "__declaration__" as a key
        """
        # Can assume decl is a {}

        lower_keys = map(lambda x: str(x).lower(), decl.keys())

        if "__declaration__" in lower_keys or "__decl__" in lower_keys:
            return True

        if "data_type" not in lower_keys:  # required!
            return False

        okay_keys = [
            "stat_type",
            "data_type",
            "id",
            "optional",
            "note",
            "comments"
        ]
        for key in lower_keys:
            if key not in okay_keys:
                return False

        return True


def _is_valid_var_decl(self, decl):
    """
    Logs in self.logger if declaration is invalid:
            "stat_type" is not in list provided
            "data_type" is not a python datatype
            "optional":True and "id":True simulteneously.
    (Passes test if key is omitted.)
    """
    is_valid = True
    lower_keys = map(lambda x: str(x).lower(), decl.keys())
    stat_types = ["nominal", "ordinal", "interval", "ratio"]

    # VALID stat_type?
    if "stat_type" in lower_keys:
        if decl["stat_type"].lower() not in stat_types:
            is_valid = False
            error = {
                "location": "schema.Schema.make.check_if_var_declaration",
                "description": "invalid stat_type",
                "stat_types": stat_types,
                "declaration": decl
            }
            tip = "VariableDefinition InvalidStatType"
            self.logger.log(error, error_type=tip)

    # VALID data_type
    if "data_type" in lower_keys:
        dt = str(decl["data_type"])
        if dt not in data_types:
            is_valid = False
            error = {
                "location": "schema.Schema.make.check_if_var_declaration",
                "description": dt + " is not a python datatype.",
                "data_type": dt,
                "declaration": decl
            }
            tip = "VariableDefinition InvalidDataType"
            self.logger.log(error, error_type=tip)

    # IS id AND optional FALSE?
    if "id" in decl.keys() and "optional" in decl.keys():
        if decl["id"] and decl["optional"]:
            is_valid = False
            error = {
                "location": "schema.Schema.make.check_if_var_declaration",
                "description": "variable declaration is id and optional!",
                "declaration": decl
            }
            tip = "VariableDefinition IdAndOptional"
            self.logger.log(error, error_type=tip)
    return is_valid
