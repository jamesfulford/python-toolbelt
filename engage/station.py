# station.py
# by James Fulford


import utilities
from abc import abstractmethod


class Station(utilities.SaveLoad):
    def __init__(self, diction):
        # so we can save everything
        for key in diction.keys():
            setattr(self, key, diction[key])

    @staticmethod
    def load(path):
        """
        Calls __init__ of dict["definition"]["type"] where dict is json at path
        Returns Station subclass definition>type defined in stations.py
        """
        import stations
        diction = utilities.load(path)
        sta = eval("stations." + diction["type"] + "(diction)")
        sta.name = path.split("/")[-1].split(".")[0]
        return sta

    @abstractmethod
    def gen(self, start, stop, subscription, account):
        """
        Returns list of updates to be posted between start and stop (inclusive)
        kwargs is subscription details provided by the account
        """
        pass
