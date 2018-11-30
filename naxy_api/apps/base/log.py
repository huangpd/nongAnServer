# coding=utf-8
from datetime import datetime
from base.models import TSysErrorLog


class log:
    def __init__(self):
        pass

    @staticmethod
    def error_log(content):
        """
        添加错误日志
        :param contetn:
        :return:
        """
        err = TSysErrorLog(
            error_content=content,
            add_date=datetime.now()
        )

        err.save()