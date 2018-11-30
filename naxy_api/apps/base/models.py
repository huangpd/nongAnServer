# coding=utf-8
from __future__ import unicode_literals
from DjangoUeditor.models import UEditorField

from django.db import models


class TUserInfo(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)                                         # 主键ID
    open_id = models.CharField(db_column='openid', max_length=50, blank=True)                      # 微信ID
    user_session = models.CharField(db_column='user_session', max_length=50, blank=True)            # 应用端登录凭证
    avatar_url = UEditorField(db_column='avatar_url', blank=True)                                   # 头像图片url
    city = models.CharField(db_column='city', max_length=50, blank=True)                            # 用户所在城市
    country = models.CharField(db_column='country', max_length=50, blank=True)                      # 用户所在国家
    gender = models.IntegerField(db_column='gender', blank=True, null=False, default=0)             # 性别0为不确定1为男2为女
    languages = models.CharField(db_column='languages', max_length=50, blank=True)                  # 用户所用语言
    nick_name = models.CharField(db_column='nick_name', max_length=50, blank=True)                  # 用户微信昵称
    province = models.CharField(db_column='province', max_length=50, blank=True)                    # 用户所在省份
    phone = models.CharField(db_column='phone', max_length=50, blank=True)                          # 用户手机号
    email = models.CharField(db_column='email', max_length=50, blank=True)                          # 用户email
    real_name = models.CharField(db_column='real_name', max_length=50, blank=True)                  # 用户真实姓名
    # age = models.IntegerField(db_column='age', blank=True, null=True)                               # 用户年龄
    id_card = models.CharField(db_column='id_card', max_length=50, blank=True)                      # 用户身份证号
    account = models.CharField(db_column='account', max_length=50, blank=True)                      # 用户账户
    passw = models.CharField(db_column='passw', max_length=50, blank=True)                          # 用户密码
    create_date = models.DateTimeField(db_column='create_date', blank=True, null=True)              # 创建日期
    user_type = models.IntegerField(db_column='user_type', blank=True, null=False, default=0)       # 用户类型：0-为小程序，1-为app，2-为web
    unionid = models.CharField(db_column='unionid', max_length=50, blank=True)                      # 用户在微信开放平台的唯一标识符。
    session_key = models.CharField(db_column='session_key', max_length=45, blank=True)              # session_key

    class Meta:
        managed = False
        db_table = 't_user_info'


class TSysDictionary(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    parent = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    value = models.CharField(max_length=100, blank=True)
    remark = models.CharField(max_length=100, blank=True)
    sort = models.IntegerField()
    add_date = models.DateTimeField(db_column='add_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_sys_dictionary'


class TSysErrorLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    error_content = models.CharField(max_length=5000, blank=True)
    add_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_sys_error_log'


class TProductInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    product_no = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True)
    status = models.IntegerField(blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_product_info'


class TUserProduct(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField(blank=True, null=True)
    product_no = models.CharField(max_length=100, blank=True)
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    add_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user_product'


class TZcxApiLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    req_tid = models.CharField(max_length=50, blank=True)
    api_name = models.CharField(max_length=100, blank=True)
    api_url = models.CharField(max_length=1000, blank=True)
    nosign_api_url = models.CharField(max_length=1000, blank=True)
    ret_txt = models.TextField(blank=True)
    user_name = models.CharField(max_length=100, blank=True)
    add_date = models.DateTimeField(blank=True, null=True,auto_now_add=True)

    class Meta:
        managed = False
        db_table = 't_zcx_api_log'


