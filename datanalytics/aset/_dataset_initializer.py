# _dataset_initializer.py
# by James Fulford

def get_name(dictionary):
    name = dictionary["name"]
    if len(name) is 0:
        message = "Error in Dataset.__init__.get_name: name must not be empty."
        raise Exception(message)
    return str(name)


def get_save_path(dictionary, save_loc, name=""):
    import os
    if(len(save_loc) is 0):  # if save_loc specified
        save_path = save_loc
    elif "save_path" in dictionary.keys():  # elif in dictionary
        save_path = dictionary["save_path"]
    else:  # otherwise, use current directory.
        save_path = os.path.curdir

    # get absolute path
    save_path = str(os.path.abspath(save_path))

    if not os.path.exists(save_path):  # error if bad path.
        open(save_path + ".json", "wb")
    if(len(name) is 0):
        name = get_name(dictionary)
    return str(save_path + "/" + name + ".json")


def get_error_path(dictionary, error_loc, name=""):
    import os
    if len(error_loc) is 0:  # error path
        err_path = os.path.curdir
    elif "error_path" in dictionary.keys():
        err_path = dictionary["error_path"]
    else:
        err_path = error_loc
    err_path = os.path.abspath(err_path)
    if not os.path.exists(err_path):
        open(err_path + ".json", "wb")
        # message = "Error in Dataset.__init__: \"" + err_path
        # message += "\" is not a valid path"
        # raise Exception(message)
    else:
        if(len(name) is 0):
            name = get_name(dictionary)
        return err_path + "/" + name + " errors.json"


def get_schema(dictionary, sch):
    from schema import Schema
    if sch:
        scheme = sch
    else:
        scheme = dictionary["schema"]
    return Schema(scheme)


def get_attr_schema(dictionary, attr_sch):
    from schema import Schema
    if attr_sch:
        attribute_schema = attr_sch
    else:
        attribute_schema = dictionary["attribute_schema"]
    return Schema(attribute_schema)
