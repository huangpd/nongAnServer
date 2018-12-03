# coding=utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('company.api_company',

    url(r'^pc/get_qualification_certificate$', 'get_qualification_certificate'),  # 资质证照
    url(r'^pc/get_administrative_supervision$', 'get_administrative_supervision'),  # 行政监管
    url(r'^pc/get_double_publicity$', 'get_double_publicity'),  # 双公示
    url(r'^pc/get_quality_check$', 'get_quality_check'),  # 质量检查
    url(r'^pc/get_association_info$', 'get_association_info'),  # 协会信息
    url(r'^pc/get_media_evaluation$', 'get_media_evaluation'),  # 媒体评价
    url(r'^pc/get_consumer_evaluation$', 'get_consumer_evaluation'),  # 消费者评价
    url(r'^pc/get_patent_info$', 'get_patent_info'),  # 专利信息
    url(r'^pc/get_trademark_info$', 'get_trademark_info'),  # 商标信息
    url(r'^pc/get_registration_right$', 'get_registration_right'),  # 著作权
    url(r'^pc/get_employee_evaluation$', 'get_employee_evaluation'),  # 员工评价
    # url(r'^pc/get_qualification_certificate$', 'get_qualification_certificate'),  # 资质证照
    url(r'^pc/get_red_black_list$', 'get_red_black_list'),  # 红黑榜
    url(r'^pc/get_supervise_examine_log$', 'get_supervise_examine_log'),  # 监督检查（执法日志，巡查日志）
    url(r'^pc/get_supervise_examine_case_register$', 'get_supervise_examine_case_register'),  # 监督检查（案件登记）
    url(r'^pc/get_nuisanceless_product$', 'get_nuisanceless_product'),  # 获取无公害产品
    url(r'^pc/get_green_food$', 'get_green_food'),  # 获取绿色食品
    url(r'^pc/get_geography_product$', 'get_geography_product'),  # 获取地理标志产品
    url(r'^pc/get_organic_products$', 'get_organic_products'),  # 获取有机产品
    url(r'^pc/get_traceability_info$', 'get_traceability_info'),  # 获取溯源信息
    url(r'^pc/get_certificate_qualification$', 'get_certificate_qualification'),  # 获取合格证信息






)