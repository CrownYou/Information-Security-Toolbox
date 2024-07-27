import base64
import copy
import re
import math
import tenseal as ts
from math import ceil
from math import floor
import random
from random import randint, choice
from tkinter import ttk
import numpy as np  # pip install numpy
from windnd import hook_dropfiles  # pip install windnd
import matplotlib.pyplot as plt  # pip install matplotlib
import sympy as sp  # pip install sympy
from moviepy.editor import VideoFileClip, AudioFileClip  # pip install moviepy
import pyperclip  # pip install pyperclip
import binascii
import hashlib
import shutil  # pip install pytest-shutil
import zlib
from Crypto import Random  # pip install pycryptodome
from Crypto.Hash import SHA384
from Crypto.Hash import MD4
from Crypto.Hash import RIPEMD160
from Crypto.Cipher import AES
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
import threading
import pyautogui as auto  # pip install pyautogui==0.9.50
from tkinter import messagebox
import zero_width_lib as zwlib  # pip install zero_width_lib
import jieba  # pip install jieba
import unvcode
import string
from reedsolo import RSCodec  # pip install reedsolo
from cryptography.hazmat.primitives import hashes, serialization  # pip install cryptography
from cryptography.hazmat.primitives.asymmetric import dh, ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from blind_watermark import WaterMark  # pip install blind-watermark==0.4.4
import tenseal as ts  # pip install tenseal
# 上面的是其他文件需要调用的库，打包文件的时候需要用上
import blind_watermark
import os
import time
import tkinter as tk
import cv2  # pip install opencv-python==4.5.1.48
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA
from system_resource import MyEncryption as myenc, MySteganography as myste, ToolKit as kit, ToolBox as mybox
from system_resource.ToolKit import Tools
'''为了防止项目文件调用的库被误删，这里以注释的方式写在这里
import base64
import copy
import re
import math
import tenseal as ts
from math import ceil
from math import floor
import random
from random import randint, choice
from tkinter import ttk
import numpy as np  # pip install numpy
from windnd import hook_dropfiles  # pip install windnd
import matplotlib.pyplot as plt  # pip install matplotlib
import sympy as sp  # pip install sympy
from moviepy.editor import VideoFileClip, AudioFileClip  # pip install moviepy
import pyperclip  # pip install pyperclip
import binascii
import hashlib
import shutil  # pip install pytest-shutil
import zlib
from Crypto import Random  # pip install pycryptodome
from Crypto.Hash import SHA384
from Crypto.Hash import MD4
from Crypto.Hash import RIPEMD160
from Crypto.Cipher import AES
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
import threading
import pyautogui as auto  # pip install pyautogui==0.9.50
from tkinter import messagebox
import zero_width_lib as zwlib  # pip install zero_width_lib
import jieba  # pip install jieba
import unvcode
import string
from reedsolo import RSCodec  # pip install reedsolo
from cryptography.hazmat.primitives import hashes, serialization  # pip install cryptography
from cryptography.hazmat.primitives.asymmetric import dh, ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from blind_watermark import WaterMark  # pip install blind-watermark==0.4.4
import tenseal as ts  # pip install tenseal
'''

window = tk.Tk()
window.title('信安工具箱')
window.geometry('1272x758')
mid_font = ('Noto Sans Mono', 13)
frm = tk.Frame(window)
frm.pack()
colors = ['mediumblue', 'hotpink', 'darkgreen', 'red', 'orange', 'darkcyan']
ind = 0
blind_watermark.bw_notes.close()


class MyTools:
    @staticmethod
    def delete_temp_file():

        @Tools.run_as_thread
        def run():
            Tools.delete_file('_temp_file.txt')
            Tools.delete_file('myplot.png')
            time.sleep(0.2)
            print('result of deleting files:', Tools.delete_file('my_audio.wav'), Tools.delete_file(myste.temp_video_path), Tools.delete_file(myste.temp_outvideo_path), Tools.delete_file(myste.temp_video_saving_path))
            print('临时文件删除完毕')

        run()

    @staticmethod
    def initiation(size='1272x758'):
        myste.alive = False
        mybox.alive = False
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
        window.geometry(size)
        Tools.clean_all_widget(frm)
        MyTools.delete_temp_file()

    @staticmethod
    def on_closing():

        @Tools.run_as_thread
        def run():
            print('开始关闭所有线程')
            myste.alive = False
            mybox.alive = False
            print('已关闭所有线程')
            icon_image.destroy()
            print('开始删除临时文件')
            MyTools.delete_temp_file()
            time.sleep(0.25)
            # cv2.destroyAllWindows()  # 窗口不用关，_exit()之后自动关
            os._exit(0)  # 必须这样退出，不然setDeamon不起作用

        run()

    @staticmethod
    def login():
        with open("./system_resource/check_enc.dll", 'rb') as f:
            pwd = f.read(32)
        login_button.destroy()
        login_window = tk.Toplevel()
        login_window.title('登录界面')
        login_window.geometry('525x300')
        login_window.iconbitmap(icon_path)
        label1 = tk.Label(login_window, text='请输入登录密码：', font=mid_font)
        label1.pack()
        entry1 = tk.Entry(login_window, width=15, font=mid_font)
        entry1.pack()
        checked_time = 0
        checked_succeed = False

        def check(*args):
            nonlocal checked_time, button1, checked_succeed
            if checked_succeed:
                login_window.destroy()
                return 0
            Tools.clean_all_widget(_frm)
            if checked_time >= 2:  # 可尝试2次 （0，1）
                label2 = tk.Label(_frm, text='密码错误，尝试次数用完', font=mid_font)
                label2.pack()
            else:
                if Tools.get_hash_digest_of_word(entry1.get() + 'Promelan^Like_the2wind') == pwd:
                    button1.destroy()
                    window.config(menu=menubar)
                    label3 = tk.Label(_frm, text='你好，欢迎使用', font=mid_font)
                    label3.pack()
                    checked_succeed = True

                    def change_pwd(*args):
                        Tools.clean_all_widget(_frm)
                        entry1.config(state='readonly')
                        label5 = tk.Label(_frm, text='请输入新密码：', font=mid_font)
                        label5.pack()
                        entry2 = tk.Entry(_frm, width=15, font=mid_font)
                        entry2.pack()
                        t2 = 0

                        def confirm_new_pwd(*args):
                            global pwd
                            nonlocal t2
                            if t2 > 0:
                                login_window.destroy()
                            else:
                                t2 += 1
                                new_pwd = Tools.get_hash_digest_of_word(entry2.get() + 'Promelan^Like_the2wind')
                                with open("system_resource/check_enc.dll", 'wb') as f:
                                    f.write(new_pwd)
                                button3.destroy()
                                label6 = tk.Label(_frm, text='修改成功', font=mid_font)
                                label6.pack()

                        button3 = tk.Button(_frm, text='确认', font=mid_font, command=confirm_new_pwd)
                        button3.pack()
                        entry2.bind('<Return>', confirm_new_pwd)

                    button2 = tk.Button(_frm, text='更改密码', font=mid_font, command=change_pwd)
                    button2.pack()
                else:
                    checked_time += 1
                    if checked_time == 1:
                        label4 = tk.Label(_frm, text=f'密码错误，还有一次机会', font=mid_font)
                        label4.pack()
                    else:
                        check()

        button1 = tk.Button(login_window, text='确认', command=check, font=mid_font)
        button1.pack()
        entry1.bind('<Return>', check)
        _frm = tk.Frame(login_window)
        _frm.pack()


class Image:
    def __init__(self, enc_path, kind: str):
        # enc_path 是被加密的图片的地址，out_path是解密出来后临时保存的地址
        self.enc_path = enc_path
        basename = enc_path[:enc_path.rindex('.')] + '_temp'
        file_number = 0
        while True:
            file_name = f"{basename}({str(file_number)}).{kind}"
            if os.path.exists(file_name):
                file_number += 1
            else:
                self.out_path = file_name
                break

    @property
    def decrypt(self):
        # 返回解密出来的地址
        p = b'-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC7ud4cS++xj/9PcTO5sm6yLO3gQmL03J1jxnyZc4RV0dPSPAp9\n99NHuGdPhDb/Vc6QwcJgq1l6ZjAkjG3/AZtr1VTia4U0qLFT1HN4HmuQ4FSbt+9x\nEDRSes/nsCN9nD8e1gvVe8W24np6oc43fvs9LKW7BQgZCqBptSrRCaJvwwIDAQAB\nAoGAF5eHZ9P35r87gpQt6spB/3IGX7bIG+YL1j8FZ/2B+ze4S0VQu5L6bPAqSkPJ\n653bggqvrxlppdMTfXcJLdEvDbpH2dGCHkuYH6sdTOIc/I29aAb5do8rOb26uDmD\nK9ofb+7C/j42NAMR03tKohFRZmjo1ALQKUFPunnjYSTdg90CQQDZTEOS2BsvVRwE\nLQ9yent2xPhDZLwl9avc8We+0wxcRNxvzWqanD5UZTjDdMfUJ0MFMoJUM37XwHC+\n0mlo6SCvAkEA3SlE/dJWUQSMDMXTfod4gvjiuNcvFzpJXEat2sG99RX6XWiKCdm+\nI9vUuA6z8Py8E/wu9SJJGbGGxFvikRWfLQJASqDypEAsNflZAeYn4/1E4emMCjlS\nlQbm257dLqB1IktUGeHGtwrqLToGYLp+1tIVJnfOYvS8n4SsNB03rpxCaQJBAI98\nEfW3PCcOEyrKQh/KFoaqoLWZbkTcnPHQLUVLA0n5+1gU1dH0QecT3ZuYdmf4ILG6\noGCL4O9ZfPzyPDky1PUCQDymv76K7CYAhgFmiOiJ179cmEigXnUIboIOk74UmaRW\n0DaTdT37hwVUb+8ORm06F/h6MK7UnpoTJpsGXbEsqQ8=\n-----END RSA PRIVATE KEY-----'
        key = RSA.importKey(p)
        privkey = PKCS1_cipher.new(key)
        Tools.decrypt_bigfile(self.enc_path, self.out_path, privkey)
        return self.out_path

    def destroy(self):
        # 将self.out_path删掉
        Tools.delete_file(self.out_path)


class Functions:
    @staticmethod
    def video_logo():
        MyTools.initiation()
        myste.video_logo()

    @staticmethod
    def nearest_neighbor():
        MyTools.initiation()
        myste.nearest_neighbor()

    @staticmethod
    def read_video_logo():
        MyTools.initiation()
        myste.read_video_logo()

    @staticmethod
    def fourier_word():
        MyTools.initiation()
        myste.fourier_word()

    @staticmethod
    def fourier_pic():
        MyTools.initiation()
        myste.fourier_pic()

    @staticmethod
    def get_hsv_value():
        MyTools.initiation()
        myste.get_hsv_value()

    @staticmethod
    def generate_random_char():
        MyTools.initiation()
        mybox.generate_random_char()

    @staticmethod
    def base64converter():
        MyTools.initiation()
        mybox.base64converter()

    @staticmethod
    def dh_exchange():
        MyTools.initiation()
        mybox.dh_exchange()

    @staticmethod
    def rs_code_word():
        MyTools.initiation()
        mybox.rs_code_word()

    @staticmethod
    def rs_code_file():
        MyTools.initiation()
        mybox.rs_code_file()

    @staticmethod
    def against_duplicate_check():
        MyTools.initiation()
        mybox.against_duplicate_check()

    @staticmethod
    def create_rsa_key():
        MyTools.initiation()
        myenc.create_rsa_key()

    @staticmethod
    def set_pwd_of_rsa_privkey():
        MyTools.initiation()
        myenc.set_pwd_of_rsa_privkey()

    @staticmethod
    def rsa_word():
        MyTools.initiation()
        myenc.rsa_word()

    @staticmethod
    def rsa_file():
        MyTools.initiation()
        myenc.rsa_file()

    @staticmethod
    def rsa_sign_and_verify():
        MyTools.initiation()
        myenc.rsa_sign_and_verify()

    @staticmethod
    def create_ecc_key():
        MyTools.initiation()
        myenc.create_ecc_key()

    @staticmethod
    def set_pwd_of_ecc_privkey():
        MyTools.initiation()
        myenc.set_pwd_of_ecc_privkey()

    @staticmethod
    def ecc_word():
        MyTools.initiation()
        myenc.ecc_word()

    @staticmethod
    def ecc_file():
        MyTools.initiation()
        myenc.ecc_file()

    @staticmethod
    def ecc_sign_and_verify():
        MyTools.initiation()
        myenc.ecc_sign_and_verify()

    @staticmethod
    def create_aes_key_by_hash_digest():
        MyTools.initiation()
        myenc.create_aes_key_by_hash_digest()

    @staticmethod
    def create_aes_key_16():
        MyTools.initiation()
        myenc.create_aes_key(16)

    @staticmethod
    def create_aes_key_32():
        MyTools.initiation()
        myenc.create_aes_key(32)

    @staticmethod
    def aes_word():
        MyTools.initiation()
        myenc.aes_word()

    @staticmethod
    def aes_file():
        MyTools.initiation()
        myenc.aes_file()

    @staticmethod
    def create_ckks_key():
        MyTools.initiation()
        myenc.create_ckks_key()

    @staticmethod
    def set_pwd_of_ckks_privkey():
        MyTools.initiation()
        myenc.set_pwd_of_ckks_privkey()

    @staticmethod
    def ckks_word():
        MyTools.initiation('1604x808')
        myenc.ckks_word()

    @staticmethod
    def hash_word():
        MyTools.initiation()
        myenc.hash_word()

    @staticmethod
    def hash_file():
        MyTools.initiation()
        myenc.hash_file()

    @staticmethod
    def hide_zip():
        MyTools.initiation()
        myste.hide_zip()

    @staticmethod
    def zero_width_ste():
        MyTools.initiation()
        myste.zero_width_ste()

    @staticmethod
    def confuse_qr_code():
        MyTools.initiation()
        mybox.confuse_qr_code()

    @staticmethod
    def hide_qr_code():
        MyTools.initiation()
        mybox.hide_qr_code()

    @staticmethod
    def intro():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    软件基本介绍
        
    这是CrownYou International Software Company开发的一款多功能加密软件，其中包括了RSA非对称加解密、数字签名、AES对称加解密、哈希计算和隐写术等多种功能。这个软件旨在为用户提供一系列方便、安全和可靠的数据保护解决方案。

    这款加密软件是一款完全脱离网络的应用，这意味着在进行加密之前，数据不会离开您的设备，也不会被传输到任何其他地方。这种安全性确保了您的数据不会被黑客窃取或被其他人访问。因此，无论您是在家里还是在公共场所，您都可以使用这款软件来加密您的数据，确保它们的安全性和隐私性。
    
    软件会经常更新，获取最新版软件的途径：1. 作者的QQ：1147978107，2. 作者的github账号：https://github.com/CrownYou。您也可以通过我的联系方式，对软件未来的更新与发展提出您宝贵的建议。'''
        text.insert('end', word)

    @staticmethod
    def intro_rsa():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    RSA非对称加解密介绍
        
一、基本介绍
    RSA非对称加密中，每个人有两把密钥，一把是可以公开的公钥，另一把是只能有自己知道的私钥。使用公钥加密的信息，只有私钥才能解密。
    RSA算法的安全基础来源于超大数质因数分解极其困难。目前使用2048位以上的密钥，安全性非常高。
    
二、非对称加密通信的基本流程
    信息的发送方：
    发送方使用收件方的公钥对需要传输的文件进行加密，加密后的文件会保存在原文件所在的文件夹中。您可以使用本软件对任意文件进行加解密处理，没有格式限制。
    信息的接收方：
    接收方接收到文件后，使用自己的私钥解密，解密后的文件会保存在原文件所在的文件夹中。

三、非对称加密的特点
    RSA非对称加解密的速度十分缓慢，仅适合作为身份验证使用。为了提高加解密速度和安全性，强烈建议在RSA非对称加密的基础上结合使用DH密钥交换算法，为每一次会话创建一个临时的对称加密密钥，既提高安全性，又提高加解密的速度。'''
        text.insert('end', word)

    @staticmethod
    def intro_sign():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    RSA数字签名介绍

一、数字签名的基本介绍
    数字签名是只有信息的发送者才能产生的别人无法伪造的一段数字串，这段数字串同时也是对信息的发送者发送信息真实性的一个有效证明。\
由于这串字符串是通过信息发送者的私钥通过加密信息的摘要产生的，而别人无法获取信息发送者的私钥，所以这串字符串别人无法伪造，所以可以验证信息发送方的身份，以及信息是否被篡改。

二、数字签名的基本流程
    发送方生成数字签名：
    发送方输入自己的私钥和想要签名的文件或文字，程序会自动生成文件或文字的SHA-384摘要，再用私钥对摘要进行签名，生成一串字符串，这串字符串就是该文件或文字的数字签名。\
用户仅需将数字签名和原文件分开发送给信息的接收方即可。

    接收方验证数字签名：
    接收方需要输入信息发送方的公钥、原文件和原文件的数字签名，程序会使用信息发送方的公钥解密数字签名，并将其与原文件的SHA-384摘要进行比较，如果一致，则证明该签名来源于信息发送方，而没有被其他人伪造或篡改。'''
        text.insert('end', word)

    @staticmethod
    def intro_ecc():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    ECC非对称加密介绍
        
一、基本介绍
    ECC算法是一种基于椭圆曲线数学的公钥密码算法。它使用椭圆曲线上点的加法和减法运算来实现密钥协商和数字签名等操作。
    
二、技术原理
    ECC算法往往与ECDH密钥交换算法和AES对称加密算法结合使用，以实现更安全、更高效的通信。
    具体结合方式如下：
    1. Alice 和 Bob 各自生成自己的ECC公钥和私钥。
    2. Alice 用自己的私钥和 Bob 的公钥通过ECDH密钥交换算法生成一个AES对称加密密钥。
    Bob 也用自己的私钥和 Alice 的公钥通过ECDH密钥交换算法生成一个AES对称加密密钥。
    Alice 和 Bob 通过这种算法生成的AES对称加密密钥是一致的。
    3. 双方通过生成的AES对称加密密钥进行通讯
    
三、特点
    与RSA算法相比，ECC算法具有更高的安全性，并且密钥长度更短。ECC算法的计算速度更快，功耗更低，更适合移动设备等资源受限的设备。'''
        text.insert('end', word)

    @staticmethod
    def intro_ecc_sign():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    ECC数字签名介绍
        
    ECC数字签名的原理与RSA数字签名原理一致，均为私钥签名，公钥验签，都可以用来验证信息发送者的身份，只是使用的算法不一样，ECC速度更快，安全性更强。'''
        text.insert('end', word)

    @staticmethod
    def intro_aes():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    AES对称加解密介绍

一、基本介绍
    对称加密算法中，加密和解密共用一把密钥。本软件中有三种生成密钥的方式：
    1. 随机生成16字节（128位）或32字节（256位）长度的密钥。
    2. 通过信息摘要技术对用户输入的任意字符串或文件生成32字节的密钥。
    3. 通过DH密钥交换算法，可以让双方安全地协商出一个无法被第三者破解的临时会话密钥。
    前两种方式生成的密钥会保存在.aes后缀的文件中，第三种会生成一段字符串作为密钥，直接复制之后输入到加密界面的相应位置即可。
    
二、专业术语介绍
    （1）模式：本软件提供了两种AES加密的模式，一种是需要偏移量的ECB模式，另一种是不需要偏移量的CBC模式。
    （2）偏移量：您可以将偏移量理解为第二密钥。
    （3）填充方式：由于AES算法要求文件的大小必须为16字节的整数倍，所以需要对大小不符合要求的文件进行填充以达到16字节的整数倍。并且在解密时会自动剔除填充的字节。\
本软件提供了三种填充方式，建议使用pkcs7 padding模式，可以有效防止误删明文尾部的信息。'''
        text.insert('end', word)

    @staticmethod
    def intro_ckks():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    CKKS同态加密介绍

    CKKS（Cloud Key Encryption and Signing）是一种高效的同态加密方案，由 Gentry 等人于2017年提出。它支持浮点向量在密文空间的加减乘运算并保持同态，但只支持有限次乘法的运算。

    CKKS的主要特点:
 * 支持浮点计算：CKKS可以对密文中的浮点数进行加减乘运算，而无需解密。
 * 高效性：CKKS具有较高的计算效率，可以满足实际应用的需求。
 * 安全性：CKKS的安全性基于近似学习误差（RLWE）问题，该问题被认为是计算上困难的。

    CKKS的应用:
 * 安全多方计算：CKKS可以用於实现安全多方计算，使多个参与者可以在不共享数据的情况下共同进行计算。
 * 机器学习：CKKS可以用於实现隐私保护的机器学习，使模型训练和预测过程更加安全。
 * 云计算：CKKS可以用於保护云端数据的安全，使数据存储和处理更加安全可靠。

    CKKS的局限性:
 * 有限的乘法次数：CKKS只支持有限次乘法运算，如果乘法次数过多，则会导致精度下降。
 * 较大的密文长度：CKKS的密文长度较大，这可能会影响存储和传输效率。
    
    总体而言，CKKS是一种具有较强应用前景的同态加密方案。'''
        text.insert('end', word)

    @staticmethod
    def intro_hsv():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    获取像素点的HSV值/范围介绍

    一、HSV值介绍
    像素的HSV值是指该像素在HSV空间中的颜色表示。HSV是一种常用的颜色模型，它的名称代表着该模型中的三个分量：色调（Hue）、饱和度（Saturation）和亮度（Value）。
    在HSV空间中，色调表示颜色的基本属性，饱和度表示颜色的纯度或鲜艳度，亮度表示颜色的明暗程度。HSV空间中的每个像素都由这三个分量的值组成，通常用一个三元组 (H, S, V) 来表示。

    二、获取像素点的HSV值/范围的作用
    这个功能是为了logo振动法隐写术中的logo图片抠像功能而开发的辅助功能。您可以在这里获取需要抠像部分的HSV范围，然后将范围一键粘贴到logo振动法隐写术中的logo HSV范围中。'''
        text.insert('end', word)

    @staticmethod
    def intro_base64():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    base64转码器介绍

一、base64编码介绍
    这是一种能将6个二进制数据转化为1个可读字符的编码方式。由于6个二进制数据有2^6=64种可能，所以需要64种字符来表示这6个二进制数据。这就是base64编码名字的由来。
    由于电脑中存储的数据都可以用二进制来表示，所以使用base64编码也可以表示这些信息，并且可以使用可读的字符来进行传输。
    
二、base64转码器功能介绍
    它可以将文字转化为base64编码，并且可以将base64编码再转化为原文字，也可以将base64编码转为字节码。'''
        text.insert('end', word)

    @staticmethod
    def intro_anti():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    反查重+反和谐神器介绍

其中包括两项功能：
    1. 在文字中随机添加零宽度字符。这项功能会先将文字进行分词，然后在词语之间插入零宽度字符，这样可以避免一个词语内部被分开，导致word文档对词语标注红色下划线。但是要注意word文档中有显示零宽字符的功能，可以在‘文件’->‘选项’->‘显示’->‘显示所有格式标记’中打开该功能。
    
    2. 近形字替换。由于unicode字符集中有许多长相相近的文字，所以您可以通过这项功能将文字与它的双胞胎兄弟进行替换，这样可以避免文字被聊天平台和谐，以及降低查重率。'''
        text.insert('end', word)

    @staticmethod
    def intro_dh():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    DH密钥交换算法介绍

一、基本介绍
    DH密钥交换算法可以让会话双方可以在不告知对方密钥具体内容的情况下，安全地协商出本次临时会话的AES对称加密密钥。通过这种协商临时密钥的算法，可以避免长时间使用同一密钥造成的密钥泄露风险，并且可以有效防止以前的会话被破解（即前向保密性：即使攻击者获得了长期密钥，也无法推断出过去的会话密钥）。
    DH密钥交换算法具有前向保密性，是因为双方需要使用私有变量和可公开交换的随机数才能生成密钥，而私有变量在密钥生成完毕后就会被销毁。这种设计使得DH密钥交换算法能够抵御各种攻击，包括中间人攻击、重放攻击和窃听攻击等。即使有第三者破获了双方协商的内容，也无法获取协商之后生成的密钥。

二、具体流程
    1. （可跳过该步骤）双方创建并交换自己的RSA公钥，并将对方的公钥和自己的私钥拖入软件所提示的地方，该密钥会用于对第2步中对协商的内容进行加密。
    2. 会话发起人和会话参与人根据操作界面中的顺序和提示进行密钥协商，并生成临时会话的AES密钥。
    3. 将这次临时会话的密钥复制下来，之后就可以在对称加密功能界面上进行使用了。'''
        text.insert('end', word)

    @staticmethod
    def intro_rs():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    ReedSolomon纠错码介绍

一、基本介绍
    在数据传输中，信息有可能收到信道中噪声的影响，导致信息接收者无法正确读取信息发送者发送的信息，为了解决信息被噪声污染的问题，人们发明了纠错码。
    RS（ReedSolomon）纠错码是一种广泛使用的纠错编码技术，它可以在数字通信和存储领域中用来检测和纠正错误。它是由Reed和Solomon在1960年代提出的，被广泛应用于光盘、数字电视、调制解调器、卫星通信等领域。
    RS纠错码可以用于发现并纠正数据中的错误，也可用来恢复缺失的数据，但是如果需要使用RS纠错码来恢复缺失的数据，需要指定缺失的位置，所以软件中只提供了纠正错误的功能，而没有恢复缺失数据的功能。RS纠错码的纠正能力取决于纠错码的长度，可纠正错误的数量等于纠错码数量的二分之一。
    
二、RS纠错码的使用方式
    添加纠错码：软件中提供了对文字或文件添加纠错码的功能，它会将纠错码放置于原信息的最后。您可以设置纠错码的纠错能力，纠错能力越强，需要的纠错码就越多，请根据信道的噪声情况选择合适的纠错能力。需要注意的是，对文字进行纠错的纠错码的长度不能超过255。
    
    纠正并去除纠错码：在去除纠错码时，需要指定纠错码的长度。并且在获取需要纠错的信息时，宁可误读信息，也不要缺失信息。
    
    用户在测试文件纠错时可能会发现无法纠错的情况，这是因为文件在添加纠错码之后，会导致系统对该文件的编码方式理解错误，导致信息被重新解码和编码，使得纠错码错乱。如果想要进行测试，请使用python程序直接对文件中的字节进行修改。'''
        text.insert('end', word)

    @staticmethod
    def intro_hash():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    哈希算法介绍

一、基本介绍
    哈希算法也称为信息摘要算法，它是一种单向函数，任何信息被哈希算法处理过都会生成固定长度的字符串，这串字符串就是该信息的哈希值或信息摘要。\
这个过程不可逆，无法通过摘要还原出原信息。此外，只要信息中出现微小变化，该信息的哈希值也会出现巨大变化，这种特性可以用于识别文件是否被篡改。\
不同信息的哈希值通常不同，但是会存在极低的概率相同，这种情况称为碰撞。
    
二、哈希算法的应用
    哈希算法被广泛应用于区块链、数字签名、文件校验等领域。本软件中，您可以使用哈希算法校验两份文件是否相同。'''
        text.insert('end', word)

    @staticmethod
    def intro_hide():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    图片隐藏压缩包介绍
    
    这种方式可以在图片中隐藏.zip压缩包，您可以在任意一张图片中隐藏一个.zip压缩包，而不影响图片的正常显示。只要将图片的后缀改为.zip即可读取压缩包的内容，再将后缀改为原图片的后缀，则又可以把压缩包隐藏起来。\
部分解压软件在读取这样的.zip压缩包时可能会遇到一些问题，经过测试“2345好压”可以正确解压。

    这种方式似乎无法隐藏其他种类的压缩包，可能是由于解压软件无法准确识别其他种类压缩包的文件头，从而造成无法识别与解压。'''
        text.insert('end', word)

    @staticmethod
    def intro_zero_width_ste():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    零宽度字符隐写术介绍
        
    零宽度字符隐写术是一种利用零宽度字符来隐藏和传递秘密信息的技术。零宽度字符是一种不占用空间也不可见的Unicode字符，它们可以插入到普通文本中而不影响其显示，也可以被复制和粘贴。

    零宽度字符隐写术的基本思路是将先秘密信息用六种零宽度字符进行编码，然后将这些零宽度字符插入到到公开文本中的某一个位置。\
这样，只有知道正确的解码方式的人才能从公开文本中提取出秘密信息。

    零宽度字符隐写术不仅可以用在传输秘密信息，也可以用来保护文章的版权保护，您可以在文章中插入零宽度字符来保留创作的证据。
    
    注意：1.零宽度字符的隐写术会将所有零宽度字符放在第一个明文字符后面，而非均匀分布在所有明文字符之间。2.在传输含有零宽度字符的文字时，可以使用QQ、微信、txt文本文档等方式，但不要使用word文档，因为零宽度字符的格式无法被正确保留在word文档中。'''
        text.insert('end', word)

    @staticmethod
    def intro_qr_confuse():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    二维码图片混淆变换介绍

一、基本介绍
    这是一种帮助您隐秘传输二维码的功能，它可以使二维码图片绕过聊天平台的检测和审核，只有读取者从一个特定角度和距离进行扫码才能识别出二维码的内容。
    
二、混淆变换的原理
    它利用了近大远小的透视原理，将二维码进行一定的形变后展现在屏幕上，使得从正面看时无法被识别，但从设定的角度和距离看时则可以识别。\
此外，用户还可以选择一张背景图片用于将二维码隐藏于其中，二维码会根据背景图片的颜色对自身的颜色进行调整，使之在视觉上融入背景图片中。

三、使用时的注意点
    在对经过透视变换的二维码进行扫描时，可能会出现对不上焦，或者是一部分能对焦，另一部分不能对焦。这种情况下可以尝试把图片缩小一点，使得整张图片处于清晰对焦的区间内。'''
        text.insert('end', word)

    @staticmethod
    def intro_fourier():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    图片盲水印介绍

一、基本介绍
    该算法能够将文字或图片隐藏在一张载体图片中，优点是隐蔽性高，抗噪声能力强，缺点是隐写容量小，隐写及读取速度慢。
    
二、使用方法
    1. 隐藏信息：按照程序界面上的提示，输入载体图片与待隐藏的信息后，点击“隐写”按钮，程序运行完成后，结果会保存在载体图片所在文件夹中。注意：请记住程序界面上的信息提取密码。
    2. 读取信息：按照程序界面上的提示，输入带有隐藏信息的载体图片与信息提取密码后，点击“提取”按钮，程序运行完成后，即可看到隐藏的信息了。
    
三、注意点
    1. 一张图片能够隐藏的信息有上限，隐写容量一般非常小，隐藏信息的大小超过隐写容量后无法在读取时正确解读信息。
    2. 用图片隐藏图片时，载体图片最好选择大一点的图片，被隐藏的图片最好选择小一点的黑白图片。
    3. 经过测试，带有盲水印的图片在噪点、滤镜、图像部分被遮掩的情况下，可以较为完好地恢复出原信息，但是在缩放、裁剪、旋转的情况下，难以恢复出原信息。'''
        text.insert('end', word)

    @staticmethod
    def intro_video_logo():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    logo振动法隐写术说明

一、基本原理
    logo振动法隐写术是通过logo的微小振动来隐写信息的方式。程序会先将要隐写的信息进行 base64 编码，这种编码方式可以将信息用65种字符（每个字符的信息熵：65 bit）进行表示，\
而logo的一次振动有9种可能的方向（即中心点、上、左上、左、左下、下、右下、右、右上），那么两帧视频即可表示9*9，即81种信息（两次振动的信息熵：81 bit）大于一个base64字节的信息熵，\
所以程序采用了两帧视频隐写一个 base64字节的方式。
    在读取隐写的信息时，用户只要框选出视频中用于隐写信息的logo，程序会逐帧定位它的位置信息，将隐写的信息还原出来，之后，用户仅需将信息转码成自己需要的格式即可正常读取。

二、如何操作软件进行隐写
    首先点击菜单栏中的“隐写信息”选项，选择“使用logo振动法进行隐写”。
    在界面的左侧，用户可以输入要隐写信息，信息可以是文字或者文件，但要注意信息的大小不能超过隐写容量（隐写容量可以在界面的右侧看到）。\
如果要隐写的文件过大的话，可以一次隐写一小部分，只要在解读的时候按顺序拼接起来即可。
    在界面的右侧，用户在选择好视频和logo之后，就可以对logo和视频进行处理，包括logo放置的位置，logo的大小，抠图的方式，logo振动的幅度等。\
其中，logo的振动幅度最好大于等于2，太小的话，误差会很大。logo的位置可以通过在视频上点击确定，也可以自己手动输入logo中心点的坐标。处理好之后，程序会自动根据输入的参数，将信息隐写至logo的位置信息上。
    一个视频上可以通过放置多个logo，来隐写更多信息，但要注意logo之间不可过近，最好间隔10个像素点以上。

三、如何操作软件读取隐写的信息
    首先点击菜单栏中的“读取信息”选项，选择“读取logo振动法隐写的信息”。
    在界面的左侧，用户需要拖入识别的一个视频，点击“确定”后，请在弹出的画面中框选出需要识别的logo对象。框住的logo背景应该越少越好，因为框住的背景信息会影响到程序对logo位置的判断，\
最好是框选logo中与周围环境（你画的框框的外围10个像素点）最不一样的部分，这样可以提高识别的准确率。
    识别完成之后，可以点击“格式转换”按钮将识别到的 base64 编码转变为自己需要的格式。

四、该隐写术的特点
    优点：具有较强的抗噪声能力，能够在视频被添加滤镜或降低分辨率的情况下识别出logo的位置变化从而获取被隐写的信息。
    缺点：不抗抽帧，由于每一帧都隐写了信息，所以在抽帧的情况下会不可避免地造成信息损失。所以在压缩视频的时候尽量选择降低分辨率而不抽帧的压缩算法。'''
        text.insert('end', word)

    @staticmethod
    def intro_nearest_neighbor():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=28, font=mid_font)
        text.pack()
        word = '''    最近邻插值法图像隐写介绍
        
一、基本原理
    最近邻插值法是一种常用于图片缩小的方法。
    举例说明算法原理：如果要将一张大图片缩小成原来的十分之一，那么最近邻插值法只会保留处于行数是10的整数倍，以及列数是10的整数倍的像素点，其他像素点会被删掉。（这种解释并不是十分精确，但理解这层概念已经足够了）
    所以可以利用这种特点，将要隐藏的小图片放在这张大图片的行数是10的整数倍，以及列数是10的整数倍的像素点上，那么将大图片缩小为原来的十分之一时，就会把隐藏的图片显现出来。
    在软件中使用的方法是将小图片的每个像素均匀地散布在大图片的特定像素点上，在解密时输入小图片的尺寸（即解密密码）从而用最近邻插值法将大图片缩小成小图片的尺寸，即可看到小图片的信息了。
    
二、具体操作的注意事项
    1. 生物学研究表明，人眼对图像平滑（低频）区域的变换比较敏感，而对纹理（高频）区域的变换不太敏感。所以为了让隐写的像素点不易察觉，选作载体的图片最好具有纹理特征。
    2. 载体图片的高宽最好是隐藏图片高宽的5、7、9或11倍这样的奇数整数倍，这样解读时不会失真。否则的话，解读出来的图片会不清晰。
    3. 在解读隐写的信息时，也可以使用PhotoShop，只要使用最近邻插值法，并且输入正确的缩小后的尺寸信息即可。'''
        text.insert('end', word)

    @staticmethod
    def to_main():
        MyTools.initiation()
        _canvas = tk.Canvas(frm, height=752, width=1266)
        _canvas.create_image(0, 0, anchor='nw', image=image_file)
        _canvas.pack()

    @staticmethod
    def sponsor():
        MyTools.initiation()
        text = tk.Text(frm, width=96, height=12, font=mid_font)
        text.pack()
        word = '''    期待您的帮助
        
    感谢您对我的软件感兴趣。我的软件是一款创新性的工具，其中的很多功能是我经过不断学习和改进而得以研发出来的。\
它可以帮助您更加高效地完成信息安全相关的任务，从而提升生产力和效率。\
我花费了大量的时间和精力来开发和完善这个软件，它的功能已经受到许多用户的好评和反馈。

    但是，要继续将这个软件开发得更好，我需要您的支持。\
作为一个独立的开发者，我没有大型公司的资金和资源来支持我，但是我有技术实力和热情，可以保证不断地更新和改进这个软件，让它更加优秀。\
因此，我真诚地请求您的赞助，任何数额的赞助都可以帮助我更好地开发这个软件，让它更加完美。感谢您的支持！

    此外，如果您是一位从事信息安全相关的程序员，期待您与我合作开发这一款软件，我可以将我的开发成果与您分享。'''
        text.insert('end', word)
        window.update()
        sponsor_canvas = tk.Canvas(frm, width=1256, height=435)
        sponsor_canvas.pack(pady=10)
        sponsor_image = Image('system_resource/support.dll', 'png')
        sponsor_image_path = sponsor_image.decrypt
        sponsor_image_file = tk.PhotoImage(file=sponsor_image_path)
        sponsor_image.destroy()
        while True:
            try:
                sponsor_canvas.create_image(0, 0, anchor='nw', image=sponsor_image_file)
            except Exception:
                break
            window.update()
            time.sleep(0.1)


# 展示主界面图片
canvas = tk.Canvas(frm, width=1266, height=752)
canvas.pack()
main_image = Image('system_resource/main.dll', 'png')
main_path = main_image.decrypt
image_file = tk.PhotoImage(file=main_path)
main_image.destroy()
canvas.create_image(0, 0, anchor='nw', image=image_file)
# 准备图标图片供随时调用，只在程序结束时删除临时图标图片
icon_image = Image('system_resource/icon.dll', 'ico')
icon_path = icon_image.decrypt
window.iconbitmap(icon_path)  # 设定主界面的icon
# 给工程文件传参
myste.initiation(window, frm, mid_font, icon_path, colors, ind)
myenc.initiation(window, frm, mid_font, icon_path, colors, ind)
mybox.initiation(window, frm, mid_font, icon_path, colors, ind)
kit.initiation(frm, mid_font, icon_path, colors, ind)
# 部署菜单栏
menubar = tk.Menu(window)
# window.config(menu=menubar)  # 在登录后才能展示菜单栏

'''隐写信息部分'''
stega_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='隐写术', menu=stega_menu)

logo_submenu = tk.Menu(stega_menu, tearoff=0)
stega_menu.add_cascade(label='视频logo振动法', menu=logo_submenu, underline=0, font=mid_font)
logo_submenu.add_command(label='隐写信息', command=Functions.video_logo, font=mid_font)
logo_submenu.add_command(label='读取信息', command=Functions.read_video_logo, font=mid_font)

stega_menu.add_command(label='最近邻插值法图像隐写', command=Functions.nearest_neighbor, font=mid_font)
stega_menu.add_command(label='图片隐藏.zip压缩包', command=Functions.hide_zip, font=mid_font)
stega_menu.add_command(label='零宽度字符隐写术', command=Functions.zero_width_ste, font=mid_font)

qr_confuse_submenu = tk.Menu(stega_menu, tearoff=0)
stega_menu.add_cascade(label='二维码图片混淆变换', menu=qr_confuse_submenu, underline=0, font=mid_font)
qr_confuse_submenu.add_command(label='第一步：逆透视变换', command=Functions.confuse_qr_code, font=mid_font)
qr_confuse_submenu.add_command(label='第二步：藏于载体图片', command=Functions.hide_qr_code, font=mid_font)

fourier_ste_submenu = tk.Menu(stega_menu, tearoff=0)
stega_menu.add_cascade(label='图片盲水印', menu=fourier_ste_submenu, underline=0, font=mid_font)
fourier_ste_submenu.add_command(label='图片隐写/读取文字', command=Functions.fourier_word, font=mid_font)
fourier_ste_submenu.add_command(label='图片隐写/读取图片', command=Functions.fourier_pic, font=mid_font)

'''工具箱部分'''
tools_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='工具箱', menu=tools_menu)
tools_menu.add_command(label='获取像素点的HSV值/范围', command=Functions.get_hsv_value, font=mid_font)
tools_menu.add_command(label='强密码生成器', command=Functions.generate_random_char, font=mid_font)
tools_menu.add_command(label='base64转码器', command=Functions.base64converter, font=mid_font)
tools_menu.add_command(label='反查重+反和谐神器', command=Functions.against_duplicate_check, font=mid_font)

rs_menu = tk.Menu(tools_menu, tearoff=0)
tools_menu.add_cascade(label='ReedSolomon纠错码', menu=rs_menu, underline=0, font=mid_font)
rs_menu.add_command(label='纠错文字', command=Functions.rs_code_word, font=mid_font)
rs_menu.add_command(label='纠错文件', command=Functions.rs_code_file, font=mid_font)

'''非对称加密与签名部分'''
asymmetric_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='非对称加密与签名', menu=asymmetric_menu)

'''RSA部分'''
rsa_menu = tk.Menu(asymmetric_menu, tearoff=0)
asymmetric_menu.add_cascade(label='RSA算法', menu=rsa_menu, underline=0, font=mid_font)
rsa_menu.add_command(label='创建RSA密钥对', command=Functions.create_rsa_key, font=mid_font)
rsa_menu.add_command(label='设置私钥使用密码', command=Functions.set_pwd_of_rsa_privkey, font=mid_font)
rsa_menu.add_command(label='文字加解密', command=Functions.rsa_word, font=mid_font)
rsa_menu.add_command(label='文件（夹）加解密', command=Functions.rsa_file, font=mid_font)
rsa_menu.add_command(label='数字签名与验签', command=Functions.rsa_sign_and_verify, font=mid_font)

'''ECC部分'''
ecc_menu = tk.Menu(asymmetric_menu, tearoff=0)
asymmetric_menu.add_cascade(label='ECC算法（推荐）', menu=ecc_menu, underline=0, font=mid_font)
ecc_menu.add_command(label='创建ECC密钥对', command=Functions.create_ecc_key, font=mid_font)
ecc_menu.add_command(label='设置私钥使用密码', command=Functions.set_pwd_of_ecc_privkey, font=mid_font)
ecc_menu.add_command(label='文字加解密', command=Functions.ecc_word, font=mid_font)
ecc_menu.add_command(label='文件（夹）加解密', command=Functions.ecc_file, font=mid_font)
ecc_menu.add_command(label='数字签名与验签', command=Functions.ecc_sign_and_verify, font=mid_font)

'''AES部分'''
aes_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='AES对称加解密', menu=aes_menu)

aes_key_submenu = tk.Menu(aes_menu, tearoff=0)
aes_menu.add_cascade(label='创建AES密钥', menu=aes_key_submenu, underline=0, font=mid_font)
aes_key_submenu.add_command(label='随机生成128位', command=Functions.create_aes_key_16, font=mid_font)
aes_key_submenu.add_command(label='随机生成256位', command=Functions.create_aes_key_32, font=mid_font)
aes_key_submenu.add_command(label='通过信息摘要创建', command=Functions.create_aes_key_by_hash_digest, font=mid_font)
aes_key_submenu.add_command(label='通过DH密钥交换算法创建', command=Functions.dh_exchange, font=mid_font)

aes_menu.add_command(label='文字加解密', command=Functions.aes_word, font=mid_font)
aes_menu.add_command(label='文件（夹）加解密', command=Functions.aes_file, font=mid_font)

'''CKKS同态加密部分'''
ckks_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='CKKS同态加密', menu=ckks_menu)
ckks_menu.add_command(label='创建CKKS密钥', command=Functions.create_ckks_key, font=mid_font)
ckks_menu.add_command(label='设置私钥使用密码', command=Functions.set_pwd_of_ckks_privkey, font=mid_font)
ckks_menu.add_command(label='文字同态加密', command=Functions.ckks_word, font=mid_font)

'''哈希部分'''
hash_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='哈希计算', menu=hash_menu)

hash_menu.add_command(label='哈希校验文字', command=Functions.hash_word, font=mid_font)
hash_menu.add_command(label='哈希校验文件', command=Functions.hash_file, font=mid_font)

'''帮助部分'''
intro_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='帮助', menu=intro_menu)
intro_menu.add_command(label='期待您的帮助', command=Functions.sponsor, font=mid_font)
intro_menu.add_command(label='软件基本介绍', command=Functions.intro, font=mid_font)

intro_ste_submenu = tk.Menu(intro_menu, tearoff=0)
intro_menu.add_cascade(label='隐写术介绍', menu=intro_ste_submenu, underline=0, font=mid_font)
intro_ste_submenu.add_command(label='logo振动法隐写术介绍', command=Functions.intro_video_logo, font=mid_font)
intro_ste_submenu.add_command(label='最近邻插值法图像隐写介绍', command=Functions.intro_nearest_neighbor, font=mid_font)
intro_ste_submenu.add_command(label='图片隐藏.zip压缩包介绍', command=Functions.intro_hide, font=mid_font)
intro_ste_submenu.add_command(label='零宽度字符隐写术介绍', command=Functions.intro_zero_width_ste, font=mid_font)
intro_ste_submenu.add_command(label='二维码图片混淆变换介绍', command=Functions.intro_qr_confuse, font=mid_font)
intro_ste_submenu.add_command(label='图片盲水印介绍', command=Functions.intro_fourier, font=mid_font)

toolbox_submenu = tk.Menu(intro_menu, tearoff=0)
intro_menu.add_cascade(label='工具箱介绍', menu=toolbox_submenu, underline=0, font=mid_font)
toolbox_submenu.add_command(label='获取像素点的HSV值/范围介绍', command=Functions.intro_hsv, font=mid_font)
toolbox_submenu.add_command(label='base64转码器介绍', command=Functions.intro_base64, font=mid_font)
toolbox_submenu.add_command(label='反查重+反和谐神器介绍', command=Functions.intro_anti, font=mid_font)
toolbox_submenu.add_command(label='ReedSolomon纠错码介绍', command=Functions.intro_rs, font=mid_font)

intro_enc_submenu = tk.Menu(intro_menu, tearoff=0)
intro_menu.add_cascade(label='加密功能介绍', menu=intro_enc_submenu, underline=0, font=mid_font)
intro_enc_submenu.add_command(label='RSA非对称加解密介绍', command=Functions.intro_rsa, font=mid_font)
intro_enc_submenu.add_command(label='RSA数字签名介绍', command=Functions.intro_sign, font=mid_font)
intro_enc_submenu.add_command(label='ECC非对称加解密介绍', command=Functions.intro_ecc, font=mid_font)
intro_enc_submenu.add_command(label='ECC数字签名介绍', command=Functions.intro_ecc_sign, font=mid_font)
intro_enc_submenu.add_command(label='DH密钥交换算法介绍', command=Functions.intro_dh, font=mid_font)
intro_enc_submenu.add_command(label='AES对称加解密介绍', command=Functions.intro_aes, font=mid_font)
intro_enc_submenu.add_command(label='CKKS同态加密介绍', command=Functions.intro_ckks, font=mid_font)

intro_menu.add_command(label='哈希算法介绍', command=Functions.intro_hash, font=mid_font)
intro_menu.add_command(label='返回主界面', command=Functions.to_main, font=mid_font)

login_button = tk.Button(frm, text='登录', fg='green', font=('Noto Sans Mono', 18), command=MyTools.login)
login_button.place(x=1118, y=596, anchor='center')
window.protocol("WM_DELETE_WINDOW", MyTools.on_closing)
window.mainloop()
