# -*- coding: utf-8 -*-
from pyDes import *
import base64
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class encryptUtils():

    @staticmethod
    def encryptMD5(strData):
        m = hashlib.md5()
        m.update(strData)
        return m.digest()

    @staticmethod
    def encryptDES(crykey,byteData):
        # data = "Please encrypt my data"
        # pyDes.des(key, [mode], [IV], [pad], [padmode])
        # pyDes.triple_des(key, [mode], [IV], [pad], [padmode])
        # crykey = "5c529b9e4f2d5044dde8c0ae"
        k = triple_des(crykey, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        encryptdata = k.encrypt(byteData)
        return encryptdata

    @staticmethod
    def decryptDES(crykey,byteData):
        # crykey = "5c529b9e4f2d5044dde8c0ae"
        k = triple_des(crykey, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        return k.decrypt(byteData, padmode=PAD_PKCS5)

    @staticmethod
    def encryptBase64(byteData):
        return str(base64.b64encode(byteData)).encode("utf8")

    @staticmethod
    def decryptBase64(data):
        return base64.b64decode(str(data).decode("utf8"))

    # 为接口输出参数编码 先3des编码后base64编码
    @staticmethod
    def encrypt(byteData):
        crykey = "sjsuenreni3410sncai12043"
        encryptStr = encryptUtils.encryptDES(crykey,byteData)
        outputStr = encryptUtils.encryptBase64(encryptStr)
        #outputStr = encryptUtils.encryptDES(crykey,byteData)
        return str(outputStr)

    # 为接口输入参数进行解码 先base64解码后3des解码
    @staticmethod
    def decrypt(byteData):
        crykey = "sjsuenreni3410sncai12043"
        decryptStr = encryptUtils.decryptBase64(byteData)
        inputStr = encryptUtils.decryptDES(crykey,decryptStr)
        #inputStr = encryptUtils.decryptDES(crykey,byteData)
        return str(inputStr)