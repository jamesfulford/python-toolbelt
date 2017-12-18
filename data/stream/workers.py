# workers.py

import requests

from worker_types import IOWorker
from worker_types import Worker


def query(connection, querystring, worker_type=IOWorker, name=""):
    @IOWorker
    def querier(pdos):
        with connection.cursor() as c:
            if pdos:
                c.execute(querystring, *pdos)
            else:
                c.execute(querystring)
            return c.fetchall()
    return querier


class API(object):
    def __init__(self, url):
        self.url = url

    @IOWorker
    def post(self, data):
        return requests.post(self.url, data=data)

    @IOWorker
    def get(self, params):
        return requests.get(self.url, params=params)


if __name__ == "__main__":
    from stream import Stream

    @Worker
    def tee(x):
        print x
        return x

    s = Stream().then(
        lambda x: requests.get(
            "https://web-small-task-portfolio-semimajor.c9users.io/square/",
            params={"val": x}
        ),
        name="Hitting Square Endpoint"
    ).then(
        lambda x: int(x.text),
        name="Parsing"
    )
    print s([7])
    print s.errors
