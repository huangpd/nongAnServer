# coding=utf-8


import urllib,urllib2
from urllib import urlencode
from django.http import HttpResponse
from datetime import datetime, date
from base.models import TZcxApiLog
from base.utils import utils
import time
import json

last_ReqTid = None #全局变量 ：最后一查询流水号
dic_api_isrun = {} #判断同一时间重复调用key：nosign_api_url
class qcc_api(object):

    def __init__(self):
        pass

    def __create_ReqTid(self):
        '''
        创建查询唯一流水号
        :return:
        '''
        try:
            reqTid = ''
            now = datetime.now()
            while True:
                reqTid = now.year.__str__() + now.month.__str__() + now.day.__str__() +\
                         now.hour.__str__() + now.minute.__str__() + now.second.__str__() +\
                         now.microsecond.__str__()

                #判断流水号是否存在
                if last_ReqTid == None or last_ReqTid != reqTid:
                    break

            return reqTid
        except Exception,e:
            return None

    def __call_api(self,reqTid,dicParam,call_api_url,api_name,isRealTime=False):
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
        appId = '38670825e7122df872620c52d9caea5b'
        sign = 'a9f937b641f7bb99710daa31b1ceee3d'
        token = '5786a71813f0f4f4b870b6e39a6c99ed'

        appId = 'ddc12502caa0cbba1eee367fbdc919fc'
        sign = '6b750f2351284c910784b0ff6bc8ffbb'
        token = '202cb962ac59075b964b07152d234b48'

        strParam = urlencode(dicParam)
        strParam += "&appId=" + appId
        strParam += "&sign=" + sign
        strParam += "&token=" + token
        api_url = call_api_url + "?" + strParam  # 拼接url
        api_url = api_url.encode('utf8')

        nosign_api_url = api_url
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
                if apiLogs.count() >0:
                    ret_txt = apiLogs[0].ret_txt
                    isGetApi = False
            if isGetApi:
                res_data = urllib2.urlopen(api_url)
                ret_txt = res_data.read()
                #保存api调用日志
                user_name = None
                if dicParam.has_key('name'):
                    user_name = dicParam.get('name')
                    #self.__saveApiLog(reqTid,api_name,api_url,nosign_api_url,ret_txt,user_name)
        except:
            return '{"resCode": "-1","resMsg": "调用接口时出现异常"}'
        finally:
            if dic_api_isrun.has_key(nosign_api_url):
                dic_api_isrun.pop(nosign_api_url)
                #接口输出内容
        return str(ret_txt)

    def __saveApiLog(self,reqTid,api_name,api_url,nosign_api_url,ret_txt,user_name):
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
        #apiLog.save()
        pass

    def get_company_detail(self,company_name):
        """
        查询企业基本信息
        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'cityCode': '',
            'industryCode': '',
            'isSortAsc' : '',
            'pageIndex' : '',
            'pageSize' : '',
            'province' : '',
            'registCapiBegin' : '',
            'registCapiEnd' : '',
            'searchIndex' : '',
            'searchKey' : company_name,
            'sortField' : '',
            'startDateBegin' : '',
            'subIndustryCode' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/base/advancedSearch'
        api_name = '企业信息高级查询'
        advancedSearch_txt = self.__call_api(reqTid,dicParam,api_url,api_name,True)
        data = json.loads(advancedSearch_txt)
        if data['status'] == 200:
            if data['result']['Result'] != None and len(data['result']['Result'])  >0:
                if data['result']['Result'][0]['Name'] != company_name:
                    #没有查询到企业
                    return '{"resCode": "202","resMsg": "未查询企业信息"}'

        company_key = data['result']['Result'][0]['KeyNo']
        #查询企业详情
        dicParam = {
            'unique': company_key
        }
        api_url = 'http://opensdk.qichacha.com/open/v1/base/getEntDetail'
        api_name = '企业详情'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,True)
        companydetail_jsonData = json.loads(ret_txt)
        ret_data = {}
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = '成功'
        ret_data['data'] = companydetail_jsonData['result']['Company']
        ret_data['CountInfo'] = companydetail_jsonData['result']['CountInfo']

        #查询企业年报
        dicParam = {
            'unique': company_key
        }
        api_url = 'http://opensdk.qichacha.com/open/v1/base/getAnnualReport'
        api_name = '企业年报'
        report_txt = self.__call_api(reqTid,dicParam,api_url,api_name)
        report_txt = report_txt.encode('utf-8')
        report_jsonData = json.loads(report_txt)
        ret_data['data']['AnnualReports'] = report_jsonData['result']
        return json.dumps(ret_data)

    """
    查询列表
    http://opensdk.qichacha.com/open/v1/base/advancedSearch?appId=38670825e7122df872620c52d9caea5b&cityCode=&industryCode=&isSortAsc=&pageIndex=1&pageSize=20&province=&registCapiBegin=&registCapiEnd=&searchIndex=&searchKey=xiaomi&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&startDateBegin=&startDateEnd=&subIndustryCode=&token=5786a71813f0f4f4b870b6e39a6c99ed

    企业详情
    1.curl 'http://opensdk.qichacha.com/open/v1/base/getEntDetail?appId=38670825e7122df872620c52d9caea5b&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed&unique=9cce0780ab7644008b73bc2120479d31' -H 'Origin: http://link.qichacha.com' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: http://link.qichacha.com/open/index.html' -H 'Connection: keep-alive' --compressed
http://opensdk.qichacha.com/open/v1/base/getEntDetail?appId=38670825e7122df872620c52d9caea5b&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed&unique=9cce0780ab7644008b73bc2120479d31


法院公告
http://opensdk.qichacha.com/open/v1/legal/getAnnouncementList?appId=38670825e7122df872620c52d9caea5b&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&pageIndex=1&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed

失信
http://opensdk.qichacha.com/open/v1/legal/getShixin

被执行人
http://opensdk.qichacha.com/open/v1/legal/getZhixing?appId=38670825e7122df872620c52d9caea5b&name=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&pageIndex=1&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed

法院判决书
http://opensdk.qichacha.com/open/v1/legal/getJudgment?appId=38670825e7122df872620c52d9caea5b&caseType=&companyType=&isExactlySame=&isSortAsc=&judgeDateBegin=&judgeDateEnd=&pageIndex=1&province=&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&searchType=&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&token=5786a71813f0f4f4b870b6e39a6c99ed



专利
http://opensdk.qichacha.com/open/v1/zscq/getPatentList?appDateBegin=&appDateEnd=&appId=38670825e7122df872620c52d9caea5b&ipc=&isSortAsc=&kindcode=&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&token=5786a71813f0f4f4b870b6e39a6c99ed

商标
http://opensdk.qichacha.com/open/v1/zscq/getTrademarkList?appDateBegin=&appDateEnd=&appId=38670825e7122df872620c52d9caea5b&intcls=&isSortAsc=&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&status=&token=5786a71813f0f4f4b870b6e39a6c99ed

著作权
http://opensdk.qichacha.com/open/v1/zscq/getCopyrightList?appId=38670825e7122df872620c52d9caea5b&isExactlySame=&isSortAsc=&pageIndex=1&searchCategory=&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&token=5786a71813f0f4f4b870b6e39a6c99ed

企业证书
http://opensdk.qichacha.com/open/v1/other/getCertificationSummary?appId=38670825e7122df872620c52d9caea5b&effectiveBegin=&effectiveEnd=&isSortAsc=&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&searchType=&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&token=5786a71813f0f4f4b870b6e39a6c99ed


新闻
http://opensdk.qichacha.com/open/v1/other/getNews?appId=38670825e7122df872620c52d9caea5b&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed

招聘
http://opensdk.qichacha.com/open/v1/other/getJobs?appId=38670825e7122df872620c52d9caea5b&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed

注册网站
http://opensdk.qichacha.com/open/v1/zscq/getWebsiteList?appId=38670825e7122df872620c52d9caea5b&pageIndex=1&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed&unique=9cce0780ab7644008b73bc2120479d31

融资记录
http://opensdk.qichacha.com/open/v1/other/getCompanyFinancings?appId=38670825e7122df872620c52d9caea5b&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed&unique=9cce0780ab7644008b73bc2120479d31

产品信息
http://opensdk.qichacha.com/open/v1/other/getCompanyProducts?appId=38670825e7122df872620c52d9caea5b&pageIndex=1&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed&unique=9cce0780ab7644008b73bc2120479d31

http://opensdk.qichacha.com/open/v1/base/advancedSearch?appId=38670825e7122df872620c52d9caea5b&cityCode=1&industryCode=&isSortAsc=&pageIndex=1&pageSize=20&province=BJ&registCapiBegin=&registCapiEnd=&searchIndex=&searchKey=huai&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&startDateBegin=&startDateEnd=&subIndustryCode=&token=5786a71813f0f4f4b870b6e39a6c99ed

对外投资
http://opensdk.qichacha.com/open/v1/base/getInvestments?appId=38670825e7122df872620c52d9caea5b&cityCode=&pageIndex=1&province=&searchKey=小米科技有限责任公司&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed
        """

    def get_AnnouncementList(self,company_name,pageIndex=1):
        """
        查询法院公告
        法院公告
http://opensdk.qichacha.com/open/v1/legal/getAnnouncementList?searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&pageIndex=1

        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/legal/getAnnouncementList'
        api_name = '法院公告'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_ZhixingList(self,company_name,pageIndex=1):
        """
        查询被执行人
被执行人
http://opensdk.qichacha.com/open/v1/legal/getZhixing?appId=38670825e7122df872620c52d9caea5b&name=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&pageIndex=1&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed
        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'name' : company_name,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/legal/getZhixing'
        api_name = '被执行人'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_ShixinList(self,company_name,pageIndex=1):
        """
        查询失信信息
失信信息
http://opensdk.qichacha.com/open/v1/legal/getShixin?appId=38670825e7122df872620c52d9caea5b&name=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&pageIndex=1&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed
        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'name' : company_name,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/legal/getShixin'
        api_name = '失信信息'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)



    def get_JudgmentList(self,company_name,pageIndex=1,caseType=None):
        """
        查询法院判决书
法院判决书
http://opensdk.qichacha.com/open/v1/legal/getJudgment?appId=38670825e7122df872620c52d9caea5b&caseType=&companyType=&isExactlySame=&isSortAsc=&judgeDateBegin=&judgeDateEnd=&pageIndex=1&province=&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&searchType=&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&token=5786a71813f0f4f4b870b6e39a6c99ed
        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex)
        }
        if caseType != None:
            dicParam = {
                'searchKey' : company_name,
                'pageIndex' : str(pageIndex),
                'caseType' : caseType
            }
            #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/legal/getJudgment'
        api_name = '法院判决书'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_PatentList(self,company_name,pageIndex=1):
        """
        查询专利
专利
http://opensdk.qichacha.com/open/v1/zscq/getPatentList?appDateBegin=&appDateEnd=&appId=38670825e7122df872620c52d9caea5b&ipc=&isSortAsc=&kindcode=&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&token=5786a71813f0f4f4b870b6e39a6c99ed
       :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex),
            'appDateBegin' : '',
            'appDateEnd' : '',
            'ipc' : '',
            'isSortAsc' : '',
            'kindcode' : '',
            'sortField' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/zscq/getPatentList'
        api_name = '查询专利'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)


    def get_TrademarkList(self,company_name,pageIndex=1):
        """
        查询商标
商标
http://opensdk.qichacha.com/open/v1/zscq/getTrademarkList?appDateBegin=&appDateEnd=&appId=38670825e7122df872620c52d9caea5b&intcls=&isSortAsc=&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&status=&token=5786a71813f0f4f4b870b6e39a6c99ed
       :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex),
            'appDateBegin' : '',
            'appDateEnd' : '',
            'intcls' : '',
            'isSortAsc' : '',
            'sortField' : '',
            'status' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/zscq/getTrademarkList'
        api_name = '查询商标'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_CopyrightList(self,company_name,pageIndex=1):
        """
        查询著作权
著作权
http://opensdk.qichacha.com/open/v1/zscq/getCopyrightList?appId=38670825e7122df872620c52d9caea5b&isExactlySame=&isSortAsc=&pageIndex=1&searchCategory=&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&token=5786a71813f0f4f4b870b6e39a6c99ed
        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex),
            'isExactlySame' : '',
            'searchCategory' : '',
            'isSortAsc' : '',
            'sortField' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/zscq/getCopyrightList'
        api_name = '查询著作权'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_CertificationSummary(self,company_name,pageIndex=1):
        """
        查询企业证书
企业证书
http://opensdk.qichacha.com/open/v1/other/getCertificationSummary?appId=38670825e7122df872620c52d9caea5b&effectiveBegin=&effectiveEnd=&isSortAsc=&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&searchType=&sign=a9f937b641f7bb99710daa31b1ceee3d&sortField=&token=5786a71813f0f4f4b870b6e39a6c99ed

        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex),
            'effectiveBegin' : '',
            'effectiveEnd' : '',
            'isSortAsc' : '',
            'searchType' : '',
            'sortField' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/other/getCertificationSummary'
        api_name = '查询企业证书'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_News(self,company_name,pageIndex=1):
        """
        查询企业新闻
新闻
http://opensdk.qichacha.com/open/v1/other/getNews?appId=38670825e7122df872620c52d9caea5b&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed

        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/other/getNews'
        api_name = '查询企业新闻'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_Jobs(self,company_name,pageIndex=1):
        """
        查询企业招聘
招聘
http://opensdk.qichacha.com/open/v1/other/getJobs?appId=38670825e7122df872620c52d9caea5b&pageIndex=1&searchKey=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed

        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/other/getJobs'
        api_name = '查询企业招聘'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)


    def get_WebsiteList(self,company_name,pageIndex=1):
        """
        查询企业注册网站
注册网站
http://opensdk.qichacha.com/open/v1/zscq/getWebsiteList?appId=38670825e7122df872620c52d9caea5b&pageIndex=1&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed&unique=9cce0780ab7644008b73bc2120479d31

        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'
        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'cityCode': '',
            'industryCode': '',
            'isSortAsc' : '',
            'pageIndex' : '',
            'pageSize' : '',
            'province' : '',
            'registCapiBegin' : '',
            'registCapiEnd' : '',
            'searchIndex' : '',
            'searchKey' : company_name,
            'sortField' : '',
            'startDateBegin' : '',
            'subIndustryCode' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/base/advancedSearch'
        api_name = '企业信息高级查询'
        advancedSearch_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(advancedSearch_txt)
        if data['status'] == 200:
            if data['result']['Result'] != None and len(data['result']['Result'])  >0:
                if data['result']['Result'][0]['Name'] != company_name:
                    #没有查询到企业
                    return '{"resCode": "202","resMsg": "未查询企业信息"}'

        company_key = data['result']['Result'][0]['KeyNo']

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'unique' : company_key,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/zscq/getWebsiteList'
        api_name = '查询企业注册网站'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_CompanyFinancings(self,company_name,pageIndex=1):
        """
        查询融资记录
融资记录
http://opensdk.qichacha.com/open/v1/other/getCompanyFinancings?appId=38670825e7122df872620c52d9caea5b&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed&unique=9cce0780ab7644008b73bc2120479d31

        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'
        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'cityCode': '',
            'industryCode': '',
            'isSortAsc' : '',
            'pageIndex' : '',
            'pageSize' : '',
            'province' : '',
            'registCapiBegin' : '',
            'registCapiEnd' : '',
            'searchIndex' : '',
            'searchKey' : company_name,
            'sortField' : '',
            'startDateBegin' : '',
            'subIndustryCode' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/base/advancedSearch'
        api_name = '企业信息高级查询'
        advancedSearch_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(advancedSearch_txt)
        if data['status'] == 200:
            if data['result']['Result'] != None and len(data['result']['Result'])  >0:
                if data['result']['Result'][0]['Name'] != company_name:
                    #没有查询到企业
                    return '{"resCode": "202","resMsg": "未查询企业信息"}'

        company_key = data['result']['Result'][0]['KeyNo']

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'unique' : company_key,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/other/getCompanyFinancings'
        api_name = '查询融资记录'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)

    def get_CompanyProducts(self,company_name,pageIndex=1):
        """
        查询企业产品信息
产品信息
http://opensdk.qichacha.com/open/v1/other/getCompanyProducts?appId=38670825e7122df872620c52d9caea5b&pageIndex=1&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed&unique=9cce0780ab7644008b73bc2120479d31

        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'
        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'cityCode': '',
            'industryCode': '',
            'isSortAsc' : '',
            'pageIndex' : '',
            'pageSize' : '',
            'province' : '',
            'registCapiBegin' : '',
            'registCapiEnd' : '',
            'searchIndex' : '',
            'searchKey' : company_name,
            'sortField' : '',
            'startDateBegin' : '',
            'subIndustryCode' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/base/advancedSearch'
        api_name = '企业信息高级查询'
        advancedSearch_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(advancedSearch_txt)
        if data['status'] == 200:
            if data['result']['Result'] != None and len(data['result']['Result'])  >0:
                if data['result']['Result'][0]['Name'] != company_name:
                    #没有查询到企业
                    return '{"resCode": "202","resMsg": "未查询企业信息"}'

        company_key = data['result']['Result'][0]['KeyNo']

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'unique' : company_key,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/other/getCompanyProducts'
        api_name = '查询企业产品信息'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)


    def get_Investments(self,company_name,pageIndex=1):
        """
        查询企业对外投资
        http://opensdk.qichacha.com/open/v1/base/getInvestments?appId=38670825e7122df872620c52d9caea5b&cityCode=&pageIndex=1&province=&searchKey=小米科技有限责任公司&sign=a9f937b641f7bb99710daa31b1ceee3d&token=5786a71813f0f4f4b870b6e39a6c99ed

        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        company_name = str(company_name).replace(' ','')
        if company_name == 'None' or company_name == '':
            return '{"resCode": "201","resMsg": "参数：company_name 不能为空"}'

        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'searchKey' : company_name,
            'pageIndex' : str(pageIndex)
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/base/getInvestments'
        api_name = '查询企业对外投资'
        ret_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(ret_txt)

        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']
        return json.dumps(ret_data)


    def company_advancedSearch(self,searchKey,pageIndex=1):
        """
        企业信息高级查询
        :param company_name: 公司名称  （这里要全名称匹配）
        :return:
        """
        isRealTime = True #是否实时查询 True每次都调用api查询最新信息，不传默认False
        #校验必填参数
        searchKey = str(searchKey).replace(' ','')
        if searchKey == 'None' or searchKey == '':
            return '{"resCode": "201","resMsg": "参数：searchKey 不能为空"}'
        reqTid = self.__create_ReqTid() #创建查询唯一流水号
        #准备api 参数
        dicParam = {
            'cityCode': '',
            'industryCode': '',
            'isSortAsc' : '',
            'pageIndex' : '',
            'pageSize' : '',
            'province' : '',
            'registCapiBegin' : '',
            'registCapiEnd' : '',
            'searchIndex' : '',
            'searchKey' : searchKey,
            'sortField' : '',
            'startDateBegin' : '',
            'subIndustryCode' : ''
        }
        #签名sign参数
        signParm = dicParam
        api_url = 'http://opensdk.qichacha.com/open/v1/base/advancedSearch'
        api_name = '企业信息高级查询'
        advancedSearch_txt = self.__call_api(reqTid,dicParam,api_url,api_name,isRealTime)
        data = json.loads(advancedSearch_txt)
        company_key = data['result']['Result'][0]['KeyNo']
        ret_data = {}
        ret_data['resCode'] = data['status']
        ret_data['resCode'] = '0000'
        ret_data['resMsg'] = data['message']
        ret_data['data'] = data['result']['Result']
        ret_data['Paging'] = data['result']['Paging']
        return json.dumps(ret_data)
