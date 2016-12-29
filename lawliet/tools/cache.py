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
        except (KeyError, IndexError):
            return None

    @classmethod
    def set(cls, key, value, times=0):
        try:
            if times != 0:
                times = int(time.time()) + int(times)
            CACHE[key] = [value, times]
        except:
            class CacheSetError(Exception):
                pass
            raise CacheSetError()

    @classmethod
    def delete(cls, key):
        try:
            CACHE.pop(key)
        except IndexError:
            pass

    @classmethod
    def expire(cls, key, times):
        try:
            a = CACHE[key]
            a[1] = int(time.time()) + int(times)
            CACHE[key] = a
        except:
            class CacheExpireError(Exception):
                pass
            raise CacheExpireError()

    @classmethod
    def id(cls):
        return id(CACHE)

    @classmethod
    def get_all(cls):
        return CACHE
