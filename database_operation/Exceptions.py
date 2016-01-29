#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Logging import Logging


class ForeignkeyException(Exception):
    def __init__(self, message):
        if (not isinstance(message, "")) or message == "":
            self.message = u"缺少外键"
        else:
            self.message = message
        Logging.error(self.message)
