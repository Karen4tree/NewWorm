#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Logging import Logging

__author__ = 'ZombieGroup'


class LoginPasswordError(Exception):
    def __init__(self, message):
        if (not isinstance(message, "")) or message == "":
            self.message = u"帐号密码错误"
        else:
            self.message = message
        Logging.error(self.message)


class NetworkError(Exception):
    def __init__(self, message):
        if (not isinstance(message, "")) or message == "":
            self.message = u"网络异常"
        else:
            self.message = message
        Logging.error(self.message)


class AccountError(Exception):
    def __init__(self, message):
        if (not isinstance(message, "")) or message == "":
            self.message = u"帐号类型错误"
        else:
            self.message = message
        Logging.error(self.message)


class NotLogin(Exception):
    def __init__(self, message):
        if (not isinstance(message, "")) or message == "":
            self.message = u"未登录"
        else:
            self.message = message
        Logging.error(self.message)
