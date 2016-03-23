# -*- coding: utf-8 -*-
import time
CACHE = dict()


class DoCache(object):
    """缓存功能"""

    @classmethod
    def get(cls, key):
        try:
            a = CACHE[key]
            if a[1] == 0:
                return a[0]
            elif a[1] > int(time.time()):
                return a[0]
            else:
                return None
        except:
            return None

    @classmethod
    def set(cls, key, value):
        try:
            CACHE[key] = [value, 0]
        except:
            pass

    @classmethod
    def expire(cls,key, times):
        try:
            a = CACHE[key]
            a[1] = int(time.time() + int(times))
            CACHE[key] = a
        except:
            pass
