# account.py
# by James Fulford
# for Joyful Love

import utilities
from utilities import dtformat


class Account(utilities.SaveLoad):
    """
    Represents a business account.
    An account can have multiple logins (into Bufferapp)
    Each login has several queues (Bufferapp allows 3 for free)
        all queues in a login are assumed to belong to the same account.
    """

    def __init__(self, account):
        """
        account is either a path to an account to load
        or a dictionary with attribute "logins" as a list of login dictionaries
        """
        from login import Login
        from queue import Queue

        argument = account
        if type(account) is str:
            argument = utilities.load(account + "/account.json")
            self.savepath = account

        for key in argument.keys():
            setattr(self, key, argument[key])
        self.queues = []  # this field is read-only, not loaded into memory

        for i in range(len(self.logins)):
            self.logins[i] = Login(self.logins[i])
            try:
                path = self.savepath + "/"
                profs = self.logins[i].profiles()
                self.queues.extend(map(lambda x: Queue(x, path=path + Queue.profile_name(x)), profs))
            except AttributeError:
                self.queues.extend(map(Queue, self.logins[i].profiles()))

        self.subscriptions = argument["subscriptions"]

    def save(self, fp=None, set_savepath=False):
        """
        Saves account to where it was loaded from
        or directory at fp.

        If fp specified, changes savepath to fp
        """
        from json import dump
        sav = {
            "logins": map(lambda x: x.dictionary(), self.logins),
            "queues": map(lambda x: x.name(), self.queues),  # courtesy
            "subscriptions": self.subscriptions
        }
        if fp:
            path = fp
            if set_savepath:
                self.savepath = fp
        else:
            path = self.savepath  # SPECIFY "fp" kwarg FOR ACCOUNT.SAVE
        try:
            dump(sav, open(path + "/account.json", "wb"), indent=4, sort_keys=True)
        except IOError:
            import os
            import errno
            try:
                os.makedirs(path)
                self.save(fp=path, set_savepath=set_savepath)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise
        for q in self.queues:
            q.save(fp=path)

    def post(self, update, queue_test=lambda x: True):
        """
        Posts update(s) to queues that pass queue_test
        """
        if type(update) is list:
            for upd in update:
                self.post(upd)
        else:
            try:
                for q in filter(queue_test, self.queues):
                    q.add(update)
            except Exception as exp:
                print exp

    def sync(self, silence=True):
        """
        Forces all queues to sync to Buffer
        Multithreads
        """
        if not silence:
            try:
                print "Syncing " + self.savepath + ":"
            except AttributeError:
                print "Syncing:"
        import threading
        tapestry = []
        for q in self.queues:
            if not silence:
                print "\t" + q.name() + "..."
            thread = threading.Thread(target=q.sync)
            thread.start()
            tapestry.append(thread)
        for thread in tapestry:
            thread.join()

    def next_time(self):
        from queue import Queue
        results = filter(lambda x: x != None, map(Queue.next_time, self.queues))
        if len(results) > 0:
            return min(results)
        else:
            return None

    def conscript(self, start, end, stations):
        # name all subscriptions
        for subs in self.subscriptions:
            try:
                ind = map(lambda x: x.name, stations).index(subs["name"])
                sta = stations[ind]
                self.post(sta.gen(start, end, subs, self))
            except ValueError:
                print self.savepath, "acc. did not find station", subs["name"]
