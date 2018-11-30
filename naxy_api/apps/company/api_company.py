# coding=utf-8
import json
import urllib2
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from base.company import company_base
from base.encrypt_utils import encryptUtils
from base.system import system_base


@csrf_exempt
def get_open_id_by_code(request):
    """
    根据code获得open_id
    :return:
    """
    try:
        # 此处需要前端传一个code值
        appid = 'wxd99146bc30d77f1f'                                        # 小程序ID
        secret = '0bffa3a3772f27dba405db5a8f34e566'                         # 小程序secret
        code = request.POST['code'].encode('utf-8')                         # 小程序前端传的code
        grant_type = 'authorization_code'                                   # 授权码
        url = 'https://api.weixin.qq.com/sns/jscode2session?'
        url += 'appid=' + appid + '&secret=' + secret + '&js_code=' + code + '&grant_type=' + grant_type
        result = urllib2.urlopen(url).read()
        we_chat_obj = json.loads(result)
        open_id = we_chat_obj['openid']
        # session_key是unicode类型
        session_key = we_chat_obj['session_key']
        # 对code进行加密  session_id是字符串类型
        session_id = encryptUtils.encrypt(code.__str__())
        request.session['session_id'] = session_id
        request.session['code'] = code
        # 根据open_id去插入数据或更新，把code放入session_id，session_key放入session_key，并判断是否是第一次登录
        user = system_base.save_open_id_and_session_key(open_id, code, session_key)
        obj = {}
        obj['status'] = 1
        obj['session_id'] = session_id
        obj['phone'] = user.phone
        obj['is_vip'] = user.is_vip
        return HttpResponse(json.dumps(obj))
    except Exception, e:
        return HttpResponse('{"status": 0, "msg": "获得openid失败"}')


@csrf_exempt
def save_user_info(request):
    """
    保存用户信息
    :param request:
    :return:
    """
    obj = {}
    try:
        session_id = request.POST['session_id']
        user_info = system_base.get_user_info_by_session_id(session_id, request)
        if not user_info:
            obj['status'] = '2'
            obj['msg'] = '登录已过期，请登录后操作'
            return HttpResponse(json.dumps(obj))
        avatar_url = request.POST.get('avatar_url', '')
        nick_name = request.POST.get('nickName', '')
        gender = request.POST.get('gender', 0)
        city = request.POST.get('city', '')
        province = request.POST.get('province', '')
        country = request.POST.get('country', '')
        language = request.POST.get('language', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        data = {}
        data['avatar_url'] = avatar_url
        data['nick_name'] = nick_name
        data['gender'] = gender
        data['city'] = city
        data['province'] = province
        data['country'] = country
        data['language'] = language
        data['phone'] = phone
        data['email'] = email
        result = system_base.save_user_info(user_info, data)
        if result:
            obj['status'] = '1'
        else:
            obj['status'] = '3'
            obj['msg'] = '用户信息保存失败'
    except Exception, e:
        obj['status'] = '0'
        obj['msg'] = e.message
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_qualification_certificate(request):
    """
    获得企业资质证照
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_qualification_certificate(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业资质证照失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_administrative_supervision(request):
    """
    获得企业行政监管
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_administrative_supervision(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业行政监管失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_double_publicity(request):
    """
    获得企业双公示
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_double_publicity(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业双公示失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_quality_check(request):
    """
    获得企业质量检查
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_quality_check(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业质量检查失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_association_info(request):
    """
    获得企业协会信息
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_association_info(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业协会信息失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_media_evaluation(request):
    """
    获得企业媒体评价
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_media_evaluation(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业媒体评价失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_consumer_evaluation(request):
    """
    获得企业消费者评价
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_consumer_evaluation(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业消费者评价失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_patent_info(request):
    """
    获得企业专利权
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_patent_info(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业专利权失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_trademark_info(request):
    """
    获得企业商标信息
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_trademark_info(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业商标信息失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_registration_right(request):
    """
    获得企业著作权
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_registration_right(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业著作权失败'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_employee_evaluation(request):
    """
    获得企业员工评价
    :param request:
    :return:
    """
    obj = {}
    try:
        credit_code = request.POST['credit_code']
        result, count = company_base.get_employee_evaluation(credit_code)
        if result:
            obj['status'] = '1'
            obj['data'] = result
            obj['count'] = count
        else:
            obj['status'] = '2'
            obj['data'] = []
            obj['count'] = 0
    except Exception, e:
        obj['status'] = '0'
        obj['data'] = []
        obj['count'] = 0
        obj['msg'] = '获得企业员工评价失败'
    return HttpResponse(json.dumps(obj))
