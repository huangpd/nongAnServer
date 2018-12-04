# coding=utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('api.out_api',

    url(r'^pc/get_company_detail$', 'get_company_detail'),  # 企业详情
    url(r'^pc/get_announcement_list$', 'get_announcement_list'),  # 法院公告
    url(r'^pc/get_zhixing_list$', 'get_zhixing_list'),  # 执行信息
    url(r'^pc/get_shixin_list$', 'get_shixin_list'),  # 失信信息
    url(r'^pc/get_judgment_list$', 'get_judgment_list'),  # 查询法院判决书
    url(r'^pc/get_patent_list$', 'get_patent_list'),  # 查询专利
    url(r'^pc/get_trademark_list$', 'get_trademark_list'),  # 查询商标
    url(r'^pc/get_copyright_list$', 'get_copyright_list'),  # 查询著作权
    url(r'^pc/get_certification_summary$', 'get_certification_summary'),  # 查询企业证书
    url(r'^pc/get_news$', 'get_news'),  # 查询企业新闻
    url(r'^pc/get_jobs$', 'get_jobs'),  # 查询企业招聘信息
    url(r'^pc/get_website_list$', 'get_website_list'),  # 查询企业注册网站
    url(r'^pc/get_company_financings$', 'get_company_financings'),  # 查询企业融资信息
    url(r'^pc/get_company_products$', 'get_company_products'),  # 查询企业产品
    url(r'^pc/get_company_Investment$', 'get_company_Investment'),  # 查询企业对外投资
    url(r'^pc/company_advancedsearch$', 'company_advancedSearch'),  # 企业信息高级查询



)
