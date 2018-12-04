# coding=utf-8
from base.models import TPcBaseInfo
from base.utils import utils


class company_base():
    """
    企业类
    """

    def __init__(self):
        pass

    @staticmethod
    def get_qualification_certificate(credit_code):
        """
        获得资质证照
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_qualification_certificate t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for qualification in data:
                obj = {}
                obj['id'] = qualification[0]
                obj['title'] = qualification[2]
                obj['file_no'] = qualification[3]
                obj['file_type'] = qualification[4]
                obj['issuer'] = qualification[5]
                obj['pubdate'] = qualification[6]
                obj['valid_time'] = qualification[7]
                obj['licence_content'] = qualification[8]
                obj['img_url'] = qualification[9]
                obj['add_date'] = qualification[10].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_administrative_supervision(credit_code):
        """
        获得行政监管
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_ad_supervision t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for supervision in data:
                obj = {}
                obj['id'] = supervision[0]
                obj['title'] = supervision[2]
                obj['file_no'] = supervision[3]
                obj['file_number'] = supervision[4]
                obj['file_property'] = supervision[5]
                obj['issuer'] = supervision[6]
                obj['pubdate'] = supervision[7]
                obj['file_content'] = supervision[8]
                obj['add_date'] = supervision[10].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_double_publicity(credit_code):
        """
        获得双公示
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_double_publicity t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for publicity in data:
                obj = {}
                obj['id'] = publicity[0]
                obj['license_number'] = publicity[2]
                obj['audit_category'] = publicity[3]
                obj['item_name'] = publicity[4]
                obj['decide_date'] = publicity[5]
                obj['limit_date'] = publicity[6]
                obj['licence_content'] = publicity[7]
                obj['license_authority'] = publicity[8]
                obj['add_date'] = publicity[10].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_quality_check(credit_code):
        """
        获得质量检查
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_quality_check t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for check in data:
                obj = {}
                obj['id'] = check[0]
                obj['title'] = check[2]
                obj['product_name'] = check[3]
                obj['file_no'] = check[4]
                obj['file_property'] = check[5]
                obj['file_number'] = check[6]
                obj['file_content'] = check[7]
                obj['issuer'] = check[8]
                obj['pubdate'] = check[9]
                obj['relate_product'] = check[10]
                obj['add_date'] = check[11].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_association_info(credit_code):
        """
        获得双公示
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_association t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for association in data:
                obj = {}
                obj['id'] = association[0]
                obj['title'] = association[2]
                obj['file_no'] = association[3]
                obj['file_number'] = association[4]
                obj['file_property'] = association[5]
                obj['issuer'] = association[6]
                obj['pubdate'] = association[7]
                obj['file_content'] = association[8]
                obj['img_url'] = association[10]
                obj['add_date'] = association[11].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_media_evaluation(credit_code):
        """
        获得双公示
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_media_evaluation t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for evaluation in data:
                obj = {}
                obj['id'] = evaluation[0]
                obj['title'] = evaluation[2]
                obj['file_no'] = evaluation[3]
                obj['file_property'] = evaluation[4]
                obj['release_media'] = evaluation[5]
                obj['pubdate'] = evaluation[6]
                obj['file_content'] = evaluation[7]
                obj['relate_url'] = evaluation[9]
                obj['add_date'] = evaluation[10].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_consumer_evaluation(credit_code):
        """
        获得消费者评价
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_consumer_evaluation t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for evaluation in data:
                obj = {}
                obj['id'] = evaluation[0]
                obj['title'] = evaluation[2]
                obj['file_property'] = evaluation[3]
                obj['content'] = evaluation[4]
                obj['general_evaluation'] = evaluation[5]
                obj['pubdate'] = evaluation[6]
                obj['consumer'] = evaluation[7]
                obj['add_date'] = evaluation[9].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_patent_info(credit_code):
        """
        获得专利信息
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_patent t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for patent in data:
                obj = {}
                obj['id'] = patent[0]
                obj['title'] = patent[2]
                obj['file_no'] = patent[3]
                obj['file_number'] = patent[4]
                obj['patent_holder'] = patent[5]
                obj['pubdate'] = patent[6]
                obj['file_type'] = patent[7]
                obj['authority_state'] = patent[8]
                obj['img_url'] = patent[9]
                obj['add_date'] = patent[10].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_trademark_info(credit_code):
        """
        获得商标信息
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_trademark t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for trademark in data:
                obj = {}
                obj['id'] = trademark[0]
                obj['title'] = trademark[2]
                obj['file_no'] = trademark[3]
                obj['file_number'] = trademark[4]
                obj['mark_applicant'] = trademark[5]
                obj['pubdate'] = trademark[6]
                obj['file_type'] = trademark[7]
                obj['img_url'] = trademark[8]
                obj['add_date'] = trademark[9].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_registration_right(credit_code):
        """
        获得双公示
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_registration_right t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for registration in data:
                obj = {}
                obj['id'] = registration[0]
                obj['file_no'] = registration[2]
                obj['file_number'] = registration[3]
                obj['author'] = registration[4]
                obj['pubdate'] = registration[5]
                obj['file_type'] = registration[6]
                obj['img_url'] = registration[7]
                obj['add_date'] = registration[8].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_employee_evaluation(credit_code):
        """
        获得员工评价
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_employee_evaluation t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for registration in data:
                obj = {}
                obj['id'] = registration[0]
                obj['title'] = registration[2]
                obj['file_property'] = registration[3]
                obj['content'] = registration[4]
                obj['general_evaluation'] = registration[5]
                obj['pubdate'] = registration[6]
                obj['employee'] = registration[7]
                obj['add_date'] = registration[9].__str__()
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_red_black_list(credit_code):
        """
        获得红黑榜
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_red_black_list t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s" order by t.is_red_black
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for red_black_list in data:
                obj = {}
                obj['id'] = red_black_list[0]
                obj['is_red_black'] = red_black_list[2]                         # 红榜或者黑榜
                obj['rank_list'] = red_black_list[3]                            # 上榜主体
                obj['contant'] = red_black_list[4]                              # 联系人
                obj['contant_number'] = red_black_list[5]                       # 联系电话
                obj['year'] = red_black_list[6]                                 # 年度
                obj['rank_time'] = red_black_list[7]                            # 上榜时间
                obj['is_repeal'] = red_black_list[8]                            # 是否撤销
                obj['is_intranet'] = red_black_list[9]                          # 是否内网公示
                obj['is_outer_net'] = red_black_list[10]                        # 是否外网公示
                obj['rank_reason'] = red_black_list[11]                         # 上榜理由
                obj['remark'] = red_black_list[12]                              # 备注
                obj['add_date'] = red_black_list[13].__str__()                  # 添加时间
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_supervise_examine_log(credit_code):
        """
        监督检查（执法日志，巡查日志）
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_supervise_examine_log t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s" order by t.log_type
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for examine_log in data:
                obj = {}
                obj['id'] = examine_log[0]
                obj['law_time'] = examine_log[2]                                    # 执法时间
                obj['law_enforcement'] = examine_log[3]                             # 执法单位
                obj['law_enforcement_person'] = examine_log[4]                      # 执法人
                obj['check_situation'] = examine_log[5]                             # 检查情况与处理意见
                obj['scene_photo'] = examine_log[6]                                 # 现场照片
                obj['log_type'] = examine_log[7]                                    # 监督检查日志类型：执法日志，巡查日志
                obj['add_date'] = examine_log[8].__str__()                          # 添加时间
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_supervise_examine_case_register(credit_code):
        """
        监督检查（案件登记）
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_supervise_examine_case_register t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for case_register in data:
                obj = {}
                obj['id'] = case_register[0]
                obj['case_number'] = case_register[2]                               # 案件编号
                obj['case_name'] = case_register[3]                                 # 案件名称
                obj['case_money'] = case_register[4]                                # 涉案金额
                obj['start_case_time'] = case_register[5]                           # 立案时间
                obj['end_case_time'] = case_register[6]                             # 结束时间
                obj['penalty'] = case_register[7]                                   # 罚款金额
                obj['illegal_fact'] = case_register[8]                              # 违法事实
                obj['judgment_basis'] = case_register[9]                            # 判定依据
                obj['law_enforcement'] = case_register[9]                           # 执法单位
                obj['law_enforcement_person'] = case_register[9]                    # 执法人员
                obj['add_date'] = case_register[9]                                  # 添加时间
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_nuisanceless_product(credit_code):
        """
        获取无公害产品
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_nuisanceless_product t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for nuisanceless_product in data:
                obj = {}
                obj['id'] = nuisanceless_product[0]
                obj['proposer'] = nuisanceless_product[2]                                  # 申请人全称
                obj['license_number'] = nuisanceless_product[3]                            # 证书编号
                obj['license_time'] = nuisanceless_product[4]                              # 证书有效期
                obj['firm_name'] = nuisanceless_product[5]                                 # 行业名称
                obj['product_type'] = nuisanceless_product[6]                              # 产品类别名称
                obj['compartment'] = nuisanceless_product[7]                               # 区划
                obj['process_scale'] = nuisanceless_product[8]                             # 生产规模
                obj['annual_output'] = nuisanceless_product[9]                             # 年产量（吨）
                obj['annual_turnover'] = nuisanceless_product[10]                          # 年销售额（万元）
                obj['origin_number'] = nuisanceless_product[11]                            # 认定产地证书编号
                obj['origin_address'] = nuisanceless_product[12]                           # 认定产地地址
                obj['company_type'] = nuisanceless_product[13]                             # 单位性质
                obj['add_date'] = nuisanceless_product[14].__str__()                       # 添加时间
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_green_food(credit_code):
        """
        获取绿色产品
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_green_food t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for geeen_food in data:
                obj = {}
                obj['id'] = geeen_food[0]
                obj['company_name'] = geeen_food[2]                             # 企业名称
                obj['product_name'] = geeen_food[3]                             # 产品名称
                obj['brand_name'] = geeen_food[4]                               # 商标名称
                obj['license_number'] = geeen_food[5]                           # 证书编号
                obj['license_time'] = geeen_food[6]                             # 证书有效期
                obj['business_type'] = geeen_food[7]                            # 业务类型
                obj['enterprise_code'] = geeen_food[8]                          # 企业信息码
                obj['compartment'] = geeen_food[9]                              # 区划
                obj['agricultural_cooperative'] = geeen_food[10]                # 农业合作社
                obj['army'] = geeen_food[11]                                    # 军队
                obj['bibcock_logo'] = geeen_food[12]                            # 龙头企业标识
                obj['add_date'] = geeen_food[13].__str__()                      # 添加时间
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_geography_product(credit_code):
        """
        获取地理标志产品
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_geography_product t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for geography_product in data:
                obj = {}
                obj['id'] = geography_product[0]
                obj['product_name'] = geography_product[2]                             # 产品名称
                obj['register_time'] = geography_product[3]                            # 登记时间
                obj['register_number'] = geography_product[4]                          # 登记证号
                obj['add_date'] = geography_product[5]                                 # 添加时间
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_organic_products(credit_code):
        """
        获取有机产品
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_organic_products t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for geography_product in data:
                obj = {}
                obj['id'] = geography_product[0]
                obj['product_name'] = geography_product[2]                             # 产品名称
                obj['add_date'] = geography_product[3]                                 # 添加时间
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_traceability_info(credit_code):
        """
        获取溯源信息
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_traceability_info t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for traceability in data:
                obj = {}
                obj['id'] = traceability[0]
                obj['product_name'] = traceability[2]                               # 产品名称
                obj['product_logo'] = traceability[3]                               # 产品logo
                obj['ipo_time'] = traceability[4]                                   # 上市时间
                obj['production_unit'] = traceability[5]                            # 生产单位
                obj['contact_phone'] = traceability[6]                              # 联系方式
                obj['duty_person'] = traceability[7]                                # 责任人
                obj['trace_code'] = traceability[8]                                 # 追溯码
                obj['main_name'] = traceability[9]                                  # 主体名称
                obj['phone'] = traceability[10]                                     # 联系电话/手机
                obj['postcode'] = traceability[11]                                  # 邮编
                obj['address'] = traceability[12]                                   # 详细地址
                obj['process_scale'] = traceability[13]                             # 生产规模
                obj['leading_product'] = traceability[14]                           # 主导产品
                obj['main_introduction'] = traceability[15]                         # 主体简介
                obj['add_date'] = traceability[16]                                  # 添加时间
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0

    @staticmethod
    def get_certificate_qualification(credit_code):
        """
        获取合格证信息
        :param credit_code:
        :return:
        """
        try:
            sql = """
                select t.* from t_pc_certificate_qualification t
                left join t_pc_base_info a on t.pc_id = a.id
                where a.credit_code = "%s"
            """ % credit_code
            data = utils.sql_helper(sql)
            result = []
            for traceability in data:
                obj = {}
                obj['id'] = traceability[0]
                obj['company_name'] = traceability[2]                                            # 企业名称
                obj['business_license'] = traceability[3]                                        # 营业执照
                obj['compartment'] = traceability[4]                                             # 区划
                obj['contant'] = traceability[5]                                                 # 联系人
                obj['contant_number'] = traceability[6]                                          # 联系电话
                obj['company_address'] = traceability[7]                                         # 企业详细地址
                obj['product_name'] = traceability[8]                                            # 产品名称
                obj['weight'] = traceability[9]                                                  # 重量
                obj['issue_date'] = traceability[10]                                             # 开具日期
                obj['certificates_number'] = traceability[11]                                    # 合格证张数
                obj['certificates_preview'] = traceability[12]                                   # 合格证预览
                obj['add_date'] = traceability[13]                                               # 添加日期
                result.append(obj)
            return result, len(result)
        except Exception, e:
            return [], 0