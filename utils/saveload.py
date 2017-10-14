# saveload.py
# by James Fulford
# handles dictionary dumping and loading
# including if it has dates

import json
import datetime as dt


def save(dictionary, path):
    """
    utils.dump.save
    Writes dictionary to given path.
        Overwrites any data that is already there.
    Can save:
        Everything json.dumps can do by default
        datetime.date
    """
    def json_serial(obj):
        """JSON serializer for dates"""
        if isinstance(obj, dt.date):
            serial = obj.strftime("%m/%d/%Y")
            return serial
        raise TypeError("Type not serializable: " + str(obj))
    with open(path, 'wb') as f:
        f.write(json.dumps(dictionary, indent=4, default=json_serial, sort_keys=True))


def load(path):
    """
    utils.dump.load
    Returns dictionary parsed from given file.
    Handles dates in form of %Y-%m-%d
    """
    def date_hook(json_dict):
        for(key, value) in json_dict.items():
            try:
                json_dict[key] = dt.strptime(value, '%Y-%m-%d').date()
            except:
                pass
        return json_dict
    # Actual loading of file
    with open(path) as f:
        data = json.load(f, object_hook=date_hook)
        return data
