#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import platform
import random
import termcolor
import sys
import json

from Exceptions import *

__author__ = 'ZombieGroup'


class Login:
    @classmethod
    def download_captcha(cls):
        url = "http://www.zhihu.com/captcha.gif"
        from Requests import requests
        r = requests.get(url, params = {"r": random.random()})
        if int(r.status_code) != 200:
            raise NetworkError(u"验证码请求失败")
        image_name = u"verify." + r.headers['content-type'].split("/")[1]
        open(image_name, "wb").write(r.content)
        """
            System platform: https://docs.python.org/2/library/platform.html
        """
        Logging.info(u"正在调用外部程序渲染验证码 ... ")
        if platform.system() == "Linux":
            Logging.info(u"Command: xdg-open %s &" % image_name)
            os.system("xdg-open %s &" % image_name)
        elif platform.system() == "Darwin":
            Logging.info(u"Command: open %s &" % image_name)
            os.system("open %s &" % image_name)
        elif platform.system() == "SunOS":
            os.system("open %s &" % image_name)
        elif platform.system() == "FreeBSD":
            os.system("open %s &" % image_name)
        elif platform.system() == "Unix":
            os.system("open %s &" % image_name)
        elif platform.system() == "OpenBSD":
            os.system("open %s &" % image_name)
        elif platform.system() == "NetBSD":
            os.system("open %s &" % image_name)
        elif platform.system() == "Windows":
            os.system("%s" % image_name)
        else:
            Logging.info(u"我们无法探测你的作业系统，请自行打开验证码 %s 文件，并输入验证码。" % os.path.join(os.getcwd(), image_name))

        sys.stdout.write(termcolor.colored(u"请输入验证码: ", "cyan"))
        captcha_code = raw_input()
        return captcha_code

    @classmethod
    def search_xsrf(cls):
        url = "http://www.zhihu.com/"
        from Requests import requests
        r = requests.get(url)
        if int(r.status_code) != 200:
            raise NetworkError(u"验证码请求失败")
        results = re.compile(r"<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"", re.DOTALL).findall(r.text)
        if len(results) < 1:
            Logging.info(u"提取XSRF 代码失败")
            return None
        return results[0]

    @classmethod
    def build_form(cls, account, password):
        if re.match(r"^1\d{10}$", account):
            account_type = "phone_num"
        elif re.match(r"^\S+@\S+\.\S+$", account):
            account_type = "email"
        else:
            raise AccountError(u"帐号类型错误")

        form = {account_type: account, "password": password, "remember_me": True, '_xsrf': cls.search_xsrf(),
                'captcha': cls.download_captcha()}

        return form

    @classmethod
    def upload_form(cls, form):
        if "email" in form:
            url = "http://www.zhihu.com/login/email"
        elif "phone_num" in form:
            url = "http://www.zhihu.com/login/phone_num"
        else:
            raise ValueError(u"账号类型错误")

        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 "
                          "Safari/537.36",
            'Host': "www.zhihu.com",
            'Origin': "http://www.zhihu.com",
            'Pragma': "no-cache",
            'Referer': "http://www.zhihu.com/",
            'X-Requested-With': "XMLHttpRequest"
        }
        from Requests import requests
        r = requests.post(url, data = form, headers = headers)
        if int(r.status_code) != 200:
            raise NetworkError(u"表单上传失败!")

        if r.headers['content-type'].lower() == "application/json":
            try:
                result = json.loads(r.content)
            except Exception as e:
                Logging.error(u"JSON解析失败！")
                Logging.debug(e)
                Logging.debug(r.content)
                result = {}
            if result["r"] == 0:
                Logging.success(u"登录成功！")
                return {"result": True}
            elif result["r"] == 1:
                Logging.success(u"登录失败！")
                return {"error": {"code": int(result['errcode']), "message": result['msg'], "data": result['data']}}
            else:
                Logging.warn(u"表单上传出现未知错误: \n \t %s )" % (str(result)))
                return {"error": {"code": -1, "message": u"unknow error"}}
        else:
            Logging.warn(u"无法解析服务器的响应内容: \n \t %s " % r.text)
            return {"error": {"code": -2, "message": u"parse error"}}

    @classmethod
    def islogin(cls):
        # check session
        url = "https://www.zhihu.com/settings/profile"
        from Requests import requests
        r = requests.get(url, allow_redirects = False)
        status_code = int(r.status_code)
        if status_code == 301 or status_code == 302:
            # 未登录
            return False
        elif status_code == 200:
            return True
        else:
            Logging.warn(u"网络故障")
            return None

    @classmethod
    def read_account_from_config_file(cls, config_file="zhihu_api/config.ini"):
        # NOTE: The ConfigParser module has been renamed to configparser in Python 3.
        #       The 2to3 tool will automatically adapt imports when converting your sources to Python 3.
        #       https://docs.python.org/2/library/configparser.html
        from ConfigParser import ConfigParser
        cf = ConfigParser()
        if os.path.exists(config_file) and os.path.isfile(config_file):
            Logging.info(u"正在加载配置文件 ...")
            cf.read(config_file)

            email = cf.get("info", "email")
            password = cf.get("info", "password")
            if email == "" or password == "":
                Logging.warn(u"帐号信息无效")
                return None, None
            else:
                return email, password
        else:
            Logging.error(u"配置文件加载失败！")
            return None, None

    @classmethod
    def login(cls, account=None, password=None):
        if cls.islogin():
            Logging.success(u"你已经登录过咯")
            return True

        if account is None:
            (account, password) = cls.read_account_from_config_file()
        if account is None:
            sys.stdout.write(u"请输入登录账号: ")
            account = raw_input()
            sys.stdout.write(u"请输入登录密码: ")
            password = raw_input()

        form_data = cls.build_form(account, password)
        """
            result:
                {"result": True}
                {"error": {"code": 19855555, "message": "unknow.", "data": "data" } }
                {"error": {"code": -1, "message": u"unknow error"} }
        """
        result = cls.upload_form(form_data)
        if "error" in result:
            if result["error"]['code'] == 1991829:
                # 验证码错误
                Logging.error(u"验证码输入错误，请准备重新输入。")
                return cls.login()
            else:
                Logging.warn(u"unknow error.")
                return False
        elif "result" in result and result['result'] == True:
            # 登录成功
            Logging.success(u"登录成功！")
            from Requests import requests
            requests.cookies.save()
            return True
