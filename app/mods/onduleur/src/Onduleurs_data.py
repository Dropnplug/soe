import time
import multiprocessing

import mods.onduleur.config as config
from src.memo import memo

from ._Onduleurs import _Onduleurs


class _Attr():
    def __init__(self, attr):
        self.attr = attr

    def send(self, *args, **kwargs):
        key = str(time.time())+self.attr
        memo["onduleurs_data"].set_request(key, self.attr, *args, **kwargs)
        for _ in range(int(1/config.SLEEP)):
            start_time = time.time()
            ret = memo["onduleurs_data"].check_response(key)
            if ret is not None:
                return ret[0]
            time.sleep(max(config.SLEEP - (time.time() - start_time), 0))
        return None

class Onduleurs(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.on = False
        self._onduleurs = None
    
    def _init(self):
        self._onduleurs = _Onduleurs()
        self.on = True
    
    def run(self):
        self._init()
        while self.on:
            start_time = time.time()
            to_do = memo["onduleurs_data"].get_requests()
            for key, value in to_do.items():
                ret = getattr(self._onduleurs, value["attr"])(*value["args"], **value["kwargs"])
                memo["onduleurs_data"].set_response(key, ret)
            time.sleep(max(config.SLEEP - (time.time() - start_time), 0))
        time.sleep(1)

class Onduleurs_data():
    def __init__(self):
        self._requests = {}
        self._responses = {}
    
    def set_request(self, key, attr, *args, **kwargs):
        self._requests[key] = {'args':args, 'kwargs':kwargs, 'attr':attr}

    def get_requests(self):
        data = self._requests
        self._requests = {}
        return data

    def set_response(self, key, response):
        self._responses[key] = response
    
    def get_response(self, key):
        if key in self._responses.keys():
            ret = self._responses[key]
            del self._responses[key]
            return ret
        return None

    def check_response(self, key):
        if key in self._responses.keys():
            ret = self._responses[key]
            del self._responses[key]
            return [ret]
        return None

    def __getattr__(self, item):
        if hasattr(_Onduleurs, item):
            return _Attr(item).send
        return super().__getattr__(item)