# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
@Author  : ziheng.ni
@Time    : 2021/4/2 13:26
@Contact : ziheng.ni@envision-energy.com
@Desc    :
"""
from cryptography.fernet import Fernet


def generate_public_key():
    """采用对称加密，所以需要保存公钥(public_key)，解密时需要用到"""
    public_key = Fernet.generate_key()
    public_key = public_key.decode(encoding='utf-8')
    return public_key


def encrypt(pwd, public_key):
    """
    加密

    Args:
        pwd: str. 原密码
        public_key: str. 公钥

    Returns:
        encryped_pwd: str. 加密后的密码
    """
    cipher = Fernet(bytes(public_key, encoding='utf-8'))
    encryped_pwd = cipher.encrypt(bytes(pwd, encoding='utf-8')).decode('utf-8')
    return encryped_pwd


def decrypt(encryped_pwd, public_key):
    """
    解密

    Args:
        encryped_pwd: str. 加密后的密码
        public_key: str. 公钥

    Returns:
        pwd: str. 原密码
    """
    pwd = Fernet(bytes(public_key, encoding='utf-8')).decrypt(bytes(encryped_pwd, encoding='utf-8')).decode(
        encoding='utf-8')
    return pwd


if __name__ == '__main__':
    """
    使用步骤：
        1. 安装cryptography
        > pip install cryptography==3.4.7

        2. 生成公钥（调用generate_public_key方法），并保存

        3. 加密原密码，生成秘钥

        4. 替换项目中原密码为秘钥，在使用时，通过‘公钥’和‘私钥’解密
    """

    # 1. 获取公钥
    public_key = generate_public_key()
    print(public_key)

    # 2. 加密
    # pwd = "EnvOkta@Future8"  # your raw password
    # pwd = "vyQXtoq2OP"
    pwd = 'aCm#gYwNP3otjP#k'
    en_pwd = encrypt(pwd, public_key)
    print(f"加密后的秘钥：{en_pwd}")

    # 3. 解密
    en_pwd = 'gAAAAABjWjmp2M2aEBzC9IM2sSZyRuYvIsi5294f7GGJq7upY7BKZXPRy4_lAw6AM3mXpj2k73vdq0h5GhvDKNS5eYFjyj5jYQ=='
    public_key = 'x1gU4awrn-fMqH4Zu77WPUdm9FYpdIDA-Me7-_UiwTM='
    raw_pwd = decrypt(en_pwd, public_key)
    print(f"解密后密码：{raw_pwd}")
