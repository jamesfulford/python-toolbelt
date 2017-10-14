# queue.py
# by James Fulford
# for Joyful Love

# implements needed functions from Buffer API


import utilities
from utilities import get_when
from utilities import dtformat
import buffpy


class Queue(utilities.SaveLoad):
    """
    Represents a single buffer.
        .name() returns a pretty string
            Queue.name(profile) returns pretty string for profile too
        .pending_updates() returns list of updates in Buffer and Reserve
        .get_buffer() returns list of updates in Buffer
        .add(update) tries to add update to Reserve
        .sync() sends reserved updates to
    """

    def __init__(self, profile, path=None):
        self._prof = profile

        part = path
        if not path:
            part = Queue.profile_name(profile)

        try:
            self.reserve = utilities.load(part)["reserve"]
        except IOError:
            self.reserve = []

    def save(self, fp=None):
        from json import dump
        part = ""
        if fp:
            part = fp + "/"
        with open(part + self.name(), "wb") as phile:
            dump(self.dictionary(), phile, indent=4, sort_keys=True)

    def dictionary(self):
        return {
            "reserve": sorted(self.reserve, key=get_when)
        }

    def name(self):
        return Queue.profile_name(self._prof)

    @staticmethod
    def profile_name(prof):
        return prof["formatted_service"] + " " + prof["formatted_username"]

    __str__ = name

    def pending_updates(self):
        """
        Returns list of posts in Buffer and in reserve
        """
        upd = self.get_buffer()
        upd.extend(self.reserve)
        return sorted(upd, key=get_when)

    def get_buffer(self):
        """
        Returns list of posts in Buffer
        """
        return self._prof.updates.pending

    def add(self, update):
        """
        Adds updates to reserve.
        """
        import buffpy
        upds = self.pending_updates()

        if get_when(update) not in map(get_when, upds):
            self.reserve.append(update)
        else:
            msg = "Already a message scheduled for " + get_when(update).strftime(dtformat())
            exp = Exception(msg)
            exp.error = {
                "update": update,
                "queue": self,
            }
            raise exp

    def sync(self):
        """
        Sends reserved updates to Buffer, stores the rest back in reserve
        Returns time of the latest post

        Order matters, so do not do major multithreading if it can be avoided
        """
        upds = self.reserve
        self.reserve = []
        upds.sort(key=get_when)
        while len(self.get_buffer()) < 10 and len(upds) > 0:
            update = upds.pop(0)
            try:
                self.post(update)
            except buffpy.exceptions.BuffpyRestException:
                print(self.name() + " did not post: " + get_when(update).strftime(dtformat()))
        self.reserve.extend(upds)

    def next_time(self):
        to_consider = []
        buff = self.get_buffer()
        if len(buff) > 0:
            to_consider.append(max(map(get_when, buff)))
        if len(self.reserve) > 0:
            to_consider.append(min(map(get_when, self.reserve)))

        if len(to_consider) > 0:
            return min(to_consider)
        return None


    def post(self, update):
        """
        Adds update to profile's buffer.
        TODO: Allow posting by sending email to secret buffer address
        """
        content = ""
        if "content" in update.keys():
            content = update["content"]
        if "text" in update.keys():
            content = update["text"]

        if "timezone" not in update.keys():
            update["timezone"] = self._prof["timezone"]

        def post_no_media(update):
            if "post_at" in update.keys():
                return self._prof.updates.new(content, when=str(get_when(update)))
            else:
                return self._prof.updates.new(content, now=True)

        def post_with_media(update):
            media = update["media"]
            if "post_at" in update.keys():
                when = str(get_when(update))
                return self._prof.updates.new(content, media=media, when=when)
            else:
                return self._prof.updates.new(content, media=media, now=True)

        def post_link(update):
            # assert url_exists(media["link"])
            # remove picture or thumbnail if url is bad
            if "picture" in media.keys():
                # if not url_exists(media["picture"]):
                del media["picture"]
            if "thumbnail" in media.keys():
                # if not url_exists(media["thumbnail"]):
                del media["thumbnail"]
            post_with_media(update)

        def url_exists(url):
            import httplib
            conn = httplib.HTTPConnection(url)
            conn.request("HEAD", "/index.html")
            res = conn.getresponse()
            return res.status < 400

        # now to post
        try:
            assert "media" in update.keys()
            # if there is not media, posts without media.

            media = update["media"]
            # if media is a photo
            if "photo" in media.keys():
                import os
                try:

                    # if photo url fails, post link
                    # assert url_exists(media["photo"])

                    # post photo
                    post_with_media(update)
                except AssertionError:
                    del media["photo"]

                    # if post_link fails, posts without media
                    post_link(update)
            else:
                # if there isn't a photo,
                # post link instead.
                # if post_link fails, posts without media
                post_link(update)
        except AssertionError:
            # posts without media
            post_no_media(update)
