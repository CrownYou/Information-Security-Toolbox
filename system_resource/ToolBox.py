# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import random
import os
from windnd import hook_dropfiles
import base64
import copy
import time
import math
from random import randint
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import jieba
import unvcode
import pickle
from reedsolo import RSCodec
from cryptography.hazmat.primitives import hashes  # pip install cryptography
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from Crypto.Protocol.SecretSharing import Shamir
from system_resource.ToolKit import Tools

window = frm = mid_font = icon_path = colors = ind = zoom = ...
alive = False


def initiation(_window, _frm, _mid_font, _icon_path, _colors, _ind, _zoom):
    global window, frm, mid_font, icon_path, colors, ind, zoom
    window = _window
    frm = _frm
    mid_font = _mid_font
    icon_path = _icon_path
    colors = _colors
    ind = _ind
    zoom = _zoom


def generate_random_char():
    label1 = tk.Label(frm, text='请选择随机字符串包含的元素：', font=mid_font)
    label1.pack()
    frm1 = tk.Frame(frm)
    frm1.pack()
    number = tk.StringVar()
    number.set('1')
    cb1 = tk.Checkbutton(frm1, text='数字', variable=number, onvalue='1', offvalue='0', font=mid_font)
    cb1.grid(row=1, column=1, padx=5)
    upper_eng = tk.StringVar()
    upper_eng.set('1')
    cb2 = tk.Checkbutton(frm1, text='大写英文字母', variable=upper_eng, onvalue='1', offvalue='0', font=mid_font)
    cb2.grid(row=1, column=2, padx=5)
    lower_eng = tk.StringVar()
    lower_eng.set('1')
    cb3 = tk.Checkbutton(frm1, text='小写英文字母', variable=lower_eng, onvalue='1', offvalue='0', font=mid_font)
    cb3.grid(row=1, column=3, padx=5)
    mark = tk.StringVar()
    mark.set('1')
    cb9 = tk.Checkbutton(frm1, text='特殊符号', variable=mark, onvalue='1', offvalue='0', font=mid_font)
    cb9.grid(row=1, column=4, padx=5)
    upper_greek = tk.StringVar()
    upper_greek.set('0')
    cb4 = tk.Checkbutton(frm1, text='大写希腊字母', variable=upper_greek, onvalue='1', offvalue='0', font=mid_font)
    cb4.grid(row=1, column=5, padx=5)
    lower_greek = tk.StringVar()
    lower_greek.set('0')
    cb5 = tk.Checkbutton(frm1, text='小写希腊字母', variable=lower_greek, onvalue='1', offvalue='0', font=mid_font)
    cb5.grid(row=1, column=6, padx=5)
    frm2 = tk.Frame(frm)
    frm2.pack()
    upper_russian = tk.StringVar()
    upper_russian.set('0')
    cb6 = tk.Checkbutton(frm2, text='大写俄语字母', variable=upper_russian, onvalue='1', offvalue='0', font=mid_font)
    cb6.grid(row=1, column=1)
    lower_russian = tk.StringVar()
    lower_russian.set('0')
    cb7 = tk.Checkbutton(frm2, text='小写俄语字母', variable=lower_russian, onvalue='1', offvalue='0', font=mid_font)
    cb7.grid(row=1, column=2, padx=10)
    customize = tk.StringVar()
    customize.set('0')
    cb8 = tk.Checkbutton(frm2, text='自定义字符集：', variable=customize, onvalue='1', offvalue='0', font=mid_font)
    cb8.grid(row=1, column=3)
    entry1 = tk.Entry(frm2, font=mid_font, width=31)
    entry1.grid(row=1, column=4)
    frm12 = tk.Frame(frm)
    frm12.pack()
    label15 = tk.Label(frm12, text='请输入随机字符串不包含的元素：', font=mid_font, fg='red')
    label15.grid(row=1, column=1)
    entry10 = tk.Entry(frm12, font=mid_font, width=31, fg='red')
    entry10.grid(row=1, column=2)
    frm3 = tk.Frame(frm)
    frm3.pack()
    label2 = tk.Label(frm3, text='请设置随机字符串的长度：', font=mid_font)
    label2.grid(row=1, column=1)
    entry2 = tk.Entry(frm3, font=mid_font, width=4)
    entry2.grid(row=1, column=2)
    entry2.insert('end', '20')
    frm4 = tk.Frame(frm)
    frm4.pack()

    def process():
        label14.config(text=' ')
        char_set = ''
        if number.get() == '1':
            char_set += '0123456789'
        if upper_eng.get() == '1':
            char_set += 'QWERTYUIOPASDFGHJKLZXCVBNM'
        if lower_eng.get() == '1':
            char_set += 'qwertyuiopasdfghjklzxcvbnm'
        if upper_greek.get() == '1':
            char_set += 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
        if lower_greek.get() == '1':
            char_set += 'αβγδεζηθικλμνξοπρστυφχψω'
        if upper_russian.get() == '1':
            char_set += 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ'
        if lower_russian.get() == '1':
            char_set += 'абвгдеёжзийклмнопрстуфхцчшщыэюя'
        if customize.get() == '1':
            char_set += entry1.get()
        if mark.get() == '1':
            char_set += r'''`~!@#$%^&*()-=_+[]{}\|;:'",.<>/?'''
        char_set = set(char_set)  # 去除char_set中的重复元素
        leach = ''.join(set(entry10.get()))  # 找到需要过滤掉的元素
        char_set = ''.join([s for s in char_set if s not in leach])  # 将char_set过滤
        try:
            length = eval(entry2.get())
            assert isinstance(length, int) and length >= 1
        except Exception:
            messagebox.showerror('长度类型错误', '字符串的长度应为正整数')
            return 0
        for i in range(5):
            result = ''
            for j in range(length):
                try:
                    result += random.choice(char_set)
                except Exception:
                    pass  # 有时char_set中为空，那么就跳过
            if i == 0:
                Tools.reset(entry3)
                entry3.insert('end', result)
            elif i == 1:
                Tools.reset(entry4)
                entry4.insert('end', result)
            elif i == 2:
                Tools.reset(entry5)
                entry5.insert('end', result)
            elif i == 3:
                Tools.reset(entry6)
                entry6.insert('end', result)
            elif i == 4:
                Tools.reset(entry7)
                entry7.insert('end', result)

    def select_all():
        number.set('1')
        upper_eng.set('1')
        lower_eng.set('1')
        upper_greek.set('1')
        lower_greek.set('1')
        upper_russian.set('1')
        lower_russian.set('1')
        customize.set('1')
        mark.set('1')

    def deselect_all():
        number.set('0')
        upper_eng.set('0')
        lower_eng.set('0')
        upper_greek.set('0')
        lower_greek.set('0')
        upper_russian.set('0')
        lower_russian.set('0')
        customize.set('0')
        mark.set('0')

    button1 = tk.Button(frm4, text='全选', font=mid_font, command=select_all)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm4, text='取消全选', font=mid_font, command=deselect_all)
    button2.grid(row=1, column=2, padx=20)
    button3 = tk.Button(frm4, text='开始随机生成', font=mid_font, command=process)
    button3.grid(row=1, column=3, padx=20)
    label3 = tk.Label(frm, text='生成结果为：', font=mid_font)
    label3.pack()
    frm5 = tk.Frame(frm)
    frm5.pack(pady=10)

    def copy1():
        Tools.copy(entry3, button4)

    label4 = tk.Label(frm5, text='1.', font=mid_font)
    label4.grid(row=1, column=1)
    entry3 = tk.Entry(frm5, width=88, font=mid_font)
    entry3.grid(row=1, column=2)
    button4 = tk.Button(frm5, text='复制', font=mid_font, command=copy1, fg=colors[ind])
    button4.grid(row=1, column=3)
    frm6 = tk.Frame(frm)
    frm6.pack(pady=10)

    def copy2():
        Tools.copy(entry4, button5)

    label5 = tk.Label(frm6, text='2.', font=mid_font)
    label5.grid(row=1, column=1)
    entry4 = tk.Entry(frm6, width=88, font=mid_font)
    entry4.grid(row=1, column=2)
    button5 = tk.Button(frm6, text='复制', font=mid_font, command=copy2, fg=colors[ind])
    button5.grid(row=1, column=3)
    frm7 = tk.Frame(frm)
    frm7.pack(pady=10)

    def copy3():
        Tools.copy(entry5, button6)

    label6 = tk.Label(frm7, text='3.', font=mid_font)
    label6.grid(row=1, column=1)
    entry5 = tk.Entry(frm7, width=88, font=mid_font)
    entry5.grid(row=1, column=2)
    button6 = tk.Button(frm7, text='复制', font=mid_font, command=copy3, fg=colors[ind])
    button6.grid(row=1, column=3)
    frm8 = tk.Frame(frm)
    frm8.pack(pady=10)

    def copy4():
        Tools.copy(entry6, button7)

    label7 = tk.Label(frm8, text='4.', font=mid_font)
    label7.grid(row=1, column=1)
    entry6 = tk.Entry(frm8, width=88, font=mid_font)
    entry6.grid(row=1, column=2)
    button7 = tk.Button(frm8, text='复制', font=mid_font, command=copy4, fg=colors[ind])
    button7.grid(row=1, column=3)
    frm9 = tk.Frame(frm)
    frm9.pack(pady=10)

    def copy5():
        Tools.copy(entry7, button8)

    label8 = tk.Label(frm9, text='5.', font=mid_font)
    label8.grid(row=1, column=1)
    entry7 = tk.Entry(frm9, width=88, font=mid_font)
    entry7.grid(row=1, column=2)
    button8 = tk.Button(frm9, text='复制', font=mid_font, command=copy5, fg=colors[ind])
    button8.grid(row=1, column=3)
    frm10 = tk.Frame(frm)
    frm10.pack()

    def drag1(files):
        label14.config(text=' ')
        file = files[0].decode("GBK")  # 用户拖入多个文件时，只取第一个
        if os.path.isdir(file):
            Tools.dragged_files(files, entry8)
        elif os.path.isfile(file):
            entry8.delete(0, 'end')
            entry8.insert('end', os.path.dirname(file))  # 只保留文件夹的名字

    def drag2(files):
        label14.config(text=' ')
        file = files[0].decode("GBK")  # 用户拖入多个文件时，只取第一个
        entry8.delete(0, 'end')
        entry8.insert('end', os.path.dirname(file))  # 在entry8中写入文件夹的名字
        entry9.delete(0, 'end')
        entry9.insert('end', os.path.splitext(os.path.basename(file))[0])  # 在entry9中写入文件的名字，并去掉后缀

    def reset1():
        Tools.reset(entry9)

    def save():
        global ind
        ind = (ind + 1) % 6
        label14.config(fg=colors[ind])
        save_file_name = entry9.get()
        for i in r':\/*?"<>|':
            if i in save_file_name:
                label14.config(text='保存失败，文件名称不能含有以下字符：\/*?"<>|:')
                return 0
        save_dir = entry8.get()
        if save_dir == '（在此拖入文件夹，默认为程序所在文件夹）' or save_dir == '':
            save_dir = os.getcwd()  # 获取程序所在的文件夹
        save_path = os.path.join(save_dir, save_file_name +'.txt')
        print('save_path:', save_path)
        try:
            with open(save_path, 'a', encoding='utf-8') as f:
                f.write('\n' + entry3.get())
                f.write('\n' + entry4.get())
                f.write('\n' + entry5.get())
                f.write('\n' + entry6.get())
                f.write('\n' + entry7.get())
            label14.config(text='保存成功')
        except Exception:
            label14.config(text='保存失败，路径有误')

    def open_folder():
        save_dir = entry8.get()
        if save_dir == '（在此拖入文件夹，默认为程序所在文件夹）' or save_dir == '':
            save_dir = os.getcwd()  # 获取程序所在的文件夹
        try:
            os.startfile(save_dir)
        except Exception:
            label14.config(text='路径错误，文件夹打开失败')

    label9 = tk.Label(frm10, text='可一键保存当前所有内容至', font=mid_font)
    label9.grid(row=1, column=1)
    entry8 = tk.Entry(frm10, width=40, font=mid_font)
    entry8.grid(row=1, column=2)
    entry8.insert('end', '（在此拖入文件夹，默认为程序所在文件夹）')
    hook_dropfiles(entry8, func=drag1)
    label10 = tk.Label(frm10, text='文件夹内的任意名称的txt文档中', font=mid_font)
    label10.grid(row=1, column=3)
    label11 = tk.Label(frm, text='若该文档已存在，则会在该文档后追加写入，不会覆盖前面的内容', font=mid_font)
    label11.pack()
    frm11 = tk.Frame(frm)
    frm11.pack()
    label12 = tk.Label(frm11, text='设置txt文档的名称：', font=mid_font)
    label12.grid(row=1, column=1)
    entry9 = tk.Entry(frm11, width=30, font=mid_font)
    entry9.grid(row=1, column=2)
    entry9.insert('end', '（可在此拖入txt文档）')
    hook_dropfiles(entry9, func=drag2)
    label13 = tk.Label(frm11, text='.txt', font=mid_font)
    label13.grid(row=1, column=3)
    button9 = tk.Button(frm11, text='重置', font=mid_font, command=reset1)
    button9.grid(row=1, column=4, padx=10)
    button10 = tk.Button(frm11, text='保存', font=mid_font, command=save)
    button10.grid(row=1, column=5, padx=10)
    button11 = tk.Button(frm11, text='打开文档所在文件夹', font=mid_font, command=open_folder)
    button11.grid(row=1, column=6, padx=10)
    label14 = tk.Label(frm, text=' ', font=mid_font, fg=colors[ind])
    label14.pack()


def base64converter():
    frm1 = tk.Frame(frm)
    frm1.pack()
    label1 = tk.Label(frm1, text='明文的编码方式：', font=mid_font)
    label1.grid(row=1, column=1)
    str_format = tk.StringVar()
    str_format.set('utf-8')
    option_menu1 = tk.OptionMenu(frm1, str_format, *('utf-8', 'gbk', '字节码'))
    option_menu1.config(font=mid_font)
    option_menu1.grid(row=1, column=2, padx=20)
    label_base64 = tk.Label(frm1, text='base64的编码方式：', font=mid_font)
    label_base64.grid(row=1, column=3, padx=20)
    base64_format = tk.StringVar()
    base64_format.set('正常')
    base64_option_menu = tk.OptionMenu(frm1, base64_format, *('正常', 'emoji'))
    base64_option_menu.grid(row=1, column=4)
    base64_option_menu.config(font=mid_font)
    intro_emoji_button = tk.Button(frm1, text='说明', font=mid_font, fg='blue', bd=0, command=Tools.intro_emoji)
    intro_emoji_button.grid(row=1, column=5, padx=10)
    frm2 = tk.Frame(frm)
    frm2.pack()
    frm_left = tk.Frame(frm2)
    frm_left.grid(row=1, column=1)
    text1 = tk.Text(frm_left, font=mid_font, width=40, height=24)
    text1.pack(pady=10)
    frm3 = tk.Frame(frm_left)
    frm3.pack()

    def reset1():
        Tools.reset(text1)

    def copy1():
        Tools.copy(text1, button2)

    button1 = tk.Button(frm3, text='重置', font=mid_font, command=reset1)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm3, text='复制', font=mid_font, command=copy1, fg=colors[ind])
    button2.grid(row=1, column=2, padx=20)

    frm_middle = tk.Frame(frm2)
    frm_middle.grid(row=1, column=2, padx=13)

    def left_to_right_b64_encode():
        origin_text = text1.get(1.0, 'end').rstrip('\n')
        try:
            if str_format.get() == 'utf-8':
                b64_text = base64.b64encode(origin_text.encode('utf-8')).decode('utf-8')
            elif str_format.get() == 'gbk':
                b64_text = base64.b64encode(origin_text.encode('gbk')).decode('utf-8')
            elif str_format.get() == '字节码':
                b64_text = base64.b64encode(eval(origin_text)).decode('utf-8')
            if base64_format.get() == 'emoji':
                b64_text = Tools.translate_base64_to_emoji(b64_text)
        except Exception:
            b64_text = '编码失败'
        Tools.reset(text2)
        text2.insert('end', b64_text)

    def right_to_left_b64_encode():
        origin_text = text2.get(1.0, 'end').rstrip('\n')
        try:
            if str_format.get() == 'utf-8':
                b64_text = base64.b64encode(origin_text.encode('utf-8')).decode('utf-8')
            elif str_format.get() == 'gbk':
                b64_text = base64.b64encode(origin_text.encode('gbk')).decode('utf-8')
            elif str_format.get() == '字节码':
                b64_text = base64.b64encode(eval(origin_text)).decode('utf-8')
            if base64_format.get() == 'emoji':
                b64_text = Tools.translate_base64_to_emoji(b64_text)
        except Exception:
            b64_text = '编码失败'
        Tools.reset(text1)
        text1.insert('end', b64_text)

    def left_to_right_b64_decode():
        b64_text = text1.get(1.0, 'end').rstrip('\n')
        try:
            if base64_format.get() == 'emoji':
                b64_text = Tools.translate_emoji_to_base64(b64_text)
            if str_format.get() == 'utf-8':
                origin_text = base64.b64decode(b64_text).decode('utf-8')
            elif str_format.get() == 'gbk':
                origin_text = base64.b64decode(b64_text).decode('gbk')
            elif str_format.get() == '字节码':
                origin_text = str(base64.b64decode(b64_text))
        except Exception:
            origin_text = '解码失败'
        Tools.reset(text2)
        text2.insert('end', origin_text)

    def right_to_left_b64_decode():
        b64_text = text2.get(1.0, 'end').rstrip('\n')
        try:
            if base64_format.get() == 'emoji':
                b64_text = Tools.translate_emoji_to_base64(b64_text)
            if str_format.get() == 'utf-8':
                origin_text = base64.b64decode(b64_text).decode('utf-8')
            elif str_format.get() == 'gbk':
                origin_text = base64.b64decode(b64_text).decode('gbk')
            elif str_format.get() == '字节码':
                origin_text = str(base64.b64decode(b64_text))
        except Exception:
            origin_text = '解码失败'
        Tools.reset(text1)
        text1.insert('end', origin_text)

    button3 = tk.Button(frm_middle, text='base64编码->', font=mid_font, command=left_to_right_b64_encode)
    button3.pack(pady=20)
    button4 = tk.Button(frm_middle, text='<-base64编码', font=mid_font, command=right_to_left_b64_encode)
    button4.pack(pady=40)
    button5 = tk.Button(frm_middle, text='base64解码->', font=mid_font, command=left_to_right_b64_decode)
    button5.pack(pady=40)
    button6 = tk.Button(frm_middle, text='<-base64解码', font=mid_font, command=right_to_left_b64_decode)
    button6.pack(pady=20)

    frm_right = tk.Frame(frm2)
    frm_right.grid(row=1, column=3)
    text2 = tk.Text(frm_right, font=mid_font, width=40, height=24)
    text2.pack(pady=10)
    frm4 = tk.Frame(frm_right)
    frm4.pack()

    def reset2():
        Tools.reset(text2)

    def copy2():
        Tools.copy(text2, button8)

    button7 = tk.Button(frm4, text='重置', font=mid_font, command=reset2)
    button7.grid(row=1, column=1, padx=20)
    button8 = tk.Button(frm4, text='复制', font=mid_font, command=copy2, fg=colors[ind])
    button8.grid(row=1, column=2, padx=20)


def confuse_qr_code():
    def drag(files):
        Tools.dragged_files(files, entry1)

    def _reset():
        Tools.reset(entry1)

    def process():
        hidden_frm.pack_forget()
        # 检查一下二维码图片是否正确，并把二维码数据读取到zoomed_qr_img中
        qr_path = Tools.get_path_from_entry(entry1)
        if os.path.exists(qr_path):
            temp_qr_path = f'_temp_qr_code{os.path.splitext(qr_path)[-1]}'
            Tools.read_all_and_write_all(qr_path, temp_qr_path)
            cv2.namedWindow('QR code')
            try:
                qr_img = cv2.imread(temp_qr_path)
                zoomed_qr_img = Tools.resize_pic(qr_img)
                cv2.imshow('QR code', zoomed_qr_img)
            except Exception as e:
                cv2.destroyAllWindows()
                Tools.delete_file(temp_qr_path)
                print(e)
                messagebox.showerror('图片格式错误', '图片的格式不正确')
                return 0
            os.remove(temp_qr_path)
        else:
            messagebox.showerror('图片错误', '图片地址错误')
            return 0

        def back_to_first():
            global alive
            alive = False
            try:
                cv2.destroyAllWindows()
                second_frm.pack_forget()
                first_frm.pack()
            except Exception:
                pass

        def select_qr_code(event, x, y, flags, param):
            nonlocal x_start, y_start, zoomed_qr_img_copy, qr_code_img
            if event == cv2.EVENT_LBUTTONDOWN:
                x_start, y_start = x, y
            elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
                zoomed_qr_img_copy = copy.deepcopy(zoomed_qr_img)
                cv2.rectangle(zoomed_qr_img_copy, (x_start, y_start), (x, y),
                              (randint(0, 255), randint(0, 255), randint(0, 255)), 2)
            elif event == cv2.EVENT_LBUTTONUP:
                row_begin = min(y_start, y) + 1  # 这里进行微调是因为线有2像素宽，要把线从图片中去掉
                row_end = max(y_start, y) - 1
                col_begin = min(x_start, x) + 1
                col_end = max(x_start, x) - 1
                qr_code_img = zoomed_qr_img_copy[row_begin: row_end, col_begin: col_end]

        global alive
        alive = True
        first_frm.pack_forget()
        second_frm = tk.Frame(frm)
        second_frm.pack()
        sf_label1 = tk.Label(second_frm, text='请在图片中框选出二维码的位置（按‘S’确认，按‘Q’放弃），不框选则意味着全选', font=mid_font, fg='red')
        sf_label1.grid(row=1)
        zoomed_qr_img_copy = copy.deepcopy(zoomed_qr_img)  # 这里的zoomed_qr_img_copy既包括二维码也包括二维码的背景
        x_start = y_start = qr_code_img = -1  # qr_code_img是用户框选出来的结果（二维码本体）
        cv2.setMouseCallback('QR code', select_qr_code)
        window.update()
        while alive:
            # 要退出这个循环，请使用alive = False
            cv2.imshow('QR code', zoomed_qr_img_copy)
            key = cv2.waitKey(10)  # 每隔10毫秒获取一下用户输入
            if key == ord('s'):
                if isinstance(qr_code_img, np.ndarray) and qr_code_img.shape != (0, 0, 3):
                    # 如果用户框选了二维码，那么就使用用户框选的部分
                    print('用户进行了框选二维码，这是框选出来的qr_code_img的大小：')
                    print(qr_code_img.shape)
                else:  # 如果用户按下‘S’键前没有框选二维码，那么就认为整张图片都是二维码
                    print('用户按下了s，并且没有进行框选，则认为选取结果为zoomed_qr_img的大小为：')
                    print(zoomed_qr_img.shape)
                    qr_code_img = zoomed_qr_img
                alive = False
            elif key == ord('q') or cv2.getWindowProperty('QR code', cv2.WND_PROP_VISIBLE) != 1:
                back_to_first()
                return 0

        # 在获取了用户框选的二维码图像后，接下来对它进行透视变换
        cv2.destroyAllWindows()
        sf_label1.destroy()
        alive = True

        @Tools.run_as_thread
        def intro_perspective():
            intro_window = tk.Toplevel()
            intro_window.title("图像透视变换介绍")
            intro_window.geometry(Tools.zoom_size('1272x758', zoom))
            intro_window.iconbitmap(icon_path)
            intro_canvas = tk.Canvas(intro_window, width=round(950 * zoom), height=round(550 * zoom))
            intro_canvas.pack()
            img = cv2.imread('system_resource\perspective_intro.png')
            if zoom > 1:
                img_resized = cv2.resize(img, dsize=None, fx=zoom, fy=zoom, interpolation=cv2.INTER_LINEAR)
            elif zoom < 1:
                img_resized = cv2.resize(img, dsize=None, fx=zoom, fy=zoom, interpolation=cv2.INTER_AREA)
            else:
                img_resized = copy.deepcopy(img)
            new_path = 'system_resource\perspective_intro2.png'
            cv2.imwrite(new_path, img_resized)
            intro_image_file = tk.PhotoImage(file=new_path)
            Tools.delete_file(new_path)
            intro_text = tk.Text(intro_window, font=mid_font, width=96, height=7)
            intro_text.pack()
            intro_text.insert('end', '''    由于一些互联网平台对于二维码的发布有严格限制，所以为了规避一些简单的常规审核，特此开发了这个二维码透视变换功能。它可以将二维码进行一定的畸变，从而导致二维码无法被直接读取，但是只要观察者从特定角度和位置进行扫码就能识别图像中的二维码内容。

            具体原理如上图所示，将原图像ABCD通过透视变换生成图像ABEF，并将ABEF显示在屏幕上。当人眼从特定角度和位置观察时，便可从ABEF中观察到原图ABCD的像。在本软件中，您可以通过调整代表眼睛位置的滑块，即可自由设置这个特定的观察角度和位置。（本软件中，1cm=28像素）''')
            while True:
                try:
                    intro_canvas.create_image(0, 0, anchor='nw', image=intro_image_file)
                except Exception:
                    pass
                time.sleep(1)

        sf_frm = tk.Frame(second_frm)
        sf_frm.pack()
        sf_frm1 = tk.Frame(sf_frm)
        sf_frm1.grid(row=1, column=1)
        sf_frm1_1 = tk.Frame(sf_frm1)
        sf_frm1_1.pack()
        sf_label2 = tk.Label(sf_frm1_1, text='透视变换示意图：', font=mid_font)
        sf_label2.grid(row=1, column=1, padx=10)
        sf_button1 = tk.Button(sf_frm1_1, text='说明', font=mid_font, fg='blue', bd=0, command=intro_perspective)
        sf_button1.grid(row=1, column=2, padx=10)
        perspective_canvas = tk.Canvas(sf_frm1, width=580, height=336)
        perspective_image = cv2.imread("system_resource\perspective_intro.png")
        print('perspective_image的大小为：')
        print(perspective_image.shape)
        resized_perspective_image = cv2.resize(perspective_image, (580, 336), interpolation=cv2.INTER_LINEAR)
        print('resized_perspective_image的大小为：')
        print(resized_perspective_image.shape)
        cv2.imwrite('_temp_pic.png', resized_perspective_image)
        perspective_file = tk.PhotoImage(file='_temp_pic.png')
        perspective_canvas.pack()
        os.remove('_temp_pic.png')
        sf_frm2 = tk.Frame(sf_frm)
        sf_frm2.grid(row=1, column=2)
        sf_label3 = tk.Label(sf_frm2, text='请在下方侧视图中调节眼睛（G）的位置：', font=mid_font)
        sf_label3.pack()
        sf_frm2_1 = tk.Frame(sf_frm2)
        sf_frm2_1.pack()
        canvas_2 = tk.Canvas(sf_frm2_1, width=550, height=300)
        canvas_2.grid(row=1, column=1)
        sf_frm2_2 = tk.Frame(sf_frm2_1)
        sf_frm2_2.grid(row=1, column=2)
        sf_label4 = tk.Label(sf_frm2_2, text='高度\n(cm):', font=mid_font)
        sf_label4.pack()  # 1 cm = 28 pixel
        height_scale = tk.Scale(sf_frm2_2, from_=100, to=10, orient=tk.VERTICAL, length=240, resolution=1, showvalue=1,
                                tickinterval=10)
        height_scale.pack()
        height_scale.set(35)
        sf_frm2_3 = tk.Frame(sf_frm2)
        sf_frm2_3.pack()
        sf_label5 = tk.Label(sf_frm2_3, text='水平距离 (cm):', font=mid_font)
        sf_label5.grid(row=1, column=1)
        distance_scale = tk.Scale(sf_frm2_3, from_=0, to=100, orient=tk.HORIZONTAL, length=360, resolution=1,
                                  showvalue=1, tickinterval=10)
        distance_scale.grid(row=1, column=2)
        distance_scale.set(70)
        sf_frm3 = tk.Frame(second_frm)
        sf_frm3.pack()
        sf_label6 = tk.Label(sf_frm3, text='眼睛的位置：图片的', font=mid_font)
        sf_label6.grid(row=1, column=1)
        selected_location = tk.StringVar()
        selected_location.set('上方')
        sf_option_menu1 = tk.OptionMenu(sf_frm3, selected_location, *('上方', '下方', '左侧', '右侧'))
        sf_option_menu1.config(font=mid_font)
        sf_option_menu1.grid(row=1, column=2)
        sf_bg_color_label = tk.Label(sf_frm3, text='背景颜色：', font=mid_font)
        sf_bg_color_label.grid(row=2, column=1)
        bg_color = tk.StringVar()
        bg_color.set('黑色')
        sf_bg_color_op_menu = tk.OptionMenu(sf_frm3, bg_color, *('黑色', '白色'))
        sf_bg_color_op_menu.grid(row=2, column=2)
        sf_bg_color_op_menu.config(font=mid_font)
        sf_true_width_height_frm = tk.Frame(second_frm)
        sf_true_width_height_frm.pack()
        twh_label1 = tk.Label(sf_true_width_height_frm, text='为了避免生成图像过大/过小，软件对其进行了缩放，这使得真实观察点与设定观察点有偏差', font=mid_font)
        twh_label1.pack()
        width_text_variable = tk.StringVar()
        width_text_variable.set('当前图像所属观察点的真实水平距离：xx cm')
        twh_label2 = tk.Label(sf_true_width_height_frm, textvariable=width_text_variable, font=mid_font)
        twh_label2.pack()
        height_text_variable = tk.StringVar()
        height_text_variable.set('  当前图像所属观察点的真实高度  ：xx cm')
        twh_label3 = tk.Label(sf_true_width_height_frm, textvariable=height_text_variable, font=mid_font)
        twh_label3.pack()
        angle_text_variable = tk.StringVar()
        angle_text_variable.set('  当前图像所属观察点的倾斜角度  ：xx 度')
        twh_label4 = tk.Label(sf_true_width_height_frm, textvariable=angle_text_variable, font=mid_font)
        twh_label4.pack()
        sf_frm4 = tk.Frame(second_frm)
        sf_frm4.pack()
        save_flag = False
        true_width = true_height = angle = 0

        @Tools.run_as_thread
        def save_outcome_img():
            nonlocal save_flag
            Tools.delete_file('pic_by_perspective_transformation.png')
            save_flag = True
            qr_dir = os.path.dirname(qr_path)
            qr_name, qr_suffix = os.path.splitext(os.path.basename(qr_path))
            direction = ''
            if selected_location.get() == '上方':
                direction = 'up'
            elif selected_location.get() == '下方':
                direction = 'down'
            elif selected_location.get() == '左侧':
                direction = 'left'
            elif selected_location.get() == '右侧':
                direction = 'right'
            out_path = os.path.join(qr_dir,
                                    qr_name + f'_{direction}_angle_{angle}degree{qr_suffix}')
            hidden_frm.pack()
            time.sleep(0.1)
            while True:
                if os.path.exists('pic_by_perspective_transformation.png'):
                    Tools.read_all_and_write_all('pic_by_perspective_transformation.png', out_path)
                    Tools.delete_file('pic_by_perspective_transformation.png')
                    Tools.reset(hf_entry1)
                    hf_entry1.insert('end', os.path.basename(out_path))
                    break
                print('未发现临时保存的结果图片，0.05秒后再找')
                time.sleep(0.05)

        sf_button2 = tk.Button(sf_frm4, text='放弃', font=mid_font, command=back_to_first)
        sf_button2.grid(row=1, column=1, padx=20)
        sf_button3 = tk.Button(sf_frm4, text='保存', font=mid_font, command=save_outcome_img)
        sf_button3.grid(row=1, column=2, padx=20)
        window.update()
        cv2.namedWindow('Outcome image')

        # 这里额外开了一个监听函数，是为了防止show_outcome_img在监听窗口关闭时不及时相应，导致出bug
        @Tools.run_as_thread
        def listening_closing_outcome_img_window():
            while alive:
                if cv2.getWindowProperty('Outcome image', cv2.WND_PROP_VISIBLE) != 1:
                    back_to_first()

        @Tools.run_as_thread
        def show_outcome_img():
            nonlocal true_width, true_height, angle
            perspective_canvas.create_image(0, 0, anchor='nw', image=perspective_file)
            # 上面这行代码的位置不要移动，一旦放到这个函数之外，这个函数就会失效！！！
            A = [0, 0]
            # 这里先确定一下d, h, location的初始值，当用户输入和上一次的值一致时就不要浪费计算资源
            d = h = location = previous_bg_color = -1
            while alive:
                # 先根据用户的观察方向旋转图片，最后透视变换完成后，还要再旋转回来，并把最后的图片大小改为qr_code_img的大小
                location_get = selected_location.get()
                if location_get == location:  # 如果用户的输入没有改变的话，就不要重复计算了
                    location_changed = False
                    pass
                else:
                    location = location_get
                    location_changed = True
                    qr_code_img_copy = copy.deepcopy(qr_code_img)
                    if location_get == '下方':
                        qr_code_img_copy = np.rot90(qr_code_img_copy, 2)
                    elif location_get == '上方':
                        pass
                    elif location_get == '左侧':
                        qr_code_img_copy = np.rot90(qr_code_img_copy, 3)
                    elif location_get == '右侧':
                        qr_code_img_copy = np.rot90(qr_code_img_copy, 1)
                    # 根据用户的输入将侧视图plot出来
                    l = qr_code_img_copy.shape[0]  # 获取旋转后的qr_code_img_copy的高（height/rows）
                    print('l的长度为：', l)  # 如果选择上下侧，则l为图片的高度：.shape[0]，否则为图片的宽度：l.shape[1]
                d_get = distance_scale.get() * 28  # 把厘米换算成像素
                h_get = height_scale.get() * 28 if height_scale.get() * 28 > l+50 else l+50  # 眼睛的高度不能比图片的高度还小
                current_bg_color = bg_color.get()
                if current_bg_color == previous_bg_color:
                    color_changed = False
                else:
                    color_changed = True
                    previous_bg_color = current_bg_color
                if d == d_get and h == h_get and not location_changed and not color_changed and not save_flag:  # 如果用户的输入没有改变的话，就不要重复计算了
                    try:  # 有时候canvans_2的图片会自动消失，所以要时不时更新
                        pic = tk.PhotoImage(file='myplot.png')
                        canvas_2.create_image(0, 0, anchor='nw', image=pic)
                    except Exception:
                        pass
                    time.sleep(0.5)
                    continue
                else:
                    d = d_get
                    h = h_get
                G = [d, h]
                print('G点的坐标是：', G)
                # 这里需要求解D点的坐标（x，y），根据G在AD中垂线上，且AD长为l列方程
                x = sp.Symbol('x')
                eq_x = 2 * d * x + 2 * h * ((l ** 2 - x ** 2) ** 0.5) - l ** 2
                sol_x = sp.solve(eq_x, x)
                x = round(sol_x[0], 2)
                y = sp.Symbol('y')
                eq_y = -2 * d * ((l ** 2 - y ** 2) ** 0.5) + 2 * h * y - l ** 2
                sol_y = sp.solve(eq_y, y)
                y = round(sol_y[0], 2)
                D = [x, y]
                H = [x / 2, y / 2]
                print('D点的坐标是：', D)
                print('H点的坐标是：', H)
                # 再求解F的坐标（a，0），根据F在GD与x轴的交点上
                a = round(h * (d - x) / (y - h) + d, 2)
                F = [a, 0]
                print('F点的坐标为：', F)
                # 之后需要根据这些点的坐标plot出侧视图
                plt.figure(figsize=(5.5, 3))
                plt.xlim((int(a - 100), int(d + 100)))
                plt.ylim((-100, int(h + 100)))
                plt.plot([G[0], F[0]], [G[1], F[1]], color='blue', linewidth=2, linestyle='--')
                plt.plot([G[0], H[0]], [G[1], H[1]], color='red', linewidth=2, linestyle='--')
                plt.plot([A[0], D[0]], [A[1], D[1]], color='black', linewidth=2, linestyle='--')
                plt.plot([A[0], F[0]], [A[1], F[1]], color='green', linewidth=2)
                plt.scatter([G[0], D[0], F[0], H[0], A[0]], [G[1], D[1], F[1], H[1], A[1]], marker='o')
                plt.annotate('G', xy=(d, h), xytext=(d - 130, h), weight='bold')
                plt.annotate('D', xy=(x, y), xytext=(x - 40, y + 40), weight='bold')
                plt.annotate('F', xy=(a, 0), xytext=(a, 70), weight='bold')
                plt.annotate('H', xy=(x / 2, y / 2), xytext=(x / 2 + 100, y / 2), weight='bold')
                plt.annotate('A', xy=(0, 0), xytext=(100, 0), weight='bold')
                # 把plot后的图保存至myplot.png
                plt.savefig('myplot.png')
                plt.close('all')
                # 之后展示在canvas_2中
                pic = tk.PhotoImage(file='myplot.png')
                # canvas_2.delete(tk.ALL)
                canvas_2.create_image(0, 0, anchor='nw', image=pic)
                # 然后就是对图片进行透视变换
                b = qr_code_img_copy.shape[1]  # 获取旋转后的qr_code_img_copy的宽（width/cols）
                print('b的长度为：', b)  # b: bottom，代表底边的长
                # 原始图像的四个顶点
                src_pts = np.float32([[0, 0], [b, 0], [b, l], [0, l]])
                print('ABCD的坐标为：', [[0, 0], [b, 0], [b, l], [0, l]])
                # 目标图像的四个顶点
                dst_pts = np.float32([[y * b / (2 * (h - y)), 0], [(2 * h * b - y * b) / (2 * (h - y)), 0],
                                      [h * b / (h - y), (x * h - d * y) / (y - h)], [0, (x * h - d * y) / (y - h)]])
                print('ABEF的坐标为：', [[y * b / (2 * (h - y)), 0], [(2 * h * b - y * b) / (2 * (h - y)), 0],
                                    [h * b / (h - y), (x * h - d * y) / (y - h)], [0, (x * h - d * y) / (y - h)]])
                # 计算变换矩阵
                M = cv2.getPerspectiveTransform(src_pts, dst_pts)
                # 对原始图像进行透视变换
                try:
                    dst = cv2.warpPerspective(qr_code_img_copy, M, (
                    round(h * b / (h - y)), round((x * h - d * y) / (y - h))))  # 括号内的是宽高，需是整数
                    if selected_location.get() == '下方':
                        dst = np.rot90(dst, 2)
                    elif selected_location.get() == '上方':
                        pass
                    elif selected_location.get() == '左侧':
                        dst = np.rot90(dst, -3)
                    elif selected_location.get() == '右侧':
                        dst = np.rot90(dst, -1)
                    # 对结果进行缩放，只要把最长的那一条边缩放到round(900*zoom)像素即可
                    dst_cols, dst_rows, dst_channels = dst.shape
                    zoom_scale = round(900*zoom / dst_cols, 2) if dst_cols > dst_rows else round(900*zoom / dst_rows, 2)
                    true_width = round(zoom_scale * d / 28)
                    width_text_variable.set(f'当前图像所属观察点的真实水平距离：{true_width} cm')
                    true_height = round(zoom_scale * h / 28)
                    height_text_variable.set(f'  当前图像所属观察点的真实高度  ：{true_height} cm')
                    angle = round(math.degrees(math.atan(true_height / true_width))) if true_width > 0 else 90
                    angle_text_variable.set(f'  当前图像所属观察点的倾斜角度  ：{angle} 度')
                    outcome_img = cv2.resize(dst, (0, 0), fx=zoom_scale, fy=zoom_scale, interpolation=cv2.INTER_AREA)
                except Exception:
                    pass  # 有时眼睛的位置会使得ABEF不存在或者过大，所以这种情况就跳过
                if bg_color.get() == '白色':
                    outcome_img = Tools.convert_black_background_to_white(outcome_img)  # 将图像的黑边转为白边
                cv2.imshow('Outcome image', outcome_img)
                if save_flag:
                    cv2.imwrite('pic_by_perspective_transformation.png', outcome_img)
                    print('已将结果临时保存在程序目录下的pic_by_perspective_transformation.png')
                    break
                time.sleep(0.5)
            Tools.delete_file('myplot.png')
            cv2.destroyAllWindows()

        listening_closing_outcome_img_window()
        show_outcome_img()

    first_frm = tk.Frame(frm)
    first_frm.pack()
    label1 = tk.Label(first_frm, text='请拖入需要进行逆透视变换的二维码图片或输入地址：', font=mid_font)
    label1.pack()
    entry1 = tk.Entry(first_frm, width=59, font=mid_font)
    entry1.pack()
    hook_dropfiles(entry1, func=drag)
    frm1 = tk.Frame(first_frm)
    frm1.pack()
    button1 = tk.Button(frm1, text='重置文件', font=mid_font, command=_reset)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm1, text='开始处理', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=20)
    hidden_frm = tk.Frame(first_frm)
    hf_label1 = tk.Label(hidden_frm, text='结果已保存至原二维码图像所在文件夹中的：', font=mid_font)
    hf_label1.pack()
    hf_entry1 = tk.Entry(hidden_frm, font=mid_font, width=59)
    hf_entry1.pack()

    def open_outcome_folder():
        if os.path.exists(Tools.get_path_from_entry(entry1)):
            save_dir = os.path.dirname(Tools.get_path_from_entry(entry1))
            os.startfile(save_dir)
        else:
            messagebox.showerror('找不到该文件', '找不到该文件了')

    hf_button1 = tk.Button(hidden_frm, text='打开文件所在文件夹', font=mid_font, command=open_outcome_folder)
    hf_button1.pack()


def hide_qr_code():
    first_frm = tk.Frame(frm)
    first_frm.pack()

    def drag1(files):
        Tools.dragged_files(files, entry1)

    def drag2(files):
        Tools.dragged_files(files, entry2)

    label1 = tk.Label(first_frm, text='请拖入需要隐藏的二维码图片或输入地址：', font=mid_font)
    label1.pack()
    entry1 = tk.Entry(first_frm, width=59, font=mid_font)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)
    label2 = tk.Label(first_frm, text='请拖入一张载体图片来隐藏上面的图片：', font=mid_font)
    label2.pack()
    entry2 = tk.Entry(first_frm, width=59, font=mid_font)
    entry2.pack()
    hook_dropfiles(entry2, func=drag2)
    frm2 = tk.Frame(first_frm)
    frm2.pack()
    label3 = tk.Label(frm2, text='请选择结果的保存位置：', font=mid_font)
    label3.grid(row=1, column=1)
    var1 = tk.StringVar()
    var1.set('二维码图片所在文件夹')
    optionmenu1 = tk.OptionMenu(frm2, var1, *('二维码图片所在文件夹', '载体图片所在文件夹'))
    optionmenu1.grid(row=1, column=2)
    optionmenu1.config(font=mid_font)
    frm1 = tk.Frame(first_frm)
    frm1.pack()

    def reset():
        Tools.reset(entry1)
        Tools.reset(entry2)
        frm3.pack_forget()

    def confirm():
        global alive
        frm3.pack_forget()
        # 获取二维码图片
        qr_path = Tools.get_path_from_entry(entry1)
        if os.path.exists(qr_path):
            temp_qr_path = f'_temp_logo{os.path.splitext(qr_path)[-1]}'
            Tools.read_all_and_write_all(qr_path, temp_qr_path)
            try:
                qr_img = cv2.imread(temp_qr_path)
                qr_img = Tools.resize_pic(qr_img)
                cv2.imshow('image', qr_img)
            except Exception:
                Tools.delete_file(temp_qr_path)
                messagebox.showerror('二维码图片格式错误', '二维码图片的格式不正确')
                return 0
            os.remove(temp_qr_path)
            cv2.destroyAllWindows()
        else:
            messagebox.showerror('二维码图片地址错误', '二维码图片地址错误')
            return 0

        # 获取背景图片
        back_path = Tools.get_path_from_entry(entry2)
        if os.path.exists(back_path):
            temp_back_path = f'_temp_back{os.path.splitext(back_path)[-1]}'
            Tools.read_all_and_write_all(back_path, temp_back_path)
            try:
                back_img = cv2.imread(temp_back_path)
                zoomed_bg_img = Tools.resize_pic(back_img)
                cv2.imshow('outcome image', zoomed_bg_img)
            except Exception:
                Tools.delete_file(temp_back_path)
                messagebox.showerror('载体图片格式错误', '载体图片的格式不正确')
                return 0
            os.remove(temp_back_path)
            bg_rows, bg_cols, _ = zoomed_bg_img.shape
            bg_img = copy.deepcopy(zoomed_bg_img)
            # 检查完两张图片都没有问题后，进入下一阶段

            def apply(*args):  # 根据用户设定的参数放置二维码
                nonlocal bg_img
                sf_label7.pack()
                window.update()
                sf_label7.pack_forget()
                # 获取一下用户设定的中心点
                try:
                    center_x = eval(sf_entry2.get())
                    assert isinstance(center_x, int) and 0 <= center_x <= bg_cols
                except Exception:
                    Tools.reset(sf_entry2)
                    center_x = round(bg_cols / 2)
                    sf_entry2.insert(0, center_x)
                try:
                    center_y = eval(sf_entry3.get())
                    assert isinstance(center_y, int) and 0 <= center_y <= bg_rows
                except Exception:
                    Tools.reset(sf_entry3)
                    center_y = round(bg_rows / 2)
                    sf_entry3.insert(0, center_y)
                # 再处理一下用户设定的缩放程度
                try:
                    set_resize = eval(sf_entry1.get())
                    assert (isinstance(set_resize, int) or isinstance(set_resize, float)) and 0 <= set_resize
                except Exception:
                    Tools.reset(sf_entry1)
                    sf_entry1.insert(0,  '0.5')
                    set_resize = 0.5
                # 将背景图片进行拷贝后再处理
                bg_img = copy.deepcopy(zoomed_bg_img)
                # 根据用户设定的qr_code的位置和大小，确定一下roi的位置（即确定qr_code要放在背景图片的哪个位置）
                if set_resize <= 1.0:
                    resized_qr_img = cv2.resize(qr_img, None, fx=set_resize, fy=set_resize, interpolation=cv2.INTER_AREA)
                else:
                    resized_qr_img = cv2.resize(qr_img, None, fx=set_resize, fy=set_resize, interpolation=cv2.INTER_CUBIC)
                qr_rows, qr_cols, _ = resized_qr_img.shape
                qr_start_x, qr_end_x, roi_start_x, roi_end_x, qr_start_y, qr_end_y, roi_start_y, roi_end_y \
                    = Tools.process_roi(bg_cols, qr_cols, center_x, bg_rows, qr_rows, center_y)
                roi = bg_img[roi_start_y: roi_end_y, roi_start_x: roi_end_x]
                print('roi.shape:', roi.shape)
                processed_qr_img = resized_qr_img[qr_start_y: qr_end_y, qr_start_x: qr_end_x]
                print('processed_qr_img.shape:', processed_qr_img.shape)
                # 根据二维码的颜色深浅来确定掩膜，用于后续处理roi
                qr2gray = cv2.cvtColor(processed_qr_img, cv2.COLOR_BGR2GRAY)
                _, dark_mask = cv2.threshold(qr2gray, 128, 255, cv2.THRESH_BINARY)  # dark_mask 是遮住了黑色部分的掩膜（剩余白色部分）
                light_mask = cv2.bitwise_not(dark_mask)  # light_mask 是遮住了白色部分的掩膜（剩余黑色部分）
                print('dark_mask.shape:', dark_mask.shape)
                print('light_mask.shape:', light_mask.shape)
                # 将roi中对应二维码黑色部分的地方颜色加深（用light_mask）
                dark_roi = np.zeros(roi.shape, dtype=np.uint8)
                down_threshold = [round((1 - contrast_var.get()) * 128)] * 3
                for i in range(roi.shape[0]):
                    for j in range(roi.shape[1]):
                        if roi[i, j][0] > down_threshold[0] or roi[i, j][1] > down_threshold[1] or roi[i, j][2] > down_threshold[2]:
                            # 如果像素值除以1.5就足够，就除以1.5，不然就除以2至至少保顶
                            if roi[i, j][0] / 1.5 < down_threshold[0] and roi[i, j][1] / 1.5 < down_threshold[1] and roi[i, j][2] / 1.5 < down_threshold[2]:
                                dark_roi[i, j] = roi[i, j] / 1.5
                            else:
                                dark_roi[i, j] = np.clip(roi[i, j] / 2, [0, 0, 0], down_threshold)
                        else:
                            dark_roi[i, j] = roi[i, j]
                print('dark_roi.shape:', dark_roi.shape)
                dark_roi = cv2.bitwise_and(dark_roi, dark_roi, mask=light_mask)  # 再去掉对应二维码白色部分的roi
                # 将roi中对应二维码白色部分的地方颜色变亮（用dark_mask）
                light_roi = np.zeros(roi.shape, dtype=np.uint8)
                up_threshold = [round((1 + contrast_var.get()) * 128)] * 3
                for i in range(roi.shape[0]):
                    for j in range(roi.shape[1]):
                        if roi[i, j][0] < up_threshold[0] or roi[i, j][1] < up_threshold[1] or roi[i, j][2] < up_threshold[2]:
                            # 如果像素值乘1.5就足够，就乘1.5，不然就乘2至至少保底
                            if roi[i, j][0] * 1.5 > up_threshold[0] and roi[i, j][1] * 1.5 > up_threshold[1] and roi[i, j][2] * 1.5 > up_threshold[2]:
                                light_roi[i, j] = np.clip(roi[i, j] * 1.5, up_threshold, [255, 255, 255])
                            else:
                                light_roi[i, j] = np.clip(roi[i, j] * 2, up_threshold, [255, 255, 255])
                        else:
                            light_roi[i, j] = roi[i, j]
                light_roi = cv2.bitwise_and(light_roi, light_roi, mask=dark_mask)  # 再去掉对应二维码白色部分的roi
                print('light_roi.shape:', light_roi.shape)
                dst_roi = cv2.add(dark_roi, light_roi)
                bg_img[roi_start_y: roi_end_y, roi_start_x: roi_end_x] = dst_roi
                cv2.imshow('outcome image', bg_img)

            def put_qr_code(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    Tools.reset(sf_entry2)
                    Tools.reset(sf_entry3)
                    sf_entry2.insert(0, x)
                    sf_entry3.insert(0, y)
                    apply()

            def back_to_first():
                global alive
                alive = False
                cv2.destroyAllWindows()
                try:
                    second_frm.pack_forget()
                    first_frm.pack()
                except Exception:
                    pass

            def save():
                cv2.destroyAllWindows()
                temp_outpath = 'with_hidden_qr.png'
                outname = f'{os.path.splitext(os.path.basename(back_path))[0]}_with_hidden_qr.png'
                cv2.imwrite(temp_outpath, bg_img)
                if var1.get() == '二维码图片所在文件夹':
                    save_dir = os.path.dirname(qr_path)
                elif var1.get() == '载体图片所在文件夹':
                    save_dir = os.path.dirname(back_path)
                if os.getcwd() != save_dir:  # 如果软件所在文件夹不是用户选择的文件夹，那么就进行移动
                    outpath = os.path.join(save_dir, outname)
                    Tools.read_all_and_write_all(temp_outpath, outpath)
                    Tools.delete_file(temp_outpath)
                else:
                    os.rename(temp_outpath, outname)
                label4.config(text=f'结果保存至{var1.get()}中的：')
                Tools.reset(entry3)
                entry3.insert('end', outname)
                frm3.pack()
                first_frm.pack()
                second_frm.pack_forget()

            @Tools.run_as_thread
            def listening_closing_window():
                while alive:
                    if cv2.getWindowProperty('outcome image', cv2.WND_PROP_VISIBLE) != 1:
                        back_to_first()
                    time.sleep(0.1)

            alive = True
            cv2.setMouseCallback('outcome image', put_qr_code)
            listening_closing_window()
            first_frm.pack_forget()
            second_frm = tk.Frame(frm)
            second_frm.pack()
            sf_label1 = tk.Label(second_frm, text='请在载体图片上单击二维码图片隐藏的位置：', fg='red', font=mid_font)
            sf_label1.pack()
            sf_label3 = tk.Label(second_frm, text='二维码中心点的位置（左上角为原点）：', font=mid_font)
            sf_label3.pack()
            sf_frm3 = tk.Frame(second_frm)
            sf_frm3.pack()
            sf_label4 = tk.Label(sf_frm3, text='x：', font=mid_font)
            sf_label4.grid(row=1, column=1)
            sf_entry2 = tk.Entry(sf_frm3, width=4, font=mid_font)
            sf_entry2.grid(row=1, column=2)
            sf_entry2.bind('<Return>', apply)
            sf_label5 = tk.Label(sf_frm3, text='像素  y：', font=mid_font)
            sf_label5.grid(row=1, column=3)
            sf_entry3 = tk.Entry(sf_frm3, width=4, font=mid_font)
            sf_entry3.grid(row=1, column=4)
            sf_entry3.bind('<Return>', apply)
            sf_label6 = tk.Label(sf_frm3, text='像素', font=mid_font)
            sf_label6.grid(row=1, column=5)
            sf_frm1 = tk.Frame(second_frm)
            sf_frm1.pack()
            sf_label2 = tk.Label(sf_frm1, text='请选择二维码图片的缩放程度：', font=mid_font)
            sf_label2.grid(row=1, column=1)
            sf_entry1 = tk.Entry(sf_frm1, width=4, font=mid_font)
            sf_entry1.grid(row=1, column=2)
            sf_entry1.insert('end', '0.5')
            sf_entry1.bind('<Return>', apply)
            sf_label8 = tk.Label(second_frm, text='请设置隐藏的二维码图片的最小对比度：', font=mid_font)
            sf_label8.pack()
            contrast_var = tk.DoubleVar()
            contrast_var.set(0.05)
            sf_scale1 = tk.Scale(second_frm, from_=0, to=1, variable=contrast_var, orient=tk.HORIZONTAL, length=500, showvalue=1, tickinterval=0.1, resolution=0.01)
            sf_scale1.pack()
            sf_frm2 = tk.Frame(second_frm)
            sf_frm2.pack()
            sf_button1 = tk.Button(sf_frm2, text='放弃', font=mid_font, command=back_to_first)
            sf_button1.grid(row=1, column=1, padx=20)
            sf_button2 = tk.Button(sf_frm2, text='应用', font=mid_font, command=apply)
            sf_button2.grid(row=1, column=2, padx=20)
            sf_button3 = tk.Button(sf_frm2, text='保存', font=mid_font, command=save)
            sf_button3.grid(row=1, column=3, padx=20)
            sf_label7 = tk.Label(second_frm, text='正在处理，请稍候，不要频繁操作', fg='red', font=mid_font)

        else:
            messagebox.showerror('载体图片地址错误', '载体图片地址错误')

    button1 = tk.Button(frm1, text='重置', command=reset, font=mid_font)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm1, text='确定', command=confirm, font=mid_font)
    button2.grid(row=1, column=2, padx=20)
    frm3 = tk.Frame(first_frm)
    label4 = tk.Label(frm3, text='结果保存至...中的：', font=mid_font)
    label4.pack()
    entry3 = tk.Entry(frm3, width=59, font=mid_font)
    entry3.pack()


def invisible_qr():
    first_frm = tk.Frame(frm)
    first_frm.pack()

    def drag1(files):
        Tools.dragged_files(files, entry1)

    def drag2(files):
        Tools.dragged_files(files, entry2)

    label1 = tk.Label(first_frm, text='请拖入需要隐藏的二维码图片或输入地址：', font=mid_font)
    label1.pack()
    entry1 = tk.Entry(first_frm, width=59, font=mid_font)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)
    label2 = tk.Label(first_frm, text='请拖入一张载体图片来隐藏上面的图片：', font=mid_font)
    label2.pack()
    entry2 = tk.Entry(first_frm, width=59, font=mid_font)
    entry2.pack()
    hook_dropfiles(entry2, func=drag2)
    frm2 = tk.Frame(first_frm)
    frm2.pack()
    label3 = tk.Label(frm2, text='请选择结果的保存位置：', font=mid_font)
    label3.grid(row=1, column=1)
    var1 = tk.StringVar()
    var1.set('二维码图片所在文件夹')
    optionmenu1 = tk.OptionMenu(frm2, var1, *('二维码图片所在文件夹', '载体图片所在文件夹'))
    optionmenu1.grid(row=1, column=2)
    optionmenu1.config(font=mid_font)
    frm1 = tk.Frame(first_frm)
    frm1.pack()

    def reset():
        Tools.reset(entry1)
        Tools.reset(entry2)
        frm3.pack_forget()

    def confirm():
        global alive
        frm3.pack_forget()

        # 获取背景图片 -> bg_img（BGRA格式，四通道）
        back_path = Tools.get_path_from_entry(entry2)
        if os.path.exists(back_path):
            temp_back_path = f'_temp_back{os.path.splitext(back_path)[-1]}'
            Tools.read_all_and_write_all(back_path, temp_back_path)
            try:
                back_img = cv2.imread(temp_back_path, cv2.IMREAD_UNCHANGED)  # 读取时保留原格式包括alpha通道
                zoomed_bg_img = Tools.resize_pic(back_img)
                zoomed_bg_img = cv2.cvtColor(zoomed_bg_img, cv2.COLOR_BGR2BGRA)
                cv2.imshow('image', zoomed_bg_img)
            except Exception:
                Tools.delete_file(temp_back_path)
                messagebox.showerror('载体图片格式错误', '载体图片的格式不正确')
                return 0
            os.remove(temp_back_path)
            cv2.destroyAllWindows()
            bg_rows, bg_cols, _ = zoomed_bg_img.shape
            bg_img = copy.deepcopy(zoomed_bg_img)
        else:
            messagebox.showerror('载体图片地址错误', '载体图片地址错误')
            return 0

        # 获取二维码图片 -> qr_img
        qr_path = Tools.get_path_from_entry(entry1)
        if os.path.exists(qr_path):
            temp_qr_path = f'_temp_logo{os.path.splitext(qr_path)[-1]}'
            Tools.read_all_and_write_all(qr_path, temp_qr_path)
            try:
                qr_img = cv2.imread(temp_qr_path)
                qr_img = Tools.resize_pic(qr_img)
                cv2.imshow('QR code', qr_img)
            except Exception:
                Tools.delete_file(temp_qr_path)
                messagebox.showerror('二维码图片格式错误', '二维码图片的格式不正确')
                return 0
            os.remove(temp_qr_path)
            # cv2.destroyAllWindows()
        else:
            messagebox.showerror('二维码图片地址错误', '二维码图片地址错误')
            return 0

        # 检查完两张图片都没有问题后，接下来让用户对二维码进行框选
        def back_to_first1():
            global alive
            alive = False
            try:
                cv2.destroyAllWindows()
                third_frm.pack_forget()
                first_frm.pack()
            except Exception:
                pass

        def select_qr_code(event, x, y, flags, param):
            nonlocal x_start, y_start, qr_img_copy, qr_code_img
            if event == cv2.EVENT_LBUTTONDOWN:
                x_start, y_start = x, y
            elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
                qr_img_copy = copy.deepcopy(qr_img)
                cv2.rectangle(qr_img_copy, (x_start, y_start), (x, y),
                              (randint(0, 255), randint(0, 255), randint(0, 255)), 2)
            elif event == cv2.EVENT_LBUTTONUP:
                row_begin = min(y_start, y) + 1  # 这里进行微调是因为线有2像素宽，要把线从图片中去掉
                row_end = max(y_start, y) - 1
                col_begin = min(x_start, x) + 1
                col_end = max(x_start, x) - 1
                qr_code_img = qr_img_copy[row_begin: row_end, col_begin: col_end]

        alive = True
        first_frm.pack_forget()
        third_frm = tk.Frame(frm)
        third_frm.pack()
        tf_label1 = tk.Label(third_frm, text='请在图片中框选出二维码的位置（按‘S’确认，按‘Q’放弃），不框选则意味着全选', font=mid_font, fg='red')
        tf_label1.grid(row=1)
        qr_img_copy = copy.deepcopy(qr_img)  # 这里的zoomed_qr_img_copy既包括二维码也包括二维码的背景
        x_start = y_start = qr_code_img = -1  # qr_code_img是用户框选出来的结果（二维码本体）
        cv2.setMouseCallback('QR code', select_qr_code)
        window.update()
        while alive:
            # 要退出这个循环，请使用alive = False
            cv2.imshow('QR code', qr_img_copy)
            key = cv2.waitKey(10)  # 每隔10毫秒获取一下用户输入
            if key == ord('s'):
                if isinstance(qr_code_img, np.ndarray) and qr_code_img.shape != (0, 0, 3):
                    # 如果用户框选了二维码，那么就使用用户框选的部分
                    print('用户进行了框选二维码，这是框选出来的qr_code_img的大小：')
                    print(qr_code_img.shape)
                else:  # 如果用户按下‘S’键前没有框选二维码，那么就认为整张图片都是二维码
                    print('用户按下了s，并且没有进行框选，则认为选取结果为zoomed_qr_img的大小为：')
                    print(qr_img.shape)
                    qr_code_img = qr_img
                alive = False
            elif key == ord('q') or cv2.getWindowProperty('QR code', cv2.WND_PROP_VISIBLE) != 1:
                back_to_first1()
                return 0
        cv2.destroyAllWindows()

        # 对二维码进行框选之后，再根据用户设置将二维码放置在背景图片上
        def apply(*args):  # 根据用户设定的参数放置二维码
            nonlocal bg_img
            sf_label7.pack()
            window.update()
            sf_label7.pack_forget()
            # 如果用户的背景颜色选择其他，那处理一下用户设定的RGB
            if sf_var1.get() == '其他':
                try:
                    r = eval(sf_entry_r.get())
                    assert (isinstance(r, int)) and 0 <= r <= 255
                    g = eval(sf_entry_g.get())
                    assert (isinstance(g, int)) and 0 <= g <= 255
                    b = eval(sf_entry_b.get())
                    assert (isinstance(b, int)) and 0 <= b <= 255
                except Exception:
                    messagebox.showerror('RGB数值错误', 'RGB数值错误，定义范围为[0, 255]，请检查后重新输入')
                    return 0
            # 获取一下用户设定的中心点
            try:
                center_x = eval(sf_entry2.get())
                assert isinstance(center_x, int) and 0 <= center_x <= bg_cols
            except Exception:
                Tools.reset(sf_entry2)
                center_x = round(bg_cols / 2)
                sf_entry2.insert(0, center_x)
            try:
                center_y = eval(sf_entry3.get())
                assert isinstance(center_y, int) and 0 <= center_y <= bg_rows
            except Exception:
                Tools.reset(sf_entry3)
                center_y = round(bg_rows / 2)
                sf_entry3.insert(0, center_y)
            # 再处理一下用户设定的缩放程度
            try:
                set_resize = eval(sf_entry1.get())
                assert (isinstance(set_resize, int) or isinstance(set_resize, float)) and 0 <= set_resize
            except Exception:
                Tools.reset(sf_entry1)
                sf_entry1.insert(0, '0.5')
                set_resize = 0.5
            # 将背景图片进行拷贝后再处理
            bg_img = copy.deepcopy(zoomed_bg_img)
            # 根据用户设定的qr_code_img的位置和大小，确定一下roi的位置（即确定qr_code要放在背景图片的哪个位置）
            if set_resize <= 1.0:
                resized_qr_img = cv2.resize(qr_code_img, None, fx=set_resize, fy=set_resize,
                                            interpolation=cv2.INTER_AREA)
            else:
                resized_qr_img = cv2.resize(qr_code_img, None, fx=set_resize, fy=set_resize,
                                            interpolation=cv2.INTER_CUBIC)
            qr_rows, qr_cols, _ = resized_qr_img.shape
            qr_start_x, qr_end_x, roi_start_x, roi_end_x, qr_start_y, qr_end_y, roi_start_y, roi_end_y \
                = Tools.process_roi(bg_cols, qr_cols, center_x, bg_rows, qr_rows, center_y)
            roi = bg_img[roi_start_y: roi_end_y, roi_start_x: roi_end_x]
            print('roi.shape:', roi.shape)
            processed_qr_img = resized_qr_img[qr_start_y: qr_end_y, qr_start_x: qr_end_x]
            print('processed_qr_img.shape:', processed_qr_img.shape)
            # 根据二维码的颜色深浅来确定掩膜，用于后续处理roi
            qr2gray = cv2.cvtColor(processed_qr_img, cv2.COLOR_BGR2GRAY)
            _, dark_mask = cv2.threshold(qr2gray, 128, 255, cv2.THRESH_BINARY)  # dark_mask 是遮住了黑色部分的掩膜（剩余白色部分）
            light_mask = cv2.bitwise_not(dark_mask)  # light_mask 是遮住了白色部分的掩膜（剩余黑色部分）
            print('dark_mask.shape:', dark_mask.shape)
            print('light_mask.shape:', light_mask.shape)
            # 对roi中的每一个像素都进行bgr值的运算，并添加透明度，最后，把对应白色部分的roi掩盖起来
            '''
            P原 = P新 * Weight新 + P背 * (1 - Weight新)
            P原：原图片的像素BGR值，定义域[[0, 0, 0], [255, 255, 255]]
            P新：要生成的新图片的像素BGR值，定义域[[0, 0, 0], [255, 255, 255]]
            P背：新图片背景图片的像素BGR值，定义域[[0, 0, 0], [255, 255, 255]]
            Weight新：新图片的不透明度（权重），定义域：[0, 1]，值越小，越透明，值越大，越不透明
            注：png图片的第四通道为不透明（权重）通道，也叫Alpha通道，值域：[0, 255]，值越小，越透明，值越大，越不透明
            => P新 = (P原 - P背 * (1 - Weight新)) / Weight新
            '''
            dark_roi = np.zeros(roi.shape, dtype=np.uint8)
            weight = 1 - transparent_var.get() / 100  # 权重，不透明度，取值范围[0, 1]
            if sf_var1.get() == '白色':
                dark_roi[:, :, :3] = (roi[:, :, :3] - np.array([255, 255, 255]) * (1 - weight)) / weight
            elif sf_var1.get() == '黑色':
                dark_roi[:, :, :3] = (roi[:, :, :3] - np.array([0, 0, 0]) * (1 - weight)) / weight
            elif sf_var1.get() == '其他':
                dark_roi[:, :, :3] = (roi[:, :, :3] - np.array([b, g, r]) * (1 - weight)) / weight
            dark_roi[:, :, 3] = round(255 * weight)
            dark_roi = cv2.bitwise_and(dark_roi, dark_roi, mask=light_mask)
            # 将对应白色部分的roi保持原样，并于上面的dark_roi相加，就可以得想要的roi效果
            light_roi = cv2.bitwise_and(roi, roi, mask=dark_mask)
            dst_roi = cv2.add(dark_roi, light_roi)
            bg_img[roi_start_y: roi_end_y, roi_start_x: roi_end_x] = dst_roi
            cv2.imshow('outcome image', bg_img)

        def put_qr_code(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                Tools.reset(sf_entry2)
                Tools.reset(sf_entry3)
                sf_entry2.insert(0, x)
                sf_entry3.insert(0, y)
                apply()

        def back_to_first2():
            global alive
            alive = False
            cv2.destroyAllWindows()
            try:
                second_frm.pack_forget()
                first_frm.pack()
            except Exception:
                pass

        def save():
            apply()  # 先根据用户参数把二维码放上去，看看参数有没有问题
            cv2.destroyAllWindows()
            if sf_var1.get() == '白色':
                background_color = 'white'
            elif sf_var1.get() == '黑色':
                background_color = 'black'
            elif sf_var1.get() == '其他':
                background_color = f'rgb_{sf_entry_r.get()}_{sf_entry_g.get()}_{sf_entry_b.get()}'
            temp_outpath = f'invisible_qr_on_{background_color}_background.png'
            outname = f'{os.path.splitext(os.path.basename(back_path))[0]}_invisible_qr_on_{background_color}_background.png'
            cv2.imwrite(temp_outpath, bg_img)
            if var1.get() == '二维码图片所在文件夹':
                save_dir = os.path.dirname(qr_path)
            elif var1.get() == '载体图片所在文件夹':
                save_dir = os.path.dirname(back_path)
            if os.getcwd() != save_dir:  # 如果软件所在文件夹不是用户选择的文件夹，那么就进行移动
                outpath = os.path.join(save_dir, outname)
                Tools.read_all_and_write_all(temp_outpath, outpath)
                Tools.delete_file(temp_outpath)
            else:
                os.rename(temp_outpath, outname)
            label4.config(text=f'结果保存至{var1.get()}中的：')
            Tools.reset(entry3)
            entry3.insert('end', outname)
            frm3.pack()
            first_frm.pack()
            second_frm.pack_forget()

        @Tools.run_as_thread
        def listening_closing_window():
            while alive:
                if cv2.getWindowProperty('outcome image', cv2.WND_PROP_VISIBLE) != 1:
                    back_to_first2()
                time.sleep(0.1)

        def change_alpha(*args):
            if sf_var1.get() == '白色':
                transparent_var.set(60)
                sf_frm_rgb.grid_forget()
            elif sf_var1.get() == '黑色':
                transparent_var.set(40)
                sf_frm_rgb.grid_forget()
            elif sf_var1.get() == '其他':
                transparent_var.set(50)
                sf_frm_rgb.grid(row=1, column=3)

        alive = True
        cv2.imshow('outcome image', bg_img)
        cv2.setMouseCallback('outcome image', put_qr_code)
        listening_closing_window()
        third_frm.pack_forget()
        second_frm = tk.Frame(frm)
        second_frm.pack()
        sf_label1 = tk.Label(second_frm, text='请在载体图片上单击二维码图片隐藏的位置：', fg='red', font=mid_font)
        sf_label1.pack()
        sf_label3 = tk.Label(second_frm, text='二维码中心点的位置（左上角为原点）：', font=mid_font)
        sf_label3.pack()
        sf_frm3 = tk.Frame(second_frm)
        sf_frm3.pack()
        sf_label4 = tk.Label(sf_frm3, text='x：', font=mid_font)
        sf_label4.grid(row=1, column=1)
        sf_entry2 = tk.Entry(sf_frm3, width=4, font=mid_font)
        sf_entry2.grid(row=1, column=2)
        sf_entry2.bind('<Return>', apply)
        sf_label5 = tk.Label(sf_frm3, text='像素  y：', font=mid_font)
        sf_label5.grid(row=1, column=3)
        sf_entry3 = tk.Entry(sf_frm3, width=4, font=mid_font)
        sf_entry3.grid(row=1, column=4)
        sf_entry3.bind('<Return>', apply)
        sf_label6 = tk.Label(sf_frm3, text='像素', font=mid_font)
        sf_label6.grid(row=1, column=5)
        sf_frm1 = tk.Frame(second_frm)
        sf_frm1.pack()
        sf_label2 = tk.Label(sf_frm1, text='请选择二维码图片的缩放程度：', font=mid_font)
        sf_label2.grid(row=1, column=1)
        sf_entry1 = tk.Entry(sf_frm1, width=4, font=mid_font)
        sf_entry1.grid(row=1, column=2)
        sf_entry1.insert('end', '0.5')
        sf_entry1.bind('<Return>', apply)
        sf_frm4 = tk.Frame(second_frm)
        sf_frm4.pack()
        sf_var1 = tk.StringVar()
        sf_var1.set('白色')
        sf_label9 = tk.Label(sf_frm4, text='请设置在何种背景下能够正确隐藏二维码：', font=mid_font)
        sf_label9.grid(row=1, column=1, padx=5)
        sf_op1 = tk.OptionMenu(sf_frm4, sf_var1, *('白色', '黑色', '其他'), command=change_alpha)
        sf_op1.config(font=mid_font)
        sf_op1.grid(row=1, column=2, padx=5)
        sf_frm_rgb = tk.Frame(sf_frm4)
        # sf_frm_rgb.grid(row=1, column=3)
        sf_label_r = tk.Label(sf_frm_rgb, text='R:', font=mid_font)
        sf_label_r.grid(row=1, column=1)
        sf_entry_r = tk.Entry(sf_frm_rgb, width=3, font=mid_font)
        sf_entry_r.grid(row=1, column=2)
        sf_label_g = tk.Label(sf_frm_rgb, text='G:', font=mid_font)
        sf_label_g.grid(row=1, column=3)
        sf_entry_g = tk.Entry(sf_frm_rgb, width=3, font=mid_font)
        sf_entry_g.grid(row=1, column=4)
        sf_label_b = tk.Label(sf_frm_rgb, text='B:', font=mid_font)
        sf_label_b.grid(row=1, column=5)
        sf_entry_b = tk.Entry(sf_frm_rgb, width=3, font=mid_font)
        sf_entry_b.grid(row=1, column=6)
        sf_label10 = tk.Label(second_frm, text='背景越白，二维码就隐藏在图片中越白的位置，透明度就越靠近60\n背景越黑，二维码就隐藏在图片中越黑的位置，透明度就越靠近40', font=mid_font)
        sf_label10.pack()
        sf_label8 = tk.Label(second_frm, text='请设置隐藏的二维码图片的透明度：', font=mid_font)
        sf_label8.pack()
        transparent_var = tk.IntVar()
        transparent_var.set(60)
        sf_scale1 = tk.Scale(second_frm, from_=40, to=60, variable=transparent_var, orient=tk.HORIZONTAL, length=500,
                             showvalue=1, tickinterval=5, resolution=1)
        sf_scale1.pack()
        sf_frm2 = tk.Frame(second_frm)
        sf_frm2.pack()
        sf_button1 = tk.Button(sf_frm2, text='放弃', font=mid_font, command=back_to_first2)
        sf_button1.grid(row=1, column=1, padx=20)
        sf_button2 = tk.Button(sf_frm2, text='应用', font=mid_font, command=apply)
        sf_button2.grid(row=1, column=2, padx=20)
        sf_button3 = tk.Button(sf_frm2, text='保存', font=mid_font, command=save)
        sf_button3.grid(row=1, column=3, padx=20)
        sf_label7 = tk.Label(second_frm, text='正在处理，请稍候，不要频繁操作', fg='red', font=mid_font)

    button1 = tk.Button(frm1, text='重置', command=reset, font=mid_font)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm1, text='确定', command=confirm, font=mid_font)
    button2.grid(row=1, column=2, padx=20)
    frm3 = tk.Frame(first_frm)
    label4 = tk.Label(frm3, text='结果保存至...中的：', font=mid_font)
    label4.pack()
    entry3 = tk.Entry(frm3, width=59, font=mid_font)
    entry3.pack()


def two_faces():

    def a_drag(files):
        Tools.dragged_files(files, a_entry1)

    def b_drag(files):
        Tools.dragged_files(files, b_entry1)

    a_label1 = tk.Label(frm, text='请拖入表图片或输入地址：\n注意：表图片的亮度和表图片能显示的背景颜色的亮度越接近效果越好', font=mid_font)
    a_label1.pack()
    a_entry1 = tk.Entry(frm, width=59, font=mid_font)
    a_entry1.pack()
    hook_dropfiles(a_entry1, func=a_drag)
    a_frm1 = tk.Frame(frm)
    a_frm1.pack()
    a_label2 = tk.Label(a_frm1, text='请设置表图片在什么背景颜色下可以显示：  R:', font=mid_font)
    a_label2.grid(row=1, column=1)
    a_entry2 = tk.Entry(a_frm1, width=3, font=mid_font)
    a_entry2.insert('end', '255')
    a_entry2.grid(row=1, column=2)
    a_label3 = tk.Label(a_frm1, text='G:', font=mid_font)
    a_label3.grid(row=1, column=3)
    a_entry3 = tk.Entry(a_frm1, width=3, font=mid_font)
    a_entry3.insert('end', '255')
    a_entry3.grid(row=1, column=4)
    a_label4 = tk.Label(a_frm1, text='B:', font=mid_font)
    a_label4.grid(row=1, column=5)
    a_entry4 = tk.Entry(a_frm1, width=3, font=mid_font)
    a_entry4.insert('end', '255')
    a_entry4.grid(row=1, column=6)
    a_label5 = tk.Label(frm, text='   ', font=mid_font)
    a_label5.pack()

    b_label1 = tk.Label(frm, text='请拖入里图片或输入地址：\n注意：里图片的亮度和里图片能显示的背景颜色的亮度越接近效果越好', font=mid_font)
    b_label1.pack()
    b_entry1 = tk.Entry(frm, width=59, font=mid_font)
    b_entry1.pack()
    hook_dropfiles(b_entry1, func=b_drag)
    b_frm1 = tk.Frame(frm)
    b_frm1.pack()
    b_label2 = tk.Label(b_frm1, text='请设置里图片在什么背景颜色下可以显示：', font=mid_font)
    b_label2.grid(row=1, column=1)
    b_entry2 = tk.Entry(b_frm1, width=3, font=mid_font)
    b_entry2.insert('end', '0')
    b_entry2.grid(row=1, column=2)
    b_label3 = tk.Label(b_frm1, text='G:', font=mid_font)
    b_label3.grid(row=1, column=3)
    b_entry3 = tk.Entry(b_frm1, width=3, font=mid_font)
    b_entry3.insert('end', '0')
    b_entry3.grid(row=1, column=4)
    b_label4 = tk.Label(b_frm1, text='B:', font=mid_font)
    b_label4.grid(row=1, column=5)
    b_entry4 = tk.Entry(b_frm1, width=3, font=mid_font)
    b_entry4.insert('end', '0')
    b_entry4.grid(row=1, column=6)
    b_label5 = tk.Label(frm, text='   ', font=mid_font)
    b_label5.pack()

    def reset():
        Tools.reset(a_entry1)
        Tools.reset(a_entry2)
        a_entry2.insert('end', '255')
        Tools.reset(a_entry3)
        a_entry3.insert('end', '255')
        Tools.reset(a_entry4)
        a_entry4.insert('end', '255')
        Tools.reset(b_entry1)
        Tools.reset(b_entry2)
        b_entry2.insert('end', '0')
        Tools.reset(b_entry3)
        b_entry3.insert('end', '0')
        Tools.reset(b_entry4)
        b_entry4.insert('end', '0')
        entry1.config(state='normal')
        Tools.reset(entry1)
        entry1.config(state='readonly')
        label3.pack_forget()

    def process():
        label3.pack_forget()
        window.update()
        # 获取一下用户输入的r, g, b
        try:
            r_o = eval(a_entry2.get())
            assert isinstance(r_o, int) and 0 <= r_o <= 255
            g_o = eval(a_entry3.get())
            assert isinstance(g_o, int) and 0 <= g_o <= 255
            b_o = eval(a_entry4.get())
            assert isinstance(b_o, int) and 0 <= b_o <= 255
            r_i = eval(b_entry2.get())
            assert isinstance(r_i, int) and 0 <= r_i <= 255
            g_i = eval(b_entry3.get())
            assert isinstance(g_i, int) and 0 <= g_i <= 255
            b_i = eval(b_entry4.get())
            assert isinstance(b_i, int) and 0 <= b_i <= 255
        except Exception:
            messagebox.showerror('RGB赋值错误', 'RGB的取值范围为[0, 255]内的正整数')
            return 0

        # 获取表图片 -> outer_img
        outer_path = Tools.get_path_from_entry(a_entry1)
        if os.path.exists(outer_path):
            temp_outer_path = f'_temp_back{os.path.splitext(outer_path)[-1]}'
            Tools.read_all_and_write_all(outer_path, temp_outer_path)
            try:
                outer_img = cv2.imread(temp_outer_path)
                outer_img_rows, outer_img_cols, _ = outer_img.shape
                # if outer_img_rows > 900 or outer_img_cols > 900:
                #     zoom = min(900 / outer_img_rows, 900 / outer_img_cols)
                # else:
                #     zoom = 1.0
                # zoomed_outer_img = cv2.resize(outer_img, None, fx=zoom, fy=zoom, interpolation=cv2.INTER_AREA)
                zoomed_outer_img = Tools.resize_pic(outer_img, outer_img_rows, outer_img_cols)
                cv2.imshow('zoomed_outer_img', zoomed_outer_img)
            except Exception:
                Tools.delete_file(temp_outer_path)
                messagebox.showerror('表图片格式错误', '表图片的格式不正确')
                return 0
            os.remove(temp_outer_path)
            # cv2.waitKey()
            cv2.destroyAllWindows()
            outer_img_rows, outer_img_cols, _ = zoomed_outer_img.shape
            print("outer_img_rows, outer_img_cols:", outer_img_rows, outer_img_cols)
            outer_img = zoomed_outer_img.astype(np.float32)
            # outer_img = copy.deepcopy(zoomed_outer_img)
        else:
            messagebox.showerror('表图片地址错误', '表图片地址错误')
            return 0

        # 获取里图片 -> inner_img
        inner_path = Tools.get_path_from_entry(b_entry1)
        if os.path.exists(inner_path):
            temp_inner_path = f'_temp_back{os.path.splitext(inner_path)[-1]}'
            Tools.read_all_and_write_all(inner_path, temp_inner_path)
            try:
                inner_img = cv2.imread(temp_inner_path)
                inner_img_rows, inner_img_cols, _ = inner_img.shape
                # if inner_img_rows > 900 or inner_img_cols > 900:
                #     zoom = min(900 / inner_img_rows, 900 / inner_img_cols)
                # else:
                #     zoom = 1.0
                # zoomed_inner_img = cv2.resize(inner_img, None, fx=zoom, fy=zoom, interpolation=cv2.INTER_AREA)
                zoomed_inner_img = Tools.resize_pic(inner_img, inner_img_rows, inner_img_cols)
                cv2.imshow('zoomed_inner_img', zoomed_inner_img)
            except Exception:
                Tools.delete_file(temp_inner_path)
                messagebox.showerror('里图片格式错误', '里图片的格式不正确')
                return 0
            os.remove(temp_inner_path)
            # cv2.waitKey()
            cv2.destroyAllWindows()
            inner_img_rows, inner_img_cols, _ = zoomed_inner_img.shape
            print('inner_img_rows, inner_img_cols:', inner_img_rows, inner_img_cols)
            inner_img = zoomed_inner_img.astype(np.float32)
            # inner_img = copy.deepcopy(zoomed_inner_img)
        else:
            messagebox.showerror('里图片地址错误', '里图片地址错误')
            return 0

        # 把表图和里图扩大成正好包含表图和里图的大图，表图填不满的地方填白色，里图填不满的地方填黑色
        max_rows = max(inner_img_rows, outer_img_rows)
        max_cols = max(inner_img_cols, outer_img_cols)
        print('max_rows, max_cols:', max_rows, max_cols)
        P_o = np.ones((max_rows, max_cols, 3), dtype=np.float32) * 255
        outer_row_start = (max_rows - outer_img_rows) // 2  # 地板除，向下取整
        outer_col_start = (max_cols - outer_img_cols) // 2
        print("outer_row_start, outer_col_start:", outer_row_start, outer_col_start)
        P_o[outer_row_start: outer_row_start + outer_img_rows, outer_col_start: outer_col_start + outer_img_cols] = outer_img
        # cv2.imshow('P_o', P_o)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        P_i = np.zeros((max_rows, max_cols, 3), dtype=np.float32)
        inner_row_start = (max_rows - inner_img_rows) // 2
        inner_col_start = (max_cols - inner_img_cols) // 2
        print("inner_row_start, inner_col_start:", inner_row_start, inner_col_start)
        P_i[inner_row_start: inner_row_start + inner_img_rows, inner_col_start: inner_col_start + inner_img_cols] = inner_img
        # cv2.imshow('P_i', P_i)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        # 从用户输入计算表图和里图能够正常显示的背景图
        P_obg = np.zeros((max_rows, max_cols, 3), dtype=np.float32)
        P_obg[:] = (b_o, g_o, r_o)
        # cv2.imshow('P_obg', P_obg)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        P_ibg = np.zeros((max_rows, max_cols, 3), dtype=np.float32)
        P_ibg[:] = (b_i, g_i, r_i)
        # cv2.imshow('P_ibg', P_ibg)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        # 再将outer_bg和inner_bg两张图按算法叠加起来
        '''
        P_x * W_x + P_obg * (1 - W_x) = P_o
        P_x * W_x + P_ibg * (1 - W_x) = P_i
        P_x: 待生成的新图片
        W_x: 待生成的新图片的权重，取值范围：[0, 1]
        P_obg: 使得表图能显示的背景图片
        P_o: 表图
        P_ibg: 使得里图能显示的背景图片
        P_i: 里图
        解得：
        W_x = (P_o - P_obg) / (P_x - P_obg)  # 以灰度图计算
        P_x = (P_o * P_ibg - P_i * P_obg) / (P_o - P_obg - P_i + P_ibg)
        '''
        P_x = np.zeros((max_rows, max_cols, 4), dtype=np.float32)
        # 先解P_x
        P_x_denominator = P_o - P_obg - P_i + P_ibg
        P_x_denominator[P_x_denominator == 0] += 1  # 把P_x分母上等于0的值加上1
        P_x[:, :, :3] = (P_o * P_ibg - P_i * P_obg) / P_x_denominator
        # 再解W_x。   255 * W_x 即 P_x[:, :, 3]
        W_x_denominator = cv2.cvtColor(P_x, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(P_obg, cv2.COLOR_BGR2GRAY)
        W_x_denominator[W_x_denominator == 0] += 1  # 把W_x分母上等于0的值加上1
        P_x[:, :, 3] = 255 * (cv2.cvtColor(P_o, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(P_obg, cv2.COLOR_BGR2GRAY)) / W_x_denominator
        P_x = P_x.clip(0, 255)
        # print(P_x[:, :, 3])
        P_x = P_x.astype(np.uint8)
        # cv2.imshow('P_x 3 channels', P_x[:, :, :3])
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        # cv2.imshow('outcome image', P_x)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        temp_outpath = f'ego_show_on_rgb_{r_i}_{g_i}_{b_i}.png'
        outname = f'{os.path.splitext(os.path.basename(outer_path))[0]}_ego_show_on_rgb_{r_i}_{g_i}_{b_i}.png'
        cv2.imwrite(temp_outpath, P_x)
        if pos.get() == '表图片所在文件夹':
            save_dir = os.path.dirname(outer_path)
        elif pos.get() == '里图片所在文件夹':
            save_dir = os.path.dirname(inner_path)
        if os.getcwd() != save_dir:  # 如果软件所在文件夹不是用户选择的文件夹，那么就进行移动
            outpath = os.path.join(save_dir, outname)
            Tools.read_all_and_write_all(temp_outpath, outpath)
            Tools.delete_file(temp_outpath)
        else:
            os.rename(temp_outpath, outname)
        entry1.config(state='normal')
        Tools.reset(entry1)
        entry1.insert('end', outname)
        entry1.config(state='readonly')
        label3.pack()

    frm1 = tk.Frame(frm)
    frm1.pack()
    button1 = tk.Button(frm1, text='重置', font=mid_font, command=reset)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm1, text='开始生成', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=20)
    frm2 = tk.Frame(frm)
    frm2.pack()
    label1 = tk.Label(frm2, text='结果保存在：', font=mid_font)
    label1.grid(row=1, column=1)
    pos = tk.StringVar()
    pos.set('表图片所在文件夹')
    op1 = tk.OptionMenu(frm2, pos, *('表图片所在文件夹', '里图片所在文件夹'))
    op1.config(font=mid_font)
    op1.grid(row=1, column=2)
    label2 = tk.Label(frm2, text='中的：', font=mid_font)
    label2.grid(row=1, column=3)
    entry1 = tk.Entry(frm, width=59, font=mid_font, state='readonly')
    entry1.pack()
    label3 = tk.Label(frm, text='处理完成！', font=mid_font, fg='red')


def against_duplicate_check():
    # 操作零宽度字符（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='操作特殊字符', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    frm2 = tk.Frame(labelframe1)
    frm2.pack()
    label1 = tk.Label(frm2, text='请输入需要插入/去除特殊字符的文字：\n（长度：0）', font=mid_font)
    label1.grid(row=1, column=1, padx=10)
    text1 = tk.Text(labelframe1, font=mid_font, width=43, height=10)
    text1.pack()
    interval = 5
    kind = tk.StringVar()
    kind.set('mix')

    def cal_len(*args):
        label1.config(text=f"请输入需要插入/去除特殊字符的文字：\n（长度：{len(text1.get(1.0, 'end'))-1}）")  # 要去掉文本框最后自带的\n所占的长度

    def reset():
        Tools.reset(text1)
        label1.config(text=f"请输入需要插入/去除特殊字符的文字：\n（长度：0）")  # 要去掉文本框最后自带的\n所占的长度
        Tools.reset(text2)
        label2.config(text=f'结果为：（长度：0）')

    def insert():
        nonlocal interval
        try:
            num = eval(entry1.get())
            assert isinstance(num, int) and num > 0
        except Exception:
            Tools.reset(entry1)
            entry1.insert('end', '1')
            num = 3
        try:
            interval = eval(entry2.get())
            assert isinstance(interval, int) and interval > 0
        except Exception:
            Tools.reset(entry2)
            entry2.insert('end', '5')
            interval = 5
        Tools.reset(text2)
        Tools.reset(lf2_text1)
        window.update()
        forbidden = text1.get(1.0, 'end').rstrip('\n')
        half_width_list = [' ', ' ']
        zero_width_list = ['‎', '‏', '‌', '‍', '​', '﻿']
        mixed_list = ['‎', '‏', '‌', '‍', '​', '﻿', ' ', ' ']
        word_list = jieba.lcut(forbidden)
        print('word_list:', word_list)
        res = word_list[0]
        count = 0
        for word in word_list[1:]:
            count += 1
            if count == interval:
                connector = ''
                for _ in range(num):
                    if kind.get() == 'zero':
                        connector += random.choice(zero_width_list)
                    elif kind.get() == 'half':
                        connector += random.choice(half_width_list)
                    elif kind.get() == 'mix':
                        connector += random.choice(mixed_list)
                res = connector.join([res, word])
                count = 0
            else:
                res += word
        text2.insert('end', res)
        lf2_text1.insert('end', res)
        label2.config(text=f'插入特殊字符后的结果为：（长度：{len(res)}）')
        cal_len2()
        window.update()
        _replace()

    def extract():
        Tools.reset(text2)
        encoded = text1.get(1.0, 'end').rstrip('\n')
        origin = encoded.replace(' ', '').replace(' ', '').replace('‌', '').replace('‍', '').replace('​', '').replace('﻿', '').replace('‎', '').replace('‏', '')
        text2.insert('end', origin)
        label2.config(text=f'去除特殊字符后的结果为：（长度：{len(origin)}）')

    def _copy():
        Tools.copy(text2, button4)

    def intro_mode():
        intro_window2 = tk.Toplevel()
        intro_window2.title("特殊字符操作介绍")
        intro_window2.geometry(Tools.zoom_size('636x758', zoom))
        intro_window2.iconbitmap(icon_path)
        iw_text = tk.Text(intro_window2, width=46, height=18, font=mid_font)
        iw_text.pack()
        word = '''    该功能可以在几个中文词组或英文单词之间插入一些特殊字符（注意：标点、空格、换行都算一个词），以此避免查重系统或聊天平台的字符串匹配，但是不会影响人类的阅读。
        
    特殊字符包括零宽度字符与窄宽空格，你可以选择使用某一种字符或混合使用。

    插入特殊字符的频率和一次插入的数量可以自己设置，值需要为正整数。且这个设置只会在插入特殊字符功能生效，不会影响去除特殊字符的功能。去除时会将两种特殊字符统统去掉。

    需要特别注意的时，一次处理的文本不要过长，生成的结果长度最好不要超过本软件中显示的2000个字，否则在粘贴到word文档中时，可能会造成word文档卡死，造成强制退出，且文件没保存的惨剧。'''
        iw_text.insert('end', word)
        iw_frm2 = tk.Frame(intro_window2)
        iw_frm2.pack(pady=20)
        iw_label1 = tk.Label(iw_frm2, text='请选择要插入的特殊字符的种类：', font=mid_font)
        iw_label1.pack()
        iw_frm1 = tk.Frame(iw_frm2)
        iw_frm1.pack()
        iw_rb1 = tk.Radiobutton(iw_frm1, text='零宽度字符', variable=kind, value='zero', font=mid_font)
        iw_rb1.grid(row=1, column=1, padx=10)
        iw_rb2 = tk.Radiobutton(iw_frm1, text='窄宽空格', variable=kind, value='half', font=mid_font)
        iw_rb2.grid(row=1, column=2, padx=10)
        iw_rb3 = tk.Radiobutton(iw_frm1, text='混合使用', variable=kind, value='mix', font=mid_font)
        iw_rb3.grid(row=1, column=3, padx=10)

    text1.bind("<KeyRelease>", cal_len)
    frm4 = tk.Frame(labelframe1)
    frm4.pack()
    label5 = tk.Label(frm4, text='每隔', font=mid_font)
    label5.grid(row=1, column=1)
    entry2 = tk.Entry(frm4, width=3, font=mid_font)
    entry2.grid(row=1, column=2)
    entry2.insert('end', interval)
    label6 = tk.Label(frm4, text='个词组插入', font=mid_font)
    label6.grid(row=1, column=3)
    entry1 = tk.Entry(frm4, width=3, font=mid_font)
    entry1.grid(row=1, column=4)
    entry1.insert('end', '1')
    label3 = tk.Label(frm4, text='个特殊字符', font=mid_font)
    label3.grid(row=1, column=5)
    button5 = tk.Button(frm4, text='说明', font=mid_font, command=intro_mode, fg='blue', bd=0)
    button5.grid(row=1, column=6, padx=5)
    frm1 = tk.Frame(labelframe1)
    frm1.pack()
    button1 = tk.Button(frm1, text='重置', font=mid_font, command=reset)
    button1.grid(row=1, column=1, padx=5)
    button2 = tk.Button(frm1, text='插入特殊字符', font=mid_font, command=insert)
    button2.grid(row=1, column=2, padx=5)
    button3 = tk.Button(frm1, text='去除特殊字符', font=mid_font, command=extract)
    button3.grid(row=1, column=3, padx=5)
    button4 = tk.Button(frm1, text='复制结果', font=mid_font, command=_copy, fg=colors[ind])
    button4.grid(row=1, column=4, padx=5)
    label2 = tk.Label(labelframe1, text='结果为：（长度：0）', font=mid_font)
    label2.pack()
    text2 = tk.Text(labelframe1, font=mid_font, width=43, height=10)
    text2.pack()

    # 近形字替换
    labelframe2 = tk.LabelFrame(frm, text='近形字替换', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)
    lf2_label1 = tk.Label(labelframe2, text='请输入需要替换近形字的文字：（长度：0）', font=mid_font)
    lf2_label1.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=11, font=mid_font)
    lf2_text1.pack()
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_label3 = tk.Label(lf2_frm2, text='近形字的相似性：', font=mid_font)
    lf2_label3.grid(row=1, column=1)
    lf2_entry1 = tk.Entry(lf2_frm2, width=4, font=mid_font)
    lf2_entry1.grid(row=1, column=2)
    lf2_entry1.insert('end', '0.9')
    ascii_selected = tk.StringVar()
    ascii_selected.set('0')
    lf2_cb1 = tk.Checkbutton(lf2_frm2, text='替换ascii字符', variable=ascii_selected, onvalue='1', offvalue='0', font=mid_font)
    lf2_cb1.grid(row=1, column=3, padx=20)

    def cal_len2(*args):
        lf2_label1.config(text=f"请输入需要替换近形字的文字：（长度：{len(lf2_text1.get(1.0, 'end'))-1}）")  # 要去掉文本框最后自带的\n所占的长度

    def reset2():
        Tools.reset(lf2_text1)
        lf2_label1.config(text='请输入需要替换近形字的文字：（长度：0）')
        Tools.reset(lf2_text2)
        lf2_label2.config(text='结果为：（长度：0，替换了 0 处）')

    def _replace(*args):
        Tools.reset(lf2_text2)
        try:
            similar = eval(lf2_entry1.get())
            assert isinstance(similar, float) and 1 > similar > 0
        except Exception:
            Tools.reset(lf2_entry1)
            lf2_entry1.insert('end', '0.9')
            similar = 0.9
        finally:
            similar = 1 - similar  # 相似性是1-用户输入的值
        text = lf2_text1.get(1.0, 'end').rstrip('\n')
        with open('system_resource/dont_replace.txt', 'r', encoding='utf-8') as f:
            skip_words = ''.join(set(list(f.read())))
        dont_replace_index = []
        dont_replace_word = []
        for word in skip_words:
            if word in text:
                dont_replace_index.append(text.index(word))
                dont_replace_word.append(word)
        if ascii_selected.get() == '0':
            res, indicate_list = unvcode.unvcode(text, skip_ascii=True, mse=similar)
        else:
            res, indicate_list = unvcode.unvcode(text, skip_ascii=False, mse=similar)
        print(indicate_list)
        minus = 0
        for index, word in zip(dont_replace_index, dont_replace_word):
            if res[index] != text[index]:
                minus += res.count(res[index])
                res = res.replace(res[index], word)
        lf2_text2.insert('end', res)
        lf2_label2.config(text=f"结果为：（长度：{len(lf2_text2.get(1.0, 'end')) - 1}，替换了 {len([i for i in indicate_list if i is not None]) - minus} 处）")

    def copy2():
        Tools.copy(lf2_text2, lf2_button3)

    def intro_similar():
        intro_window2 = tk.Toplevel()
        intro_window2.title("近形字替换介绍与设置")
        intro_window2.geometry(Tools.zoom_size('636x758', zoom))
        intro_window2.iconbitmap(icon_path)

        def save():
            global ind
            ind = (ind + 1) % 6
            with open('system_resource/dont_replace.txt', 'w', encoding='utf-8') as f:
                f.write(''.join(set(list(iw_text2.get(1.0, 'end').replace('\n', '').replace(' ', '')))))
            iw_button.config(fg=colors[ind])

        iw_text = tk.Text(intro_window2, width=46, height=15, font=mid_font)
        iw_text.pack()
        word = '''    在unicode字符集中，有很多字，它们看起来长得很像，但是它们的字符编码不一样。利用这个特点，只需将原本的字替换成另外一个长相相似的字，您就可以实现反和谐和反查重的功能。

    您可以设置替换文字与原本文字的相似程度，取值在0到1之间。此外，您还可以选择是否替换ascii编码表中的字符。常见的ascii字符包括以下这些字符：!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
    
    有一些汉字替换后形变比较大，您可以把这些字的原型写在下面，来避免替换它们。'''
        iw_text.insert('end', word)
        iw_label1 = tk.Label(intro_window2, text='请输入不需要替换的字：', font=mid_font)
        iw_label1.pack()
        iw_text2 = tk.Text(intro_window2, width=46, height=10, font=mid_font)
        iw_text2.pack()
        iw_button = tk.Button(intro_window2, text='保存', font=mid_font, fg=colors[ind], command=save)
        iw_button.pack()
        try:
            with open('system_resource/dont_replace.txt', 'r', encoding='utf-8') as f:
                iw_text2.insert(1.0, f.read())
        except Exception:
            pass

    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_button1 = tk.Button(lf2_frm1, text='重置', font=mid_font, command=reset2)
    lf2_button1.grid(row=1, column=1, padx=15)
    lf2_button2 = tk.Button(lf2_frm1, text='近形字替换', font=mid_font, command=_replace)
    lf2_button2.grid(row=1, column=2, padx=15)
    lf2_button3 = tk.Button(lf2_frm1, text='复制结果', font=mid_font, command=copy2, fg=colors[ind])
    lf2_button3.grid(row=1, column=3, padx=15)
    lf2_button4 = tk.Button(lf2_frm1, text='设置', font=mid_font, command=intro_similar, fg='blue', bd=0)
    lf2_button4.grid(row=1, column=4, padx=15)
    lf2_label2 = tk.Label(labelframe2, text='结果为：（长度：0，替换了 0 处）', font=mid_font)
    lf2_label2.pack()
    lf2_text2 = tk.Text(labelframe2, width=43, height=10, font=mid_font)
    lf2_text2.pack()
    lf2_text1.bind("<KeyRelease>", cal_len2)


def rs_code_word():
    # 添加RS纠错码（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='添加RS纠错码', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def change_entry1(value):
        Tools.change_zentry(value, entry1)

    def change_scale1(*args):
        _var = tk.StringVar()
        _var.set('1')
        Tools.change_zscale(_var, entry1, percent)

    def reset1():
        Tools.reset(text1)
        Tools.reset(text2)
        label3.config(text='纠错码长度：0，结果为（base64编码）：')

    def add_rs(*args):
        if not text1.get(1.0, 'end').rstrip('\n'):
            return 0
        Tools.reset(text2)
        code_get = code.get()
        if code_get == 'utf-8' or code_get == 'gbk':
            try:
                info = text1.get(1.0, 'end').rstrip('\n').encode(code_get)
            except Exception:
                text2.insert('end', '字符编码错误')
                return 0
        elif code_get == 'base64':
            info = base64.b64decode(text1.get(1.0, 'end'))
        rs_length = Tools.round_to_even(len(info) * percent.get() * 0.02)
        print('rs_length:', rs_length)
        try:
            rs = RSCodec(rs_length)
            outcome = base64.b64encode(bytes(rs.encode(info)))
        except Exception:
            outcome = '纠错码字数过多，请降低纠错比例，或减少原信息大小'
        label3.config(text=f'纠错码长度：{rs_length}，结果为（base64编码）：')
        text2.insert('end', outcome)

    def copy1():
        Tools.copy(text2, button3)

    frm4 = tk.Frame(labelframe1)
    frm4.pack()
    label1 = tk.Label(frm4, text='请设置能够纠错的比例：', font=mid_font)
    label1.grid(row=1, column=1)
    entry1 = tk.Entry(frm4, font=mid_font, width=5)
    entry1.grid(row=1, column=2)
    entry1.insert('end', '10')
    entry1.bind('<KeyRelease>', change_scale1)
    label4 = tk.Label(frm4, text='%', font=mid_font)
    label4.grid(row=1, column=3)
    percent = tk.IntVar()
    percent.set(10)
    scale1 = tk.Scale(labelframe1, from_=0, to=100, orient=tk.HORIZONTAL, length=400, tickinterval=10, resolution=1, showvalue=0, variable=percent, command=change_entry1)
    scale1.pack()
    frm1 = tk.Frame(labelframe1)
    frm1.pack()
    label2 = tk.Label(frm1, text='请输入需要添加纠错码的文字：', font=mid_font)
    label2.grid(row=1, column=1)
    code = tk.StringVar()
    code.set('utf-8')
    optionmenu1 = tk.OptionMenu(frm1, code, *('utf-8', 'gbk', 'base64'), command=add_rs)
    optionmenu1.config(font=mid_font)
    optionmenu1.grid(row=1, column=2)
    text1 = tk.Text(labelframe1, width=43, height=10, font=mid_font)
    text1.pack()
    frm3 = tk.Frame(labelframe1)
    frm3.pack()
    button1 = tk.Button(frm3, text='重置', font=mid_font, command=reset1)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm3, text='确定', font=mid_font, command=add_rs)
    button2.grid(row=1, column=2, padx=20)
    button3 = tk.Button(frm3, text='复制结果', font=mid_font, command=copy1, fg=colors[ind])
    button3.grid(row=1, column=3, padx=20)
    label3 = tk.Label(labelframe1, text='纠错码长度：0，结果为（base64编码）：', font=mid_font)
    label3.pack()
    text2 = tk.Text(labelframe1, width=43, height=9, font=mid_font)
    text2.pack()

    # 纠正并去除RS纠错码（左边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='纠正错误并去除RS纠错码', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()
    lf2_label1 = tk.Label(lf2_frm3, text='请输入纠错码的长度：', font=mid_font)
    lf2_label1.grid(row=1, column=1)
    lf2_entry1 = tk.Entry(lf2_frm3, width=4, font=mid_font)
    lf2_entry1.grid(row=1, column=2)
    lf2_label2 = tk.Label(labelframe2, text='请输入需要进行纠错的base64字符：', font=mid_font)
    lf2_label2.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, font=mid_font, height=10)
    lf2_text1.pack()
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_frm4.pack()

    def reset2():
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)

    def repair(*args):
        re_length = lf2_entry1.get()
        Tools.reset(lf2_text2)
        try:
            re_length = eval(re_length)
            assert isinstance(re_length, int) and re_length > 0
        except Exception:
            messagebox.showerror('纠错码长度错误', '纠错码的长度应为正整数')
            return 0
        try:
            encoded_text_with_error = base64.b64decode(lf2_text1.get(1.0, 'end').rstrip('\n'))
        except Exception:
            messagebox.showerror('base64格式错误', '输入的不是正确的base64编码')
            return 0
        try:
            rs = RSCodec(re_length)
            decoded_text = rs.decode(encoded_text_with_error)[0]
        except Exception:
            lf2_text2.insert('end', '纠错码长度有误或错误过多，无法纠错')
            return 0
        lf2_code_get = lf2_code.get()
        if lf2_code_get == 'utf-8' or lf2_code_get == 'gbk':
            try:
                decoded_text = decoded_text.decode(lf2_code_get)
            except Exception:
                decoded_text = '编码错误'
        elif lf2_code_get == 'base64':
            decoded_text = base64.b64encode(decoded_text)
        lf2_text2.insert('end', decoded_text)

    def copy2():
        Tools.copy(lf2_text2, lf2_button3)

    lf2_button1 = tk.Button(lf2_frm4, text='重置', font=mid_font, command=reset2)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm4, text='确定', font=mid_font, command=repair)
    lf2_button2.grid(row=1, column=2, padx=20)
    lf2_button3 = tk.Button(lf2_frm4, text='复制结果', font=mid_font, command=copy2, fg=colors[ind])
    lf2_button3.grid(row=1, column=3, padx=20)
    frm2 = tk.Frame(labelframe2)
    frm2.pack()
    lf2_label3 = tk.Label(frm2, text='纠错后的文字为：', font=mid_font)
    lf2_label3.grid(row=1, column=1)
    lf2_code = tk.StringVar()
    lf2_code.set('utf-8')
    lf2_option_menu1 = tk.OptionMenu(frm2, lf2_code, *('utf-8', 'gbk', 'base64'), command=repair)
    lf2_option_menu1.config(font=mid_font)
    lf2_option_menu1.grid(row=1, column=2)
    lf2_text2 = tk.Text(labelframe2, font=mid_font, width=43, height=11)
    lf2_text2.pack()
    lf2_entry1.bind('<Return>', repair)


def rs_code_file():
    # 添加RS纠错码（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='添加RS纠错码', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def change_entry1(value):
        Tools.change_zentry(value, entry1)

    def change_scale1(*args):
        _var = tk.StringVar()
        _var.set('1')
        Tools.change_zscale(_var, entry1, percent)

    def reset1():
        Tools.reset(entry2)
        Tools.reset(entry3)
        label3.config(text='纠错码长度：0x0')

    def drag1(files):
        Tools.dragged_files(files, entry2)

    def add_rs(*args):
        '''
        将原文件以64字节为单位分块添加纠错码，并把纠错码全部放在文件的最后，如下所示：
        block1, block2, ..., rs_code1, rs_code2, ...
        将纠错码放在文件最后的好处是：在一些文件没有损坏时，不用先去除纠错码就能直接打开。
        纠错码长度的格式为axb，a代表有多少个rs_code块，b代表每一个rs_code块有多少字节
        '''
        Tools.reset(entry3)
        label3.config(text='纠错码长度：0x0')
        file_path = Tools.get_path_from_entry(entry2)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            pass  # 这里pass的意思是继续执行下面的程序
        else:
            messagebox.showerror(title='文件路径错误', message='文件路径错误')
            return 0
        label3.config(text=f'正在处理，请稍候...')
        window.update()
        rs_length = Tools.round_to_even(64 * percent.get() * 0.02)  # RS纠错码的长度需要是被保护信息长度的两倍，所以乘了0.02
        # print('rs_length:', rs_length)
        block_num = 0
        # 生成纠错码，并把所有纠错码放在临时文件中
        with open(file_path, 'rb') as inf, open('temp.tmp', 'wb') as outf:
            block = inf.read(64)
            while block:
                # print('block:', block, '\nlen(block):', len(block))
                block_num += 1
                rs = RSCodec(rs_length)
                block_with_rs = bytes(rs.encode(block))
                # print('block_with_rs:', block_with_rs, '\nlen(block_with_rs):', len(block_with_rs))
                rs_code = block_with_rs[len(block):]
                # print('rs_code:', rs_code, '\nlen(rs_code):', len(rs_code))
                outf.write(rs_code)
                block = inf.read(64)
        axb = f'{block_num}x{rs_length}'
        outfile_path = f'{os.path.splitext(file_path)[0]}_rs_{axb}{os.path.splitext(file_path)[1]}'
        # 把原文件和纠错码整合起来放进结果文件中
        with open(file_path, 'rb') as inf1, open('temp.tmp', 'rb') as inf2, open(outfile_path, 'wb') as outf:
            content = inf1.read(10240)
            while content:
                outf.write(content)
                content = inf1.read(10240)
            content = inf2.read(10240)
            while content:
                outf.write(content)
                content = inf2.read(10240)
        entry3.insert('end', os.path.basename(outfile_path))
        label3.config(text=f'纠错码长度：{axb}')
        Tools.delete_file('temp.tmp')

    frm4 = tk.Frame(labelframe1)
    frm4.pack()
    label1 = tk.Label(frm4, text='请设置能够纠错的比例：', font=mid_font)
    label1.grid(row=1, column=1)
    entry1 = tk.Entry(frm4, font=mid_font, width=5)
    entry1.grid(row=1, column=2)
    entry1.insert('end', '10')
    entry1.bind('<KeyRelease>', change_scale1)
    label4 = tk.Label(frm4, text='%', font=mid_font)
    label4.grid(row=1, column=3)
    percent = tk.IntVar()
    percent.set(10)
    scale1 = tk.Scale(labelframe1, from_=0, to=100, orient=tk.HORIZONTAL, length=400, tickinterval=10, resolution=1,
                      showvalue=0, variable=percent, command=change_entry1)
    scale1.pack()
    label2 = tk.Label(labelframe1, text='请拖入需要添加纠错码的文件或输入地址：', font=mid_font)
    label2.pack()
    entry2 = tk.Entry(labelframe1, width=43, font=mid_font)
    entry2.pack()
    hook_dropfiles(entry2, func=drag1)
    frm1 = tk.Frame(labelframe1)
    frm1.pack()
    button1 = tk.Button(frm1, text='重置', font=mid_font, command=reset1)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm1, text='确定', font=mid_font, command=add_rs)
    button2.grid(row=1, column=2, padx=20)
    label3 = tk.Label(labelframe1, text='纠错码长度：0x0', font=mid_font)
    label3.pack()
    label4 = tk.Label(labelframe1, text='结果保存在原文件所在文件夹中的：', font=mid_font)
    label4.pack()
    entry3 = tk.Entry(labelframe1, width=43, font=mid_font)
    entry3.pack()

    # 纠正并去除RS纠错码（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='纠正错误并去除RS纠错码', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变

    def drag2(files):
        Tools.dragged_files(files, lf2_entry3)

    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()
    lf2_label1 = tk.Label(lf2_frm3, text='请输入纠错码的长度：', font=mid_font)
    lf2_label1.grid(row=1, column=1)
    lf2_entry1 = tk.Entry(lf2_frm3, width=8, font=mid_font)
    lf2_entry1.grid(row=1, column=2)
    lf2_label4 = tk.Label(lf2_frm3, text='x', font=mid_font)
    lf2_label4.grid(row=1, column=3)
    lf2_entry2 = tk.Entry(lf2_frm3, width=3, font=mid_font)
    lf2_entry2.grid(row=1, column=4)
    lf2_label2 = tk.Label(labelframe2, text='请拖入需要进行纠错的文件或输入地址：', font=mid_font)
    lf2_label2.pack()
    lf2_entry3 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry3.pack()
    hook_dropfiles(lf2_entry3, func=drag2)
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_frm4.pack()

    def reset2():
        Tools.reset(lf2_entry1)
        Tools.reset(lf2_entry2)
        Tools.reset(lf2_entry3)
        Tools.reset(lf2_entry4)
        lf2_label5.pack_forget()

    def repair(*args):
        # print('============================================================')
        repair_success = True
        Tools.reset(lf2_entry4)
        lf2_label5.pack_forget()
        file_path = Tools.get_path_from_entry(lf2_entry3)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            pass
        else:
            messagebox.showerror(title='文件路径错误', message='待纠错的文件路径错误')
            return 0
        block_num = lf2_entry1.get().strip()
        rs_length = lf2_entry2.get().strip()
        try:
            rs_length = eval(rs_length)
            assert isinstance(rs_length, int) and rs_length > 0
            block_num = eval(block_num)
            assert isinstance(block_num, int) and block_num > 0
        except Exception:
            messagebox.showerror('纠错码长度错误', '纠错码的长度应为正整数')
            return 0
        lf2_label3.config(text='正在处理中，请稍候...')
        window.update()
        outfile_path = f'{os.path.splitext(file_path)[0]}_repaired{os.path.splitext(file_path)[1]}'
        # 从文件的末尾读取纠错码，并把它从文件中截断，最后不管纠错是否成功都需要把截断的部分续上
        with open(file_path, 'rb+') as inf, open('temp2.tmp', 'wb+') as outf, open(outfile_path, 'wb') as outf2:
            # 把原文中的纠错码读取出来放在临时文件中
            inf.seek(-1 * rs_length * block_num, 2)
            rs_code = inf.read(10240)
            while rs_code:
                outf.write(rs_code)
                rs_code = inf.read(10240)
            # 读取并转移走纠错码之后，将原文中的纠错码截断
            inf.seek(-1 * rs_length * block_num, 2)
            inf.truncate()
            # 接下来对原文进行纠错
            inf.seek(0)
            outf.seek(0)
            block = inf.read(64)
            while block:
                # print('block:', block, '\nlen(block):', len(block))
                rs = RSCodec(rs_length)
                rs_block = outf.read(rs_length)
                # print('rs_block:', rs_block, '\nlen(rs_block):', len(rs_block))
                try:
                    outf2.write(rs.decode(block + rs_block)[0])
                except Exception:
                    outf2.write(block)
                    repair_success = False
                block = inf.read(64)
        if not repair_success:
            lf2_label5.pack()
        lf2_entry4.insert('end', outfile_path)
        # 无论纠错是否成功，都需要把纠错码添回原文件中
        with open(file_path, 'ab') as outf, open('temp2.tmp', 'rb') as inf:
            content = inf.read(10240)
            while content:
                outf.write(content)
                content = inf.read(10240)
        Tools.delete_file('temp2.tmp')
        lf2_label3.config(text='纠错后的结果保存在原文件所在文件夹中的：')

    lf2_button1 = tk.Button(lf2_frm4, text='重置', font=mid_font, command=reset2)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm4, text='确定', font=mid_font, command=repair)
    lf2_button2.grid(row=1, column=2, padx=20)
    lf2_label3 = tk.Label(labelframe2, text='纠错后的结果保存在原文件所在文件夹中的：', font=mid_font)
    lf2_label3.pack()
    lf2_entry4 = tk.Entry(labelframe2, font=mid_font, width=43)
    lf2_entry4.pack()
    lf2_label5 = tk.Label(labelframe2, text='已尽最大努力纠错，但仍有无法纠正的错误', font=mid_font)


def dh_exchange():
    # 会话发起人创建临时密钥（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='会话发起人', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()
    dh_private_key = p = g = ...

    def lf1_change_pack():
        lf1_frm2.pack_forget()
        lf1_frm7.pack_forget()
        Tools.reset(lf1_text1)
        Tools.reset(lf1_text2)
        lf1_text3.config(state='normal')
        Tools.reset(lf1_text3)
        lf1_text3.config(state='disabled')
        if lf1_with_rsa.get() == 'on':
            lf1_frm2.pack()
            lf1_text1.config(height=5)
            lf1_text2.config(height=4)
        elif lf1_with_rsa.get() == 'off':
            lf1_text1.config(height=8)
            lf1_text2.config(height=8)
        lf1_frm7.pack()

    def change_lf1_pwd_entry_show():
        Tools.change_entry_show(lf1_pwd_var, lf1_pwd_entry)

    def lf1_re_generate():
        Tools.reset(lf1_text1)
        Tools.reset(lf1_text2)
        lf1_text3.config(state='normal')
        Tools.reset(lf1_text3)
        lf1_text3.config(state='disabled')
        with_rsa = lf1_with_rsa.get()
        if with_rsa == 'on':
            pubkey_cipher = Tools.get_key(lf1_entry1, method='cipher')
            if pubkey_cipher == 0:
                return 0
            privkey_cipher = Tools.get_key(lf1_entry2, method='decipher', pwd_entry=lf1_pwd_entry)
            if privkey_cipher == 0:
                return 0
        nonlocal dh_private_key, p, g
        if safety.get() == '弱':
            key_size = 512
        elif safety.get() == '中':
            key_size = 1024
        elif safety.get() == '强':
            key_size = 1536
        parameters = dh.generate_parameters(generator=2, key_size=key_size)
        p, g = parameters.parameter_numbers().p, parameters.parameter_numbers().g
        dh_private_key = parameters.generate_private_key()
        y = dh_private_key.public_key().public_numbers().y
        dic = {'p': p, 'g': g, 'y1': y}  # p, g代表参数，y1代表会话发起人的DH公钥
        if with_rsa == 'on':
            ontology_path = '_temp_ontology.txt'
            ontology_sec_path = '_temp_ontology_RSAencrypted.txt'
            with open(ontology_path, 'w', encoding='utf-8') as f:
                f.write(str(dic))
            try:
                Tools.encrypt_bigfile(ontology_path, ontology_sec_path, pubkey_cipher)
            except Exception:
                tk.messagebox.showerror(title='加密出错', message='密钥可能有问题，请检查后重新选择')
            else:
                with open(ontology_sec_path, 'rb') as f:
                    lf1_text1.insert('end', base64.b64encode(f.read()).decode('utf-8'))
            os.remove(ontology_path)
            os.remove(ontology_sec_path)
        elif with_rsa == 'off':
            lf1_text1.insert('end', dic)

    def lf1_generate():
        lf1_text3.config(state='normal')
        Tools.reset(lf1_text3)
        lf1_text3.config(state='disabled')
        with_rsa = lf1_with_rsa.get()
        if with_rsa == 'on':
            privkey_cipher = Tools.get_key(lf1_entry2, method='decipher', pwd_entry=lf1_pwd_entry)
            if privkey_cipher == 0:
                return 0
            # 获取会话参与人发送的信息
            try:
                ontology_sec = base64.b64decode(lf1_text2.get(1.0, 'end').strip('\n'))
            except Exception:
                messagebox.showerror(title='密文格式错误', message="不是正确的base64编码")
                return 0
            ontology_sec_path = '_temp_ontology_sec.txt'
            ontology_path = '_temp_ontology_sec_RSA_Decrypted.txt'
            with open(ontology_sec_path, 'wb') as f:
                f.write(ontology_sec)
            try:
                Tools.decrypt_bigfile(ontology_sec_path, ontology_path, privkey_cipher)
            except Exception:
                tk.messagebox.showerror(title='解密出错', message='密钥或密文可能有问题，请检查后重新选择')
            else:
                with open(ontology_path, 'rb') as f:
                    ontology = f.read()
                try:
                    info = ontology.decode('utf-8')
                except Exception:
                    messagebox.showinfo(title='解密失败', message='密钥或密文可能不正确')
                    os.remove(ontology_path)
                    os.remove(ontology_sec_path)
                    return 0
            os.remove(ontology_path)
            os.remove(ontology_sec_path)
        elif with_rsa == 'off':
            info = lf1_text2.get(1.0, 'end').strip('\n')
        # 再获取信息中的值
        try:
            dic = eval(info)
            assert isinstance(dic, dict) and isinstance(dic.get('y2'), int)
        except Exception:
            messagebox.showerror('格式错误', '会话参与人回复的信息格式不正确')
            return 0
        y2 = dic['y2']
        # 计算共享密钥
        try:
            peer_public_key = dh.DHPublicNumbers(y2, dh.DHParameterNumbers(p, g)).public_key()
        except Exception:
            messagebox.showerror('无法生成临时密钥', '请先点击上方的刷新按钮，再进行密钥生成')
            return 0
        shared_key = dh_private_key.exchange(peer_public_key)
        # 进行密钥派生（将密钥摘要成合适长度）
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=30,
            salt=None,
            info=b'handshake data').derive(shared_key)
        lf1_text3.config(state='normal')
        lf1_text3.insert('end', base64.b64encode(derived_key))
        lf1_text3.config(state='disabled')

    def lf1_copy1():
        Tools.copy(lf1_text1, lf1_button1)

    def lf1_copy2():
        Tools.copy(lf1_text3, lf1_button4)

    def lf1_drag1(files):
        Tools.reset(lf1_text1)
        Tools.reset(lf1_text2)
        lf1_text3.config(state='normal')
        Tools.reset(lf1_text3)
        lf1_text3.config(state='disabled')
        Tools.dragged_files(files, lf1_entry1)

    def lf1_drag2(files):
        Tools.reset(lf1_text1)
        Tools.reset(lf1_text2)
        lf1_text3.config(state='normal')
        Tools.reset(lf1_text3)
        lf1_text3.config(state='disabled')
        Tools.dragged_files(files, lf1_entry2)

    def lf1_reset():
        Tools.reset(lf1_text2)
        lf1_text3.config(state='normal')
        Tools.reset(lf1_text3)
        lf1_text3.config(state='disabled')

    lf1_with_rsa = tk.StringVar()
    lf1_with_rsa.set('on')
    lf1_rb1 = tk.Radiobutton(lf1_frm1, text='配合RSA算法', variable=lf1_with_rsa, value='on', font=mid_font, command=lf1_change_pack)
    lf1_rb1.grid(row=1, column=1, padx=5)
    lf1_rb2 = tk.Radiobutton(lf1_frm1, text='单独使用DH算法', variable=lf1_with_rsa, value='off', font=mid_font, command=lf1_change_pack)
    lf1_rb2.grid(row=1, column=2, padx=5)
    lf1_frm2 = tk.Frame(labelframe1)
    lf1_frm2.pack()
    lf1_label1 = tk.Label(lf1_frm2, text='请拖入会话参与人的RSA公钥或输入地址：', font=mid_font)
    lf1_label1.pack()
    lf1_entry1 = tk.Entry(lf1_frm2, font=mid_font, width=43)
    lf1_entry1.pack()
    hook_dropfiles(lf1_entry1, func=lf1_drag1)
    lf1_label2 = tk.Label(lf1_frm2, text='请拖入自己的RSA私钥或输入地址：', font=mid_font)
    lf1_label2.pack()
    lf1_entry2 = tk.Entry(lf1_frm2, font=mid_font, width=43)
    lf1_entry2.pack()
    hook_dropfiles(lf1_entry2, func=lf1_drag2)
    lf1_pwd_frm = tk.Frame(lf1_frm2)
    lf1_pwd_frm.pack()
    lf1_pwd_label = tk.Label(lf1_pwd_frm, text='请输入该私钥的使用密码：', font=mid_font)
    lf1_pwd_label.grid(row=1, column=1, padx=5)
    lf1_pwd_var = tk.StringVar()
    lf1_pwd_var.set('1')
    lf1_pwd_cb = tk.Checkbutton(lf1_pwd_frm, text='隐藏', font=mid_font, variable=lf1_pwd_var, onvalue='1', offvalue='0', command=change_lf1_pwd_entry_show)
    lf1_pwd_cb.grid(row=1, column=2, padx=5)
    lf1_pwd_entry = tk.Entry(lf1_frm2, width=43, font=mid_font, show='*')
    lf1_pwd_entry.pack()
    lf1_frm7 = tk.Frame(labelframe1)
    lf1_frm7.pack()
    lf1_frm6 = tk.Frame(lf1_frm7)
    lf1_frm6.pack()
    lf1_label6 = tk.Label(lf1_frm6, font=mid_font, text='选择DH算法的安全性：')
    lf1_label6.grid(row=1, column=1, padx=5)
    safety = tk.StringVar()
    safety.set('中')
    lf1_rb3 = tk.Radiobutton(lf1_frm6, text='弱', font=mid_font, value='弱', variable=safety)
    lf1_rb3.grid(row=1, column=2, padx=5)
    lf1_rb4 = tk.Radiobutton(lf1_frm6, text='中', font=mid_font, value='中', variable=safety)
    lf1_rb4.grid(row=1, column=3, padx=5)
    lf1_rb4 = tk.Radiobutton(lf1_frm6, text='强', font=mid_font, value='强', variable=safety)
    lf1_rb4.grid(row=1, column=4, padx=5)
    lf1_frm3 = tk.Frame(lf1_frm7)
    lf1_frm3.pack()
    lf1_label3 = tk.Label(lf1_frm3, text='请将下面的信息发送给会话参与人：', font=mid_font)
    lf1_label3.grid(row=1, column=1)
    lf1_button2 = tk.Button(lf1_frm3, text='刷新', command=lf1_re_generate, font=mid_font)
    lf1_button2.grid(row=1, column=2)
    lf1_button1 = tk.Button(lf1_frm3, text='复制', command=lf1_copy1, fg=colors[ind], font=mid_font)
    lf1_button1.grid(row=1, column=3)
    lf1_text1 = tk.Text(lf1_frm7, font=mid_font, width=43, height=5)
    lf1_text1.pack()
    lf1_label4 = tk.Label(lf1_frm7, text='请输入会话参与人回复的信息：', font=mid_font)
    lf1_label4.pack()
    lf1_text2 = tk.Text(lf1_frm7, font=mid_font, width=43, height=4)
    lf1_text2.pack()
    lf1_frm4 = tk.Frame(lf1_frm7)
    lf1_frm4.pack()
    lf1_button5 = tk.Button(lf1_frm4, text='重置', font=mid_font, command=lf1_reset)
    lf1_button5.grid(row=1, column=1, padx=20)
    lf1_button3 = tk.Button(lf1_frm4, text='生成密钥', font=mid_font, command=lf1_generate)
    lf1_button3.grid(row=1, column=2, padx=20)
    lf1_button4 = tk.Button(lf1_frm4, text='复制结果', font=mid_font, command=lf1_copy2, fg=colors[ind])
    lf1_button4.grid(row=1, column=3, padx=20)
    lf1_label5 = tk.Label(lf1_frm7, text='此次会话的临时密钥为：（无需告知参与人）', font=mid_font)
    lf1_label5.pack()
    lf1_text3 = tk.Text(lf1_frm7, width=43, height=1, font=mid_font, state='disabled')
    lf1_text3.pack()

    # 会话参与人获取临时密钥（左边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='会话参与人', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    peer_dh_private_key = y1 = _p = _g = ...

    def lf2_change_pack():
        lf2_frm2.pack_forget()
        lf2_frm7.pack_forget()
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)
        lf2_text3.config(state='normal')
        Tools.reset(lf2_text3)
        lf2_text3.config(state='disabled')
        if lf2_with_rsa.get() == 'on':
            lf2_frm2.pack()
            lf2_text1.config(height=5)
            lf2_text2.config(height=5)
        elif lf2_with_rsa.get() == 'off':
            lf2_text1.config(height=9)
            lf2_text2.config(height=8)
        lf2_frm7.pack()

    def change_lf2_pwd_entry_show():
        Tools.change_entry_show(lf2_pwd_var, lf2_pwd_entry)

    def lf2_re_generate():
        if not lf2_text1.get(1.0, 'end').strip('\n'):
            return 0
        nonlocal peer_dh_private_key, y1, _p, _g
        Tools.reset(lf2_text2)
        lf2_text3.config(state='normal')
        Tools.reset(lf2_text3)
        lf2_text3.config(state='disabled')
        with_rsa = lf2_with_rsa.get()
        # 首先获取会话发起人发送的信息
        if with_rsa == 'on':
            pubkey_cipher = Tools.get_key(lf2_entry1, method='cipher')
            if pubkey_cipher == 0:
                return 0
            privkey_cipher = Tools.get_key(lf2_entry2, method='decipher', pwd_entry=lf2_pwd_entry)
            if privkey_cipher == 0:
                return 0
            try:
                ontology_sec = base64.b64decode(lf2_text1.get(1.0, 'end').strip('\n'))
            except Exception:
                messagebox.showerror(title='密文格式错误', message="不是正确的base64编码")
                return 0
            ontology_sec_path = '_temp_ontology_sec.txt'
            ontology_path = '_temp_ontology_sec_RSA_Decrypted.txt'
            with open(ontology_sec_path, 'wb') as f:
                f.write(ontology_sec)
            try:
                Tools.decrypt_bigfile(ontology_sec_path, ontology_path, privkey_cipher)
            except Exception:
                tk.messagebox.showerror(title='解密出错', message='密钥或密文可能有问题，请检查后重新选择')
                os.remove(ontology_path)
                os.remove(ontology_sec_path)
                return 0
            else:
                with open(ontology_path, 'rb') as f:
                    ontology = f.read()
                try:
                    info = ontology.decode('utf-8')
                except Exception:
                    messagebox.showinfo(title='解密失败', message='密钥或密文可能不正确')
                    os.remove(ontology_path)
                    os.remove(ontology_sec_path)
                    return 0
            os.remove(ontology_path)
            os.remove(ontology_sec_path)
        elif with_rsa == 'off':
            info = lf2_text1.get(1.0, 'end').strip('\n')
        # 再获取信息中的值
        try:
            dic = eval(info)
            assert isinstance(dic, dict) and isinstance(dic.get('p'), int) and isinstance(dic.get('g'), int) and isinstance(dic.get('y1'), int)
        except Exception:
            messagebox.showerror('格式错误', '会话发起人发送的信息格式不正确')
            return 0
        _p, _g, y1 = dic['p'], dic['g'], dic['y1']
        pn = dh.DHParameterNumbers(_p, _g)
        parameters = pn.parameters()
        peer_dh_private_key = parameters.generate_private_key()
        res_dic = {'y2': peer_dh_private_key.public_key().public_numbers().y}
        if with_rsa == 'off':
            lf2_text2.insert('end', res_dic)
        elif with_rsa == 'on':
            ontology_path = '_temp_ontology.txt'
            ontology_sec_path = '_temp_ontology_RSAencrypted.txt'
            with open(ontology_path, 'w', encoding='utf-8') as f:
                f.write(str(res_dic))
            try:
                Tools.encrypt_bigfile(ontology_path, ontology_sec_path, pubkey_cipher)
            except Exception:
                tk.messagebox.showerror(title='加密出错', message='密钥可能有问题，请检查后重新选择')
            else:
                with open(ontology_sec_path, 'rb') as f:
                    lf2_text2.insert('end', base64.b64encode(f.read()).decode('utf-8'))
            os.remove(ontology_path)
            os.remove(ontology_sec_path)

    def lf2_generate():
        lf2_text3.config(state='normal')
        Tools.reset(lf2_text3)
        lf2_text3.config(state='disabled')
        try:
            dh_public_key = dh.DHPublicNumbers(y1, dh.DHParameterNumbers(_p, _g)).public_key()
        except Exception:
            messagebox.showerror('无法生成临时密钥', '请先点击上方的刷新按钮，再进行密钥生成')
            return 0
        shared_key = peer_dh_private_key.exchange(dh_public_key)
        # 进行密钥派生（将密钥摘要成合适长度）
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=30,
            salt=None,
            info=b'handshake data').derive(shared_key)
        lf2_text3.config(state='normal')
        lf2_text3.insert('end', base64.b64encode(derived_key))
        lf2_text3.config(state='disabled')

    def lf2_copy1():
        Tools.copy(lf2_text2, lf2_button2)

    def lf2_copy2():
        Tools.copy(lf2_text3, lf2_button4)

    def lf2_drag1(files):
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)
        lf2_text3.config(state='normal')
        Tools.reset(lf2_text3)
        lf2_text3.config(state='disabled')
        Tools.dragged_files(files, lf2_entry1)

    def lf2_drag2(files):
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)
        lf2_text3.config(state='normal')
        Tools.reset(lf2_text3)
        lf2_text3.config(state='disabled')
        Tools.dragged_files(files, lf2_entry2)

    def lf2_reset():
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)
        lf2_text3.config(state='normal')
        Tools.reset(lf2_text3)
        lf2_text3.config(state='disabled')

    lf2_with_rsa = tk.StringVar()
    lf2_with_rsa.set('on')
    lf2_rb1 = tk.Radiobutton(lf2_frm1, text='配合RSA算法', variable=lf2_with_rsa, value='on', font=mid_font, command=lf2_change_pack)
    lf2_rb1.grid(row=1, column=1, padx=5)
    lf2_rb2 = tk.Radiobutton(lf2_frm1, text='单独使用DH算法', variable=lf2_with_rsa, value='off', font=mid_font, command=lf2_change_pack)
    lf2_rb2.grid(row=1, column=2, padx=5)
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_label1 = tk.Label(lf2_frm2, text='请拖入会话发起人的RSA公钥或输入地址：', font=mid_font)
    lf2_label1.pack()
    lf2_entry1 = tk.Entry(lf2_frm2, font=mid_font, width=43)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=lf2_drag1)
    lf2_label2 = tk.Label(lf2_frm2, text='请拖入自己的RSA私钥或输入地址：', font=mid_font)
    lf2_label2.pack()
    lf2_entry2 = tk.Entry(lf2_frm2, font=mid_font, width=43)
    lf2_entry2.pack()
    hook_dropfiles(lf2_entry2, func=lf2_drag2)
    lf2_pwd_frm = tk.Frame(lf2_frm2)
    lf2_pwd_frm.pack()
    lf2_pwd_label = tk.Label(lf2_pwd_frm, text='请输入该私钥的使用密码：', font=mid_font)
    lf2_pwd_label.grid(row=1, column=1, padx=5)
    lf2_pwd_var = tk.StringVar()
    lf2_pwd_var.set('1')
    lf2_pwd_cb = tk.Checkbutton(lf2_pwd_frm, text='隐藏', font=mid_font, variable=lf2_pwd_var, onvalue='1', offvalue='0',
                            command=change_lf2_pwd_entry_show)
    lf2_pwd_cb.grid(row=1, column=2, padx=5)
    lf2_pwd_entry = tk.Entry(lf2_frm2, width=43, font=mid_font, show='*')
    lf2_pwd_entry.pack()
    lf2_frm7 = tk.Frame(labelframe2)
    lf2_frm7.pack()
    lf2_label3 = tk.Label(lf2_frm7, text='请输入会话发起人发送的信息：', font=mid_font)
    lf2_label3.pack()
    lf2_text1 = tk.Text(lf2_frm7, font=mid_font, width=43, height=5)
    lf2_text1.pack()
    lf2_frm3 = tk.Frame(lf2_frm7)
    lf2_frm3.pack()
    lf2_label4 = tk.Label(lf2_frm3, text='请将下面的信息回复给会话发起人：', font=mid_font)
    lf2_label4.grid(row=1, column=1)
    lf2_button1 = tk.Button(lf2_frm3, text='刷新', command=lf2_re_generate, font=mid_font)
    lf2_button1.grid(row=1, column=2)
    lf2_button2 = tk.Button(lf2_frm3, text='复制', command=lf2_copy1, font=mid_font, fg=colors[ind])
    lf2_button2.grid(row=1, column=3)
    lf2_text2 = tk.Text(lf2_frm7, font=mid_font, width=43, height=5)
    lf2_text2.pack()
    lf2_frm4 = tk.Frame(lf2_frm7)
    lf2_frm4.pack(pady=7)
    lf2_button5 = tk.Button(lf2_frm4, text='重置', font=mid_font, command=lf2_reset)
    lf2_button5.grid(row=1, column=1, padx=20)
    lf2_button3 = tk.Button(lf2_frm4, text='生成密钥', font=mid_font, command=lf2_generate)
    lf2_button3.grid(row=1, column=2, padx=20)
    lf2_button4 = tk.Button(lf2_frm4, text='复制结果', font=mid_font, command=lf2_copy2, fg=colors[ind])
    lf2_button4.grid(row=1, column=3, padx=20)
    lf2_label5 = tk.Label(lf2_frm7, text='此次会话的临时密钥为：（无需告知发起人）', font=mid_font)
    lf2_label5.pack()
    lf2_text3 = tk.Text(lf2_frm7, width=43, height=1, font=mid_font, state='disabled')
    lf2_text3.pack()


def shamir_share():
    # 会话发起人创建并分发密钥（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='会话发起人创建并分发密钥', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def refresh():
        key = base64.b64encode(os.urandom(16)).decode()
        lf1_entry1.config(state='normal')
        Tools.reset(lf1_entry1)
        lf1_entry1.insert('end', key)
        lf1_entry1.config(state='readonly')
        lf1_label4.config(text='   ')

    def lf1_copy():
        Tools.copy(lf1_entry1, lf1_button2)

    def generate():
        number = lf1_entry2.get().strip()
        threshold = lf1_entry3.get().strip()
        try:
            number = eval(number)
            assert isinstance(number, int) and number >= 2
            threshold = eval(threshold)
            assert isinstance(threshold, int) and 2 <= threshold <= number
        except Exception:
            messagebox.showerror(title='输入错误', message='输入应为大于等于2的正整数，\n且密钥碎片数量应该大于等于能拼凑出密钥的碎片数量')
            return 0
        lf1_label4.config(text='生成中，请稍候...')
        window.update()
        shares = Shamir.split(threshold, number, base64.b64decode(lf1_entry1.get().encode()))
        shares_dir_path = os.path.join(os.getcwd(), 'Shamir_Shares')
        if not os.path.exists(shares_dir_path):
            os.mkdir(shares_dir_path)
        for ind, share in enumerate(shares, start=1):
            file_path = os.path.join(shares_dir_path, f'Shamir_share_{ind}.shamir')
            with open(file_path, 'wb') as f:
                pickle.dump(share, f)
        lf1_label4.config(text='结果保存在程序所在文件夹中的\nShamir_shares文件夹中')

    def open_dir():
        shares_dir_path = os.path.join(os.getcwd(), 'Shamir_Shares')
        if not os.path.exists(shares_dir_path):
            os.mkdir(shares_dir_path)
        os.system(f"explorer {os.path.join(os.getcwd(), 'Shamir_Shares')}")

    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()
    lf1_label1 = tk.Label(lf1_frm1, text='此次会话的临时密钥为：', font=mid_font)
    lf1_label1.grid(row=1, column=1, padx=5)
    lf1_button1 = tk.Button(lf1_frm1, text='刷新', font=mid_font, command=refresh)
    lf1_button1.grid(row=1, column=2, padx=5)
    lf1_button2 = tk.Button(lf1_frm1, text='复制', font=mid_font, command=lf1_copy, fg=colors[ind])
    lf1_button2.grid(row=1, column=3, padx=5)
    lf1_entry1 = tk.Entry(labelframe1, width=43, font=mid_font, state='readonly')
    lf1_entry1.pack()
    lf1_frm2 = tk.Frame(labelframe1)
    lf1_frm2.pack()
    lf1_label2 = tk.Label(lf1_frm2, text='设置将密钥分为多少碎片：    ', font=mid_font)
    lf1_label2.grid(row=1, column=1, padx=5)
    lf1_entry2 = tk.Entry(lf1_frm2, width=5, font=mid_font)
    lf1_entry2.grid(row=1, column=2, padx=5)
    lf1_frm3 = tk.Frame(labelframe1)
    lf1_frm3.pack()
    lf1_label3 = tk.Label(lf1_frm3, text='设置多少碎片可拼出完整密钥：', font=mid_font)
    lf1_label3.grid(row=1, column=1, padx=5)
    lf1_entry3 = tk.Entry(lf1_frm3, width=5, font=mid_font)
    lf1_entry3.grid(row=1, column=2, padx=5)
    lf1_frm4 = tk.Frame(labelframe1)
    lf1_frm4.pack()
    lf1_button3 = tk.Button(lf1_frm4, text='生成密钥碎片', font=mid_font, command=generate)
    lf1_button3.grid(row=1, column=1, padx=20)
    lf1_button4 = tk.Button(lf1_frm4, text='打开结果所在文件夹', font=mid_font, command=open_dir)
    lf1_button4.grid(row=1, column=2, padx=20)
    lf1_label4 = tk.Label(labelframe1, text='   ', font=mid_font)
    lf1_label4.pack()
    refresh()

    # 会话参与人拼凑密钥（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='会话参与人拼凑密钥', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变

    def lf2_drag(files):
        if not lf2_text1.get(1.0, 'end').strip():
            lf2_text1.insert('end', ',\n\n'.join([f.decode('GBK') for f in files]))
        else:
            lf2_text1.insert('end', ', \n\n')
            lf2_text1.insert('end', ',\n\n'.join([f.decode('GBK') for f in files]))

    def lf2_reset():
        Tools.reset(lf2_text1)
        lf2_entry1.config(state='normal')
        Tools.reset(lf2_entry1)
        lf2_entry1.config(state='readonly')

    def lf2_copy():
        Tools.copy(lf2_entry1, lf2_button3)

    def combine():
        lf2_entry1.config(state='normal')
        Tools.reset(lf2_entry1)
        lf2_entry1.config(state='readonly')
        file_paths = [f.strip() for f in lf2_text1.get(1.0, 'end').strip().replace('，', ',').split(',')]
        shares = []
        for ind, file_path in enumerate(file_paths, start=1):
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    try:
                        share = pickle.load(f)
                        print('share:', share)
                    except Exception:
                        messagebox.showerror('密钥碎片内容错误', f'第{ind}个密钥碎片的内容读取失败')
                        return 0
                    shares.append(share)
            else:
                messagebox.showerror('密钥碎片路径错误', f'第{ind}个密钥碎片的路径不存在')
                return 0
        try:
            key = Shamir.combine(shares)
        except Exception:
            messagebox.showerror('密钥碎片拼凑失败', f'密钥碎片拼凑失败，请检查输入')
            return 0
        lf2_entry1.config(state='normal')
        lf2_entry1.insert('end', base64.b64encode(key).decode())
        lf2_entry1.config(state='readonly')

    lf2_label1 = tk.Label(labelframe2, text='请拖入密钥碎片或输入地址\n（用‘，’或‘,’分隔）：', font=mid_font)
    lf2_label1.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, font=mid_font, height=20)
    lf2_text1.pack()
    hook_dropfiles(lf2_text1, func=lf2_drag)
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_button1 = tk.Button(lf2_frm1, text='重置', font=mid_font, command=lf2_reset)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm1, text='确定', font=mid_font, command=combine)
    lf2_button2.grid(row=1, column=2, padx=20)
    lf2_button3 = tk.Button(lf2_frm1, text='复制密钥', font=mid_font, command=lf2_copy, fg=colors[ind])
    lf2_button3.grid(row=1, column=3, padx=20)
    lf2_label2 = tk.Label(labelframe2, text='此次会话的临时密钥为：', font=mid_font)
    lf2_label2.pack()
    lf2_entry1 = tk.Entry(labelframe2, width=43, font=mid_font, state='readonly')
    lf2_entry1.pack()
