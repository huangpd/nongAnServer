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
    url(r'^pc/get_employee_evaluation$', 'get_employee_evaluation'),  # 资质证照
    # url(r'^pc/get_qualification_certificate$', 'get_qualification_certificate'),  # 资质证照
)