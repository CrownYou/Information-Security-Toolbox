# -*- coding: utf-8 -*-
import base64
import tkinter as tk
from tkinter import messagebox
from random import randint, choice
import threading
import cv2
import numpy as np
import math
from math import ceil
from math import floor
import os
import shutil
import pyautogui as auto
import pyperclip
from Crypto.PublicKey import RSA
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Hash import SHA384
import hashlib
import string

frm = mid_font = icon_path = colors = ind = ...


def initiation(_frm, _mid_font, _icon_path, _colors, _ind):
    global frm, mid_font, icon_path, colors, ind
    frm = _frm
    mid_font = _mid_font
    icon_path = _icon_path
    colors = _colors
    ind = _ind


class ZebrizedFile:
    '''
    定义一个类，对被加密的文件进行分隔，以及读取文件头部的参数信息
    '''

    def __init__(self, file_path, outfile_path):
        self.file_path = file_path  # 密文的地址
        self.outfile_path = outfile_path  # 解密后的明文的地址

    @staticmethod
    def __rsa_decrypt(outfile, infile, black_width, privkey, length_of_one_unit_cipher_text: int):
        processed_width = 0
        while processed_width < black_width:
            block_enc = infile.read(length_of_one_unit_cipher_text)  # 从密文文件中读取1单位密文
            if not block_enc:  # 如果已经读空了，就退出循环
                break
            outfile.write(privkey.decrypt(block_enc, 0))
            processed_width += length_of_one_unit_cipher_text

    @staticmethod
    def __aes_decrypt(outfile, infile, black_width, aes, padding):
        processed_width = 0
        block = infile.read(16)
        while True:
            de_text = aes.decrypt(block)  # 先把当前的16字节密文解密
            processed_width += 16  # 记录一下：又处理了16字节的密文
            if processed_width < black_width:  # 如果此时处理的密文还没达到要求
                block = infile.read(16)  # 就继续读取下一个16字节密文
                if not block:  # 如果下一个16字节的信息是空的
                    outfile.write(Tools.de_padding(de_text, padding))  # 那么写入这次解密出来的信息后就退出
                    break
            else:  # 如果处理的长度达标了，那么写入这次解密出来的信息后也要退出
                outfile.write(Tools.de_padding(de_text, padding))
                break
            # 只有在下一个16字节不为空且处理长度没达到black_width的时候，才能继续循环
            outfile.write(de_text)

    def decrypt(self, mode='rsa', privkey_cipher=None, aes=None, padding=None):
        '''
        读取文件头部的参数信息，并进行解密
        这个函数里的报错不要捕获，直接报错即可
        main_body||suffix  # 主体和尾部参数之间有两根‘|’分割
        suffix: Auto, begin| black_width| white_width| number| end[| length_of_one_unit_cipher_text]
        如果是被rsa加密的文件，则有第六个参数：length_of_one_unit_cipher_text，代表一单位的明文信息，被加密成了多长的密文信息
        如果是被aes加密的文件，则只有前面五个参数
        '''
        with open(self.file_path, 'rb+') as f:  # 第一步读取suffix，并把它从密文文件中截断
            f.seek(-13, 2)  # 可以从倒数第13位开始往前找
            count = 0
            while True:
                first = f.read(1)
                second = f.read(1)
                if first == b'|' and second == b'|':  # 去找b'||'分隔符
                    suffix = f.read()
                    f.seek(-len(suffix) - 2, 2)  # 找到后需要截掉后缀
                    f.truncate()  # 注意：不论文件是否解密失败，这里截断的suffix，最后都要重新写入密文末尾
                    break
                f.seek(-3, 1)  # 没找到分隔符的话，就把光标从当前位置往前挪3位
                count += 1
                if count > 200:  # 如果找了200位了还没找到b'||'，就报错
                    raise IOError('没找到suffix')

        # 此时已经获取了suffix，下面要根据参数进行解密
        if suffix[:4] == b'Auto':  # 如果开头四个字符是'Auto'，则说明参数信息可以以明文方式读取
            try:
                parameters = [int(i) for i in suffix[4:].decode('utf-8').split('|')]
            except Exception:
                with open(self.file_path, 'ab') as f:
                    f.write(b'||' + suffix)
                raise IOError('斑马线参数不正确')
            if mode == 'rsa' and len(parameters) == 6:
                print("解密的 begin, black_width, white_width, number, end, length_of_one_unit_cipher_text 分别为：")
                print(parameters)
                begin, black_width, white_width, number, end, length_of_one_unit_cipher_text = parameters
                with open(self.outfile_path, 'wb') as outfile, open(self.file_path, 'ab+') as infile:
                    try:
                        infile.seek(0, 0)  # 由于是ab+模式打开infile，所以需要先将光标移动到开头
                        Tools.read_and_write(infile, outfile, begin)  # 写入开头
                        if number == 1:
                            ZebrizedFile.__rsa_decrypt(outfile, infile, black_width, privkey_cipher,
                                                       length_of_one_unit_cipher_text)
                            Tools.read_and_write(infile, outfile, white_width)
                        else:
                            for i in range(1, 2 * number):  # 范围是 [1, 2 * number - 1]
                                if i % 2 == 1:
                                    ZebrizedFile.__rsa_decrypt(outfile, infile, black_width, privkey_cipher,
                                                               length_of_one_unit_cipher_text)
                                else:
                                    Tools.read_and_write(infile, outfile, white_width)
                        Tools.read_and_write(infile, outfile, end)
                        infile.seek(0, 2)  # 把光标移动到文件末尾
                        infile.write(b'||' + suffix)  # 如果解密成功，还要把密文文件恢复
                    except Exception:
                        infile.seek(0, 2)
                        infile.write(b'||' + suffix)  # 如果解密错误，还要把suffix，写回原密文文件，并报错
                        raise IOError('解密失败，原文件已恢复')
            elif mode == 'aes' and len(parameters) == 5:
                begin, black_width, white_width, number, end = parameters
                with open(self.outfile_path, 'wb') as outfile, open(self.file_path, 'ab+') as infile:
                    try:
                        infile.seek(0, 0)
                        Tools.read_and_write(infile, outfile, begin)
                        if number == 1:  # 当黑线数量等于1时，白线和黑线数量相等
                            if white_width + end > 0:  # 当白线长度和末尾明文的长度大于0时，使用no padding进行解密
                                ZebrizedFile.__aes_decrypt(outfile, infile, black_width, aes, 'no padding')
                                Tools.read_and_write(infile, outfile, white_width)
                            else:  # 当白线和末尾明文的长度为0时，才使用设定的padding模式进行解密
                                ZebrizedFile.__aes_decrypt(outfile, infile, black_width, aes, padding)
                                # 由于白线的长度为0，所以不需要写入了
                        else:  # 当黑线数量大于1时，白线数量等于黑线数量减一
                            for i in range(1, 2 * number):
                                if i % 2 == 1:  # i 为奇数，代表黑线
                                    if (i == 2 * number - 1) and end == 0:
                                        # 末尾明文的长度为0，且为最后一根黑线时，解密使用用户设定的padding模式
                                        ZebrizedFile.__aes_decrypt(outfile, infile, black_width, aes, padding)
                                    else:  # 其他的黑线解密时使用 no padding 模式，防止误删
                                        ZebrizedFile.__aes_decrypt(outfile, infile, black_width, aes, 'no padding')
                                else:  # i 为偶数，代表白线
                                    Tools.read_and_write(infile, outfile, white_width)
                        Tools.read_and_write(infile, outfile, end)
                        infile.seek(0, 2)
                        infile.write(b'||' + suffix)  # 如果解密成功，还要把密文文件恢复
                    except Exception:
                        infile.seek(0, 2)
                        infile.write(b'||' + suffix)
                        raise IOError('解密失败，原文件已恢复')
            else:  # 如果不是的话，就需要把suffix重新写回去，并报错
                with open(self.file_path, 'ab') as f:
                    f.write(b'||' + suffix)
                raise IOError('不是一个正确的斑马线密文')
        else:
            with open(self.file_path, 'ab') as f:
                f.write(b'||' + suffix)
            raise IOError('明文文件不是ZebrizedFile')


class OriginFile:
    '''定义一个类，用作斑马线加密法的文件分割，加密。
    如果文件路径不存在会报错'''

    def __init__(self, infile_path, outfile_path, begin: str, width: int, number: int, end: str):
        self.infile_path = infile_path
        self.outfile_path = outfile_path
        self.begin = begin  # str
        self.width = width  # int
        self.number = number  # int
        self.end = end  # str
        self.size = os.path.getsize(infile_path)  # 获取文件的大小（单位：字节）

    @staticmethod
    def __rsa_encrypt(outfile, infile, black_width, pubkey_cipher):
        # 返回两个值，一个是：加密后的密文的长度（new_black_width）
        # 另一个是：一单位明文加密后变成了多长的密文（length_of_one_unit_cipher_text）
        new_black_width, processed_width = 0, 0  # 一个代表加密后的密文长度，一个代表加密了的明文长度
        block_enc1 = pubkey_cipher.encrypt(infile.read(112))
        outfile.write(block_enc1)
        new_black_width += len(block_enc1)
        processed_width += 112
        length_of_one_unit_cipher_text = len(block_enc1)
        while processed_width < black_width:
            block = infile.read(112)
            if not block:  # 如果infile已经读完了，就要结束循环
                break
            block_enc = pubkey_cipher.encrypt(block)
            outfile.write(block_enc)
            new_black_width += len(block_enc)
            processed_width += 112
        return new_black_width, length_of_one_unit_cipher_text

    @staticmethod
    def __aes_encrypt(outfile, infile, black_width, aes, padding='pkcs7 padding'):
        # 这里的 aes 必须是处理好的 aes 密钥， 需要已经设置好了模式，偏移量
        processed_width = 0
        while processed_width < black_width:
            block = infile.read(16)
            if not block:  # 如果block为空说明infile已经读完了，就停止读取
                break
            elif len(block) < 16:  # 只有在block的长度在（0，16）范围内时才填充
                if padding == 'zero padding':
                    block = Tools.add_to_16(block)
                elif padding == 'iso 10126 padding':
                    block = Tools.iso_padding(block)
                elif padding == 'pkcs7 padding':
                    block = Tools.pkcs7_padding(block)
                outfile.write(aes.encrypt(block))
                break
            outfile.write(aes.encrypt(block))
            processed_width += 16

    def tag(self, mode='rsa') -> list:
        '''
        在加密前，对用户的输入进行初步处理
        :return: [头部长度: int, 黑线长度: int, 白线长度: int, 黑线数量: int, 尾部长度: int]  # 单位都是 bytes
        '''
        print(f'原文件的总大小为：{self.size}，下面开始进行划分：')
        # 第一步将百分位的位置转化为绝对值（int）
        if '%' in self.begin and '%' in self.end:
            begin = round((float(self.begin.rstrip('%')) / 100) * self.size)
            end = round((float(self.end.rstrip('%')) / 100) * self.size)
        else:
            begin = round(1024 * float(self.begin))
            end = round(1024 * float(self.end))
            begin = begin if begin >= 0 else self.size + begin  # 如果用户输入的位置为负数，代表倒着数的，这里把它转为正数
            end = end if end > 0 else self.size + end  # 如果用户输入的末尾位置为0，则代表-0（即 self.size）
            begin = begin if begin >= 0 else 0  # 如果转正后还是为负，就设为0
            end = end if end >= 0 else 0
        print(f'第一步中互换前的 begin: {begin}, end: {end}')
        # 注意：上面计算出的end值代表最后一根黑线的末尾位置（在第三步会变为尾部的大小）
        # 如果begin > end，就互换
        if begin > end:
            begin, end = end, begin
        print(f'第一步中互换后的 begin: {begin}, end: {end}')
        # 还需要比较起始位置、末尾位置和文件大小的关系，不能让设定的位置比文件大小还大
        begin = begin if begin < self.size else 0
        end = end if end <= self.size else self.size
        print(f'经过与文件大小的比较，最终确定的 begin: {begin}, end: {end}')
        # 第二步，确定黑线的宽度
        if mode == 'rsa':
            black_width = self.width * 112
        elif mode == 'aes':
            try:
                with open("system_resource/settings.dll", 'r', encoding='utf-8') as f:
                    count = eval(f.read())  # 读出来的count要再乘以16才是正确的一单位的长度
                    assert isinstance(count, int) and count >= 1
            except Exception:
                count = 7
            black_width = self.width * count * 16
        print(f'第二步中黑线的宽度 black_width: {black_width}')
        number = self.number
        print(f'黑线的根数 number: {number}')
        # 第三步，确定白线的宽度
        # 在计算白线的宽度时，要特别注意黑线的根数为1的情况（黑线的根数的取值范围为：[1, 正无穷)）
        white_width = floor(
            (end - begin - number * black_width) / (number - 1)) if number > 1 else end - begin - black_width
        # 要特别注意计算白线的宽度千万不能向上取整！因为如果白线的数量很多，可能导致最后一根黑线都被挤出去了，宁可让末尾大一点
        print(f'第三步中白线宽度的初始值 white_width: {white_width}')
        if white_width < 0:  # 如果白线宽度为负，则代表斑马线中没有白线，斑马线主体全部由黑线组成
            black_width = ceil((end - begin) / 112) * 112  # 向上取整，以防取到0
            number = 1
            white_width = 0
        print(f'第三步中处理后的白线宽度 white_width: {white_width}')
        # 第四步，重新确定末尾的大小（注意：这里的end的含义变为了尾部的大小）
        # 还是要注意number为1的情况（number 为 1，白线和黑线的数量都为1）
        end = self.size - begin - black_width * number - white_width * (
                    number - 1) if number > 1 else self.size - begin - black_width - white_width
        print(f'第四步中末尾大小的初始值 end: {end}')
        end = end if end > 0 else 0
        print(f'第四步中处理后的末尾大小 end: {end}')
        # 第五步，返回标签
        print(f"begin: {begin}, black_width: {black_width}, white_width: {white_width}, number: {number}, end: {end}")
        return [begin, black_width, white_width, number, end]

    @staticmethod
    def write_suffix(outfile, begin: int, black_width: int, white_width: int, number: int, end: int,
                     length_of_one_unit_cipher_text=None):
        # 在文件尾部写入参数信息
        # 如果是rsa加密则还需要在参数信息部分写入一单位（112字节）的明文被加密成了多长的密文
        suffix = '|'.join([str(begin), str(black_width), str(white_width), str(number), str(end)])
        suffix = suffix if length_of_one_unit_cipher_text is None else "|".join(
            [suffix, str(length_of_one_unit_cipher_text)])
        outfile.write(bytes('Auto' + suffix, encoding='utf-8'))

    def encrypt(self, *, mode='rsa', pubkey_cipher=None, aes=None, padding=None):
        '''
        加密后的结果为：
        begin_content, black_content, white_content, ..., black_content, end_content||Auto, begin|black_width|white_width|number|end[|length_of_one_unit_cipher_text]
        小括号内的代表被加密
        中括号内的是rsa加密特有的参数，代表一单位明文被加密后变成了多长的密文
        :param mode: 'rsa' 或者 'aes'
        :param pubkey_cipher: rsa 密钥
        :param aes: 加工好的 aes 密钥
        :param padding: 'pkcs7 padding'， 'iso 10126 padding'，'zero padding'
        :return: 无返回值，加密后的结果在 self.outfile_path 中
        '''
        # 第一步，加密前获取用户输入的参数（被加工过的）
        begin, black_width, white_width, number, end = self.tag(mode)
        with open(self.infile_path, 'rb') as infile, open(self.outfile_path, 'wb') as outfile:
            # 第二步，要写入头部的文件（begin_content)，头部文件的大小为begin
            Tools.read_and_write(infile, outfile, begin)
            # 第三步，写入斑马线的主体
            if number > 1:  # 如果黑线数量 > 1，那么白线的数量等于黑线数量减1
                for i in range(1, 2 * number):  # 白线加黑线是从第 1 条到第 2 * number - 1 条的
                    # i 为奇数时，代表黑线，i 为偶数时，代表白线
                    if i % 2 == 1:
                        if mode == 'aes':
                            OriginFile.__aes_encrypt(outfile, infile, black_width, aes, padding)
                        elif mode == 'rsa':
                            # rsa模式在加密第一根黑线的时候，要计算一下 length_of_one_unit_cipher_text 和 new_black_width
                            if i == 1:
                                new_black_width, length_of_one_unit_cipher_text = OriginFile.__rsa_encrypt(outfile,
                                                                                                           infile,
                                                                                                           black_width,
                                                                                                           pubkey_cipher)
                            else:
                                OriginFile.__rsa_encrypt(outfile, infile, black_width, pubkey_cipher)
                    else:  # 为白线时，将明文直接写入密文中即可
                        Tools.read_and_write(infile, outfile, white_width)
            else:  # 如果黑线数量为1时，白线的数量等于黑线的数量，都为1
                if mode == 'rsa':
                    new_black_width, length_of_one_unit_cipher_text = OriginFile.__rsa_encrypt(outfile, infile,
                                                                                               black_width,
                                                                                               pubkey_cipher)
                elif mode == 'aes':
                    OriginFile.__aes_encrypt(outfile, infile, black_width, aes, padding)
                Tools.read_and_write(infile, outfile, white_width)
            # 第四步，读取完斑马线后，再写入文件末尾的明文
            Tools.read_and_write(infile, outfile, end)
            # 最后一步，写完文件末尾的明文后，还要再写入参数信息
            outfile.write(b'||')
            if mode == 'rsa':
                print("加密后的参数信息变为：")
                print(
                    f"begin: {begin}, new_black_width: {new_black_width}, white_width: {white_width}, number: {number}, end: {end}, length_of_one_unit_cipher_text: {length_of_one_unit_cipher_text}")
                OriginFile.write_suffix(outfile, begin, new_black_width, white_width, number, end,
                                        length_of_one_unit_cipher_text)
            elif mode == 'aes':
                print("加密后的参数信息变为：")
                print(
                    f"begin: {begin}, black_width: {black_width}, white_width: {white_width}, number: {number}, end: {end}")
                OriginFile.write_suffix(outfile, begin, black_width, white_width, number, end)


class Tools:
    base64dic = {'0': [(0, -1), (0, -1)], '1': [(0, -1), (-1, -1)], '2': [(0, -1), (-1, 0)],
                 '3': [(0, -1), (-1, 1)], '4': [(0, -1), (0, 1)], '5': [(0, -1), (1, 1)], '6': [(0, -1), (1, 0)],
                 '7': [(0, -1), (1, -1)], '8': [(-1, -1), (0, -1)], '9': [(-1, -1), (-1, -1)],
                 'A': [(-1, -1), (-1, 0)], 'B': [(-1, -1), (-1, 1)], 'C': [(-1, -1), (0, 1)],
                 'D': [(-1, -1), (1, 1)], 'E': [(-1, -1), (1, 0)], 'F': [(-1, -1), (1, -1)],
                 'G': [(-1, 0), (0, -1)], 'H': [(-1, 0), (-1, -1)], 'I': [(-1, 0), (-1, 0)],
                 'J': [(-1, 0), (-1, 1)], 'K': [(-1, 0), (0, 1)], 'L': [(-1, 0), (1, 1)], 'M': [(-1, 0), (1, 0)],
                 'N': [(-1, 0), (1, -1)], 'O': [(-1, 1), (0, -1)], 'P': [(-1, 1), (-1, -1)],
                 'Q': [(-1, 1), (-1, 0)], 'R': [(-1, 1), (-1, 1)], 'S': [(-1, 1), (0, 1)], 'T': [(-1, 1), (1, 1)],
                 'U': [(-1, 1), (1, 0)], 'V': [(-1, 1), (1, -1)], 'W': [(0, 1), (0, -1)], 'X': [(0, 1), (-1, -1)],
                 'Y': [(0, 1), (-1, 0)], 'Z': [(0, 1), (-1, 1)], 'a': [(0, 1), (0, 1)], 'b': [(0, 1), (1, 1)],
                 'c': [(0, 1), (1, 0)], 'd': [(0, 1), (1, -1)], 'e': [(1, 1), (0, -1)], 'f': [(1, 1), (-1, -1)],
                 'g': [(1, 1), (-1, 0)], 'h': [(1, 1), (-1, 1)], 'i': [(1, 1), (0, 1)], 'j': [(1, 1), (1, 1)],
                 'k': [(1, 1), (1, 0)], 'l': [(1, 1), (1, -1)], 'm': [(1, 0), (0, -1)], 'n': [(1, 0), (-1, -1)],
                 'o': [(1, 0), (-1, 0)], 'p': [(1, 0), (-1, 1)], 'q': [(1, 0), (0, 1)], 'r': [(1, 0), (1, 1)],
                 's': [(1, 0), (1, 0)], 't': [(1, 0), (1, -1)], 'u': [(1, -1), (0, -1)], 'v': [(1, -1), (-1, -1)],
                 'w': [(1, -1), (-1, 0)], 'x': [(1, -1), (-1, 1)], 'y': [(1, -1), (0, 1)], 'z': [(1, -1), (1, 1)],
                 '+': [(1, -1), (1, 0)], '/': [(1, -1), (1, -1)], '=': [(0, 0), (1, 1)]}

    @staticmethod
    def clean_all_widget(frame: tk.Frame):
        for widget in frame.winfo_children():
            widget.destroy()

    @staticmethod
    def dragged_files(files, entry):
        file = files[0].decode("GBK")  # 用户拖入多个文件时，只取第一个
        entry.delete(0, 'end')
        entry.insert('end', file)

    @staticmethod
    def reset(text_or_entry):
        if isinstance(text_or_entry, tk.Text):
            text_or_entry.delete(1.0, 'end')
        if isinstance(text_or_entry, tk.Entry):
            text_or_entry.delete(0, 'end')

    @staticmethod
    def run_as_thread(func):  # 装饰器，让函数运行时另开一个线程
        def wrapper(*args, **kwargs):
            t = threading.Thread(target=func, args=args, kwargs=kwargs)
            t.setDaemon(True)
            t.start()
        return wrapper

    @staticmethod
    def process_logo_img_according_to_parameters(logo_img, zoom: float, *, threshold=None, origin=False,
                                                 adaptive_method=None, threshold_type=None, block_size=None, C=None,
                                                 Otsus=False, bright=True, lower_threshold=None, upper_threshold=None):
        '''根据参数把logo图片的背景转为黑色，返回logo_fg和用于处理视频帧的mask'''
        # 首先对logo进行缩放
        if zoom <= 1.0:
            resized_logo_img = cv2.resize(logo_img, None, fx=zoom, fy=zoom, interpolation=cv2.INTER_AREA)
        else:
            resized_logo_img = cv2.resize(logo_img, None, fx=zoom, fy=zoom, interpolation=cv2.INTER_CUBIC)
        if origin:
            logo_rows, logo_cols, _ = resized_logo_img.shape
            mask = np.zeros(shape=(logo_rows, logo_cols), dtype=np.uint8)
            return resized_logo_img, mask
        if threshold is not None:
            logo2gray = cv2.cvtColor(resized_logo_img, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(logo2gray, threshold, 255, cv2.THRESH_BINARY)
        elif adaptive_method is not None and threshold_type is not None and block_size is not None and C is not None:
            logo2gray = cv2.cvtColor(resized_logo_img, cv2.COLOR_BGR2GRAY)
            mask = cv2.adaptiveThreshold(logo2gray, 255, adaptive_method, threshold_type, block_size, C)
        elif Otsus:
            logo2gray = cv2.cvtColor(resized_logo_img, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(logo2gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            if bright:
                mask = cv2.bitwise_not(mask)
        elif lower_threshold is not None and upper_threshold is not None:
            logo2hsv = cv2.cvtColor(resized_logo_img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(logo2hsv, lower_threshold, upper_threshold)
            mask = cv2.bitwise_not(mask)
        mask_inv = cv2.bitwise_not(mask)
        logo_fg = cv2.bitwise_and(resized_logo_img, resized_logo_img, mask=mask_inv)
        return logo_fg, mask

    @staticmethod
    def process_roi(bg_cols, logo_cols, logo_center_x, bg_rows, logo_rows, logo_center_y):
        # 特别注意我设定的logo中心点左边的宽度是ceil(logo_cols/2)，右边的宽度是floor(logo_cols/2);
        # 上边的高度是ceil(logo_rows/2)，下边的高度是floor(logo_rows/2)
        if bg_cols - math.floor(logo_cols / 2) < logo_center_x < math.ceil(logo_cols / 2):
            logo_start_x = math.ceil(logo_cols / 2) - logo_center_x
            logo_end_x = logo_start_x + bg_cols
            roi_start_x = 0
            roi_end_x = bg_cols
            # print('logo同时超出背景左右边界')
        elif logo_center_x < math.ceil(logo_cols / 2):
            logo_start_x = math.ceil(logo_cols / 2) - logo_center_x
            logo_end_x = logo_cols
            roi_start_x = 0
            roi_end_x = logo_center_x + math.floor(logo_cols / 2)
            # print('logo只超出背景左边界')
        elif logo_center_x > bg_cols - math.floor(logo_cols / 2):
            logo_start_x = 0
            logo_end_x = math.ceil(logo_cols / 2) + bg_cols - logo_center_x
            roi_start_x = logo_center_x - math.ceil(logo_cols / 2)
            roi_end_x = bg_cols
            # print('logo只超出背景右边界')
        else:
            logo_start_x = 0
            logo_end_x = logo_cols
            roi_start_x = logo_center_x - math.ceil(logo_cols / 2)
            roi_end_x = logo_center_x + math.floor(logo_cols / 2)
            # print('logo没有超出背景左右边界')
        if bg_rows - math.floor(logo_rows / 2) < logo_center_y < math.ceil(logo_rows / 2):
            logo_start_y = math.ceil(logo_rows / 2) - logo_center_y
            logo_end_y = logo_start_y + bg_rows
            roi_start_y = 0
            roi_end_y = bg_rows
            # print('logo同时超出背景上下边界')
        elif logo_center_y < math.ceil(logo_rows / 2):
            logo_start_y = math.ceil(logo_rows / 2) - logo_center_y
            logo_end_y = logo_rows
            roi_start_y = 0
            roi_end_y = logo_center_y + math.floor(logo_rows / 2)
            # print('logo只超出背景上边界')
        elif logo_center_y > bg_rows - math.floor(logo_rows / 2):
            logo_start_y = 0
            logo_end_y = math.ceil(logo_rows / 2) + bg_rows - logo_center_y
            roi_start_y = logo_center_y - math.ceil(logo_rows / 2)
            roi_end_y = bg_rows
            # print('logo只超出背景下边界')
        else:
            logo_start_y = 0
            logo_end_y = logo_rows
            roi_start_y = logo_center_y - math.ceil(logo_rows / 2)
            roi_end_y = logo_center_y + math.floor(logo_rows / 2)
            # print('logo没有超出背景上下边界')
        return logo_start_x, logo_end_x, roi_start_x, roi_end_x, logo_start_y, logo_end_y, roi_start_y, roi_end_y

    @staticmethod
    def put_logo_according_to_parameters(bg_img, processed_logo_img, mask, logo_center_x, logo_center_y):
        bg_rows, bg_cols, _ = bg_img.shape
        logo_rows, logo_cols, _ = processed_logo_img.shape
        # 其次是，确定roi的位置和大小，要注意logo位置超出bg_img的情况下需要进行截取
        logo_start_x, logo_end_x, roi_start_x, roi_end_x, logo_start_y, logo_end_y, roi_start_y, roi_end_y \
            = Tools.process_roi(bg_cols, logo_cols, logo_center_x, bg_rows, logo_rows, logo_center_y)
        roi = bg_img[roi_start_y: roi_end_y, roi_start_x: roi_end_x]  # 注意是rows在前，即y在前，cols在后，即x在后
        # print('roi.shape:', roi.shape)
        logo_fg = processed_logo_img[logo_start_y: logo_end_y, logo_start_x: logo_end_x]
        mask = mask[logo_start_y: logo_end_y, logo_start_x: logo_end_x]
        # print('logo_fg.shape:', resized_logo_img.shape)
        back_bg = cv2.bitwise_and(roi, roi, mask=mask)
        dst = cv2.add(back_bg, logo_fg)
        bg_img[roi_start_y: roi_end_y, roi_start_x: roi_end_x] = dst
        return bg_img

    @staticmethod
    def get_vibration_information(frame_count, amplitude, start=None, end=None):
        if amplitude == 0:
            return 0, 0
        if os.path.exists('_temp_file.txt') and os.path.getsize('_temp_file.txt') > 0:
            # 注意这里传入的数字要从0开始计数
            if frame_count >= 36:
                # 从第36帧开始读取文件的第一个信息
                frame_count -= 36
                print(f'当前是第{frame_count + 36}帧，即第{frame_count}帧有效帧：')
                if start is not None and end is not None:
                    frame_count += start * 2 - 2  # 注意start和end都是从1开始的，并且包含头尾
                    end_count = end * 2 - 1
                else:
                    end_count = frame_count + 1
                if frame_count <= end_count:
                    with open('_temp_file.txt', 'r', encoding='utf-8') as f:
                        f.seek(math.floor(frame_count / 2), 0)
                        base64code = f.read(1)
                        print(f'{base64code}：{frame_count % 2}')
                        if base64code:
                            print([i * amplitude for i in Tools.base64dic[base64code][frame_count % 2]])
                            return [i * amplitude for i in Tools.base64dic[base64code][frame_count % 2]]
                        else:
                            print(0, 0)
                            return 0, 0
                else:
                    print(0, 0)
                    return 0, 0
            elif frame_count % 9 == 0:  # 中心点
                return 0, 0
            elif frame_count % 9 == 1:  # 北
                return 0, -1 * amplitude
            elif frame_count % 9 == 2:  # 西北
                return -1 * amplitude, -1 * amplitude
            elif frame_count % 9 == 3:  # 西
                return -1 * amplitude, 0
            elif frame_count % 9 == 4:  # 西南
                return -1 * amplitude, 1 * amplitude
            elif frame_count % 9 == 5:  # 南
                return 0, 1 * amplitude
            elif frame_count % 9 == 6:  # 东南
                return 1 * amplitude, 1 * amplitude
            elif frame_count % 9 == 7:  # 东
                return 1 * amplitude, 0
            elif frame_count % 9 == 8:  # 东北
                return 1 * amplitude, -1 * amplitude
        else:
            return 0, 0

    @staticmethod
    def delete_file(path):
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                return False
            else:
                return True
        else:
            return True  # 如果文件已经不存在，就证明已经被删过了

    @staticmethod
    def get_logo_position_from_frame(frame, logo, constraint=None):
        '''
        从帧中获取logo的位置信息，返回的结果是logo的中心位置 type: Point
        constraint是限制logo在frame的哪一个部分去寻找，这样可以提高寻找速度和正确率
        constraint的格式为：
        [(x_nw, y_nw), (x_se, y_se)] 或者理解为 [(col_begin, row_begin), (col_end, row_end)]
        '''
        confidence = 0.9
        while True:
            try:
                if constraint is None:
                    position = auto.center(auto.locate(logo, frame))
                else:
                    # 特别注意这里切片的方式是frame[y_nw: y_se, x_nw: x_se]
                    # print(constraint[0][1], constraint[1][1], constraint[0][0], constraint[1][0], frame[constraint[0][1]: constraint[1][1], constraint[0][0]: constraint[1][0]].shape, logo.shape)
                    position = auto.center(auto.locate(logo, frame[constraint[0][1]: constraint[1][1], constraint[0][0]: constraint[1][0]], confidence=confidence))
            except Exception:
                confidence = max(confidence - 0.02, 0)
                print('confidence: ', confidence)
                if confidence <= 0:
                    return 0, 0
            else:
                return position

    @staticmethod
    def close_to_which(point, c, n, nw, w, sw, s, se, e, ne) -> tuple:
        '''
        注意这里传进来的point是pyautogui中的Point对象，不过取值方法跟tuple一样
        根据logo的位置信息，找出靠近哪一个方位，返回值的格式如下：
        (0, -1)  # type: tuple
        '''

        def distance_between(point_a, point_b):
            # 注意这里的距离是距离的平方（因为这里不开根号没影响，还算的快）
            return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2

        min_distance = distance_between(point, c)
        res = (0, 0)
        if distance_between(point, n) < min_distance:
            min_distance = distance_between(point, n)
            res = (0, -1)
        if distance_between(point, nw) < min_distance:
            min_distance = distance_between(point, nw)
            res = (-1, -1)
        if distance_between(point, w) < min_distance:
            min_distance = distance_between(point, w)
            res = (-1, 0)
        if distance_between(point, sw) < min_distance:
            min_distance = distance_between(point, sw)
            res = (-1, 1)
        if distance_between(point, s) < min_distance:
            min_distance = distance_between(point, s)
            res = (0, 1)
        if distance_between(point, se) < min_distance:
            min_distance = distance_between(point, se)
            res = (1, 1)
        if distance_between(point, e) < min_distance:
            min_distance = distance_between(point, e)
            res = (1, 0)
        if distance_between(point, ne) < min_distance:
            res = (1, -1)
        return res

    @staticmethod
    def decrypt_bigfile(infile_path, outfile_path, privkey_cipher):
        '''
        :param infile_path: 输入密文的地址
        :param outfile_path: 输入明文的地址
        :param privkey_cipher: 输入私钥的地址
        :return: 无返回值，结果直接保存在了 outfile_path 的文件里了
        '''

        def decrypt_by_zebrized_file():
            zebrized_file = ZebrizedFile(infile_path, outfile_path)
            zebrized_file.decrypt(mode='rsa', privkey_cipher=privkey_cipher)

        '''
        文件头部被加密后的格式：
        infile := times|length|, block_enc, block_enc, ...
        outfile := 112 bytes (block_content), 112 bytes (block_content), ...
        '''
        # 先判断是不是文件头部被加密的格式
        with open(infile_path, 'rb') as infile, open(outfile_path, 'wb') as outfile:
            # 先读取循环次数 times，如果读取不到（或错误），就尝试用ZebrizedFile来解密
            times = ""
            current = str(infile.read(1)).lstrip("b'").rstrip("'")
            while True:
                next = str(infile.read(1)).lstrip("b'").rstrip("'")
                times += current
                try:
                    _times = eval(times)  # 先判断times是不是能被eval函数解析
                except (SyntaxError, NameError):
                    decrypt_by_zebrized_file()
                    return 0
                else:
                    if not isinstance(_times, int):  # 当发现_times不是个整数时，尝试用ZebrizedFile来解密
                        decrypt_by_zebrized_file()
                        return 0
                if next == "|":
                    break
                current = next
                if not next:  # 当读空整个文件都没找到'|'时，就尝试用ZebrizedFile来解密
                    decrypt_by_zebrized_file()
                    return 0
            times = int(times)  # 如果读到的不是个整数，也会抛出异常，并被接下来的程序捕获
            # 再读取一个block_enc有多长
            length = ""
            current = str(infile.read(1)).lstrip("b'").rstrip("'")
            while True:
                next = str(infile.read(1)).lstrip("b'").rstrip("'")
                length += current
                try:
                    _length = eval(length)
                except (SyntaxError, NameError):
                    decrypt_by_zebrized_file()
                    return 0
                else:
                    if not isinstance(_length, int):  # 当发现length不是个整数时，也尝试用ZebrizedFile来解密
                        decrypt_by_zebrized_file()
                        return 0
                if next == '|':
                    break
                current = next
                if not next:  # 当读空整个文件都没找到'|'时，就尝试用ZebrizedFile来解密
                    decrypt_by_zebrized_file()
                    return 0
            length = int(length)
            count = 0
            block_enc = infile.read(length)
            while block_enc:
                count += 1
                back_text = privkey_cipher.decrypt(block_enc, 0)
                outfile.write(back_text)
                block_enc = infile.read(length)
                if count == times:  # 如果达到次数，就把剩下的数据写入outfile
                    # 但不能一下子全部写入，因为如果原文件太大，内存会爆炸！
                    while block_enc:
                        outfile.write(block_enc)
                        block_enc = infile.read(1024)
                    break
                # 如果在没有达到次数就已经处理完了，那么也不用再管了

    @staticmethod
    def read_and_write(infile, outfile, length):
        if length >= 20480000:
            outfile.write(infile.read(20480000))
            Tools.read_and_write(infile, outfile, length - 20480000)  # 使用递归，每次读取20MB，避免一次性读取信息过多
        else:
            outfile.write(infile.read(length))

    @staticmethod
    def read_all_and_write_all(infile_path, outfile_path):
        with open(infile_path, 'rb') as infile, open(outfile_path, 'wb') as outfile:
            while True:
                block = infile.read(10240)
                if block:
                    outfile.write(block)
                else:
                    break

    @staticmethod
    def de_iso_padding(de_text):
        # 先读取末尾的十六进制数
        hex = '123456789ABCDEF'
        tail = str(de_text[-1:]).lstrip("b'").rstrip("'")
        if tail in hex:
            padding_number = hex.index(tail) + 1
            # 再去掉padding
            de_text = de_text[: 16 - padding_number]
        return de_text

    @staticmethod
    def de_pkcs7_padding(de_text):
        # 先读取末尾的内容
        tails = [eval(rf"b'\x0{i}'") for i in '123456789abcdef']
        tail = de_text[-1:]
        if tail in tails:
            padding_nummber = tails.index(tail) + 1
            # 检查一下 padding 内容中的每一个字节是不是都是一样的
            # 如果不一样就不去掉（为了防止误删）
            padding = de_text[16 - padding_nummber:]
            for i in padding:  # 这里的 i 会变成 int 类型
                if i != tail[0]:  # 所以这里也要把 tail 转成 int 类型再和 i 比较
                    break
            # 如果循环正常结束（没有被break），则说明可以删掉padding
            else:
                # 如果 padding 中的内容全都是一样的，才删掉 padding
                de_text = de_text[: 16 - padding_nummber]
        # 如果发现在 padding 中有混入了其他不一致的内容，则不删除
        return de_text

    @staticmethod
    def de_padding(de_text: bytes, padding):
        if padding == 'zero padding':
            de_text = de_text.rstrip(b'\x00')
        elif padding == 'iso 10126 padding':
            de_text = Tools.de_iso_padding(de_text)
        elif padding == 'pkcs7 padding':
            de_text = Tools.de_pkcs7_padding(de_text)
        elif padding == 'no padding':
            pass  # 为 no padding 时，不进行任何操作
        return de_text

    @staticmethod
    def copy(text_or_entry, button):
        global ind
        ind = (ind + 1) % 6
        button.config(fg=colors[ind])
        if isinstance(text_or_entry, tk.Text):
            pyperclip.copy(text_or_entry.get(1.0, 'end').rstrip("\n"))
        elif isinstance(text_or_entry, tk.Entry):
            pyperclip.copy(text_or_entry.get().rstrip("\n"))

    @staticmethod
    def change_entry_show(var, entry):
        if var.get() == '1':
            entry.config(show='*')
        elif var.get() == '0':
            entry.config(show='')

    @staticmethod
    def encrypt_privkey(privkey_bytes, key, is_ecc=False):
        '''
        对私钥进行加密
        :param privkey_bytes: 字节类型
        :param key: 字符串类型
        :return: 加密好的私钥字节码
        '''
        # 函数遇到错误就返回b''，让外部函数来捕获
        if b'Encrypted:' in privkey_bytes:
            return b''  # 返回这个代表私钥已经被加密过了
        privkey_bytes = b'\n'.join(privkey_bytes.split(b'\n')[1:-1])
        key = Tools.get_hash_digest_of_word(key)
        aes = AES.new(key, AES.MODE_CBC, b'1234567890abcdef')
        ontology_sec = b''
        with open('_temp.txt', 'wb') as f:
            letters = string.ascii_lowercase
            f.write(''.join(choice(letters) for _ in range(6)).encode('utf-8'))
            f.write(key)
            f.write(privkey_bytes)
        with open('_temp.txt', 'rb') as f:
            content = f.read(16)
            while content:
                if len(content) < 16:
                    content = Tools.pkcs7_padding(content)
                en_text = aes.encrypt(content)
                ontology_sec += en_text
                content = f.read(16)
        os.remove('_temp.txt')
        if not is_ecc:
            return b'\n'.join([b'-----BEGIN RSA PRIVATE KEY-----\nEncrypted:', base64.b64encode(ontology_sec), b'-----END RSA PRIVATE KEY-----'])
        else:
            return b'\n'.join([b'-----BEGIN PRIVATE KEY-----\nEncrypted:', base64.b64encode(ontology_sec), b'-----END PRIVATE KEY-----'])

    @staticmethod
    def decrypt_privkey(privkey_bytes, key, is_ecc=False):
        '''
        对被加密的私钥字节进行解密
        函数遇到错误就返回b''或b'1'，让外部函数来捕获
        :param privkey_bytes: 字节类型
        :param key: 字符串类型
        :return: 字节类型
        '''
        if b'Encrypted:' not in privkey_bytes:
            return b'1'  # 返回这个代表已经被解密过了
        privkey_bytes = privkey_bytes.split(b'\n')[2]
        key = Tools.get_hash_digest_of_word(key)
        aes = AES.new(key, AES.MODE_CBC, b'1234567890abcdef')
        ontology = b''
        with open('_temp.txt', 'wb') as f:
            f.write(base64.b64decode(privkey_bytes))
        with open('_temp.txt', 'rb') as f:
            content = f.read(16)
            while content:
                try:
                    de_text = aes.decrypt(content)
                except Exception:
                    return b''  # 返回这个代表解密失败
                else:
                    next = f.read(16)
                    if len(next) == 0:
                        de_text = Tools.de_pkcs7_padding(de_text)
                    ontology += de_text
                    content = next
        os.remove('_temp.txt')
        if key == ontology[6:38]:
            if not is_ecc:
                return b'\n'.join([b'-----BEGIN RSA PRIVATE KEY-----', ontology[38:], b'-----END RSA PRIVATE KEY-----'])
            else:
                return b'\n'.join([b'-----BEGIN PRIVATE KEY-----', ontology[38:], b'-----END PRIVATE KEY-----'])
        else:
            return b''

    @staticmethod
    def get_key(entry, *, method='cipher', pwd_entry=None, is_ecc=False):
        '''
        用于获取用户输入的密钥。既可以是公钥，也可以是私钥
        :param entry: 用户输入的密钥地址在entry1中，所以要从这里获取数据
        :param method: 如果是加密，method就是cipher（默认）。如果是签名，method就是signer
        :param is_ecc: 默认为False，代表为RSA密钥，如果为True，代表为ECC密钥
        :return: 如果能够获取到密钥就返回密钥，获取不到就返回 0
        '''
        key_path = Tools.get_path_from_entry(entry)
        if os.path.exists(key_path) and '.pem' in key_path:
            with open(key_path, 'rb') as keyfile:
                p = keyfile.read()  # bytes类型
            try:
                if method == 'cipher' or method == 'verifier':
                    if not is_ecc and b'-----BEGIN PUBLIC KEY-----' in p:
                        key = RSA.importKey(p)
                        if method == 'cipher':
                            result = PKCS1_cipher.new(key)
                        else:
                            result = PKCS1_signature.new(key)
                    elif is_ecc and b"-----BEGIN PUBLIC KEY-----" in p:
                        key = ECC.import_key(p)
                        if method == 'cipher':
                            result = ...
                        else:
                            result = DSS.new(key, 'fips-186-3')
                    else:
                        messagebox.showerror(title='密钥错误', message="输入的密钥不正确")
                        return 0
                elif method == 'decipher' or method == 'signer':
                    if not is_ecc and b'-----BEGIN RSA PRIVATE KEY-----' in p:
                        if b'Encrypted:' in p:
                            p = Tools.decrypt_privkey(p, pwd_entry.get())
                            if p == b'':
                                messagebox.showerror(title='私钥的使用密码错误', message="私钥的使用密码错误")
                                return 0
                        key = RSA.importKey(p)
                        if method == 'decipher':
                            result = PKCS1_cipher.new(key)
                        else:
                            result = PKCS1_signature.new(key)
                    elif is_ecc and b'-----BEGIN PRIVATE KEY-----' in p:
                        if b'Encrypted:' in p:
                            p = Tools.decrypt_privkey(p, pwd_entry.get(), is_ecc=is_ecc)
                            if p == b'':
                                messagebox.showerror(title='私钥的使用密码错误', message="私钥的使用密码错误")
                                return 0
                        key = ECC.import_key(p)
                        if method == 'decipher':
                            result = ...
                        else:
                            result = DSS.new(key, 'fips-186-3')
                    else:
                        messagebox.showerror(title='密钥错误', message="输入的密钥不正确")
                        return 0
                else:
                    return 0
            except Exception:
                messagebox.showerror(title='密钥错误', message='读取到的.pem文件不是密钥')
                return 0
            else:
                return result
        else:
            messagebox.showerror(title='密钥错误', message='密钥文件路径错误')
            return 0

    @staticmethod
    def encrypt_bigfile(infile_path, outfile_path, pubkey_cipher, size="完整文件", begin=None, width=None, number=None,
                         end=None):
        '''
        由于RSA计算密文时用到了求余运算，余数就是密文。
        因为余数不可能大于除数，这意味着余数，即密文所能表示的信息容量必定是小于除数的值的
        为了密文能够正确解密回明文，正常的RSA加密计算通常对明文的大小有限制
        为了处理大文件，这里使用分段的方法来处理大文件，拆分逻辑如下：
        infile := 112 bytes (block_content), 112 bytes (block_content), ...
        outfile := times|length|, block_enc, block_enc, ...
        由于加密出来的每一个block_enc的长度都是一样的（可能是被填充成一样长度的），
        所以直接把length放在前面
        mode代表加密的方式，如全部加密，部分加密
        目前来看没有找到拆分的标准，这里参考的是3.1.4版rsa库里encrypt_bigfile函数的方法
        :param infile_path: 输入明文的地址
        :param outfile_path: 输入密文的地址
        :param pubkey_cipher: 输入公钥
        :param size: 输入要加密的大小（完整文件，1单位，10单位，516单位，5160单位，或用户手动输入的内容，如 '123'）
        :param begin: 第一根黑线的起始位置，为str
        :param width: 黑线的宽度，为int
        :param number: 黑线的根数，为int
        :param end: 最后一根黑线的结束位置，为str
        :return:无返回值
        '''
        if size == '斑马线加密法':
            origin_file = OriginFile(infile_path, outfile_path, begin, width, number, end)
            origin_file.encrypt(mode='rsa', pubkey_cipher=pubkey_cipher)
        else:
            # 把接收到的size转变为循环的次数
            if size == "完整文件":
                times = 0
            else:
                times = int(size.rstrip("单位"))
            # times 为0，1，10，516，5160，或用户手动输入的内容。（0代表一直循环）
            block_size = 112  # 每次从明文中拆分112个字节，这个数不大不小，差不多正好
            # 如果 infile_path 或 outfile_path 写错的话，这里会自动报错的
            with open(infile_path, 'rb') as infile, open(outfile_path, 'wb') as outfile:
                block_content = infile.read(block_size)
                count = 0
                while block_content:
                    count += 1
                    try:
                        block_enc = pubkey_cipher.encrypt(block_content)
                    except Exception:
                        raise IOError('输入的公钥错误')
                    else:
                        if count == 1:  # 需要在文件头部写上times和每一段block的长度
                            length = str(len(block_enc))
                            prefix = ''.join([str(times), '|', length, '|'])
                            outfile.write(bytes(prefix.encode("utf-8")))
                        outfile.write(block_enc)
                        block_content = infile.read(block_size)
                        if count == times:  # 如果达到次数，就把剩下的以明文方式写入outfile
                            # 但不能一下子全部写入，因为如果原文件太大，内存会爆炸！
                            while block_content:
                                outfile.write(block_content)
                                block_content = infile.read(1024)
                            break
                        # 如果在没有达到次数就已经处理完了，那么也不用再管了

    @staticmethod
    def add_to_16(content: bytes):  # 这里自建一个 ZeroPadding 填充方式
        length = len(content)
        if length % 16:
            add = 16 - (length % 16)
        else:
            add = 0
        content = content + (b'\0' * add)
        return content

    @staticmethod
    def iso_padding(content: bytes):  # 这里自建一个 ISO 10126 填充方式, 返回填充好的content
        # 先随机填充，最后一个字节（十六进制[1, F]）显示填充了多少字节
        # 填充的长度为16 - len(content)
        padding_length = 16 - len(content)
        if 15 >= padding_length >= 1:
            mark = r''' ,./;'[]\`1234567890-=<>?:"{}|~!@#$%^&*()_+'''

            def _chr(num: int):  # 将编码[0, 94]变成字符
                if 0 <= num <= 25:
                    return chr(num + 65)  # A-Z
                elif 26 <= num <= 51:
                    return chr(num - 26 + 97)
                elif 52 <= num <= 94:
                    return mark[num - 52]
                else:
                    return _chr(num % 95)

            hex = '123456789ABCDEF'
            padding = ''
            for i in range(padding_length - 1):
                padding += _chr(randint(0, 94))
            padding += hex[padding_length - 1]
            return content + bytes(padding, encoding='utf-8')
        else:
            return content

    @staticmethod
    def pkcs7_padding(content: bytes):  # 这里自建一个 PKCS7 填充方式, 返回填充好的content
        # 每个填充的字节都显示填充了多少字节
        # 填充的内容是b'\x01', b'\02', ..., b'\x0a', ..., b'b\x0f'
        # 填充的长度为16 - len(content)
        padding_length = 16 - len(content)
        hex = '123456789abcdef'
        if 15 >= padding_length >= 1:
            padding = eval(rf"b'\x0{hex[padding_length - 1]}'") * padding_length
            return content + padding
        else:
            return content

    @staticmethod
    def enter_length(size, entry, label, frm4, zebra_frm=None, setting_button=None):
        Tools.clean_all_widget(frm4)
        zebra_frm.pack_forget()
        if setting_button is not None:
            setting_button.grid_forget()
        if size.get() == "其他长度":
            entry.grid(row=1, column=3)
            label.grid(row=1, column=4)
        else:
            entry.grid_forget()
            label.grid_forget()
            if size.get() == "斑马线加密法":
                zebra_frm.pack()
                if setting_button is not None:
                    setting_button.grid(row=1, column=3, padx=15)

    @staticmethod
    def change_zscale(show_method, zentry, begin_or_end):
        if show_method.get() == '1':
            if not zentry.get():
                begin_or_end.set(0)
            else:
                try:
                    value = eval(zentry.get())
                    if not isinstance(value, int) and not isinstance(value, float):
                        raise IOError('需要输入正整数，或浮点数')
                    else:
                        if value < 0 or value > 100:
                            raise IOError('需要输入0到100的数')
                except Exception:
                    messagebox.showerror('输入错误', '需要输入0到100的正整数或浮点数')
                    return 0
                else:
                    begin_or_end.set(round(value))

    @staticmethod
    def change_zentry(value, zentry):
        Tools.reset(zentry)
        zentry.insert('end', value)

    @staticmethod
    def get_correct_size(_size: tk.StringVar, entry=None):
        '''
        返回的size为：'完整文件'，'1单位'，'10单位'，'516单位'，'5160单位'，'123'（123为用户输入的示例），'斑马线加密法'
        如果用户输入错误，则返回 0
        '''
        size = _size.get()
        if size == "其他长度":
            size = entry.get().strip()
            try:
                assert isinstance(eval(size), int) and int(size) > 0
            except Exception:
                messagebox.showerror(title='输入错误', message='输入的数字应为正整数')
                return 0
            else:
                return size  # 正确的 size 为 str 类型
        else:
            return size

    @staticmethod
    def get_correct_zebra_parameter(size, show_method, zentry1, zentry2, zentry3, zentry4):
        '''
        需要特别注意在用户没有选择斑马线加密法时，不要报错！
        :param show_method:位置的显示方式
        :param size:处理好的size，str型
        :param zentry1:第一根黑线的起始位置（百分位或绝对值）
        :param zentry2:黑线的宽度（需要大于等于 1）
        :param zentry3:黑线的数量（需要大于等于 1）
        :param zentry4:最后一根黑线的末尾位置（百分位或绝对值）
        :return: 如果用户输入正确，则返回begin: str, width: int, number: int, end: str
        否则，返回 False, False, False, False
        '''
        if size == '斑马线加密法':
            try:
                if (isinstance(eval(zentry1.get()), float) or isinstance(eval(zentry1.get()), int)) and isinstance(
                        eval(zentry2.get()), int) and eval(zentry2.get()) >= 1 and isinstance(eval(zentry3.get()),
                                                                                              int) and eval(
                    zentry3.get()) >= 1 and (
                        isinstance(eval(zentry4.get()), float) or isinstance(eval(zentry4.get()), int)):
                    begin = zentry1.get() if show_method.get() == '2' else zentry1.get() + '%'
                    end = zentry4.get() if show_method.get() == '2' else zentry4.get() + '%'
                    width = int(zentry2.get())
                    number = int(zentry3.get())
                    return begin, width, number, end
                else:
                    messagebox.showerror('参数错误', '输入的参数格式不正确，请检查后重新输入')
                    return [False] * 4
            except Exception:
                messagebox.showerror('参数错误', '无法识别参数，请检查后重新输入')
                return [False] * 4
        else:
            return [None] * 4

    @staticmethod
    def intro_enc_head():
        intro_window = tk.Toplevel()
        intro_window.title("加密大小介绍")
        intro_window.geometry('636x758')
        intro_window.iconbitmap(icon_path)
        iw_text = tk.Text(intro_window, width=46, height=28, font=mid_font)
        iw_text.pack()
        word = '''    为了更快速地完成加解密，您可以在这里选择加密的数据大小。如果选择仅加密部分信息，程序会加密明文头部的部分信息，以此破坏明文的数据结构，防止信息被读取。在解密时，程序会自动识别加密的部分，并还原信息。
    注意：1单位代表112 bytes，5160 单位约564 kb，手动输入加密大小时，应输入正整数。
    
斑马线加密法介绍：
    这种加密方法可以将文件内容一段隔一段地加密。加密的效果就像斑马线一样，密文与明文交错排列，其中加密的部分被称为黑线，未被加密的部分称为白线。\
您可以根据需求设定斑马线的位置，线的宽度等参数信息。在设定起始或末尾的绝对位置时，可以使用小数，也可以使用负数，如-10 kb，代表倒数10 kb（1 kb = 1024 bytes）。\
如果输入的末尾位置为0 kb，程序会转为倒数第0 kb。如果您设定的斑马线的起始位置大于末尾位置，程序会自动交换这两个值，使起始位置小于末尾位置。\
输入黑线的宽度和黑线的根数时，需要输入正整数。此外，您还可以设置 AES 对称加密在斑马线加密法中一单位加密块的大小。'''
        iw_text.insert('end', word)

    @staticmethod
    def remove_file_or_dir(path, frm: tk.Frame):
        global ind
        Tools.clean_all_widget(frm)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
                label = tk.Label(frm, text='已清除明文文件夹', font=mid_font)
            elif os.path.isfile(path):
                os.remove(path)
                label = tk.Label(frm, text='已清除明文文件', font=mid_font)
        else:
            label = tk.Label(frm, text='明文文件（夹）已被清除或移动', font=mid_font, fg=colors[ind])
            ind = (1 + ind) % 6
        label.pack()

    @staticmethod
    def intro_destroy():
        intro_window = tk.Toplevel()
        intro_window.title("阅后即焚功能介绍")
        intro_window.geometry('636x758')
        intro_window.iconbitmap(icon_path)
        iw_text = tk.Text(intro_window, width=46, height=28, font=mid_font)
        iw_text.pack()
        word = '''    阅后即焚功能可以把解密后的明文文件或文件夹彻底删除，删除后不会在回收站找到被删除的文件。
    
    注意：
    1.在销毁明文文件夹时，会将整个文件夹全部删除。
    2.不要修改需要阅后即焚的文件名。'''
        iw_text.insert('end', word)

    @staticmethod
    def get_hasher_of_file(file_path):
        '''
        将文件的内容更新给hasher
        :param file_path: 文件的地址
        :return: 文件的哈希值（bytes格式)
        '''
        hasher = SHA384.new()
        block_size = 33554432  # 为了防止内存溢出，每一次读取的长度限定为32mb
        with open(file_path, 'rb') as f:
            content = f.read(block_size)
            while content:
                hasher.update(content)
                content = f.read(block_size)
        return hasher

    @staticmethod
    def get_hash_digest_of_word(content, mode='SHA256') -> bytes:
        if mode == 'SHA256':
            hasher = hashlib.sha256()
        elif mode == 'MD5':
            hasher = hashlib.md5()
        else:
            return b''
        hasher.update(bytes(content, encoding='utf-8'))
        return hasher.digest()

    @staticmethod
    def get_aes_key(var, entry, *, mode='ECB', iv=None):
        if entry.get().strip() == "":
            return 0

        def _get_key(key, mode, iv):
            try:
                if mode == 'ECB':
                    aes = AES.new(key, AES.MODE_ECB)  # 创建一个 AES 加密工具，使用 ECB 模式
                elif mode == 'CBC':
                    # 将获取到的iv转成md5值（16字节）
                    if iv:
                        iv = Tools.get_hash_digest_of_word(iv, mode='MD5')
                    else:
                        iv = Tools.get_hash_digest_of_word("default", mode='MD5')
                    aes = AES.new(key, AES.MODE_CBC, iv)
                else:
                    aes = 0
            except Exception:
                tk.messagebox.showerror(title='密钥错误', message='密钥文件可能有问题')
                return 0
            else:
                return aes

        if var.get() == '1':
            key_file = Tools.get_path_from_entry(entry)
            if os.path.exists(key_file) and key_file.endswith('.aes') and os.path.isfile(key_file):
                with open(key_file, 'rb') as f:
                    key = f.read()
                return _get_key(key, mode, iv)
            else:
                tk.messagebox.showerror(title='密钥错误', message='密钥文件路径错误')
                return 0
        elif var.get() == '2':
            content = entry.get()
            key = Tools.get_hash_digest_of_word(content)  # 获取SHA256摘要
            return _get_key(key, mode, iv)
        else:
            return 0

    @staticmethod
    def intro_iv():
        intro_window = tk.Toplevel()
        intro_window.title('说明')
        intro_window.geometry("636x758")
        intro_window.iconbitmap(icon_path)
        iw_text = tk.Text(intro_window, width=46, height=28, font=mid_font)
        iw_text.pack()
        word = '''    CBC模式需要输入偏移量，可以将其理解为第二密钥。
        
    如果不输入，则会使用默认的偏移量。如果输入，可以输入任意字符，程序会自动将输入的偏移量摘要成合适长度。
'''
        iw_text.insert('end', word)

    @staticmethod
    def aes_enc_file(aes, padding, infile_path, outfile_path, size="完整文件", begin=None, width=None, number=None,
                      end=None):
        '''
        :param aes:
        :param padding:
        :param infile_path:
        :param outfile_path:
        :param size:
        :param begin: 第一根黑线的起始位置，为str
        :param width: 黑线的宽度，为int
        :param number: 黑线的根数，为int
        :param end: 最后一根黑线的结束位置，为str
        :return:无返回值
        '''
        if size == '斑马线加密法':
            origin_file = OriginFile(infile_path, outfile_path, begin, width, number, end)
            origin_file.encrypt(mode='aes', aes=aes, padding=padding)
        else:
            # size 为要加密的大小（完整文件，1单位，10单位，516单位，5160单位，或用户手动输入的内容，如 '123'）
            # 加密后的文件为 times|encrypyed_content, content
            # 把接收到的size转变为循环的次数
            if size == "完整文件":
                times = 0
            else:
                times = int(size.rstrip("单位"))
            # times 为0，1，10，516，5160，或用户手动输入的内容。（0代表一直循环）
            with open(infile_path, 'rb') as infile, open(outfile_path, 'wb') as outfile:
                content = infile.read(16)
                count = 0
                while content:
                    count += 1
                    if count == 1:  # 在文件头写入times
                        prefix = str(times) + '|'
                        outfile.write(bytes(prefix.encode("UTF-8")))
                    if len(content) < 16:
                        if padding == 'zero padding':
                            content = Tools.add_to_16(content)
                        elif padding == 'iso 10126 padding':
                            content = Tools.iso_padding(content)
                        elif padding == 'pkcs7 padding':
                            content = Tools.pkcs7_padding(content)
                    en_text = aes.encrypt(content)
                    outfile.write(en_text)
                    content = infile.read(16)
                    if count == times:  # 如果达到次数，就把剩下的以明文方式写入outfile
                        # 但不能一下子全部写入，因为如果原文件太大，内存会爆炸！
                        while content:
                            outfile.write(content)
                            content = infile.read(1024)
                        break
                    # 如果在没有达到次数就已经处理完了，那么也不用再管了

    @staticmethod
    def setting():
        global ind
        setting_window = tk.Toplevel()
        setting_window.title("设置1单位加密块的大小")
        setting_window.geometry("450x158")
        setting_window.iconbitmap(icon_path)
        label1 = tk.Label(setting_window, text='请设置1单位加密块的大小：', font=mid_font)
        label1.pack()
        label2 = tk.Label(setting_window, text='（仅适用于aes模式的斑马线加密法）', font=mid_font)
        label2.pack()

        def change_label(*args):
            global ind
            ind = (ind + 1) % 6
            entry2.config(state='normal', fg=colors[ind])
            entry2.delete(0, 'end')
            entry2.insert(0, '未保存')
            entry2.config(state='readonly')
            try:
                res = eval(entry1.get())
                assert isinstance(res, int) and res >= 1
            except Exception:
                textvar.set(" x 16 = 错误！")
            else:
                textvar.set(f" x 16 = {res * 16} bytes")

        frm1 = tk.Frame(setting_window)
        frm1.pack()
        entry1 = tk.Entry(frm1, width=4, font=mid_font)
        entry1.grid(row=1, column=1)
        entry1.bind("<KeyRelease>", change_label)
        textvar = tk.StringVar()
        label3 = tk.Label(frm1, textvariable=textvar, font=mid_font)
        label3.grid(row=1, column=2)
        if os.path.exists("./system_resource/settings.dll"):
            with open('./system_resource/settings.dll', 'r+', encoding='utf-8') as f:
                try:
                    res = eval(f.read())
                    assert isinstance(res, int) and res >= 1
                except Exception:
                    f.seek(0, 0)
                    f.truncate()
                    f.write('7')
                    entry1.insert(0, '7')
                else:
                    entry1.insert(0, res)
        else:
            with open("./system_resource/settings.dll", 'w', encoding='utf-8') as f:
                f.write('7')
                entry1.insert('0', '7')

        def confirm(*args):
            global ind
            ind = (ind + 1) % 6
            try:
                res = eval(entry1.get())
                assert isinstance(res, int) and res >= 1
            except Exception:
                entry2.config(state='normal', fg=colors[ind])
                entry2.delete(0, 'end')
                entry2.insert(0, '未保存')
                entry2.config(state='readonly')
            else:
                with open('system_resource/settings.dll', 'w', encoding='utf-8') as f:
                    f.write(entry1.get())
                entry2.config(state='normal', fg=colors[ind])
                entry2.delete(0, 'end')
                entry2.insert(0, '已保存')
                entry2.config(state='readonly')

        frm2 = tk.Frame(setting_window)
        frm2.pack()
        entry2 = tk.Entry(frm2, width=6, font=mid_font, fg=colors[ind])
        entry2.grid(row=1, column=1, padx=20)
        button1 = tk.Button(frm2, text='确认', font=mid_font, command=confirm)
        button1.grid(row=1, column=2, padx=20)
        change_label()
        entry2.config(state='normal')
        entry2.delete(0, 'end')
        entry2.insert(0, '已保存')
        entry2.config(state='readonly')

    @staticmethod
    def aes_dec_file(aes, padding, infile_path, outfile_path, show_error=True):
        # infile := times|encrypted_content, content
        # outfile := 112 bytes (content), 112 bytes (content), ...
        # 该函数有返回值，返回 True 代表解密成功，返回 False 代表解密失败

        def raise_wrong():
            # 通过这个函数抛出异常
            if show_error:
                tk.messagebox.showerror(title='解密失败', message='解密失败，可能是密文信息被删改')
            return False

        def decrypt_by_zebrized_file():
            zebrized_file = ZebrizedFile(infile_path, outfile_path)
            zebrized_file.decrypt(mode='aes', aes=aes, padding=padding)

        with open(infile_path, 'rb') as infile, open(outfile_path, 'wb') as outfile:
            # 先读取times，如果读取不到（或错误），就尝试用ZebrizedFile来解密
            times = ""
            current = str(infile.read(1)).lstrip("b'").rstrip("'")
            while True:
                next = str(infile.read(1)).lstrip("b'").rstrip("'")
                times += current
                try:
                    _times = eval(times)
                except Exception:  # 如果times不能被eval解析，也是要交给ZebrizedFile来解密
                    try:
                        decrypt_by_zebrized_file()
                    except Exception:
                        return raise_wrong()
                    return True
                else:
                    if not isinstance(_times, int):  # 当发现times不是个整数时，也尝试用ZebrizedFile来解密
                        try:
                            decrypt_by_zebrized_file()
                        except Exception:
                            return raise_wrong()
                        return True
                if next == "|":
                    break
                current = next
                if not next:  # 当读空整个文件都没找到'|'时，就尝试用ZebrizedFile来解密
                    try:
                        decrypt_by_zebrized_file()
                    except Exception:
                        return raise_wrong()
                    return True
            try:
                times = int(times)
            except Exception:
                return raise_wrong()
            content = infile.read(16)
            count = 0
            # 如果正确读取了 times，且文件不是ZebrizedFile，那么就根据 times 解密
            while content:
                count += 1
                try:
                    de_text = aes.decrypt(content)
                except Exception:
                    return raise_wrong()
                else:
                    next = infile.read(16)
                    if len(next) == 0:  # 这里的len(next) == 0，只有一种情况，就是已经读到文件的最末尾了
                        de_text = Tools.de_padding(de_text, padding)
                    outfile.write(de_text)
                    content = next
                    if count == times:  # 如果达到次数，就把剩下的数据写入outfile
                        # 但不能一下子全部写入，因为如果原文件太大，内存会爆炸！
                        while content:
                            outfile.write(content)
                            content = infile.read(1024)
                        break
                    # 如果在没有达到次数就已经处理完了，那么也不用再管了
        return True

    @staticmethod
    def open_software_dir():
        os.system('start ' + os.getcwd())

    @staticmethod
    def get_path_from_entry(entry):
        return entry.get().strip().strip('\"').lstrip('“').rstrip('”')

    @staticmethod
    def convert_black_background_to_white(img: np.ndarray):
        height, width, _ = img.shape  # 获取图片宽高
        # 去除黑色背景，seedPoint代表初始种子，进行四次，即对四个角都做一次，可去除最外围的黑边
        img = cv2.floodFill(img, mask=None, seedPoint=(0, 0), newVal=(255, 255, 255))[1]
        img = cv2.floodFill(img, mask=None, seedPoint=(0, height - 1), newVal=(255, 255, 255))[1]
        img = cv2.floodFill(img, mask=None, seedPoint=(width - 1, height - 1), newVal=(255, 255, 255))[1]
        img = cv2.floodFill(img, mask=None, seedPoint=(width - 1, 0), newVal=(255, 255, 255))[1]
        return img

    @staticmethod
    def intro_emoji():
        intro_window = tk.Toplevel()
        intro_window.title('emoji编码介绍')
        intro_window.geometry("636x758")
        intro_window.iconbitmap(icon_path)
        iw_text = tk.Text(intro_window, width=46, height=28, font=mid_font)
        iw_text.pack()
        word = '''    emoji编码方式介绍
        
    这种编码方式在base64基础之上演变而来。它的原理是将每一个base64字符与一个emoji表情一一对应起来，其本质还是base64编码的信息，只是用来表示的符号变成emoji表情。
    
    需要特别注意的是在传输这种通过emoji编码的信息时需要使用邮件的形式发送，不能使用微信或者QQ发送，不然接收方无法复制您发送的emoji信息至软件内进行解密。
        '''
        iw_text.insert('end', word)

    @staticmethod
    def translate_base64_to_emoji(b64_text: str) -> str:
        base64_to_emoji_dic = {'A': '😃', 'B': '😄', 'C': '😆', 'D': '😅', 'E': '🤣', 'F': '😂', 'G': '🙂', 'H': '🙃', 'I': '😉', 'J': '😊', 'K': '🐵', 'L': '😍', 'M': '🐒', 'N': '😘', 'O': '😇', 'P': '😚', 'Q': '🐶', 'R': '😋', 'S': '😜', 'T': '🤗', 'U': '🐱', 'V': '🦁', 'W': '🤔', 'X': '😴', 'Y': '😷', 'Z': '🤒', 'a': '🤕', 'b': '🤢', 'c': '🐴', 'd': '🤧', 'e': '🐮', 'f': '🐷', 'g': '😵', 'h': '🐭', 'i': '😎', 'j': '🤓', 'k': '🐧', 'l': '😟', 'm': '😯', 'n': '😳', 'o': '😲', 'p': '🐸', 'q': '🍋', 'r': '😧', 's': '😥', 't': '😢', 'u': '😭', 'v': '😱', 'w': '😖', 'x': '😣', 'y': '😓', 'z': '🌶', '0': '👻', '1': '💖', '2': '💌', '3': '💔', '4': '👰', '5': '🍖', '6': '🎅', '7': '💇', '8': '🚶', '9': '🏇', '+': '🛀', '/': '🛌', '=': '💏'}
        res = ''
        for i in b64_text:
            res += base64_to_emoji_dic[i]
        return res

    @staticmethod
    def translate_emoji_to_base64(emoji_text: str) -> str:
        # 这个函数需要检查emoji_text编码是否正确
        emoji_to_base64_dic = {'😃': 'A', '😄': 'B', '😆': 'C', '😅': 'D', '🤣': 'E', '😂': 'F', '🙂': 'G', '🙃': 'H', '😉': 'I', '😊': 'J', '🐵': 'K', '😍': 'L', '🐒': 'M', '😘': 'N', '😇': 'O', '😚': 'P', '🐶': 'Q', '😋': 'R', '😜': 'S', '🤗': 'T', '🐱': 'U', '🦁': 'V', '🤔': 'W', '😴': 'X', '😷': 'Y', '🤒': 'Z', '🤕': 'a', '🤢': 'b', '🐴': 'c', '🤧': 'd', '🐮': 'e', '🐷': 'f', '😵': 'g', '🐭': 'h', '😎': 'i', '🤓': 'j', '🐧': 'k', '😟': 'l', '😯': 'm', '😳': 'n', '😲': 'o', '🐸': 'p', '🍋': 'q', '😧': 'r', '😥': 's', '😢': 't', '😭': 'u', '😱': 'v', '😖': 'w', '😣': 'x', '😓': 'y', '🌶': 'z', '👻': '0', '💖': '1', '💌': '2', '💔': '3', '👰': '4', '🍖': '5', '🎅': '6', '💇': '7', '🚶': '8', '🏇': '9', '🛀': '+', '🛌': '/', '💏': '='}
        res = ''
        for i in emoji_text:
            if i in emoji_to_base64_dic:
                res += emoji_to_base64_dic[i]
            else:
                res += '?'
        return res
