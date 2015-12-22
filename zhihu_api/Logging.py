#!/usr/bin/env python
# -*- coding:utf-8 -*-
import termcolor


class Logging:
    flag = True

    @staticmethod
    def error(msg):
        if Logging.flag:
            print "".join([termcolor.colored("ERROR", "red"), ": ", termcolor.colored(msg, "white")])

    @staticmethod
    def warn(msg):
        if Logging.flag:
            print "".join([termcolor.colored("WARN", "yellow"), ": ", termcolor.colored(msg, "white")])

    @staticmethod
    def info(msg):
        # attrs=['reverse', 'blink']
        if Logging.flag:
            print "".join([termcolor.colored("INFO", "magenta"), ": ", termcolor.colored(msg, "white")])

    @staticmethod
    def debug(msg, value):
        if Logging.flag:
            print "".join([termcolor.colored("DEBUG", "magenta"), ": ", termcolor.colored(msg, "white"), "  ",
                           termcolor.colored(value, "white")])

    @staticmethod
    def success(msg):
        if Logging.flag:
            print "".join([termcolor.colored("SUCCES", "green"), ": ", termcolor.colored(msg, "white")])
