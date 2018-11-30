# coding=utf-8
import traceback
from base.global_list import GLOBAL_Dictionary
from base.log import log
from base.models import TSysDictionary


class dictionary:
    """
    字典类
    """

    def __init__(self):
        pass

    @staticmethod
    def get_model_for_value(value):
        """
        通过值获取名称
        :rtype : object
        :param name:
        :return:
        """
        try:
            if GLOBAL_Dictionary.has_key(value):
                name = GLOBAL_Dictionary[value]
            else:
                tsd = TSysDictionary.objects.get(value=value)
                name = tsd.name

                GLOBAL_Dictionary[value] = name

            return name
        except Exception, e:
            log.error_log(e.message)
            return ""