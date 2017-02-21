# load_types.py
# by James Fulford
# always do "from load_types import load"

from copy import deepcopy as dc
import utils
locale = dc(locals().keys())  # ignore these local variables


# hard defined load functions:


def load_date(var):
    pass


def load_geographic(var):
    pass


# inherent types built-in to Python
inherent_types = ["int", "bool", "str", "float", "dict", "list", "tuple", "unicode", "complex"]
for tip in inherent_types:
    exec("def load_" + tip + "(var):\n\treturn " + tip + "(var)")


# gateway function - this is the one to import
def load(data_type, data):
    return eval("load_" + data_type + "(data)")


# hard_coded ignored variables
locale.append("load")
locale.append("tip")
locale.append("locale")
locale.append("inherent_types")

# update acceptable data_types list.
filtered = filter(lambda x: x not in locale, locals().keys())
filtered = map(lambda x: x.split("_")[1], filtered)
print(sorted(filtered))
utils.save(sorted(filtered), "supported_data_types.json")
