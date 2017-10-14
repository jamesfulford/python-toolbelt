# stations.py
# by James Fulford

from station import Station
from datetime import datetime as dt
from datetime import timedelta as td
from utilities import *

"""
The purpose of this file is to allow people to define
new types of stations, which follow different patterns.

i.e. Weekly patterns, Monthly patterns, etc.
"""


def dayspan(start, end):
    """
    Returns list of dates between start and end, inclusive.
    """
    upds = []
    for i in range((end - start).days + 1):
        upds.append(start + td(days=i))
    return upds


class Weekly(Station):
    def gen(self, start, end, subscription, account):
        upds = []
        hour = int(subscription["time"].split(":")[0])
        minute = int(subscription["time"].split(":")[1])
        for day in dayspan(start, end):
            thistime = day.replace(hour=hour, minute=minute)
            upd = {
                "text": "What is this, {my_name}?".format(**subscription),
                "post_at": thistime.strftime(dtformat())
            }
            upds.append(upd)
        return upds

