# coding=utf-8
import traceback
from base.log import log
from base.models import TUserProduct, TProductInfo


class product:
    """
    产品类
    """
    def __init__(self):
        pass


    @staticmethod
    def get_product_price_for_user(product_no, user_id):
        """
        通过用户ID获取指定产品价格
        :param product_no: 产品编号
        :param user_id: 用户ID
        :return:
        """
        try:
            tup = TUserProduct.objects.filter(user_id=user_id, product_no=product_no)

            if len(tup) > 0:
                return tup[0].money
            else:
                product = TProductInfo.objects.get(product_no=product_no, status=1)

                return product.money
        except Exception, e:
            log.error_log(e.message)
            return None


    @staticmethod
    def get_product_for_user(product_no):
        """
        通过用户ID获取指定产品对象
        :param product_no: 产品编号
        :return:
        """
        try:
            product = TProductInfo.objects.get(product_no=product_no)

            return product
        except Exception, e:
            log.error_log(e.message)
            return None