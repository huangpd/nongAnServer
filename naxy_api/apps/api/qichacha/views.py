# coding=utf-8
from datetime import datetime
import json
import urllib
import traceback
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from base.dictionary import dictionary
from api.qichacha.qcc_api import *
from base.log import log

@csrf_exempt
def get_company_detail(request):
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        rest = qcc_api().get_company_detail(company_name)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))


def get_announcement_list(request):
    """
    查询法院公告
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_AnnouncementList(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))


def get_zhixing_list(request):
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_ZhixingList(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))


def get_shixin_list(request):
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_ShixinList(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))


def get_judgment_list(request):
    """
    查询法院判决书
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_JudgmentList(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))


def get_patent_list(request):
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_PatentList(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))

def get_trademark_list(request):
    """
    查询商标
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_TrademarkList(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))

def get_copyright_list(request):
    """
    查询著作权
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_CopyrightList(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))


def get_certification_summary(request):
    """
    查询企业证书
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_CertificationSummary(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))

def get_news(request):
    """
    查询企业新闻
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_News(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))

def get_jobs(request):
    """
    查询企业招聘信息
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_Jobs(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))

def get_website_list(request):
    """
    查询企业注册网站
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_WebsiteList(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))

def get_company_financings(request):
    """
    查询融资记录
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_CompanyFinancings(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))

def get_company_products(request):
    """
    查询企业注册网站
    :param request:
    :return:
    """
    try:
        data = ""
        company_name = request.GET.get("company_name", "")  # 企业名称
        pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().get_CompanyProducts(company_name,pageIndex)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))


def company_advancedSearch(request):
    """
    企业信息高级查询
    :param request:
    :return:
    """
    try:
        data = ""
        searchKey = request.GET.get("searchKey", "")  # 关键词
        #pageIndex = request.GET.get("pageIndex", "")  # 页号
        rest = qcc_api().company_advancedSearch(searchKey)
        return HttpResponse(rest)
    except Exception, e:
        log.error_log(e.message)
        obj = {"resCode": "9999", "resMsg": dictionary.get_model_for_value("9999"), "date": datetime.now().__str__(),
               "data": ""}
        return HttpResponse(json.dumps(obj))