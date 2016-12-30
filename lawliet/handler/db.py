# -*- coding: utf-8 -*-


class InitSession(object):
    db_session = None
    exc = None


class LawSession(object):

    def __init__(self, no_raise=False):
        self.DBSession = InitSession.db_session
        self.exc = InitSession.exc
        self.bool = no_raise

    def __enter__(self):
        self.session = self.DBSession()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, self.exc):
            self.session.rollback()
        self.session.close()
        return self.bool
