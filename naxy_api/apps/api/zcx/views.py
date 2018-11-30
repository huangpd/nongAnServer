# coding=utf-8
from api.zcx.config import zcx_config
from base.log import log
from base.utils import utils


class zcx_api:
    def __init__(self):
        pass

    @staticmethod
    def __parm_assembly(data):
        """
        url参数组装
        :param data: dict格式
        :return: 指定格式的url参数
        """
        try:
            parm = "account=" + zcx_config.account
            sign = "account" + zcx_config.account

            for d, x in data.items():
                parm += "&" + d + "=" + x
                sign += d + x

            parm += "&sign=" + utils.md5(sign)

            return parm
        except Exception, e:
            log.error_log(e.message)
            return None