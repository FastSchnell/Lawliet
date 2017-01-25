# -*- coding: utf-8 -*-


class SessionEmptyError(Exception):
    pass


class LawSession(object):
    init_session = None
    init_exc = None

    def __init__(self, is_raise=True):
        if not (self.init_session and self.init_exc):
            raise SessionEmptyError()
        self.DBSession = self.init_session
        self.exc = self.init_exc
        self.bool = not is_raise

    def __enter__(self):
        self.session = self.DBSession()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, self.exc):
            self.session.rollback()
        self.session.close()
        return self.bool
