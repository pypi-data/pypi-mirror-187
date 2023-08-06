import socket
from urllib import request
import traceback


class PingHC:
    def __init__(self, uuid, server="https://hc-ping.com"):
        self.url = f"{server}/{uuid}"
        self.start

    @property
    def start(self):
        return self.ping(start=True)

    @property
    def failure(self):
        return self.ping(failure=True)

    @property
    def end(self):
        return self.ping()

    @property
    def success(self):
        return self.ping()

    def ping(self, start=False, failure=False):
        data = None
        if start:
            url = self.url + "/start"
        elif failure:
            url = self.url + "/fail"
            # check if there is exception traceback and if so send it as data
            tb = traceback.format_exc()
            if tb:
                data = tb.encode()
        else:
            url = self.url
        try:
            request.urlopen(url, data=data, timeout=1000)
        except socket.error as e:
            # Log ping failure here...
            print("Ping failed: %s" % e)
            raise e
