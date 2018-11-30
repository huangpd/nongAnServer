# coding=utf-8
import hashlib

__author__ = 'zhangly'

import urllib, urllib2
from urllib import urlencode
from django.http import HttpResponse
# from apitest.zcx_api import *
from api.zcx.config import zcx_config
from datetime import datetime, date
from base.models import TZcxApiLog
from base.utils import utils
import time

last_ReqTid = None  # 全局变量 ：最后一查询流水号
dic_api_isrun = {}  # 判断同一时间重复调用key：nosign_api_url


class zcx_api(object):
    def __init__(self):
        pass

    # 获取签名sign字符串
    def __getSign(self, dicParam):
        #输入参数排序，拼装字符串 然后md5加密
        dict = sorted(dicParam.iteritems(), key=lambda d: d[0])
        ss = ''
        for k, v in dict:
            ss += str(k) + str(v)

        ss = ss + zcx_config.privateKey
        import hashlib

        sign = str(hashlib.md5(ss).hexdigest()).upper()
        return sign

    def __create_ReqTid(self):
        '''
        创建查询唯一流水号
        :return:
        '''
        try:
            reqTid = ''
            now = datetime.now()
            while True:
                reqTid = now.year.__str__() + now.month.__str__() + now.day.__str__() + \
                         now.hour.__str__() + now.minute.__str__() + now.second.__str__() + \
                         now.microsecond.__str__()

                #判断流水号是否存在
                if last_ReqTid == None or last_ReqTid != reqTid:
                    break

            return reqTid
        except Exception, e:
            return None

    def __saveApiLog(self, reqTid, api_name, api_url, nosign_api_url, ret_txt, user_name):
        '''
        保存api调用日志
        :param reqTid: 查询唯一流水号
        :param api_name:
        :param api_url:
        :param ret_txt:
        :return:
        '''
        apiLog = TZcxApiLog()
        apiLog.req_tid = reqTid
        apiLog.api_name = api_name
        apiLog.api_url = api_url
        apiLog.nosign_api_url = nosign_api_url
        apiLog.ret_txt = ret_txt
        apiLog.user_name = user_name
        apiLog.save()
        pass

    def __call_api(self, reqTid, dicParam, signParm, call_api_url, api_name, isRealTime=False):
        """
        调用接口api
        :param reqTid: 查询唯一流水号
        :param dicParam: 接口api输入参数
        :param signParm: 接口api签名sign参数
        :param api_url: 接口url
        :param api_name: 接口名称
        :param isRealTime: 会否实时查询 默认False
        :return:
        """
        #生成sign
        sign = self.__getSign(signParm)
        strParam = urlencode(dicParam)
        strParam += "&sign=" + sign
        api_url = call_api_url + "?" + strParam  # 拼接url
        api_url = api_url.encode('utf8')

        nosign_dicParam = dicParam.copy()
        if nosign_dicParam.has_key('reqTid'):
            nosign_dicParam.pop('reqTid')
        nosign_api_url = call_api_url + "?" + urlencode(nosign_dicParam)
        while True:
            if dic_api_isrun.has_key(nosign_api_url):
                time.sleep(0.2)
            else:
                dic_api_isrun[nosign_api_url] = True
                break

        ret_txt = ''
        #调用api
        isGetApi = True
        try:
            if not isRealTime:
                apiLogs = TZcxApiLog.objects.filter(nosign_api_url=nosign_api_url)
                if apiLogs.count() > 0:
                    ret_txt = apiLogs[0].ret_txt
                    isGetApi = False
            if isGetApi:
                res_data = urllib2.urlopen(api_url)
                ret_txt = res_data.read()
                #保存api调用日志
                user_name = None
                if dicParam.has_key('name'):
                    user_name = dicParam.get('name')
                self.__saveApiLog(reqTid, api_name, api_url, nosign_api_url, ret_txt, user_name)
        except Exception, e:
            return '{"resCode": "-1","resMsg": "调用接口时出现异常"}'
        finally:
            if dic_api_isrun.has_key(nosign_api_url):
                dic_api_isrun.pop(nosign_api_url)
        #接口输出内容
        return str(ret_txt)


    def get_credit_report(self, cid, name, mobile, card):
        """
        个人信用报告
        :param cid:
        :param name:
        :param mobile:
        :param card:
        :return:
        """
        isRealTime = False  #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        cid = str(cid).replace(' ', '')
        name = str(name).replace(' ', '')
        mobile = str(mobile).replace(' ', '')
        card = str(card).replace(' ', '')
        if cid == 'None' or cid == '':
            return '{"resCode": "201","resMsg": "参数：身份证号 不能为空"}'
        if name == 'None' or name == '':
            return '{"resCode": "201","resMsg": "参数：姓名 不能为空"}'
        if mobile == 'None' or mobile == '':
            return '{"resCode": "201","resMsg": "参数：手机号 不能为空"}'
        if card == 'None' or card == '':
            return '{"resCode": "201","resMsg": "参数：银行卡号 不能为空"}'
        if len(cid) != 18:
            return '{"resCode": "202","resMsg": "参数：身份证号 长度不是18位"}'
        if not utils.checkIDCardNo(cid):
            return '{"resCode": "202","resMsg": "参数：身份证号 格式不正确"}'
        if not utils.checkPhoneNo(mobile):
            return '{"resCode": "202","resMsg": "参数：手机号 格式不正确"}'
        if not utils.checkBankCardNo(card):
            return '{"resCode": "202","resMsg": "参数：银行卡 格式不正确"}'

        #        cid = '632125199009293421' #身份证号
        #        name = '赵海珠'#姓名
        #        mobile = '18629523398'#手机号
        #        card = '6207002022070700864'#银行卡
        #        cid = '360104198210241953' #身份证号
        #        name = '肖俊'#姓名
        #        mobile = '13970810889'#手机号
        #        card = '6217231502001666353'#银行卡

        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name,
            'mobile': mobile,
            'card': card,
            'reqTid': reqTid
        }
        #签名sign参数
        signParm = dicParam
        api_url = zcx_config.credit_report_url
        api_name = '个人信用报告'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)
        pass

    def get_education(self, cid, name):
        """
        学历信息
        :param cid: 身份证号
        :param name: 姓名
        :return:
        """
        #        cid = '632125199009293421' #身份证号
        #        name = '赵海珠'#姓名
        #校验必填参数
        cid = str(cid).replace(' ', '')
        name = str(name).replace(' ', '')
        if cid == 'None' or cid == '':
            return '{"resCode": "201","resMsg": "参数：身份证号 不能为空"}'
        if name == 'None' or name == '':
            return '{"resCode": "201","resMsg": "参数：姓名 不能为空"}'
        if len(cid) != 18:
            return '{"resCode": "202","resMsg": "参数：身份证号 长度不是18位"}'
        if not utils.checkIDCardNo(cid):
            return '{"resCode": "202","resMsg": "参数：身份证号 格式不正确"}'
        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name,
            'reqTid': reqTid
        }
        #签名sign参数
        signParm = dicParam
        api_url = zcx_config.education_url
        api_name = '学历信息'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)
        pass


    def get_identity_auth(self, cid, name):
        """
        个人身份验证
        :param cid: 身份证号
        :param name: 姓名
        :return:
        """
        #        cid = '632125199009293421' #身份证号
        #        name = '赵海珠'#姓名
        #校验必填参数
        cid = str(cid).replace(' ', '')
        name = str(name).replace(' ', '')
        if cid == 'None' or cid == '':
            return '{"resCode": "201","resMsg": "参数：身份证号 不能为空"}'
        if name == 'None' or name == '':
            return '{"resCode": "201","resMsg": "参数：姓名 不能为空"}'
        if len(cid) != 18:
            return '{"resCode": "202","resMsg": "参数：身份证号 长度不是18位"}'
        if not utils.checkIDCardNo(cid):
            return '{"resCode": "202","resMsg": "参数：身份证号 格式不正确"}'
        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name,
            'reqTid': reqTid
        }
        #签名sign参数
        #signParm = dicParam
        signParm = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name
        }
        api_url = zcx_config.identity_auth_url
        api_name = '个人身份验证'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)


    def get_identity_photo(self, cid, name):
        """
        个人身份验证(照片)
        :param cid: 身份证号
        :param name: 姓名
        :return:
        """
        cid = str(cid).replace(' ', '')
        name = str(name).replace(' ', '')
        if cid == 'None' or cid == '':
            return '{"resCode": "201","resMsg": "参数：身份证号 不能为空"}'
        if name == 'None' or name == '':
            return '{"resCode": "201","resMsg": "参数：姓名 不能为空"}'
        if len(cid) != 18:
            return '{"resCode": "202","resMsg": "参数：身份证号 长度不是18位"}'
        if not utils.checkIDCardNo(cid):
            return '{"resCode": "202","resMsg": "参数：身份证号 格式不正确"}'
        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name,
            'reqTid': reqTid
        }
        #签名sign参数
        signParm = dicParam
        # signParm = {
        #     'account': zcx_config.account,
        #     'cid': cid,
        #     'name' : name
        # }
        api_url = zcx_config.identity_photo_url
        api_name = '个人身份验证(照片)'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)


    def get_icinfo_category_cid(self, cid):
        """
        工商信息查询-按自然人证件号查询
        :param cid: 身份证号
        :param name: 姓名
        :return:
        """
        cid = str(cid).replace(' ', '')
        if cid == 'None' or cid == '':
            return '{"resCode": "201","resMsg": "参数：身份证号 不能为空"}'
        if len(cid) != 18:
            return '{"resCode": "202","resMsg": "参数：身份证号 长度不是18位"}'
        if not utils.checkIDCardNo(cid):
            return '{"resCode": "202","resMsg": "参数：身份证号 格式不正确"}'
        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'key': cid,  #键值
            'type': 3,  #键值类型1 企业名称 2 工商注册号 3 自然人 证件号
            'cat': 0,  #信息类别,使用 int 类型的 bit 位标 识,具体见附录 4.2,不输入或输入 0,则返回全部字段
            'reqTid': reqTid
        }
        #签名sign参数
        #signParm = dicParam
        signParm = {
            'account': zcx_config.account,
            'key': cid,  #键值
            'type': 3,  #键值类型1 企业名称 2 工商注册号 3 自然人 证件号
        }
        api_url = zcx_config.icinfo_category_url
        api_name = '个人工商信息查询'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)


    def get_cert(self, cid, name):
        """
        个人职业资格证书查询
        :param cid: 身份证号
        :param name: 姓名
        :return:
        """
        #        cid = '632125199009293421' #身份证号
        #        name = '赵海珠'#姓名
        #校验必填参数
        cid = str(cid).replace(' ', '')
        name = str(name).replace(' ', '')
        if cid == 'None' or cid == '':
            return '{"resCode": "201","resMsg": "参数：身份证号 不能为空"}'
        if name == 'None' or name == '':
            return '{"resCode": "201","resMsg": "参数：姓名 不能为空"}'
        if len(cid) != 18:
            return '{"resCode": "202","resMsg": "参数：身份证号 长度不是18位"}'
        if not utils.checkIDCardNo(cid):
            return '{"resCode": "202","resMsg": "参数：身份证号 格式不正确"}'
        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name,
            'reqTid': reqTid
        }
        #签名sign参数
        signParm = dicParam
        api_url = zcx_config.cert_url
        api_name = '个人职业资格证书查询'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)


    def get_riskinfo_classify(self, cid, name, **kwargs):
        """
        风险信息查询
        :param cid: 身份证号
        :param name: 姓名
        :return:
        """
        cid = str(cid).replace(' ', '')
        name = str(name).replace(' ', '')
        if cid == 'None' or cid == '':
            return '{"resCode": "201","resMsg": "参数：身份证号 不能为空"}'
        if name == 'None' or name == '':
            return '{"resCode": "201","resMsg": "参数：姓名 不能为空"}'
        if len(cid) != 18:
            return '{"resCode": "202","resMsg": "参数：身份证号 长度不是18位"}'
        if not utils.checkIDCardNo(cid):
            return '{"resCode": "202","resMsg": "参数：身份证号 格式不正确"}'
        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        page = 1
        num = 100
        if kwargs.has_key('page'):
            page = kwargs['page']
        if kwargs.has_key('num'):
            num = kwargs['num']

        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name,
            'type': 1,  #键值类型 1 自然人查询 2 企业查询
            'page': page,  #页码
            'num': num,  #每页数量
            'reqTid': reqTid
        }
        #签名sign参数
        #signParm = dicParam
        signParm = {
            'account': zcx_config.account,
            'type': 1,  #键值类型 1 自然人查询 2 企业查询
        }
        api_url = zcx_config.riskinfo_classify_url
        api_name = ' 风险信息查询'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)


    def get_criminal(self, cid, name):
        """
        犯罪信息查询
        :param cid: 身份证号
        :param name: 姓名
        :return:
        """
        #        cid = '632125199009293421' #身份证号
        #        name = '赵海珠'#姓名
        #校验必填参数
        cid = str(cid).replace(' ', '')
        name = str(name).replace(' ', '')
        if cid == 'None' or cid == '':
            return '{"resCode": "201","resMsg": "参数：身份证号 不能为空"}'
        if name == 'None' or name == '':
            return '{"resCode": "201","resMsg": "参数：姓名 不能为空"}'
        if len(cid) != 18:
            return '{"resCode": "202","resMsg": "参数：身份证号 长度不是18位"}'
        if not utils.checkIDCardNo(cid):
            return '{"resCode": "202","resMsg": "参数：身份证号 格式不正确"}'
        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name,
            'reqTid': reqTid
        }
        #签名sign参数
        signParm = {
            'account': zcx_config.account,
            'cid': cid,
            'name': name,
        }
        api_url = zcx_config.criminal_url
        api_name = '个人不良信息查询'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)


    def get_telecom_identity(self, mobile, name, cid):
        """
        手机号码实名验证
        :param mobile: 手机号码
        :param cid: 身份证找骂
        :param name: 姓名
        :return:
        """
        #校验必填参数
        mobile = str(mobile).replace(' ', '')
        name = str(name).replace(' ', '')
        cid = str(cid).replace(' ', '')
        if mobile == 'None' or mobile == '':
            return '{"resCode": "201","resMsg": "参数：手机号码 不能为空"}'
        if name == 'None' or name == '':
            return '{"resCode": "201","resMsg": "参数：姓名 不能为空"}'
        if not utils.checkPhoneNo(mobile):
            return '{"resCode": "202","resMsg": "参数：手机号码 格式不正确"}'
        reqTid = self.__create_ReqTid()  #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'account': zcx_config.account,
            'mobile': mobile,
            'cid': cid,
            'name': name,
            'reqId': reqTid
        }
        #签名sign参数
        signParm = {
            'account': zcx_config.account,
            'mobile': mobile,
            'name': name,
            'cid': cid,
            'reqId': reqTid,
        }
        api_url = zcx_config.telecom_identity
        api_name = '手机号码实名验证'
        return self.__call_api(reqTid, dicParam, signParm, api_url, api_name)