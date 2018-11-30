# coding=utf-8
import calendar
import json
import urllib
import urllib2
import re
from datetime import datetime, date
from decimal import *
from django.db import connection


class utils:
    """
    工具类
    """

    def __init__(self):
        pass


    @staticmethod
    def md5(str):
        """
        md5加密
        :param str:
        :return:
        """
        import hashlib

        m = hashlib.md5()
        m.update(str)
        return m.hexdigest().upper()


    @staticmethod
    def send_request(type, url, params={}):
        """
        发送请求
        :param type: 请求类型-str POST或GET
        :param url: 请求地址-str
        :param params: 发送请求参数 dict
        :return:
        """
        try:
            if type in ['POST', 'GET']:
                request = urllib2.Request(url)
                if type == 'GET':
                    res_data = urllib2.urlopen(request)
                elif type == 'POST':
                    encode_param = urllib.urlencode(params)
                    res_data = urllib2.urlopen(url=request, data=encode_param)
                data = res_data.read()
                return data
            else:
                return ''
        except Exception as e:
            return ''


    @staticmethod
    def param_list_index_value(parameter_list, str):
        '''
        接口参数值查询
        :param parameter_list: 参数列表
        :param str: 要查询得参数名称
        :return:
        '''
        if str == "service_charge":
            ret = "0"
        else:
            ret = ""

        for parameter in parameter_list:
            parameter_info = parameter.split(':')
            if parameter_info[0] == str:
                if len(parameter_info) > 1:
                    ret = parameter_info[1]
                else:
                    ret = ''
                break

        return ret

    @staticmethod
    def hiding_info(info, type):
        """
        隐藏用户信息
        :param user_info: 用户信息手机或者email
        :param type: 屏蔽类型 1 手机， 2 email, 3 身份证号码, 4 银行卡号
        :return:
        """
        try:
            if info:
                if type == 1:
                    info = info[0:3] + "****" + info[-4]
                elif type == 2:
                    index = info.index("@")
                    info = info[0:index - 4] + "****" + info[index:]
                elif type == 3:
                    info = info[0:6] + "********" + info[len(info) - 2:len(info)]
                elif type == 4:
                    info = info[0:6] + " **** **** ****" + info[len(info) - 3:len(info)]

            return info
        except Exception, e:
            return ""

    @staticmethod
    def checkPhoneNo(phone_no):
        """
        校验手机号
        :param phone_no:
        :return:
        """
        reMobile = re.match(r'1\d{10}$', phone_no)
        if not reMobile:
            return False
        else:
            return True
        pass

    @staticmethod
    def checkBankCardNo(card_no):
        """
        校验银行卡号
        :param phone_no:
        :return:
        """
        # 现在暂时只校验卡号长度，现在一般银行卡号都是16位和19位
        if len(card_no) == 16 or len(card_no) == 19:
            return True
        return False
        pass

    @staticmethod
    def checkIDCardNo(card_no):
        """
        校验身份证号码
        :param card_no: 身份证号
        :return:
        """

        def get_checkCode(card_no):
            CountValue = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            get_checkcode_key = reduce(
                lambda x, y: x + y,
                map(
                    lambda x, y: x * y,
                    [int(x) for x in card_no[:-1]],
                    CountValue))

            checkcode_key = get_checkcode_key % 11
            CountRule = {
                '0': '1',
                '1': '0',
                '2': 'X',
                '3': '9',
                '4': '8',
                '5': '7',
                '6': '6',
                '7': '5',
                '8': '4',
                '9': '3',
                '10': '2'}
            get_checkcode_value = CountRule.get(str(checkcode_key), None)
            return get_checkcode_value

        if card_no[-1] == get_checkCode(card_no):
            return True
        return False


    @staticmethod
    def toJSON(self):
        """
        将models转换成json
        :return:
        """
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]),
                          cls=JsonDateEncoder)

    @staticmethod
    def calculate_age(born):
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:
            # raised when birth date is February 29
            # and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year


    @staticmethod
    def sql_helper(sql):
        """
        sql语句操作,只执行sql语句查询
        :param sql: sql语句
        :return:返回查询结果
        """
        cursor = connection.cursor()  # 创建游标

        try:
            cursor.execute(sql)  # 执行sql
            info = cursor.fetchall()  # 获取查询结果集（元组类型）
            cursor.close()  # 关闭连接

            return info
        except Exception, e:
            cursor.close()
            return None


    @staticmethod
    def add_months(dt, months):
        month = dt.month - 1 + months
        year = dt.year + month / 12
        month = month % 12 + 1
        day = min(dt.day, calendar.monthrange(year, month)[1])
        return dt.replace(year=year, month=month, day=day)

class JsonDateEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        对时间格式进行json转换
        :param obj:
        :return:
        """
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return "%.2f" % obj
        else:
            return json.JSONEncoder.default(self, obj)