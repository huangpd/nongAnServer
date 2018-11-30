# coding=utf-8
from datetime import datetime
from base.encrypt_utils import encryptUtils
from base.models import TUserInfo


class system_base:
    """
    系统基本类
    """

    def __init__(self):
        pass

    @staticmethod
    def save_open_id_and_session_key(open_id, code, session_key):
        """
        保存open_id和session_key
        :param open_id:
        :param code:
        :param session_key:
        :return:
        """
        try:
            # 根据open_id获得用户信息，返回值为list
            users = TUserInfo.objects.filter(open_id=open_id)
            # 当没有该用户时，插入数据，有则修改数据
            if users.count() == 0:
                user = TUserInfo(create_date=datetime.now(), open_id=open_id, user_session=code, session_key=session_key)
                user.save()
            else:
                # 存在该用户在修改code及session_key
                user = users[0]
                user.user_session = code
                user.session_key = session_key
                user.save()
            return user
        except Exception, e:
            return None

    @staticmethod
    def get_user_info_by_session_id(session_id, request):
        """
        根据session_id获得用户信息
        :param session_id:
        :param request:
        :return:
        """
        try:
            # 解密session_id
            if request.session.get('session_id') == session_id.replace(' ', '+'):
                user_session = request.session.get('code')
            else:
                user_session = encryptUtils.decrypt(session_id.replace(' ', '+'))
                request.session['session_id'] = session_id.replace(' ', '+')
                request.session['code'] = user_session
            user_info = TUserInfo.objects.get(user_session=user_session)
            return user_info
        except Exception, e:
            return None

    @staticmethod
    def save_user_info(user_info, data):
        """
        保存用户信息
        :param user_info:
        :return:
        """
        try:
            user_info.avatar_url = data['avatar_url']
            user_info.nick_name = data['nick_name']
            user_info.gender = data['gender']
            user_info.city = data['city']
            user_info.province = data['province']
            user_info.country = data['country']
            user_info.language = data['language']
            user_info.phone = data['phone']
            user_info.email = data['email']
            user_info.language = data['language']
            user_info.save()
            return user_info
        except Exception, e:
            return None

