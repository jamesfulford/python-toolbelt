# utilities.py
# by James Fulford



def dtformat():
    return "%Y/%m/%d %H:%M"


def get_when(update):
    """
    Gets datetime.datetime of when to post this update
    """
    import pytz
    import datetime

    # Local format
    if "post_at" in update.keys():
        try:
            when = datetime.datetime.strptime(update["post_at"], dtformat())
        except:
            # Fix for old-fashion dates
            when = datetime.datetime.strptime(update["post_at"], "%m/%d/%Y %H:%M")
            update["post_at"] = when.strftime(dtformat())

    # Buffer format
    elif "due_at" in update.keys():
        dt_int = update["due_at"]
        when = datetime.datetime.fromtimestamp(dt_int)

    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    if "timezone" in update.keys():
        timezone = update["timezone"]
    else:
        timezone = "America/New_York"
    when = pytz.timezone(timezone).localize(when)
    return when


class SaveLoad():
    """
    File-writing read/write class:
        __init__ loads json from file
        .save() writes json to file
    """

    def save(self, path):
        import json
        dic = {}
        keys = filter(lambda x: x[0] != "_", dir(self))
        keys = filter(lambda x: not callable(getattr(self, x)), keys)
        for key in keys:
            dic[key] = getattr(self, key)

        def json_serial(obj):
            """JSON serializer for dates"""
            from datetime import date
            if isinstance(obj, date):
                serial = obj.strftime(dtformat())
                return serial
            try:
                return str(obj)
            except:
                raise TypeError("Type not serializable: " + str(obj))
        json.dump(dic, open(path, "wb"), indent=4, default=json_serial, sort_keys=True)


def load(path):
    import json
    from datetime import datetime as dt

    def datetime_hook(json_dict):
        for(key, value) in json_dict.items():
            try:
                json_dict[key] = get_when(value)
            except:
                json_dict[key] = value
        return json_dict
    return json.load(open(path), object_hook=datetime_hook)
    # for key in content.keys():
    #     setattr(cls, key, content[key])
