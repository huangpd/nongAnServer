# coding=utf-8
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
                obj['pubdate'] = qualification[6].__str__()
                obj['valid_time'] = qualification[7]
                obj['licence_content'] = qualification[8]
                obj['img_url'] = qualification[9]
                obj['add_date'] = qualification[10].__str__()
                obj['license_number'] = qualification[11]
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
                where a.credit_code = "%s" order by file_property
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
                obj['pubdate'] = supervision[7].__str__()
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
        获得双公示
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
        协会信息
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
        获得双公示
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



