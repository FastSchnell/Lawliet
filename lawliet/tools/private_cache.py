# -*- coding: utf-8 -*-
import time


class PrivateCache(object):
    """私有缓存"""

    def __init__(self):
        self.CACHE = dict()

    def get(self, key):
        try:
            a = self.CACHE[key]
            if a[1] == 0:
                return a[0]
            elif a[1] > int(time.time()):
                return a[0]
            else:
                return None
        except (KeyError, IndexError):
            return None

    def set(self, key, value, times=0):
        try:
            if times != 0:
                times = int(time.time()) + int(times)
            self.CACHE[key] = [value, times]
        except:
            class CacheSetError(Exception):
                pass
            raise CacheSetError()

    def delete(self, key):
        try:
            self.CACHE.pop(key)
        except IndexError:
            pass

    def expire(self, key, times):
        try:
            a = self.CACHE[key]
            a[1] = int(time.time()) + int(times)
            self.CACHE[key] = a
        except:
            class CacheExpireError(Exception):
                pass
            raise CacheExpireError()

    def id(self):
        return id(self.CACHE)

    def get_all(self):
        return self.CACHE
