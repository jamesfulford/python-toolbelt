# rally.py
# by James Fulford

# Collection of campaigns


import utilities
import os


def load_directory(path):
        ls = os.listdir(path)
        ls = filter(lambda x: "*" not in x and "." != x[0], ls)
        ls = map(lambda x: path + "/" + x, ls)
        return ls


def weave(op, lisst, *args, **kwargs):
    import threading
    tapestry = []
    results = []

    def oper(*arguments, **morearguments):
        res = op(*arguments, **morearguments)
        results.append(res)

    for item in lisst:
        argument = [item]
        argument.extend(list(args))

        thread = threading.Thread(target=oper, args=tuple(argument), kwargs=kwargs)
        thread.start()
        tapestry.append(thread)

    for x in tapestry:
        x.join()

    return results


class Rally():
    def __init__(self, path):
        from account import Account
        from station import Station
        import threading

        self.savepath = path

        for di in ["Accounts", "Stations"]:
            try:
                setattr(self, di.lower(), load_directory(path + "/" + di))
            except Exception:
                os.makedirs(path + "/" + di)
                setattr(self, di.lower(), load_directory(path + "/" + di))

        weave(self.add_account, range(len(self.accounts)))
        weave(self.add_station, range(len(self.stations)))

    @staticmethod
    def new(path):
        """
        Convenient testing thingy
        """
        print "Called rally.Rally.new"
        os.makedirs("TestRally/Accounts")
        os.makedirs("TestRally/Stations")

    def add_account(self, account_index):
        from account import Account
        self.accounts[account_index] = Account(self.accounts[account_index])

    def add_station(self, station_index):
        from station import Station
        self.stations[station_index] = Station.load(self.stations[station_index])

    def save(self):
        ret1 = weave(lambda x: x.save(), self.accounts)
        # ret2 = weave(lambda x: x.save(self.savepath + "/Stations"),
        # self.stations)
        return ret1

    def advance(self, start, end):
        return weave(lambda x: x.conscript(start, end, self.stations), self.accounts)

    def sync(self):
        return weave(lambda x: x.sync(), self.accounts)

    def next_time(self):
        """
        For each account, returns next time accounts should be supplied
        """
        return weave(lambda x: x.next_time(), self.accounts)

    def how_full(self):
        def res(acc):
            diction = {}
            for q in acc.queues:
                diction[q.name()] = len(q.pending_updates())
            return diction
        return weave(res, self.accounts)

    def how_far_out(self):
        res = []

        def far_out(acc):
            for q in acc.queues:
                res.append(utilities.get_when(q.pending_updates()[-1]))
        weave(far_out, self.accounts)
        return res
