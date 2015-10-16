# -*- coding: utf-8 -*-


class Validator(object):

    @staticmethod
    def is_string(value):
        if value is None  or not isinstance(value, (str, unicode)):
            return False
        return True
