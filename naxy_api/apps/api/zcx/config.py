# coding=utf-8

# ============== 测试接口信息 ============
# 测试地址：https://tapi.ccxcredit.com
# 测试环境账号：youxin1234，CODE：9f3a7e1df0e4891f

# 测试地址：https://api.ccxcredit.com
# 测试环境账号：zhaohaizhu_test，CODE：a79d284415b5732f
# =======================================


class zcx_config(object):
    def __init__(self):
        pass
    # 正式账号地址
    # account = 'zhaohaizhu_test'  #账号
    # privateKey = 'a79d284415b5732f'  #私钥
    # zcx_api_host = 'https://api.ccxcredit.com'

    # 测试账号地址
    account = 'youxin1234'  #账号
    privateKey = '9f3a7e1df0e4891f'  #私钥
    zcx_api_host = 'https://tapi.ccxcredit.com'

    credit_report_url = zcx_api_host + '/data-service/credit/report/t1'  # 个人信用报告 接口地址
    education_url = zcx_api_host + '/data-service/edu/query'  # 学历信息 接口地址
    identity_auth_url = zcx_api_host + '/data-service/identity/auth'  # 个人身份验证 接口地址
    identity_photo_url = zcx_api_host + '/data-service/identity/photo'  # 个人身份验证(照片) 接口地址
    icinfo_category_url = zcx_api_host + '/data-service/icinfo/category'  # 工商信息查询 接口地址
    cert_url = zcx_api_host + '/data-service/cert'  # 个人职业资格证书查询 接口地址
    riskinfo_classify_url = zcx_api_host + '/data-service/riskinfo/classify'  # 风险信息查询 接口地址
    criminal_url = zcx_api_host + '/data-service/criminal/query'  # 犯罪信息查询 接口地址
    telecom_identity = zcx_api_host + '/data-service/telecom/identity/3mo/t1'  # 手机验证
