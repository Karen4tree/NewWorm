#!/usr/bin/env python
# -*- coding:utf-8 -*-
import termcolor
from __init__ import debug_info_flag

__author__ = 'ZombieGroup'


class Logging:
    flag = True

    @staticmethod
    def error(msg):
        if Logging.flag == True:
            print "".join(  [ termcolor.colored("ERROR", "red"), ": ", termcolor.colored(msg, "white") ] )
    @staticmethod
    def warn(msg):
        if Logging.flag == True:
            print "".join(  [ termcolor.colored("WARN", "yellow"), ": ", termcolor.colored(msg, "white") ] )
    @staticmethod
    def info(msg):
        # attrs=['reverse', 'blink']
        if Logging.flag == True:
            print "".join(  [ termcolor.colored("INFO", "magenta"), ": ", termcolor.colored(msg, "white") ] )
    @staticmethod
    def debug(msg):
        if Logging.flag == True:
            print "".join(  [ termcolor.colored("DEBUG", "magenta"), ": ", termcolor.colored(msg, "white") ] )
    @staticmethod
    def success(msg):
        if Logging.flag == True:
            print "".join(  [ termcolor.colored("SUCCES", "green"), ": ", termcolor.colored(msg, "white") ] )