# -*- coding: utf-8 -*-
import base64
import numpy as np
import binascii
import hashlib
import random
import os
import re
import shutil
import time
import tkinter as tk
import zlib
import tenseal as ts
from random import randint
from tkinter import messagebox
from tkinter import ttk
from Crypto import Random  # pip install pycryptodome
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384
from Crypto.Hash import MD4
from Crypto.Hash import RIPEMD160
from windnd import hook_dropfiles
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from system_resource.ToolKit import Tools  # 注意：这里没有写错，因为这句话是交给main.py执行的，必须从它的视角进行相对引用

window = frm = mid_font = icon_path = colors = ind = ...


def initiation(_window, _frm, _mid_font, _icon_path, _colors, _ind):
    global window, frm, mid_font, icon_path, colors, ind
    window = _window
    frm = _frm
    mid_font = _mid_font
    icon_path = _icon_path
    colors = _colors
    ind = _ind


def create_rsa_key():
    frm_of_labelframe = tk.Frame(frm)
    frm_of_labelframe.pack()
    # 连续随机生成
    labelframe1 = tk.LabelFrame(frm_of_labelframe, text='连续随机生成RSA密钥对', height=457, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def clean_entry_length():
        Tools.reset(entry_length)

    frm1 = tk.Frame(labelframe1)
    frm1.pack()
    number_of_frm1 = 1
    label1 = tk.Label(frm1, text=f'请选择第 {number_of_frm1} 对密钥的长度：', font=mid_font)
    label1.pack()
    frm2 = tk.Frame(labelframe1)
    frm2.pack()
    var1 = tk.IntVar()
    var1.set(1024)
    rb1 = tk.Radiobutton(frm2, variable=var1, text='1024', font=mid_font, value=1024)
    rb1.grid(row=1, column=1, padx=20)
    rb2 = tk.Radiobutton(frm2, variable=var1, text='2048', font=mid_font, value=2048)
    rb2.grid(row=1, column=2, padx=0)
    rb3 = tk.Radiobutton(frm2, variable=var1, text='3072', font=mid_font, value=3072)
    rb3.grid(row=1, column=3, padx=20)
    rb4 = tk.Radiobutton(frm2, variable=var1, text='', font=mid_font, value=0, command=clean_entry_length)
    rb4.grid(row=1, column=4, padx=0)
    entry_length = tk.Entry(frm2, font=mid_font, width=6)
    entry_length.grid(row=1, column=5, padx=0)
    entry_length.insert('end', '自定义')
    _lab = tk.Label(frm2, text='')
    _lab.grid(row=1, column=6, padx=20)
    frm3 = tk.Frame(labelframe1)
    frm3.pack()
    label2 = tk.Label(frm3, text=f'第 {number_of_frm1} 对密钥将保存在', font=mid_font)
    label2.grid(row=1, column=1)
    entry1 = tk.Entry(frm3, show=None, width=4, font=mid_font)
    entry1.grid(row=1, column=2)
    entry1.insert('end', '1')
    label3 = tk.Label(frm3, text=f'号文件夹内', font=mid_font)
    label3.grid(row=1, column=3)
    frm4 = tk.Frame(labelframe1)
    frm4.pack()
    top_lay = []

    def start(*args):
        nonlocal number_of_frm1  # f'请选择第 {number_of_frm1} 对密钥的长度：'

        # 获取用户输入的保存目录
        try:
            number_of_entry1 = int(entry1.get())
            if number_of_entry1 < 0:
                messagebox.showerror(title='输入错误', message='请在输入框内输入非负整数')
                return 0
        except ValueError:
            messagebox.showerror(title='输入错误', message='请在输入框内输入非负整数')
            return 0

        frm6.pack_forget()
        for i in top_lay:
            i.destroy()

        flag = True  # 用于表示现在在正在进行生成还是停止生成
        new_created_key = 0  # 新产生了多少密钥对

        def stop():
            nonlocal flag, entry1, new_created_key
            flag = False
            Tools.clean_all_widget(frm3)
            label6 = tk.Label(frm3, text=f'第 {number_of_frm1} 对密钥将保存在', font=mid_font)
            label6.grid(row=1, column=1)
            entry1 = tk.Entry(frm3, width=4, font=mid_font)
            entry1.grid(row=1, column=2)
            entry1.insert('end', number_of_entry1)
            label11 = tk.Label(frm3, text=f'号文件夹内', font=mid_font)
            label11.grid(row=1, column=3)
            Tools.clean_all_widget(frm4)
            label10 = tk.Label(frm4, text='请等待当前密钥生成完成', font=mid_font)
            label10.pack()
            frm6.pack(side='bottom', pady=40)
            new_created_key = 0

        Tools.clean_all_widget(frm4)
        button3 = tk.Button(frm4, text='暂停生成', font=mid_font, command=stop)
        button3.pack(side='right', padx=80)
        label_invisible = tk.Label(frm4, text='', font=mid_font)
        label_invisible.pack(side='left', padx=80)  # 这个label不显示信息，只是排版需要

        previous_key_length = None
        while flag:
            current_key_length = var1.get()
            if current_key_length == 0:
                try:
                    current_key_length = eval(entry_length.get())
                    assert isinstance(current_key_length, int) and current_key_length >= 1024
                except Exception:
                    messagebox.showerror(title='数值错误', message='密钥长度应为大于等于1024的正整数')
                    break
            Tools.clean_all_widget(frm1)
            number_of_frm1 += 1
            label4 = tk.Label(frm1, text=f'请选择第 {number_of_frm1} 对密钥的长度', font=mid_font)
            label4.pack()
            Tools.clean_all_widget(frm3)
            number_of_entry1 += 1
            label5 = tk.Label(frm3, text=f'第 {number_of_frm1} 对密钥将保存在 {number_of_entry1} 号文件夹内', font=mid_font)
            label5.pack()
            Tools.clean_all_widget(frm5)
            label7 = tk.Label(frm5, text=f'正在生成第 {number_of_frm1 - 1} 对{current_key_length}位密钥，请稍候...', font=mid_font)
            label7.pack()
            if new_created_key >= 1:
                label8 = tk.Label(frm5, text=f'第 {number_of_frm1 - 2} 对{previous_key_length}位密钥生成完成', font=mid_font)
                label8.pack()
            window.update()
            # 创建公私钥
            random_generator = Random.new(random.random()).read
            rsa = RSA.generate(current_key_length, random_generator)
            # 生成私钥
            pri = rsa.exportKey()
            # 生成公钥（从私钥中推导）
            pub = rsa.publickey().exportKey()
            # 保存公私钥
            current_path = os.getcwd()
            keys_dir_path = current_path + '\\keys'
            if not os.path.exists(keys_dir_path):
                os.mkdir(keys_dir_path)
            key_path = keys_dir_path + f'\\{number_of_entry1 - 1}'
            if not os.path.exists(key_path):
                os.mkdir(key_path)
            else:
                shutil.rmtree(key_path)
                os.mkdir(key_path)
            with open(key_path + f'\\RSA_public_key_{current_key_length}.pem', 'wb+') as pubfile:
                pubfile.write(pub)
            with open(key_path + f'\\RSA_private_key_{current_key_length}.pem', 'wb+') as prifile:
                prifile.write(pri)
            new_created_key += 1
            previous_key_length = current_key_length

        Tools.clean_all_widget(frm4)
        button1 = tk.Button(frm4, text='开始生成', font=mid_font, command=start)
        button1.pack(side='left', padx=50)
        Tools.clean_all_widget(frm5)
        label9 = tk.Label(frm5, text=f'已生成{number_of_frm1 - 1}对密钥', font=mid_font)
        label9.pack()

    button1 = tk.Button(frm4, text='开始生成', font=mid_font, command=start)
    button1.pack()
    entry1.bind('<Return>', start)
    frm5 = tk.Frame(labelframe1)
    frm5.pack()

    def tell_detail():
        detail_window = tk.Toplevel(window)
        detail_window.geometry('1290x900')
        detail_window.title('RSA密钥详情')
        detail_window.iconbitmap(icon_path)
        top_lay.append(detail_window)

        def get_key_content(path: str):
            path = path.strip().strip('\"').lstrip("“").rstrip("”")
            if os.path.exists(path) and path.endswith('.pem'):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content
            else:
                return '读取失败'

        def read_default():

            def get_key_pairs_name_and_path_in_keys_dir():
                # 找到keys文件夹内所有的数字型名称的文件夹的名字和地址
                _key_pair_name_list = []
                _key_path_dic = {}  # 通过字典保存文件夹的地址
                current_path = os.getcwd()
                keys_dir_path = current_path + '\\keys'
                if not os.path.exists(keys_dir_path):
                    os.mkdir(keys_dir_path)
                for i in os.listdir(keys_dir_path):
                    key_pair_path = keys_dir_path + f'\\{i}'
                    try:
                        if os.path.isdir(key_pair_path) and int(i) >= 0:
                            _key_pair_name_list.append(int(i))
                            _key_path_dic[i] = key_pair_path
                    except Exception:
                        ...  # 如果报错就不执行
                _key_pair_name_list = sorted(_key_pair_name_list)
                return [str(j) for j in _key_pair_name_list], _key_path_dic
            Tools.clean_all_widget(_frm)
            _frm2 = tk.Frame(_frm)
            _frm2.pack()
            label1 = tk.Label(_frm2, text='打开', font=mid_font)
            label1.grid(row=1, column=1)
            key_pair_name_list, key_path_dic = get_key_pairs_name_and_path_in_keys_dir()
            entry1 = tk.Entry(_frm2, width=4, font=mid_font, show=None)
            entry1.grid(row=1, column=2)
            key_name = None
            if len(key_pair_name_list) >= 1:
                key_name = key_pair_name_list[-1]
                entry1.insert('end', key_name)
            label2 = tk.Label(_frm2, text='号文件夹', font=mid_font)
            label2.grid(row=1, column=3)

            def show_key_content(*args):
                nonlocal key_pair_name_list, key_path_dic, label_list, key_name
                key_pair_name_list, key_path_dic = get_key_pairs_name_and_path_in_keys_dir()
                _key_name = entry1.get()
                try:
                    if int(_key_name) < 0:
                        messagebox.showerror(title='输入错误', message='请输入非负整数')
                        return 0
                except ValueError:
                    messagebox.showerror(title='输入错误', message='请输入非负整数')
                    return 0
                if _key_name in key_pair_name_list:
                    key_path = key_path_dic[_key_name]
                else:
                    messagebox.showerror(title='输入错误', message='输入的文件夹的名称不存在')
                    return 0
                key_name = _key_name
                two_keys = os.listdir(key_path)
                find_pub_key, find_priv_key = False, False
                for i in two_keys:
                    if re.findall('public_key_\d{3,4}\.pem', i):
                        pubkey_path = key_path + "\\" + i
                        find_pub_key = True
                    elif re.findall('private_key_\d{3,4}\.pem', i):
                        privkey_path = key_path + "\\" + i
                        find_priv_key = True
                text1.delete('1.0', 'end')
                text2.delete('1.0', 'end')
                if find_pub_key:
                    pubkey_content = get_key_content(pubkey_path)
                    text1.insert('end', pubkey_content)
                else:
                    text1.insert('end', '未找到RSA公钥')
                if find_priv_key:
                    privkey_content = get_key_content(privkey_path)
                    text2.insert('end', privkey_content)
                else:
                    text2.insert('end', '未找到RSA私钥')
                label_list[0].configure(text=f'第 {key_name} 号公钥：')
                label_list[1].configure(text=f'第 {key_name} 号私钥：')

            button1 = tk.Button(_frm2, text='确认', font=mid_font, command=show_key_content)
            button1.grid(row=1, column=4, padx=30)
            entry1.bind('<Return>', show_key_content)
            _frm5 = tk.Frame(_frm)
            _frm5.pack()
            _frm6 = tk.Frame(_frm5)
            _frm6.pack(side='left', padx=5)
            _frm7 = tk.Frame(_frm5)
            _frm7.pack(side='right', padx=5)
            label_list = []
            label4 = tk.Label(_frm6, text='公钥：', font=mid_font)
            label4.pack()
            label_list.append(label4)
            text1 = tk.Text(_frm6, width=47, height=27, font=mid_font)
            text1.pack()
            label5 = tk.Label(_frm7, text='私钥：', font=mid_font)
            label5.pack()
            label_list.append(label5)
            text2 = tk.Text(_frm7, width=47, height=27, font=mid_font)
            text2.pack()
            _frm8 = tk.Frame(_frm)
            _frm8.pack(pady=10)
            if entry1.get():
                show_key_content()

            def previous_pair():
                nonlocal key_name, entry1
                key_pair_name_list, key_path_dic = get_key_pairs_name_and_path_in_keys_dir()
                if len(key_pair_name_list) >= 1:
                    if key_name is None:
                        entry1.delete(0, 'end')
                        entry1.insert('end', key_pair_name_list[0])
                        show_key_content()
                    else:
                        previous_key_name = None
                        for i in key_pair_name_list:
                            if int(i) >= int(key_name):
                                break
                            else:
                                previous_key_name = i
                        if previous_key_name is not None:
                            entry1.delete(0, 'end')
                            entry1.insert('end', previous_key_name)
                            show_key_content()

            def next_pair():
                nonlocal key_name, entry1
                key_pair_name_list, key_path_dic = get_key_pairs_name_and_path_in_keys_dir()
                if len(key_pair_name_list) >= 1:
                    if key_name is None:
                        entry1.delete(0, 'end')
                        entry1.insert('end', key_pair_name_list[-1])
                        show_key_content()
                    else:
                        for i in key_pair_name_list:
                            if int(i) > int(key_name):
                                entry1.delete(0, 'end')
                                entry1.insert('end', i)
                                show_key_content()
                                break
                        else:
                            ...  # 如果没有比key_name大的，就不要执行

            button2 = tk.Button(_frm8, text='上一对', font=mid_font, command=previous_pair)
            button2.grid(row=1, column=1, padx=15)
            button3 = tk.Button(_frm8, text='下一对', font=mid_font, command=next_pair)
            button3.grid(row=1, column=2, padx=15)

        def read_input():
            Tools.clean_all_widget(_frm)

            def show_key_content():
                pubkey_path = entry1.get()
                if pubkey_path:
                    text1.delete(1.0, 'end')
                    pubkey_content = get_key_content(pubkey_path)
                    if 'BEGIN PUBLIC KEY' in pubkey_content or '读取失败' in pubkey_content:
                        text1.insert('end', pubkey_content)
                    else:
                        text1.insert('end', '这不是RSA公钥')

                privkey_path = entry2.get()
                if privkey_path:
                    text2.delete(1.0, 'end')
                    privkey_content = get_key_content(privkey_path)
                    if 'BEGIN RSA PRIVATE KEY' in privkey_content or '读取失败' in privkey_content:
                        text2.insert('end', privkey_content)
                    else:
                        text2.insert('end', '这不是RSA私钥')

            def drag1(files):
                Tools.dragged_files(files, entry1)
                show_key_content()

            def drag2(files):
                Tools.dragged_files(files, entry2)
                show_key_content()

            _frm2 = tk.Frame(_frm)
            _frm2.pack()
            _frm3 = tk.Frame(_frm2)
            _frm3.grid(row=1, column=1, padx=18)
            label4 = tk.Label(_frm3, text='拖入公钥或输入地址：', font=mid_font)
            label4.pack()
            entry1 = tk.Entry(_frm3, width=42, font=mid_font, show=None)
            entry1.pack()
            hook_dropfiles(entry1, func=drag1)
            button3 = tk.Button(_frm2, text='确认', font=mid_font, command=show_key_content)
            button3.grid(row=1, column=2, padx=18)
            _frm4 = tk.Frame(_frm2)
            _frm4.grid(row=1, column=3, padx=18)
            label5 = tk.Label(_frm4, text='拖入私钥或输入地址：', font=mid_font)
            label5.pack()
            entry2 = tk.Entry(_frm4, width=42, font=mid_font, show=None)
            entry2.pack()
            hook_dropfiles(entry2, func=drag2)
            _frm5 = tk.Frame(_frm)
            _frm5.pack()
            _frm6 = tk.Frame(_frm5)
            _frm6.pack(side='left', padx=5)
            label6 = tk.Label(_frm6, text='公钥：', font=mid_font)
            label6.pack()
            text1 = tk.Text(_frm6, width=47, height=29, font=mid_font)
            text1.pack()
            _frm7 = tk.Frame(_frm5)
            _frm7.pack(side='right', padx=5)
            label7 = tk.Label(_frm7, text='私钥：', font=mid_font)
            label7.pack()
            text2 = tk.Text(_frm7, width=47, height=29, font=mid_font)
            text2.pack()

        _frm1 = tk.Frame(detail_window)
        _frm1.pack()
        _frm = tk.Frame(detail_window)
        _frm.pack()
        inner_var1 = tk.StringVar()
        inner_var1.set('1')
        _rb1 = tk.Radiobutton(_frm1, font=mid_font, text='读取RSA密钥对的默认地址', variable=inner_var1, value='1', command=read_default)
        _rb1.grid(row=1, column=1, padx=20)
        _rb2 = tk.Radiobutton(_frm1, font=mid_font, text='输入RSA密钥对的地址', variable=inner_var1, value='2', command=read_input)
        _rb2.grid(row=1, column=2, padx=20)
        read_default()

    def open_dir():
        keys_dir_path = os.path.join(os.getcwd(), 'keys')
        if not os.path.exists(keys_dir_path):
            os.mkdir(keys_dir_path)
        os.system(f"explorer {os.path.join(os.getcwd(), 'keys')}")

    frm6 = tk.Frame(frm)
    frm6.pack()
    button2 = tk.Button(frm6, text='查看密钥详情', font=mid_font, command=tell_detail)
    button2.grid(row=1, column=1, padx=20)
    open_dir_button = tk.Button(frm6, text='打开密钥保存的文件夹', font=mid_font, command=open_dir)
    open_dir_button.grid(row=1, column=2, padx=20)

    # 随机生成一对
    labelframe2 = tk.LabelFrame(frm_of_labelframe, text='随机生成一对RSA密钥', height=457, width=606, font=mid_font)
    labelframe2.pack(side='left', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_label1 = tk.Label(labelframe2, text='请选择密钥的长度：', font=mid_font)
    lf2_label1.pack()

    def clean_lf2_entry_length():
        Tools.reset(lf2_entry_length)

    def lf2_confirm(*args):
        Tools.clean_all_widget(lf2_frm2)
        length = lf2_var1.get()
        if length == 0:
            try:
                length = eval(lf2_entry_length.get())
                assert isinstance(length, int) and length >= 1024
            except Exception:
                messagebox.showerror(title='数值错误', message='密钥长度应为大于等于1024的正整数')
                return 0
        lf2_label2 = tk.Label(lf2_frm2, text='程序正在进行中，请稍候...', font=mid_font)
        lf2_label2.pack()
        window.update()
        lf2_label2.destroy()
        random_generator = Random.new(random.random()).read
        rsa = RSA.generate(length, random_generator)
        # 生成私钥
        private_key = rsa.exportKey()
        # 生成公钥（从私钥中推导）
        public_key = rsa.public_key().exportKey()
        lf2_label3 = tk.Label(lf2_frm2, text='公钥（public key）：\n' + public_key.decode('utf-8')[26: 30].replace('\n', ' ') + ' ... ' + public_key.decode('utf-8')[-50: -24].replace('\n', ' '), font=mid_font)
        lf2_label3.pack()
        lf2_label4 = tk.Label(lf2_frm2, font=mid_font, text='私钥（private key）：\n' + private_key.decode('utf-8')[31: 35].replace('\n', ' ') + ' ... ' + private_key.decode('utf-8')[-55: -29].replace('\n', ' '))
        lf2_label4.pack()
        # 保存公私钥
        current_dir = os.getcwd()  # 获取程序所在目录
        key_path = current_dir + '\\keys'
        if not os.path.exists(key_path):
            os.mkdir(key_path)  # 创建文件夹
        with open(key_path + f'\\RSA_public_key_{length}.pem', 'wb+') as pubfile:
            pubfile.write(public_key)
        with open(key_path + f'\\RSA_private_key_{length}.pem', 'wb+') as prifile:
            prifile.write(private_key)
        lf2_label5 = tk.Label(lf2_frm2, text='公私钥已经保存至', font=mid_font)
        lf2_label5.pack()
        lf2_entry1 = tk.Entry(lf2_frm2, width=43, font=mid_font)
        lf2_entry1.pack()
        lf2_entry1.insert(0, key_path)
        lf2_label6 = tk.Label(lf2_frm2, text='文件夹中的.pem文件内', font=mid_font)
        lf2_label6.pack()
        lf2_label7 = tk.Label(lf2_frm2, text='注意：新生成的密钥会替换文件夹内同名的旧密钥', font=mid_font, fg='red')
        lf2_label7.pack()

    lf2_var1 = tk.IntVar()
    lf2_var1.set(1024)
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_rb1 = tk.Radiobutton(lf2_frm1, variable=lf2_var1, text='1024', font=mid_font, value=1024)
    lf2_rb1.grid(row=1, column=1, padx=20)
    lf2_rb2 = tk.Radiobutton(lf2_frm1, variable=lf2_var1, text='2048', font=mid_font, value=2048)
    lf2_rb2.grid(row=1, column=2, padx=0)
    lf2_rb3 = tk.Radiobutton(lf2_frm1, variable=lf2_var1, text='3072', font=mid_font, value=3072)
    lf2_rb3.grid(row=1, column=3, padx=20)
    lf2_rb4 = tk.Radiobutton(lf2_frm1, variable=lf2_var1, text='', font=mid_font, value=0, command=clean_lf2_entry_length)
    lf2_rb4.grid(row=1, column=4, padx=0)
    lf2_entry_length = tk.Entry(lf2_frm1, font=mid_font, width=6)
    lf2_entry_length.grid(row=1, column=5, padx=0)
    lf2_entry_length.insert('end', '自定义')
    lf2_entry_length.bind('<Return>', lf2_confirm)
    lf2_button1 = tk.Button(labelframe2, text='确定', font=mid_font, command=lf2_confirm)
    lf2_button1.pack()
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()


def set_pwd_of_rsa_privkey():
    # 添加密码或去除密码（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='为RSA私钥添加或去除使用密码', height=741, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()

    def change_lf1_entry1_show():
        Tools.change_entry_show(lf1_var1, lf1_entry1)

    def change_lf1_entry2_show():
        Tools.change_entry_show(lf1_var2, lf1_entry2)

    def lf1_confirm():
        lf1_label4.config(text='   ')
        lf1_text1.config(state='normal')
        Tools.reset(lf1_text1)
        key_path = Tools.get_path_from_entry(lf1_entry1)
        if os.path.exists(key_path):
            with open(Tools.get_path_from_entry(lf1_entry1), 'rb') as f:
                key = f.read()
                if bytes("-----BEGIN RSA PRIVATE KEY-----".encode('utf-8')) in key:
                    lf1_text1.insert('end', key.decode('utf-8'))
                else:
                    lf1_text1.insert('end', '这不是正确的私钥')
        else:
            lf1_text1.insert('end', '私钥地址错误')
        lf1_text1.config(state='disabled')

    def lf1_drag(files):
        Tools.dragged_files(files, lf1_entry1)
        lf1_confirm()

    def lf1_reset():
        Tools.reset(lf1_entry1)
        Tools.reset(lf1_entry2)
        lf1_text1.config(state='normal')
        Tools.reset(lf1_text1)
        lf1_text1.config(state='disabled')
        lf1_label4.config(text='   ')

    lf1_label1 = tk.Label(lf1_frm1, text='请拖入您的私钥或输入地址：', font=mid_font)
    lf1_label1.grid(row=1, column=1, padx=5)
    lf1_var1 = tk.StringVar()
    lf1_var1.set('0')
    lf1_cb1 = tk.Checkbutton(lf1_frm1, text='隐藏', font=mid_font, variable=lf1_var1, onvalue='1', offvalue='0', command=change_lf1_entry1_show)
    lf1_cb1.grid(row=1, column=2, padx=5)
    lf1_entry1 = tk.Entry(labelframe1, width=43, font=mid_font)
    lf1_entry1.pack()
    hook_dropfiles(lf1_entry1, func=lf1_drag)
    lf1_frm3 = tk.Frame(labelframe1)
    lf1_frm3.pack()
    lf1_button3 = tk.Button(lf1_frm3, text='重置', font=mid_font, command=lf1_reset)
    lf1_button3.grid(row=1, column=1, padx=20)
    lf1_button4 = tk.Button(lf1_frm3, text='确定', font=mid_font, command=lf1_confirm)
    lf1_button4.grid(row=1, column=2, padx=20)
    lf1_label2 = tk.Label(labelframe1, text='该私钥的内容为：', font=mid_font)
    lf1_label2.pack()
    lf1_text1 = tk.Text(labelframe1, width=43, height=16, font=mid_font, state='disabled')
    lf1_text1.pack()
    lf1_frm4 = tk.Frame(labelframe1)
    lf1_frm4.pack()
    lf1_label3 = tk.Label(lf1_frm4, text='请输入私钥的使用密码：', font=mid_font)
    lf1_label3.grid(row=1, column=1, padx=5)
    lf1_var2 = tk.StringVar()
    lf1_var2.set('1')
    lf1_cb2 = tk.Checkbutton(lf1_frm4, text='隐藏', font=mid_font, variable=lf1_var2, onvalue='1', offvalue='0', command=change_lf1_entry2_show)
    lf1_cb2.grid(row=1, column=2, padx=5)
    lf1_entry2 = tk.Entry(labelframe1, width=43, font=mid_font, show='*')
    lf1_entry2.pack()
    lf1_frm2 = tk.Frame(labelframe1)
    lf1_frm2.pack()

    def encrypt():
        global ind
        ind = (ind + 1) % 6
        lf1_label4.config(fg=colors[ind])
        lf1_text1.config(state='normal')
        privkey = lf1_text1.get(1.0, 'end').strip('\n')
        lf1_text1.config(state='disabled')
        if privkey == '这不是正确的私钥' or privkey == '私钥地址错误' or not privkey:
            lf1_label4.config(text='无法加密')
        elif not lf1_entry2.get().strip(' '):
            lf1_label4.config(text='密码不能为空')
        else:
            enc_key = Tools.encrypt_privkey(privkey.encode('utf-8'), lf1_entry2.get())
            if enc_key == b'':
                lf1_label4.config(text='已经加密过，无法再次加密')
                return 0
            with open(Tools.get_path_from_entry(lf1_entry1), 'wb') as f:
                f.write(enc_key)
            lf1_label4.config(text='加密成功')
            lf1_text1.config(state='normal')
            Tools.reset(lf1_text1)
            lf1_text1.insert('end', enc_key.decode('utf-8'))
            lf1_text1.config(state='disabled')

    def decrypt():
        global ind
        ind = (ind + 1) % 6
        lf1_label4.config(fg=colors[ind])
        lf1_text1.config(state='normal')
        privkey = lf1_text1.get(1.0, 'end').strip('\n')
        lf1_text1.config(state='disabled')
        if privkey == '这不是正确的私钥' or privkey == '私钥地址错误' or not privkey:
            lf1_label4.config(text='无法解密')
            return 0
        elif not lf1_entry2.get().strip(' '):
            lf1_label4.config(text='密码不能为空')
            return 0
        else:
            dec_key = Tools.decrypt_privkey(privkey.encode('utf-8'), lf1_entry2.get())
            if dec_key == b'':
                lf1_label4.config(text='私钥的使用密码错误')
                return 0
            elif dec_key == b'1':
                lf1_label4.config(text='已经去除过密码，无法再次去除')
                return 0
            with open(Tools.get_path_from_entry(lf1_entry1), 'wb') as f:
                f.write(dec_key)
            lf1_label4.config(text='已去除密码')
            lf1_text1.config(state='normal')
            Tools.reset(lf1_text1)
            lf1_text1.insert('end', dec_key)
            lf1_text1.config(state='disabled')

    lf1_button1 = tk.Button(lf1_frm2, text='去除密码', font=mid_font, command=decrypt)
    lf1_button1.grid(row=1, column=1, padx=20)
    lf1_button2 = tk.Button(lf1_frm2, text='添加密码', font=mid_font, command=encrypt)
    lf1_button2.grid(row=1, column=2, padx=20)
    lf1_label4 = tk.Label(labelframe1, text='   ', font=mid_font, fg=colors[ind])
    lf1_label4.pack()

    # 修改密码（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='为RSA私钥修改使用密码', height=741, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()

    def change_lf2_entry1_show():
        Tools.change_entry_show(lf2_var1, lf2_entry1)

    def change_lf2_entry2_show():
        Tools.change_entry_show(lf2_var2, lf2_entry2)

    def change_lf2_entry3_show():
        Tools.change_entry_show(lf2_var3, lf2_entry3)

    def lf2_drag(files):
        Tools.dragged_files(files, lf2_entry1)
        lf2_confirm1()

    def lf2_reset1():
        Tools.reset(lf2_entry1)
        lf2_label5.config(text='   ')
        lf2_text1.config(state='normal')
        Tools.reset(lf2_text1)
        lf2_text1.config(state='disabled')
        lf2_reset2()

    def lf2_confirm1():
        lf2_label5.config(text='   ')
        lf2_text1.config(state='normal')
        Tools.reset(lf2_text1)
        key_path = Tools.get_path_from_entry(lf2_entry1)
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                key = f.read()
                if bytes("-----BEGIN RSA PRIVATE KEY-----\nEncrypted:".encode('utf-8')) in key:
                    lf2_text1.insert('end', key.decode('utf-8'))
                else:
                    lf2_text1.insert('end', '这不是已加密的私钥')
        else:
            lf2_text1.insert('end', '私钥地址错误')
        lf2_text1.config(state='disabled')

    def lf2_reset2():
        Tools.reset(lf2_entry2)
        Tools.reset(lf2_entry3)
        lf2_label5.config(text='   ')

    def lf2_confirm2():
        global ind
        ind = (ind + 1) % 6
        lf2_label5.config(fg=colors[ind])
        lf2_text1.config(state='normal')
        enc_key = lf2_text1.get(1.0, 'end').strip('\n')
        lf2_text1.config(state='disabled')
        if enc_key == '这不是已加密的私钥' or enc_key == '私钥地址错误' or not enc_key:
            lf2_label5.config(text='无法修改密码')
            return 0
        elif not lf2_entry2.get().strip('') or not lf2_entry3.get().strip(''):
            lf2_label5.config(text='密码不能为空')
            return 0
        else:
            dec_key = Tools.decrypt_privkey(enc_key.encode('utf-8'), lf2_entry2.get())
            if dec_key == b'':
                lf2_label5.config(text='旧密码错误')
                return 0
            enc_key = Tools.encrypt_privkey(dec_key, lf2_entry3.get())
            with open(Tools.get_path_from_entry(lf2_entry1), 'wb') as f:
                f.write(enc_key)
            lf2_label5.config(text='修改成功')
            lf2_text1.config(state='normal')
            Tools.reset(lf2_text1)
            lf2_text1.insert('end', enc_key.decode('utf-8'))
            lf2_text1.config(state='disabled')

    lf2_label1 = tk.Label(lf2_frm1, text='请拖入被加密的私钥或输入地址：', font=mid_font)
    lf2_label1.grid(row=1, column=1, padx=5)
    lf2_var1 = tk.StringVar()
    lf2_var1.set('0')
    lf2_cb1 = tk.Checkbutton(lf2_frm1, text='隐藏', font=mid_font, variable=lf2_var1, onvalue='1', offvalue='0',
                             command=change_lf2_entry1_show)
    lf2_cb1.grid(row=1, column=2, padx=5)
    lf2_entry1 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=lf2_drag)
    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()
    lf2_button3 = tk.Button(lf2_frm3, text='重置', font=mid_font, command=lf2_reset1)
    lf2_button3.grid(row=1, column=1, padx=20)
    lf2_button4 = tk.Button(lf2_frm3, text='确定', font=mid_font, command=lf2_confirm1)
    lf2_button4.grid(row=1, column=2, padx=20)
    lf2_label2 = tk.Label(labelframe2, text='该私钥的内容为：', font=mid_font)
    lf2_label2.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=13, font=mid_font, state='disabled')
    lf2_text1.pack()
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_label3 = tk.Label(lf2_frm2, text='请输入旧密码：', font=mid_font)
    lf2_label3.grid(row=1, column=1, padx=5)
    lf2_var2 = tk.StringVar()
    lf2_var2.set('1')
    lf2_cb2 = tk.Checkbutton(lf2_frm2, text='隐藏', font=mid_font, variable=lf2_var2, onvalue='1', offvalue='0',
                             command=change_lf2_entry2_show)
    lf2_cb2.grid(row=1, column=2, padx=5)
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font, show='*')
    lf2_entry2.pack()
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_frm4.pack()
    lf2_label4 = tk.Label(lf2_frm4, text='请输入新密码：', font=mid_font)
    lf2_label4.grid(row=1, column=1, padx=5)
    lf2_var3 = tk.StringVar()
    lf2_var3.set('1')
    lf2_cb3 = tk.Checkbutton(lf2_frm4, text='隐藏', font=mid_font, variable=lf2_var3, onvalue='1', offvalue='0',
                             command=change_lf2_entry3_show)
    lf2_cb3.grid(row=1, column=2, padx=5)
    lf2_entry3 = tk.Entry(labelframe2, width=43, font=mid_font, show='*')
    lf2_entry3.pack()
    lf2_frm5 = tk.Frame(labelframe2)
    lf2_frm5.pack()
    lf2_button5 = tk.Button(lf2_frm5, text='重置', font=mid_font, command=lf2_reset2)
    lf2_button5.grid(row=1, column=1, padx=20)
    lf2_button6 = tk.Button(lf2_frm5, text='确定', font=mid_font, command=lf2_confirm2)
    lf2_button6.grid(row=1, column=2, padx=20)
    lf2_label5 = tk.Label(labelframe2, text='   ', font=mid_font, fg=colors[ind])
    lf2_label5.pack()


def rsa_word():
    base64_or_emoji_frm = tk.Frame(frm)
    base64_or_emoji_frm.pack()
    label3 = tk.Label(base64_or_emoji_frm, text="请选择密文的编码方式：", font=mid_font)
    label3.grid(row=1, column=1, padx=10)
    base64_or_emoji = tk.StringVar()
    base64_or_emoji.set('base64')
    base64_rb = tk.Radiobutton(base64_or_emoji_frm, text='base64编码', variable=base64_or_emoji, value='base64', font=mid_font)
    base64_rb.grid(row=1, column=2, padx=10)
    emoji_rb = tk.Radiobutton(base64_or_emoji_frm, text='emoji编码', variable=base64_or_emoji, value='emoji', font=mid_font)
    emoji_rb.grid(row=1, column=3, padx=10)
    intro_emoji_button = tk.Button(base64_or_emoji_frm, text='说明', font=mid_font, command=Tools.intro_emoji, bd=0, fg='blue')
    intro_emoji_button.grid(row=1, column=4, padx=10)
    frm_of_labelframe = tk.Frame(frm)
    frm_of_labelframe.pack()

    # 加密（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm_of_labelframe, text='RSA加密文字', height=708, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    frm3 = tk.Frame(labelframe1)
    frm3.pack()

    def change_entry1_show():
        Tools.change_entry_show(var2, entry1)

    def drag(files):
        Tools.dragged_files(files, entry1)
        Tools.reset(text2)

    label1 = tk.Label(frm3, text='请拖入收信人公钥或输入地址：', font=mid_font)
    label1.grid(row=1, column=1, padx=5)
    var2 = tk.StringVar()
    var2.set('0')
    cb1 = tk.Checkbutton(frm3, text='隐藏', variable=var2, onvalue='1', offvalue='0', command=change_entry1_show, font=mid_font)
    cb1.grid(row=1, column=2, padx=5)
    entry1 = tk.Entry(labelframe1, font=mid_font, width=43)
    entry1.pack()
    hook_dropfiles(entry1, func=drag)
    label2 = tk.Label(labelframe1, text='请输入需要加密的文字：', font=mid_font)
    label2.pack()
    text1 = tk.Text(labelframe1, font=mid_font, width=43, height=9)
    text1.pack()

    def process(*args):
        '''
        :param entry1: 公钥所在的绝对路径
        :param text2: 需要加密的文字
        :param text3: 密文
        :return:
        '''
        if var3.get() == "0" and args:
            return 0
        Tools.reset(text2)
        window.update()
        # 先处理公钥
        if entry1.get().strip() == "":  # 如果用户没有输入密钥就不处理
            return 0
        pubkey_cipher = Tools.get_key(entry1, method='cipher')
        if pubkey_cipher == 0:
            return 0
        # 再对文字进行处理
        ontology_path = '_temp_ontology.txt'
        ontology_sec_path = '_temp_ontology_RSAencrypted.txt'
        with open(ontology_path, 'w', encoding='utf-8') as f:
            f.write(text1.get(1.0, 'end').rstrip('\n'))
        try:
            Tools.encrypt_bigfile(ontology_path, ontology_sec_path, pubkey_cipher)
        except Exception:
            tk.messagebox.showerror(title='加密出错', message='密钥可能有问题，请检查后重新选择')
        else:
            with open(ontology_sec_path, 'rb') as f:
                Tools.reset(text2)
                res = base64.b64encode(f.read()).decode('utf-8')
                if base64_or_emoji.get() == 'base64':
                    text2.insert('end', res)
                elif base64_or_emoji.get() == 'emoji':
                    text2.insert('end', Tools.translate_base64_to_emoji(res))
        os.remove(ontology_path)
        os.remove(ontology_sec_path)

    def reset():
        Tools.reset(text1)
        Tools.reset(text2)

    def copy_():
        Tools.copy(text2, button3)

    frm2 = tk.Frame(labelframe1)
    frm2.pack(pady=9)
    var3 = tk.StringVar()
    var3.set('0')
    cb2 = tk.Checkbutton(frm2, font=mid_font, text='实时计算', variable=var3, onvalue='1', offvalue='0')
    cb2.grid(row=1, column=1, padx=15)
    button1 = tk.Button(frm2, font=mid_font, text='重置', command=reset)
    button1.grid(row=1, column=2, padx=15)
    button2 = tk.Button(frm2, font=mid_font, text='加密', command=process)
    button2.grid(row=1, column=3, padx=15)
    button3 = tk.Button(frm2, font=mid_font, text='复制密文', command=copy_, fg=colors[ind])
    button3.grid(row=1, column=4, padx=15)
    label4 = tk.Label(labelframe1, text='密文：', font=mid_font)
    label4.pack()
    text2 = tk.Text(labelframe1, font=mid_font, width=43, height=9)
    text2.pack()
    text1.bind('<KeyRelease>', process)

    # 解密（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm_of_labelframe, text='RSA解密文字', height=708, width=606, font=mid_font)
    labelframe2.pack(side='left', padx=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()

    def drag2(files):
        Tools.dragged_files(files, lf2_entry1)
        Tools.reset(lf2_text2)

    def change_lf2_entry1_show():
        Tools.change_entry_show(lf2_hide, lf2_entry1)

    def change_pwd_entry_show():
        Tools.change_entry_show(pwd_var, pwd_entry)

    def decrypt(*args):
        if (live_cal.get() == '0' and args) or (not lf2_text1.get(1.0, 'end').replace('\n', '').replace(' ', '')):
            return 0  # 如果用户关闭了实时计算或是开启了实时计算，但是输入了一些没意义的符号，就不管
        Tools.reset(lf2_text2)
        window.update()
        # 先处理私钥
        if lf2_entry1.get().strip() == "":  # 如果用户没有输入密钥，就需要清理lf2_text，但不执行其他操作
            return 0
        privkey_cipher = Tools.get_key(lf2_entry1, method='decipher', pwd_entry=pwd_entry)
        if privkey_cipher == 0:
            return 0
        # 再对文字进行处理
        try:
            info = lf2_text1.get(1.0, 'end').strip('\n')
            if base64_or_emoji.get() == 'base64':
                ontology_sec = base64.b64decode(info)
            elif base64_or_emoji.get() == 'emoji':
                ontology_sec = base64.b64decode(Tools.translate_emoji_to_base64(info))
        except Exception:
            if base64_or_emoji.get() == 'base64':
                messagebox.showerror(title='密文格式错误', message="不是正确的base64编码，密文是否为emoji编码？")
            elif base64_or_emoji.get() == 'emoji':
                messagebox.showerror(title='密文格式错误', message="无法将输入的emoji字符转为base64编码")
            return 0
        # 如果文字正常，就进行解密
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
            Tools.reset(lf2_text2)
            try:
                ontology = ontology.decode('utf-8')
                assert len(ontology)
            except Exception:
                messagebox.showinfo(title='解密失败', message='密钥或密文可能不正确')
            else:
                lf2_text2.insert('end', str(ontology))
        os.remove(ontology_path)
        os.remove(ontology_sec_path)

    def reset2():
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)

    def copy2():
        Tools.copy(lf2_text2, lf2_button3)

    lf2_label1 = tk.Label(lf2_frm1, text='请拖入私钥或输入地址：', font=mid_font)
    lf2_label1.grid(row=1, column=1, padx=5)
    lf2_hide = tk.StringVar()
    lf2_hide.set('0')
    lf2_cb1 = tk.Checkbutton(lf2_frm1, text='隐藏', variable=lf2_hide, onvalue='1', offvalue='0', command=change_lf2_entry1_show, font=mid_font)
    lf2_cb1.grid(row=1, column=2, padx=5)
    lf2_entry1 = tk.Entry(labelframe2, font=mid_font, width=43)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=drag2)
    pwd_frm = tk.Frame(labelframe2)
    pwd_frm.pack()
    pwd_label = tk.Label(pwd_frm, text='请输入该私钥的使用密码：', font=mid_font)
    pwd_label.grid(row=1, column=1, padx=5)
    pwd_var = tk.StringVar()
    pwd_var.set('1')
    pwd_cb = tk.Checkbutton(pwd_frm, text='隐藏', font=mid_font, variable=pwd_var, onvalue='1', offvalue='0', command=change_pwd_entry_show)
    pwd_cb.grid(row=1, column=2, padx=5)
    pwd_entry = tk.Entry(labelframe2, width=43, font=mid_font, show='*')
    pwd_entry.pack()
    lf2_label2 = tk.Label(labelframe2, text='请输入需要解密的文字：', font=mid_font)
    lf2_label2.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=7, font=mid_font)
    lf2_text1.pack()
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    live_cal = tk.StringVar()
    live_cal.set('1')
    lf2_cb1 = tk.Checkbutton(lf2_frm2, font=mid_font, text='实时计算', variable=live_cal, onvalue='1', offvalue='0')
    lf2_cb1.grid(row=1, column=1, padx=15)
    lf2_button1 = tk.Button(lf2_frm2, font=mid_font, text='重置', command=reset2)
    lf2_button1.grid(row=1, column=2, padx=15)
    lf2_button2 = tk.Button(lf2_frm2, font=mid_font, text='解密', command=decrypt)
    lf2_button2.grid(row=1, column=3, padx=15)
    lf2_button3 = tk.Button(lf2_frm2, font=mid_font, text='复制明文', command=copy2, fg=colors[ind])
    lf2_button3.grid(row=1, column=4, padx=15)
    lf2_label3 = tk.Label(labelframe2, text='明文：', font=mid_font)
    lf2_label3.pack()
    lf2_text2 = tk.Text(labelframe2, font=mid_font, width=43, height=9)
    lf2_text2.pack()
    lf2_text1.bind('<KeyRelease>', decrypt)


def rsa_file():
    # 加密文件（夹）（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='RSA加密文件（夹）', height=741, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    frm3 = tk.Frame(labelframe1)
    frm3.pack()

    def change_entry1_show():
        Tools.change_entry_show(var2, entry1)

    def _enter_length(*args):
        Tools.enter_length(_size, _entry1, _label1, frm4, zebra_frm)

    def drag1(files):
        Tools.dragged_files(files, entry1)
        Tools.clean_all_widget(frm4)

    def drag2(files):
        Tools.dragged_files(files, entry2)
        Tools.clean_all_widget(frm4)

    label1 = tk.Label(frm3, text='请拖入收信人公钥或输入地址：', font=mid_font)
    label1.grid(row=1, column=1, padx=5)
    var2 = tk.StringVar()
    var2.set('0')
    cb1 = tk.Checkbutton(frm3, text='隐藏', variable=var2, onvalue='1', offvalue='0', command=change_entry1_show, font=mid_font)
    cb1.grid(row=1, column=2, padx=5)
    entry1 = tk.Entry(labelframe1, font=mid_font, width=43)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)
    label2 = tk.Label(labelframe1, text='请拖入需要加密的文件（夹）或输入地址：', font=mid_font)
    label2.pack()
    entry2 = tk.Entry(labelframe1, show=None, width=43, font=mid_font)
    entry2.pack()
    hook_dropfiles(entry2, func=drag2)
    delete_origin = tk.StringVar()
    delete_origin.set('0')
    delete_origin_cb = tk.Checkbutton(labelframe1, text='加密完后删除原文件', font=mid_font, variable=delete_origin, onvalue='1', offvalue='0')
    delete_origin_cb.pack()
    _frm5 = tk.Frame(labelframe1)
    _frm5.pack()
    frm5 = tk.Frame(_frm5)
    frm5.pack()
    label6 = tk.Label(frm5, text="请选择加密的大小：", font=mid_font)
    label6.grid(row=1, column=1)
    _size = tk.StringVar()
    _size.set("完整文件")
    option_menu1 = tk.OptionMenu(frm5, _size, *("完整文件", "1单位", "10单位", "516单位", "5160单位", "其他长度", "斑马线加密法"),
                                 command=_enter_length)
    option_menu1.config(font=mid_font)
    option_menu1.grid(row=1, column=2)
    _entry1 = tk.Entry(frm5, width=5, font=mid_font)
    _label1 = tk.Label(frm5, text='单位', font=mid_font)
    intro_button = tk.Button(frm5, text="说明", font=mid_font, command=Tools.intro_enc_head, bd=0, fg='blue')
    intro_button.grid(row=1, column=5)
    zebra_frm = tk.Frame(_frm5)
    zfrm1 = tk.Frame(zebra_frm)
    zfrm1.grid(row=1)
    zlabel1 = tk.Label(zfrm1, text='位置的显示方式：', font=mid_font)
    zlabel1.grid(row=1, column=1, padx=10)
    show_method = tk.StringVar()
    show_method.set('1')

    def change_show_method():
        Tools.reset(zentry1)
        Tools.reset(zentry4)
        if show_method.get() == '2':
            zlabel3.config(text=' kb ')
            zlabel7.config(text=' kb ')
            zscale1.grid_forget()
            zscale2.grid_forget()
        elif show_method.get() == '1':
            zlabel3.config(text=' %  ')
            zlabel7.config(text='%')
            begin.set(0)
            end.set(100)
            zentry1.insert('end', '0')
            zentry4.insert('end', '100')
            zscale1.grid(row=3)
            zscale2.grid(row=5)

    def change_zentry1(value):
        Tools.change_zentry(value, zentry1)

    def change_zentry4(value):
        Tools.change_zentry(value, zentry4)

    def change_zscale1(*args):
        Tools.change_zscale(show_method, zentry1, begin)

    def change_zscale2(*args):
        Tools.change_zscale(show_method, zentry4, end)

    zrb1 = tk.Radiobutton(zfrm1, text='百分比', font=mid_font, variable=show_method, value='1', command=change_show_method)
    zrb1.grid(row=1, column=2, padx=10)
    zrb2 = tk.Radiobutton(zfrm1, text='绝对值', font=mid_font, variable=show_method, value='2', command=change_show_method)
    zrb2.grid(row=1, column=3, padx=10)
    zfrm2 = tk.Frame(zebra_frm)
    zfrm2.grid(row=2)
    zlabel2 = tk.Label(zfrm2, text='第一根黑线的起始位置：  ', font=mid_font)
    zlabel2.grid(row=1, column=1)
    zentry1 = tk.Entry(zfrm2, width=5, font=mid_font)
    zentry1.grid(row=1, column=2)
    zentry1.insert('end', '0')
    zentry1.bind('<KeyRelease>', change_zscale1)
    zlabel3 = tk.Label(zfrm2, text=' %  ', font=mid_font)
    zlabel3.grid(row=1, column=3)
    begin = tk.IntVar()
    begin.set(0)
    zscale1 = tk.Scale(zebra_frm, from_=0, to=100, orient=tk.HORIZONTAL, length=400, tickinterval=10, resolution=1, showvalue=0, variable=begin, command=change_zentry1)
    zscale1.grid(row=3)
    zfrm4 = tk.Frame(zebra_frm)
    zfrm4.grid(row=4)
    zlabel4 = tk.Label(zfrm4, text='黑线的宽度：            ', font=mid_font)
    zlabel4.grid(row=1, column=1)
    zentry2 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry2.grid(row=1, column=2)
    zlabel8 = tk.Label(zfrm4, text='单位', font=mid_font)
    zlabel8.grid(row=1, column=3)
    zlabel5 = tk.Label(zfrm4, text='黑线的根数：            ', font=mid_font)
    zlabel5.grid(row=2, column=1)
    zentry3 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry3.grid(row=2, column=2)
    zlabel9 = tk.Label(zfrm4, text=' 根 ', font=mid_font)
    zlabel9.grid(row=2, column=3)
    zlabel6 = tk.Label(zfrm4, text='最后一根黑线的末尾位置：', font=mid_font)
    zlabel6.grid(row=3, column=1)
    zentry4 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry4.grid(row=3, column=2)
    zentry4.insert('end', '100')
    zentry4.bind('<KeyRelease>', change_zscale2)
    zlabel7 = tk.Label(zfrm4, text=' %  ', font=mid_font)
    zlabel7.grid(row=3, column=3)
    end = tk.IntVar()
    end.set(100)
    zscale2 = tk.Scale(zebra_frm, from_=0, to=100, orient=tk.HORIZONTAL, length=400, tickinterval=10, resolution=1, showvalue=0, variable=end, command=change_zentry4)
    zscale2.grid(row=5)

    def process():
        Tools.clean_all_widget(frm4)
        # 先处理公钥
        pubkey = Tools.get_key(entry1, method='cipher')
        if pubkey == 0:
            return 0
        # 再判断要加密的文件（夹）是否存在
        ontology_path = Tools.get_path_from_entry(entry2)
        if not os.path.exists(ontology_path):
            tk.messagebox.showerror(title='路径错误', message='待加密的文件地址不正确，请重新输入')
            return 0
        # 为了防止在运行过程中，用户改变_size的值，这里需要先固定这个值
        size = Tools.get_correct_size(_size, _entry1)
        if size == 0:
            return 0
        _begin, width, number, _end = Tools.get_correct_zebra_parameter(size, show_method, zentry1, zentry2, zentry3, zentry4)
        if _begin is False:
            return 0
        setting_of_delete_origin = delete_origin.get()
        # 再判断到底是文件还是文件夹
        if os.path.isfile(ontology_path):  # 如果是文件
            label3 = tk.Label(frm4, text='处理时间可能会较长，请耐心等待', font=mid_font)
            label3.pack()
            window.update()
            label3.destroy()
            # 再处理要加密的文件
            base, suffix = os.path.splitext(ontology_path)
            ontology_sec_path = base + '_RSA_Encrypted' + suffix
            try:
                Tools.encrypt_bigfile(ontology_path, ontology_sec_path, pubkey, size, _begin, width, number, _end)
            except Exception:
                os.remove(ontology_sec_path)
                tk.messagebox.showerror(title='加密出错', message='密钥可能有问题，请检查后重新选择')
                return 0
            else:
                if setting_of_delete_origin == '1':
                    Tools.delete_file(ontology_path)
                    label4 = tk.Label(frm4, text='加密成功并已删除原文件，\n文件保存至原文件所在文件夹中的', font=mid_font)
                else:
                    label4 = tk.Label(frm4, text='加密成功，文件保存至原文件所在文件夹中的', font=mid_font)
                label4.pack()
                entry3 = tk.Entry(frm4, width=43, font=mid_font)
                entry3.insert('end', os.path.basename(ontology_sec_path))
                entry3.pack()
        elif os.path.isdir(ontology_path):  # 如果是文件夹
            # 定义进度条
            progress_bar = ttk.Progressbar(frm4)
            progress_bar['length'] = 200
            progress_bar['value'] = 0
            files = os.listdir(ontology_path)
            out_dir = os.path.join(ontology_path, 'RSA_Encrypted')
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            cleaned_files = []  # 只将files里的纯文件的绝对路径保存到这里，其他的，比如文件夹会删掉
            for file in files:
                file_path = os.path.join(ontology_path, file)
                if os.path.isfile(file_path):
                    cleaned_files.append(file_path)
            progress_bar['maximum'] = len(cleaned_files)  # 这里定义进度条的总长度
            progress_bar.pack(pady=10)  # 再放置进度条
            window.update()  # 这里的窗口更新很重要，因为如果第一个文件处理完了再更新窗口，用户会觉得卡顿
            for file_path in cleaned_files:
                out_path = os.path.join(out_dir, os.path.basename(file_path))
                try:
                    Tools.encrypt_bigfile(file_path, out_path, pubkey, size, _begin, width, number, _end)
                except Exception:
                    shutil.rmtree(out_dir)
                    tk.messagebox.showerror(title='加密出错', message='密钥可能有问题，请检查后重新选择')
                    return 0
                else:
                    if setting_of_delete_origin == '1':
                        Tools.delete_file(file_path)
                    progress_bar['value'] += 1
                    window.update()
            if setting_of_delete_origin == '1':
                label3 = tk.Label(frm4, text='加密成功并已删除原文件，文件保存至\n原文件夹中新建的 RSA_Encrypted 文件夹中', font=mid_font)
            else:
                label3 = tk.Label(frm4, text='加密成功，文件保存至原文件夹中\n新建的 RSA_Encrypted 文件夹中', font=mid_font)
            label3.pack()
        else:
            tk.messagebox.showerror(title='路径错误', message='待加密的文件（夹）地址不正确，请重新输入')
            return 0

    def _reset():
        Tools.reset(entry2)
        Tools.clean_all_widget(frm4)

    frm2 = tk.Frame(labelframe1)
    frm2.pack()
    button1 = tk.Button(frm2, text='重置', font=mid_font, command=_reset)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm2, text='加密', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=20)
    frm4 = tk.Frame(labelframe1)
    frm4.pack()

    # 解密文件（夹）（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='RSA解密文件（夹）', height=741, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变

    def change_lf2_entry1_show():
        Tools.change_entry_show(lf2_var2, lf2_entry1)

    def change_pwd_entry_show():
        Tools.change_entry_show(pwd_var, pwd_entry)

    def drag3(files):
        Tools.dragged_files(files, lf2_entry1)
        Tools.clean_all_widget(lf2_frm4)

    def drag4(files):
        Tools.dragged_files(files, lf2_entry2)
        Tools.clean_all_widget(lf2_frm4)

    def decrypt(*args):
        Tools.clean_all_widget(lf2_frm4)
        # 先处理私钥
        privkey = Tools.get_key(lf2_entry1, method='decipher', pwd_entry=pwd_entry)
        if privkey == 0:
            return 0
        # 再判断要解密的文件（夹）是否存在
        ontology_sec_path = Tools.get_path_from_entry(lf2_entry2)
        if not os.path.exists(ontology_sec_path):
            tk.messagebox.showerror(title='路径错误', message='待解密的文件地址不正确，请重新输入')
            return 0
        setting_of_delete_sec = delete_sec.get()
        if os.path.isfile(ontology_sec_path):
            lf2_label3 = tk.Label(lf2_frm4, text='处理时间可能会较长，请耐心等待', font=mid_font)
            lf2_label3.pack()
            window.update()
            lf2_label3.destroy()
            # 再处理解密的文件
            base, suffix = os.path.splitext(ontology_sec_path)
            ontology_path = base + '_RSA_Decrypted' + suffix
            try:
                Tools.decrypt_bigfile(ontology_sec_path, ontology_path, privkey)
                assert os.path.getsize(ontology_path)  # 如果解密后的文件大小为0，说明解密失败
            except Exception:
                Tools.delete_file(ontology_path)
                tk.messagebox.showerror(title='解密出错', message='密钥或文件可能有问题，请检查后重新选择')
                return 0
            else:
                if setting_of_delete_sec == '1':
                    Tools.delete_file(ontology_sec_path)
                    lf2_label4 = tk.Label(lf2_frm4, text='解密成功并已删除密文文件，\n文件保存至原文件所在文件夹中的', font=mid_font)
                else:
                    lf2_label4 = tk.Label(lf2_frm4, text='解密成功，文件保存至原文件所在文件夹中的', font=mid_font)
                lf2_label4.pack()
                lf2_entry3 = tk.Entry(lf2_frm4, width=43, font=mid_font)
                lf2_entry3.insert('end', os.path.basename(ontology_path))
                lf2_entry3.pack()

                def _remove():
                    Tools.remove_file_or_dir(ontology_path, lf2_frm6)

                lf2_frm5 = tk.Frame(lf2_frm4)
                lf2_frm5.pack()
                destroy_button = tk.Button(lf2_frm5, text='阅后即焚', font=mid_font, command=_remove)
                destroy_button.grid(row=1, column=1, padx=10)
                intro_destroy_button = tk.Button(lf2_frm5, text='说明', font=mid_font, bd=0, fg='blue', command=Tools.intro_destroy)
                intro_destroy_button.grid(row=1, column=2, padx=10)
                lf2_frm6 = tk.Frame(lf2_frm4)
                lf2_frm6.pack()
        elif os.path.isdir(ontology_sec_path):
            # 定义进度条
            progress_bar = ttk.Progressbar(lf2_frm4)
            progress_bar['length'] = 200
            progress_bar['value'] = 0
            # 再处理要解密的文件夹
            files = os.listdir(ontology_sec_path)
            out_dir = os.path.join(ontology_sec_path, 'RSA_Decrypted')
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            cleaned_files = []  # 只将files里的纯文件的绝对路径保存到这里，其他的，比如文件夹会删掉
            for file in files:
                file_path = os.path.join(ontology_sec_path, file)
                if os.path.isfile(file_path):
                    cleaned_files.append(file_path)
            progress_bar['maximum'] = len(cleaned_files)  # 这里定义进度条的总长度
            progress_bar.pack(pady=10)  # 再放置进度条
            window.update()
            failed_files = []
            for file_path in cleaned_files:
                out_path = os.path.join(out_dir, os.path.basename(file_path))
                try:
                    Tools.decrypt_bigfile(file_path, out_path, privkey)
                    assert os.path.getsize(out_path)  # 如果解密后的文件大小为0，说明解密失败
                except Exception:
                    Tools.delete_file(out_path)
                    failed_files.append(os.path.basename(file_path))
                else:
                    if setting_of_delete_sec == '1':
                        Tools.delete_file(file_path)
                progress_bar['value'] += 1
                window.update()
            if setting_of_delete_sec == '1':
                lf2_label3 = tk.Label(lf2_frm4, text='解密成功并已删除密文文件，文件保存至\n原文件夹中新建的 RSA_Decrypted 文件夹中', font=mid_font)
            else:
                lf2_label3 = tk.Label(lf2_frm4, text='解密成功，文件保存至原文件夹中\n新建的 RSA_Decrypted 文件夹中', font=mid_font)
            lf2_label3.pack()
            if failed_files:
                lf2_text = tk.Text(lf2_frm4, width=43, font=mid_font, height=9)
                lf2_text.insert('end', f'其中，{len(failed_files)}个文件解密失败，分别为：\n' + '\n'.join(failed_files))
                lf2_text.pack()

            def _remove():
                Tools.remove_file_or_dir(out_dir, lf2_frm6)

            lf2_frm5 = tk.Frame(lf2_frm4)
            lf2_frm5.pack()
            destroy_button = tk.Button(lf2_frm5, text='阅后即焚', font=mid_font, command=_remove)
            destroy_button.grid(row=1, column=1, padx=10)
            intro_destroy_button = tk.Button(lf2_frm5, text='说明', font=mid_font, fg='blue', bd=0,
                                             command=Tools.intro_destroy)
            intro_destroy_button.grid(row=1, column=2, padx=10)
            lf2_frm6 = tk.Frame(lf2_frm4)
            lf2_frm6.pack()
        else:
            tk.messagebox.showerror(title='路径错误', message='待解密的文件（夹）地址不正确，请重新输入')
            return 0

    def reset2():
        Tools.reset(lf2_entry2)
        Tools.clean_all_widget(lf2_frm4)

    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()
    lf2_label1 = tk.Label(lf2_frm3, text='请拖入私钥或输入地址：', font=mid_font)
    lf2_label1.grid(row=1, column=1, padx=5)
    lf2_var2 = tk.StringVar()
    lf2_var2.set('0')
    lf2_cb1 = tk.Checkbutton(lf2_frm3, text='隐藏', variable=lf2_var2, onvalue='1', offvalue='0', command=change_lf2_entry1_show, font=mid_font)
    lf2_cb1.grid(row=1, column=2, padx=5)
    lf2_entry1 = tk.Entry(labelframe2, font=mid_font, width=43)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, drag3)
    pwd_frm = tk.Frame(labelframe2)
    pwd_frm.pack()
    pwd_label = tk.Label(pwd_frm, text='请输入该私钥的使用密码：', font=mid_font)
    pwd_label.grid(row=1, column=1, padx=5)
    pwd_var = tk.StringVar()
    pwd_var.set('1')
    pwd_cb = tk.Checkbutton(pwd_frm, text='隐藏', font=mid_font, variable=pwd_var, onvalue='1', offvalue='0', command=change_pwd_entry_show)
    pwd_cb.grid(row=1, column=2, padx=5)
    pwd_entry = tk.Entry(labelframe2, width=43, font=mid_font, show='*')
    pwd_entry.pack()
    lf2_label2 = tk.Label(labelframe2, font=mid_font, text='请拖入需要解密的文件（夹）或输入地址：')
    lf2_label2.pack()
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry2.pack()
    hook_dropfiles(lf2_entry2, func=drag4)
    delete_sec = tk.StringVar()
    delete_sec.set('0')
    delete_sec_cb = tk.Checkbutton(labelframe2, text='解密完后删除密文文件', font=mid_font, variable=delete_sec, onvalue='1', offvalue='0')
    delete_sec_cb.pack()
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_button1 = tk.Button(lf2_frm2, text='重置', font=mid_font, command=reset2)
    lf2_button1.pack(side='left', padx=20)
    lf2_button2 = tk.Button(lf2_frm2, text='解密', font=mid_font, command=decrypt)
    lf2_button2.pack(side='right', padx=20)
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_frm4.pack()


def rsa_sign_and_verify():
    # 数字签名（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='RSA数字签名', height=741, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    frm1 = tk.Frame(labelframe1)
    frm1.pack()

    def change_entry1_show():
        Tools.change_entry_show(var1, entry1)

    def drag1(files):
        Tools.clean_all_widget(frm4)
        Tools.reset(text2)
        Tools.dragged_files(files, entry1)

    label1 = tk.Label(frm1, text='请拖入私钥或输入地址：', font=mid_font)
    label1.grid(row=1, column=1, padx=5)
    var1 = tk.StringVar()
    var1.set('0')
    cb1 = tk.Checkbutton(frm1, text='隐藏', variable=var1, onvalue='1', offvalue='0', command=change_entry1_show,
                         font=mid_font)
    cb1.grid(row=1, column=2, padx=5)
    entry1 = tk.Entry(labelframe1, font=mid_font, width=43)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)

    def change_target():
        Tools.clean_all_widget(frm4)
        frm3.pack_forget()
        Tools.reset(text2)
        if target.get() == 'file':
            label2.config(text='请拖入需要签名的文件或输入地址：')
            text1.pack_forget()
            entry2.pack()
            frm4.pack()
        elif target.get() == 'word':
            label2.config(text='请输入需要签名的文字：')
            entry2.pack_forget()
            text1.pack()
            frm4.pack_forget()
        frm3.pack()

    def drag2(files):
        Tools.clean_all_widget(frm4)
        Tools.reset(text2)
        Tools.dragged_files(files, entry2)

    def change_pwd_entry_show():
        Tools.change_entry_show(pwd_var, pwd_entry)

    pwd_frm = tk.Frame(labelframe1)
    pwd_frm.pack()
    pwd_label = tk.Label(pwd_frm, text='请输入该私钥的使用密码：', font=mid_font)
    pwd_label.grid(row=1, column=1, padx=5)
    pwd_var = tk.StringVar()
    pwd_var.set('1')
    pwd_cb = tk.Checkbutton(pwd_frm, text='隐藏', font=mid_font, variable=pwd_var, onvalue='1', offvalue='0',
                            command=change_pwd_entry_show)
    pwd_cb.grid(row=1, column=2, padx=5)
    pwd_entry = tk.Entry(labelframe1, width=43, font=mid_font, show='*')
    pwd_entry.pack()
    target_frm = tk.Frame(labelframe1)
    target_frm.pack()
    target = tk.StringVar()
    target.set('word')
    rb1 = tk.Radiobutton(target_frm, text='签名文字', font=mid_font, variable=target, value='word', command=change_target)
    rb1.grid(row=1, column=1, padx=15)
    rb2 = tk.Radiobutton(target_frm, text='签名文件', font=mid_font, variable=target, value='file', command=change_target)
    rb2.grid(row=1, column=2, padx=15)
    label2 = tk.Label(labelframe1, text='请输入需要签名的文字：', font=mid_font)
    label2.pack()
    text1 = tk.Text(labelframe1, width=43, height=9, font=mid_font)
    text1.pack()
    entry2 = tk.Entry(labelframe1, width=43, font=mid_font)
    hook_dropfiles(entry2, func=drag2)

    def process():
        global ind
        Tools.clean_all_widget(frm4)
        Tools.reset(text2)
        # 先处理私钥
        privkey_signer = Tools.get_key(entry1, method='signer', pwd_entry=pwd_entry)
        if privkey_signer == 0:
            return 0
        ind = (ind + 1) % 6
        if target.get() == 'word':
            hasher = SHA384.new()
            hasher.update(text1.get(1.0, 'end').rstrip("\n").encode('utf-8'))
            try:
                signature = base64.b64encode(privkey_signer.sign(hasher))
            except Exception:
                Tools.reset(text2)
                text2.insert('end', '签名出错，密钥可能有问题')
                return 0
        elif target.get() == 'file':
            ontology_path = Tools.get_path_from_entry(entry2)
            if os.path.exists(ontology_path) and os.path.isfile(ontology_path):
                ontology_sec_path = ontology_path + '.sign'
                process_succeed = True
                # 先获取infile的hasher
                hasher = Tools.get_hasher_of_file(ontology_path)
                try:
                    signature = base64.b64encode(privkey_signer.sign(hasher))
                except Exception:
                    text2.insert('end', '签名出错，请检查密钥与文件')
                    process_succeed = False
                else:
                    with open(ontology_sec_path, 'wb') as outfile:
                        outfile.write(signature)
                    label4 = tk.Label(frm4, text='签名成功，其中信息摘要采用SHA-384算法', font=mid_font, fg=colors[ind])
                    label4.pack()
                    label5 = tk.Label(frm4, text='数字签名文件保存至原文件所在文件夹中的', font=mid_font, fg=colors[ind])
                    label5.pack()
                    entry3 = tk.Entry(frm4, width=43, font=mid_font, fg=colors[ind])
                    entry3.insert('end', os.path.basename(ontology_sec_path))
                    entry3.pack()
                if not process_succeed:
                    os.remove(ontology_sec_path)
            else:
                text2.insert('end', '待签名的文件地址不正确，请重新输入')
                return 0
        text2.insert('end', signature)

    def _reset():
        Tools.clean_all_widget(frm4)
        Tools.reset(text1)
        Tools.reset(text2)

    def _copy():
        Tools.copy(text2, button3)

    frm3 = tk.Frame(labelframe1)
    frm3.pack(pady=5)
    frm2 = tk.Frame(frm3)
    frm2.pack()
    button1 = tk.Button(frm2, text='重置', font=mid_font, command=_reset)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm2, text='签名', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=20)
    button3 = tk.Button(frm2, font=mid_font, text='复制签名', command=_copy, fg=colors[ind])
    button3.grid(row=1, column=3, padx=20)
    label3 = tk.Label(frm3, text='签名结果为：', font=mid_font)
    label3.pack()
    text2 = tk.Text(frm3, width=43, height=7, font=mid_font)
    text2.pack()
    frm4 = tk.Frame(frm3)

    # 验证签名（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='RSA验证签名', height=741, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()

    def change_lf2_entry1_show():
        Tools.change_entry_show(lf2_var1, lf2_entry1)

    def drag2(files):
        Tools.clean_all_widget(lf2_frm4)
        Tools.dragged_files(files, lf2_entry1)

    lf2_label1 = tk.Label(lf2_frm1, text='请拖入签名发送方的公钥或输入地址：', font=mid_font)
    lf2_label1.grid(row=1, column=1, padx=5)
    lf2_var1 = tk.StringVar()
    lf2_var1.set('0')
    lf2_cb1 = tk.Checkbutton(lf2_frm1, text='隐藏', variable=lf2_var1, onvalue='1', offvalue='0', command=change_lf2_entry1_show, font=mid_font)
    lf2_cb1.grid(row=1, column=2, padx=5)
    lf2_entry1 = tk.Entry(labelframe2, font=mid_font, width=43)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=drag2)

    def change_check():
        Tools.clean_all_widget(lf2_frm4)
        lf2_frm7.pack_forget()
        if check_mode.get() == 'file':
            lf2_text2.pack_forget()
            lf2_entry3.pack()
        elif check_mode.get() == 'word':
            lf2_entry3.pack_forget()
            lf2_text2.pack()
        lf2_frm7.pack()

    def change_target2():
        Tools.clean_all_widget(lf2_frm4)
        check_mode.set('word')
        change_check()
        lf2_frm5.pack_forget()
        lf2_frm6.pack_forget()
        if target2.get() == 'file':
            lf2_label2.config(text='请拖入需要验签的文件或输入地址：')
            lf2_text1.pack_forget()
            lf2_entry2.pack()
            lf2_label3.grid_forget()
            lf2_rb3.grid(row=1, column=1, padx=15)
            lf2_rb4.grid(row=1, column=2, padx=15)
        elif target2.get() == 'word':
            lf2_label2.config(text='请输入需要验签的文字：')
            lf2_text1.pack()
            lf2_entry2.pack_forget()
            lf2_label3.grid(row=1, column=1)
            lf2_rb3.grid_forget()
            lf2_rb4.grid_forget()
        lf2_frm5.pack()
        lf2_frm6.pack()

    def drag3(files):
        Tools.clean_all_widget(lf2_frm4)
        Tools.dragged_files(files, lf2_entry2)

    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()
    target2 = tk.StringVar()
    target2.set('word')
    lf2_rb1 = tk.Radiobutton(lf2_frm3, text='验证文字', font=mid_font, variable=target2, value='word', command=change_target2)
    lf2_rb1.grid(row=1, column=1, padx=15)
    lf2_rb2 = tk.Radiobutton(lf2_frm3, text='验证文件', font=mid_font, variable=target2, value='file', command=change_target2)
    lf2_rb2.grid(row=1, column=2, padx=15)
    lf2_label2 = tk.Label(labelframe2, text='请输入需要验签的文字：', font=mid_font)
    lf2_label2.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=9, font=mid_font)
    lf2_text1.pack()
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font)
    hook_dropfiles(lf2_entry2, func=drag3)
    lf2_frm5 = tk.Frame(labelframe2)
    lf2_frm5.pack()
    check_mode = tk.StringVar()
    check_mode.set('word')
    lf2_label3 = tk.Label(lf2_frm5, text='请输入数字签名：', font=mid_font)
    lf2_label3.grid(row=1, column=1)
    lf2_rb3 = tk.Radiobutton(lf2_frm5, text='输入数字签名', font=mid_font, variable=check_mode, value='word', command=change_check)
    lf2_rb4 = tk.Radiobutton(lf2_frm5, text='拖入签名文件', font=mid_font, variable=check_mode, value='file', command=change_check)

    def verify():
        global ind
        Tools.clean_all_widget(lf2_frm4)
        # 先处理公钥
        pubkey_verifier = Tools.get_key(lf2_entry1, method='verifier')
        if pubkey_verifier == 0:
            return 0
        ind = (ind + 1) % 6
        if target2.get() == 'word':
            hasher = SHA384.new()
            hasher.update(lf2_text1.get(1.0, 'end').rstrip("\n").encode('utf-8'))
            try:
                signature = base64.b64decode(lf2_text2.get(1.0, 'end').rstrip("\n"))
            except Exception:
                lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名编码有误', fg=colors[ind])
                lf2_label4.pack()
            else:
                if pubkey_verifier.verify(hasher, signature):
                    lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名验证通过', fg=colors[ind])
                    lf2_label4.pack()
                    lf2_label5 = tk.Label(lf2_frm4, font=mid_font, text='原信息的SHA-384数字摘要与数字签名内容一致', fg=colors[ind])
                    lf2_label5.pack()
                else:
                    lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名验证未能通过', fg=colors[ind])
                    lf2_label4.pack()
                    lf2_label5 = tk.Label(lf2_frm4, font=mid_font, text='原信息的SHA-384数字摘要与数字签名内容不一致', fg=colors[ind])
                    lf2_label5.pack()
        elif target2.get() == 'file':
            if check_mode.get() == 'file':
                signature_path = Tools.get_path_from_entry(lf2_entry3)
                try:
                    with open(signature_path, 'rb') as signature_file:
                        signature = base64.b64decode(signature_file.read())
                except Exception:
                    lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名文件路径错误', fg=colors[ind])
                    lf2_label4.pack()
                    return 0
            elif check_mode.get() == 'word':
                try:
                    signature = base64.b64decode(lf2_text2.get(1.0, 'end').rstrip("\n"))
                except Exception:
                    lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名编码有误', fg=colors[ind])
                    lf2_label4.pack()
                    return 0
            # 然后处理原始文件的地址
            message_path = Tools.get_path_from_entry(lf2_entry2)
            if (not os.path.exists(message_path)) or (not os.path.isfile(message_path)):
                lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='需要验签的文件路径错误', fg=colors[ind])
                lf2_label4.pack()
                return 0
            # 最后检查原始文件的摘要和数字签名是否一致
            hasher = Tools.get_hasher_of_file(message_path)
            if pubkey_verifier.verify(hasher, signature):
                lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名验证通过', fg=colors[ind])
                lf2_label4.pack()
                lf2_entry4 = tk.Entry(lf2_frm4, font=mid_font, width=43, fg=colors[ind])
                lf2_entry4.insert('end', os.path.basename(message_path))
                lf2_entry4.pack()
                lf2_label5 = tk.Label(lf2_frm4, font=mid_font, text='的SHA-384数字摘要与数字签名内容一致', fg=colors[ind])
                lf2_label5.pack()
            else:
                lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名验证未能通过', fg=colors[ind])
                lf2_label4.pack()
                lf2_entry4 = tk.Entry(lf2_frm4, font=mid_font, width=43, fg=colors[ind])
                lf2_entry4.insert('end', os.path.basename(message_path))
                lf2_entry4.pack()
                lf2_label5 = tk.Label(lf2_frm4, font=mid_font, text='的SHA-384数字摘要与数字签名内容不一致', fg=colors[ind])
                lf2_label5.pack()

    def reset2():
        Tools.clean_all_widget(lf2_frm4)
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)
        Tools.reset(lf2_entry2)
        Tools.reset(lf2_entry3)

    def drag4(files):
        Tools.clean_all_widget(lf2_frm4)
        Tools.dragged_files(files, lf2_entry3)

    lf2_frm6 = tk.Frame(labelframe2)
    lf2_frm6.pack()
    lf2_text2 = tk.Text(lf2_frm6, width=43, height=7, font=mid_font)
    lf2_text2.pack()
    lf2_entry3 = tk.Entry(lf2_frm6, width=43, font=mid_font)
    hook_dropfiles(lf2_entry3, func=drag4)
    lf2_frm7 = tk.Frame(lf2_frm6)
    lf2_frm7.pack()
    lf2_frm2 = tk.Frame(lf2_frm7)
    lf2_frm2.pack()
    lf2_button1 = tk.Button(lf2_frm2, text='重置', font=mid_font, command=reset2)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm2, text='验签', font=mid_font, command=verify)
    lf2_button2.grid(row=1, column=2, padx=20)
    lf2_frm4 = tk.Frame(lf2_frm7)
    lf2_frm4.pack()


def create_ecc_key():
    frm_of_labelframe = tk.Frame(frm)
    frm_of_labelframe.pack()

    # 连续随机生成
    labelframe1 = tk.LabelFrame(frm_of_labelframe, text='连续随机生成ECC密钥对', height=457, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    frm1 = tk.Frame(labelframe1)
    frm1.pack()
    number_of_frm1 = 1
    label1 = tk.Label(frm1, text=f'请选择第 {number_of_frm1} 对密钥的长度：', font=mid_font)
    label1.pack()
    frm2 = tk.Frame(labelframe1)
    frm2.pack()
    var1 = tk.StringVar()
    var1.set('SECP256K1')
    rb1 = tk.Radiobutton(frm2, variable=var1, text='SECP256K1（兼顾安全性、速度和兼容性）', font=mid_font, value='SECP256K1')
    rb1.grid(row=1, column=1, padx=10)
    frm3 = tk.Frame(labelframe1)
    frm3.pack()
    label2 = tk.Label(frm3, text=f'第 {number_of_frm1} 对密钥将保存在', font=mid_font)
    label2.grid(row=1, column=1)
    entry1 = tk.Entry(frm3, show=None, width=4, font=mid_font)
    entry1.grid(row=1, column=2)
    entry1.insert('end', '1')
    label3 = tk.Label(frm3, text=f'号文件夹内', font=mid_font)
    label3.grid(row=1, column=3)
    frm4 = tk.Frame(labelframe1)
    frm4.pack()
    top_lay = []

    def start(*args):
        nonlocal number_of_frm1  # f'请选择第 {number_of_frm1} 对密钥的长度：'

        # 获取用户输入的保存目录
        try:
            number_of_entry1 = int(entry1.get())
            if number_of_entry1 < 0:
                messagebox.showerror(title='输入错误', message='请在输入框内输入非负整数')
                return 0
        except ValueError:
            messagebox.showerror(title='输入错误', message='请在输入框内输入非负整数')
            return 0

        frm6.pack_forget()
        for i in top_lay:
            i.destroy()

        flag = True  # 用于表示现在在正在进行生成还是停止生成
        new_created_key = 0  # 新产生了多少密钥对

        def stop():
            nonlocal flag, entry1, new_created_key
            flag = False
            Tools.clean_all_widget(frm3)
            label6 = tk.Label(frm3, text=f'第 {number_of_frm1} 对密钥将保存在', font=mid_font)
            label6.grid(row=1, column=1)
            entry1 = tk.Entry(frm3, width=4, font=mid_font)
            entry1.grid(row=1, column=2)
            entry1.insert('end', number_of_entry1)
            label11 = tk.Label(frm3, text=f'号文件夹内', font=mid_font)
            label11.grid(row=1, column=3)
            Tools.clean_all_widget(frm4)
            label10 = tk.Label(frm4, text='请等待当前密钥生成完成', font=mid_font)
            label10.pack()
            frm6.pack(side='bottom', pady=40)
            new_created_key = 0

        Tools.clean_all_widget(frm4)
        button3 = tk.Button(frm4, text='暂停生成', font=mid_font, command=stop)
        button3.pack(side='right', padx=80)
        label_invisible = tk.Label(frm4, text='', font=mid_font)
        label_invisible.pack(side='left', padx=80)  # 这个label不显示信息，只是排版需要

        previous_key_length = None
        while flag:
            current_key_length = var1.get()
            Tools.clean_all_widget(frm1)
            number_of_frm1 += 1
            label4 = tk.Label(frm1, text=f'请选择第 {number_of_frm1} 对密钥的长度', font=mid_font)
            label4.pack()
            Tools.clean_all_widget(frm3)
            number_of_entry1 += 1
            label5 = tk.Label(frm3, text=f'第 {number_of_frm1} 对密钥将保存在 {number_of_entry1} 号文件夹内', font=mid_font)
            label5.pack()
            Tools.clean_all_widget(frm5)
            label7 = tk.Label(frm5, text=f'正在生成第 {number_of_frm1 - 1} 对{current_key_length}位密钥，请稍候...', font=mid_font)
            label7.pack()
            if new_created_key >= 1:
                label8 = tk.Label(frm5, text=f'第 {number_of_frm1 - 2} 对{previous_key_length}位密钥生成完成', font=mid_font)
                label8.pack()
            window.update()
            # 生成密钥对
            if var1.get() == 'SECP256K1':
                private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
                public_key = private_key.public_key()
            # 保存公私钥
            current_path = os.getcwd()
            keys_dir_path = current_path + '\\keys'
            if not os.path.exists(keys_dir_path):
                os.mkdir(keys_dir_path)
            key_path = keys_dir_path + f'\\{number_of_entry1 - 1}'
            if not os.path.exists(key_path):
                os.mkdir(key_path)
            else:
                shutil.rmtree(key_path)
                os.mkdir(key_path)
            with open(key_path + f'\\ECC_private_key_{current_key_length}.pem', 'wb') as prifile:
                prifile.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat("TraditionalOpenSSL"), encryption_algorithm=serialization.BestAvailableEncryption(b'1234')))
            with open(key_path + f'\\ECC_public_key_{current_key_length}.pem', 'wb') as pubfile:
                pubfile.write(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat("X.509 subjectPublicKeyInfo with PKCS#1")))
            time.sleep(0.1)
            new_created_key += 1
            previous_key_length = current_key_length

        Tools.clean_all_widget(frm4)
        button1 = tk.Button(frm4, text='开始生成', font=mid_font, command=start)
        button1.pack(side='left', padx=50)
        Tools.clean_all_widget(frm5)
        label9 = tk.Label(frm5, text=f'已生成{number_of_frm1 - 1}对密钥', font=mid_font)
        label9.pack()

    button1 = tk.Button(frm4, text='开始生成', font=mid_font, command=start)
    button1.pack()
    entry1.bind('<Return>', start)
    frm5 = tk.Frame(labelframe1)
    frm5.pack()

    def tell_detail():
        detail_window = tk.Toplevel(window)
        detail_window.geometry('1290x900')
        detail_window.title('ECC密钥详情')
        detail_window.iconbitmap(icon_path)
        top_lay.append(detail_window)

        def get_key_content(path: str):
            path = path.strip().strip('\"').lstrip("“").rstrip("”")
            if os.path.exists(path) and path.endswith('.pem'):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content
            else:
                return '读取失败'

        def read_default():

            def get_key_pairs_name_and_path_in_keys_dir():
                # 找到keys文件夹内所有的数字型名称的文件夹的名字和地址
                _key_pair_name_list = []
                _key_path_dic = {}  # 通过字典保存文件夹的地址
                current_path = os.getcwd()
                keys_dir_path = current_path + '\\keys'
                if not os.path.exists(keys_dir_path):
                    os.mkdir(keys_dir_path)
                for i in os.listdir(keys_dir_path):
                    key_pair_path = keys_dir_path + f'\\{i}'
                    try:
                        if os.path.isdir(key_pair_path) and int(i) >= 0:
                            _key_pair_name_list.append(int(i))
                            _key_path_dic[i] = key_pair_path
                    except Exception:
                        pass  # 如果报错就不执行
                _key_pair_name_list = sorted(_key_pair_name_list)
                return [str(j) for j in _key_pair_name_list], _key_path_dic
            Tools.clean_all_widget(_frm)
            _frm2 = tk.Frame(_frm)
            _frm2.pack()
            label1 = tk.Label(_frm2, text='打开', font=mid_font)
            label1.grid(row=1, column=1)
            key_pair_name_list, key_path_dic = get_key_pairs_name_and_path_in_keys_dir()
            entry1 = tk.Entry(_frm2, width=4, font=mid_font, show=None)
            entry1.grid(row=1, column=2)
            key_name = None
            if len(key_pair_name_list) >= 1:
                key_name = key_pair_name_list[-1]
                entry1.insert('end', key_name)
            label2 = tk.Label(_frm2, text='号文件夹', font=mid_font)
            label2.grid(row=1, column=3)

            def show_key_content(*args):
                nonlocal key_pair_name_list, key_path_dic, label_list, key_name
                key_pair_name_list, key_path_dic = get_key_pairs_name_and_path_in_keys_dir()
                _key_name = entry1.get()
                try:
                    if int(_key_name) < 0:
                        messagebox.showerror(title='输入错误', message='请输入非负整数')
                        return 0
                except ValueError:
                    messagebox.showerror(title='输入错误', message='请输入非负整数')
                    return 0
                if _key_name in key_pair_name_list:
                    key_path = key_path_dic[_key_name]
                else:
                    messagebox.showerror(title='输入错误', message='输入的文件夹的名称不存在')
                    return 0
                key_name = _key_name
                two_keys = os.listdir(key_path)
                find_pub_key, find_priv_key = False, False
                for i in two_keys:
                    if re.findall('ECC_public_key_.*\.pem', i):
                        pubkey_path = key_path + "\\" + i
                        find_pub_key = True
                    elif re.findall('ECC_private_key_.*\.pem', i):
                        privkey_path = key_path + "\\" + i
                        find_priv_key = True
                text1.delete('1.0', 'end')
                text2.delete('1.0', 'end')
                if find_pub_key:
                    pubkey_content = get_key_content(pubkey_path)
                    if 'BEGIN PUBLIC KEY' in pubkey_content or '读取失败' in pubkey_content:
                        text1.insert('end', pubkey_content)
                    else:
                        text1.insert('end', '这不是ECC公钥')
                else:
                    text1.insert('end', '未找到ECC公钥')
                if find_priv_key:
                    privkey_content = get_key_content(privkey_path)
                    if 'BEGIN EC PRIVATE KEY' in privkey_content or '读取失败' in privkey_content:
                        text2.insert('end', privkey_content)
                    else:
                        text2.insert('end', '这不是ECC私钥')
                else:
                    text2.insert('end', '未找到ECC私钥')
                label_list[0].configure(text=f'第 {key_name} 号公钥：')
                label_list[1].configure(text=f'第 {key_name} 号私钥：')

            button1 = tk.Button(_frm2, text='确认', font=mid_font, command=show_key_content)
            button1.grid(row=1, column=4, padx=30)
            entry1.bind('<Return>', show_key_content)
            _frm5 = tk.Frame(_frm)
            _frm5.pack()
            _frm6 = tk.Frame(_frm5)
            _frm6.pack(side='left', padx=5)
            _frm7 = tk.Frame(_frm5)
            _frm7.pack(side='right', padx=5)
            label_list = []
            label4 = tk.Label(_frm6, text='公钥：', font=mid_font)
            label4.pack()
            label_list.append(label4)
            text1 = tk.Text(_frm6, width=47, height=27, font=mid_font)
            text1.pack()
            label5 = tk.Label(_frm7, text='私钥：', font=mid_font)
            label5.pack()
            label_list.append(label5)
            text2 = tk.Text(_frm7, width=47, height=27, font=mid_font)
            text2.pack()
            _frm8 = tk.Frame(_frm)
            _frm8.pack(pady=10)
            if entry1.get():
                show_key_content()

            def previous_pair():
                nonlocal key_name, entry1
                key_pair_name_list, key_path_dic = get_key_pairs_name_and_path_in_keys_dir()
                if len(key_pair_name_list) >= 1:
                    if key_name is None:
                        entry1.delete(0, 'end')
                        entry1.insert('end', key_pair_name_list[0])
                        show_key_content()
                    else:
                        previous_key_name = None
                        for i in key_pair_name_list:
                            if int(i) >= int(key_name):
                                break
                            else:
                                previous_key_name = i
                        if previous_key_name is not None:
                            entry1.delete(0, 'end')
                            entry1.insert('end', previous_key_name)
                            show_key_content()

            def next_pair():
                nonlocal key_name, entry1
                key_pair_name_list, key_path_dic = get_key_pairs_name_and_path_in_keys_dir()
                if len(key_pair_name_list) >= 1:
                    if key_name is None:
                        entry1.delete(0, 'end')
                        entry1.insert('end', key_pair_name_list[-1])
                        show_key_content()
                    else:
                        for i in key_pair_name_list:
                            if int(i) > int(key_name):
                                entry1.delete(0, 'end')
                                entry1.insert('end', i)
                                show_key_content()
                                break
                        else:
                            pass  # 如果没有比key_name大的，就不要执行

            button2 = tk.Button(_frm8, text='上一对', font=mid_font, command=previous_pair)
            button2.grid(row=1, column=1, padx=15)
            button3 = tk.Button(_frm8, text='下一对', font=mid_font, command=next_pair)
            button3.grid(row=1, column=2, padx=15)

        def read_input():
            Tools.clean_all_widget(_frm)

            def show_key_content():
                pubkey_path = Tools.get_path_from_entry(entry1)
                if pubkey_path:
                    text1.delete(1.0, 'end')
                    pubkey_content = get_key_content(pubkey_path)
                    if 'BEGIN PUBLIC KEY' in pubkey_content or '读取失败' in pubkey_content:
                        text1.insert('end', pubkey_content)
                    else:
                        text1.insert('end', '这不是ECC公钥')

                privkey_path = Tools.get_path_from_entry(entry2)
                if privkey_path:
                    text2.delete(1.0, 'end')
                    privkey_content = get_key_content(privkey_path)
                    if 'BEGIN EC PRIVATE KEY' in privkey_content or '读取失败' in privkey_content:
                        text2.insert('end', privkey_content)
                    else:
                        text2.insert('end', '这不是ECC私钥')

            def drag1(files):
                Tools.dragged_files(files, entry1)
                show_key_content()

            def drag2(files):
                Tools.dragged_files(files, entry2)
                show_key_content()

            _frm2 = tk.Frame(_frm)
            _frm2.pack()
            _frm3 = tk.Frame(_frm2)
            _frm3.grid(row=1, column=1, padx=12)
            label4 = tk.Label(_frm3, text='拖入公钥或输入地址：', font=mid_font)
            label4.pack()
            entry1 = tk.Entry(_frm3, width=42, font=mid_font, show=None)
            entry1.pack()
            hook_dropfiles(entry1, func=drag1)
            button3 = tk.Button(_frm2, text='确认', font=mid_font, command=show_key_content)
            button3.grid(row=1, column=2, padx=12)
            _frm4 = tk.Frame(_frm2)
            _frm4.grid(row=1, column=3, padx=12)
            label5 = tk.Label(_frm4, text='拖入私钥或输入地址：', font=mid_font)
            label5.pack()
            entry2 = tk.Entry(_frm4, width=42, font=mid_font, show=None)
            entry2.pack()
            hook_dropfiles(entry2, func=drag2)
            _frm5 = tk.Frame(_frm)
            _frm5.pack()
            _frm6 = tk.Frame(_frm5)
            _frm6.pack(side='left', padx=5)
            label6 = tk.Label(_frm6, text='公钥：', font=mid_font)
            label6.pack()
            text1 = tk.Text(_frm6, width=47, height=29, font=mid_font)
            text1.pack()
            _frm7 = tk.Frame(_frm5)
            _frm7.pack(side='right', padx=5)
            label7 = tk.Label(_frm7, text='私钥：', font=mid_font)
            label7.pack()
            text2 = tk.Text(_frm7, width=47, height=29, font=mid_font)
            text2.pack()

        _frm1 = tk.Frame(detail_window)
        _frm1.pack()
        _frm = tk.Frame(detail_window)
        _frm.pack()
        inner_var1 = tk.StringVar()
        inner_var1.set('1')
        _rb1 = tk.Radiobutton(_frm1, font=mid_font, text='读取ECC密钥对的默认地址', variable=inner_var1, value='1', command=read_default)
        _rb1.grid(row=1, column=1, padx=20)
        _rb2 = tk.Radiobutton(_frm1, font=mid_font, text='输入ECC密钥对的地址', variable=inner_var1, value='2', command=read_input)
        _rb2.grid(row=1, column=2, padx=20)
        read_default()

    def open_dir():
        keys_dir_path = os.path.join(os.getcwd(), 'keys')
        if not os.path.exists(keys_dir_path):
            os.mkdir(keys_dir_path)
        os.system(f"explorer {os.path.join(os.getcwd(), 'keys')}")

    frm6 = tk.Frame(frm)
    frm6.pack()
    button2 = tk.Button(frm6, text='查看密钥详情', font=mid_font, command=tell_detail)
    button2.grid(row=1, column=1, padx=20)
    open_dir_button = tk.Button(frm6, text='打开密钥保存的文件夹', font=mid_font, command=open_dir)
    open_dir_button.grid(row=1, column=2, padx=20)

    # 随机生成一对
    labelframe2 = tk.LabelFrame(frm_of_labelframe, text='随机生成一对ECC密钥', height=457, width=606, font=mid_font)
    labelframe2.pack(side='left', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_label1 = tk.Label(labelframe2, text='请选择密钥的长度：', font=mid_font)
    lf2_label1.pack()

    def lf2_confirm():
        Tools.clean_all_widget(lf2_frm2)
        lf2_label2 = tk.Label(lf2_frm2, text='程序正在进行中，请稍候...', font=mid_font)
        lf2_label2.pack()
        window.update()
        lf2_label2.destroy()
        # 生成密钥对
        if var1.get() == 'SECP256K1':
            private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
            private_key_str = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat("TraditionalOpenSSL"), encryption_algorithm=serialization.BestAvailableEncryption(b'1234')).decode('utf-8')
            public_key = private_key.public_key()
            public_key_str = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat("X.509 subjectPublicKeyInfo with PKCS#1")).decode('utf-8')
        lf2_label3 = tk.Label(lf2_frm2, text=''.join(['公钥（public key）：\n', public_key_str[27: 53].replace('\n', ' '), ' ... ', public_key_str[-29: -26].replace('\n', ' ')]), font=mid_font)
        lf2_label3.pack()
        lf2_label4 = tk.Label(lf2_frm2, font=mid_font, text=''.join(['私钥（private key）：\n', private_key_str[110: 136].replace('\n', ' '), ' ... ', private_key_str[-33: -30].replace('\n', ' ')]))
        lf2_label4.pack()
        # 保存公私钥
        current_dir = os.getcwd()
        key_path = current_dir + '\\keys'
        if not os.path.exists(key_path):
            os.mkdir(key_path)
        with open(key_path + f'\\ECC_private_key_{var1.get()}.pem', 'w', encoding='utf-8') as prifile:
            prifile.write(private_key_str)
        with open(key_path + f'\\ECC_public_key_{var1.get()}.pem', 'w', encoding='utf-8') as pubfile:
            pubfile.write(public_key_str)
        lf2_label5 = tk.Label(lf2_frm2, text='公私钥已经保存至', font=mid_font)
        lf2_label5.pack()
        lf2_entry1 = tk.Entry(lf2_frm2, width=43, font=mid_font)
        lf2_entry1.pack()
        lf2_entry1.insert(0, key_path)
        lf2_label6 = tk.Label(lf2_frm2, text='文件夹中的.pem文件内', font=mid_font)
        lf2_label6.pack()
        lf2_label7 = tk.Label(lf2_frm2, text='注意：新生成的密钥会替换文件夹内同名的旧密钥', font=mid_font, fg='red')
        lf2_label7.pack()

    lf2_var1 = tk.StringVar()
    lf2_var1.set('SECP256K1')
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_rb1 = tk.Radiobutton(lf2_frm1, variable=lf2_var1, text='SECP256K1（兼顾安全性、速度和兼容性）', font=mid_font, value='SECP256K1')
    lf2_rb1.grid(row=1, column=1, padx=10)
    lf2_button1 = tk.Button(labelframe2, text='确定', font=mid_font, command=lf2_confirm)
    lf2_button1.pack()
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()


def set_pwd_of_ecc_privkey():
    # 添加密码或去除密码（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='为ECC私钥添加或去除使用密码', height=741, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()

    def change_lf1_entry1_show():
        Tools.change_entry_show(lf1_var1, lf1_entry1)

    def change_lf1_entry2_show():
        Tools.change_entry_show(lf1_var2, lf1_entry2)

    def lf1_confirm():
        lf1_label4.config(text='   ')
        lf1_text1.config(state='normal')
        Tools.reset(lf1_text1)
        key_path = Tools.get_path_from_entry(lf1_entry1)
        if os.path.exists(key_path):
            with open(Tools.get_path_from_entry(lf1_entry1), 'rb') as f:
                key = f.read()
                if bytes("-----BEGIN EC PRIVATE KEY-----".encode('utf-8')) in key:
                    lf1_text1.insert('end', key.decode('utf-8'))
                else:
                    lf1_text1.insert('end', '这不是正确的私钥')
        else:
            lf1_text1.insert('end', '私钥地址错误')
        lf1_text1.config(state='disabled')

    def lf1_drag(files):
        Tools.dragged_files(files, lf1_entry1)
        lf1_confirm()

    def lf1_reset():
        Tools.reset(lf1_entry1)
        Tools.reset(lf1_entry2)
        lf1_text1.config(state='normal')
        Tools.reset(lf1_text1)
        lf1_text1.config(state='disabled')
        lf1_label4.config(text='   ')

    lf1_label1 = tk.Label(lf1_frm1, text='请拖入您的私钥或输入地址：', font=mid_font)
    lf1_label1.grid(row=1, column=1, padx=5)
    lf1_var1 = tk.StringVar()
    lf1_var1.set('0')
    lf1_cb1 = tk.Checkbutton(lf1_frm1, text='隐藏', font=mid_font, variable=lf1_var1, onvalue='1', offvalue='0', command=change_lf1_entry1_show)
    lf1_cb1.grid(row=1, column=2, padx=5)
    lf1_entry1 = tk.Entry(labelframe1, width=43, font=mid_font)
    lf1_entry1.pack()
    hook_dropfiles(lf1_entry1, func=lf1_drag)
    lf1_frm3 = tk.Frame(labelframe1)
    lf1_frm3.pack()
    lf1_button3 = tk.Button(lf1_frm3, text='重置', font=mid_font, command=lf1_reset)
    lf1_button3.grid(row=1, column=1, padx=20)
    lf1_button4 = tk.Button(lf1_frm3, text='确定', font=mid_font, command=lf1_confirm)
    lf1_button4.grid(row=1, column=2, padx=20)
    lf1_label2 = tk.Label(labelframe1, text='该私钥的内容为：', font=mid_font)
    lf1_label2.pack()
    lf1_text1 = tk.Text(labelframe1, width=43, height=16, font=mid_font, state='disabled')
    lf1_text1.pack()
    lf1_frm4 = tk.Frame(labelframe1)
    lf1_frm4.pack()
    lf1_label3 = tk.Label(lf1_frm4, text='请输入私钥的使用密码：', font=mid_font)
    lf1_label3.grid(row=1, column=1, padx=5)
    lf1_var2 = tk.StringVar()
    lf1_var2.set('1')
    lf1_cb2 = tk.Checkbutton(lf1_frm4, text='隐藏', font=mid_font, variable=lf1_var2, onvalue='1', offvalue='0', command=change_lf1_entry2_show)
    lf1_cb2.grid(row=1, column=2, padx=5)
    lf1_entry2 = tk.Entry(labelframe1, width=43, font=mid_font, show='*')
    lf1_entry2.pack()
    lf1_frm2 = tk.Frame(labelframe1)
    lf1_frm2.pack()

    def encrypt():
        global ind
        ind = (ind + 1) % 6
        lf1_label4.config(fg=colors[ind])
        lf1_text1.config(state='normal')
        privkey = lf1_text1.get(1.0, 'end').strip('\n')
        lf1_text1.config(state='disabled')
        if privkey == '这不是正确的私钥' or privkey == '私钥地址错误' or not privkey:
            lf1_label4.config(text='无法加密')
        elif not lf1_entry2.get().strip(' '):
            lf1_label4.config(text='密码不能为空')
        else:
            enc_key = Tools.encrypt_privkey(privkey.encode('utf-8'), lf1_entry2.get(), is_ecc=True)
            if enc_key == b'':
                lf1_label4.config(text='已经加密过，无法再次加密')
                return 0
            with open(Tools.get_path_from_entry(lf1_entry1), 'wb') as f:
                f.write(enc_key)
            lf1_label4.config(text='加密成功')
            lf1_text1.config(state='normal')
            Tools.reset(lf1_text1)
            lf1_text1.insert('end', enc_key.decode('utf-8'))
            lf1_text1.config(state='disabled')

    def decrypt():
        global ind
        ind = (ind + 1) % 6
        lf1_label4.config(fg=colors[ind])
        lf1_text1.config(state='normal')
        privkey = lf1_text1.get(1.0, 'end').strip('\n')
        lf1_text1.config(state='disabled')
        if privkey == '这不是正确的私钥' or privkey == '私钥地址错误' or not privkey:
            lf1_label4.config(text='无法解密')
            return 0
        elif not lf1_entry2.get().strip(' '):
            lf1_label4.config(text='密码不能为空')
            return 0
        else:
            dec_key = Tools.decrypt_privkey(privkey.encode('utf-8'), lf1_entry2.get(), is_ecc=True)
            if dec_key == b'':
                lf1_label4.config(text='私钥的使用密码错误')
                return 0
            elif dec_key == b'1':
                lf1_label4.config(text='已经去除过密码，无法再次去除')
                return 0
            with open(Tools.get_path_from_entry(lf1_entry1), 'wb') as f:
                f.write(dec_key)
            lf1_label4.config(text='已去除密码')
            lf1_text1.config(state='normal')
            Tools.reset(lf1_text1)
            lf1_text1.insert('end', dec_key)
            lf1_text1.config(state='disabled')

    lf1_button1 = tk.Button(lf1_frm2, text='去除密码', font=mid_font, command=decrypt)
    lf1_button1.grid(row=1, column=1, padx=20)
    lf1_button2 = tk.Button(lf1_frm2, text='添加密码', font=mid_font, command=encrypt)
    lf1_button2.grid(row=1, column=2, padx=20)
    lf1_label4 = tk.Label(labelframe1, text='   ', font=mid_font, fg=colors[ind])
    lf1_label4.pack()

    # 修改密码（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='为ECC私钥修改使用密码', height=741, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()

    def change_lf2_entry1_show():
        Tools.change_entry_show(lf2_var1, lf2_entry1)

    def change_lf2_entry2_show():
        Tools.change_entry_show(lf2_var2, lf2_entry2)

    def change_lf2_entry3_show():
        Tools.change_entry_show(lf2_var3, lf2_entry3)

    def lf2_drag(files):
        Tools.dragged_files(files, lf2_entry1)
        lf2_confirm1()

    def lf2_reset1():
        Tools.reset(lf2_entry1)
        lf2_label5.config(text='   ')
        lf2_text1.config(state='normal')
        Tools.reset(lf2_text1)
        lf2_text1.config(state='disabled')
        lf2_reset2()

    def lf2_confirm1():
        lf2_label5.config(text='   ')
        lf2_text1.config(state='normal')
        Tools.reset(lf2_text1)
        key_path = Tools.get_path_from_entry(lf2_entry1)
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                key = f.read()
                if bytes("-----BEGIN EC PRIVATE KEY-----\nEncrypted:".encode('utf-8')) in key:
                    lf2_text1.insert('end', key.decode('utf-8'))
                else:
                    lf2_text1.insert('end', '这不是已加密的私钥')
        else:
            lf2_text1.insert('end', '私钥地址错误')
        lf2_text1.config(state='disabled')

    def lf2_reset2():
        Tools.reset(lf2_entry2)
        Tools.reset(lf2_entry3)
        lf2_label5.config(text='   ')

    def lf2_confirm2():
        global ind
        ind = (ind + 1) % 6
        lf2_label5.config(fg=colors[ind])
        lf2_text1.config(state='normal')
        enc_key = lf2_text1.get(1.0, 'end').strip('\n')
        lf2_text1.config(state='disabled')
        if enc_key == '这不是已加密的私钥' or enc_key == '私钥地址错误' or not enc_key:
            lf2_label5.config(text='无法修改密码')
            return 0
        elif not lf2_entry2.get().strip('') or not lf2_entry3.get().strip(''):
            lf2_label5.config(text='密码不能为空')
            return 0
        else:
            dec_key = Tools.decrypt_privkey(enc_key.encode('utf-8'), lf2_entry2.get(), is_ecc=True)
            if dec_key == b'':
                lf2_label5.config(text='旧密码错误')
                return 0
            enc_key = Tools.encrypt_privkey(dec_key, lf2_entry3.get(), is_ecc=True)
            with open(Tools.get_path_from_entry(lf2_entry1), 'wb') as f:
                f.write(enc_key)
            lf2_label5.config(text='修改成功')
            lf2_text1.config(state='normal')
            Tools.reset(lf2_text1)
            lf2_text1.insert('end', enc_key.decode('utf-8'))
            lf2_text1.config(state='disabled')

    lf2_label1 = tk.Label(lf2_frm1, text='请拖入被加密的私钥或输入地址：', font=mid_font)
    lf2_label1.grid(row=1, column=1, padx=5)
    lf2_var1 = tk.StringVar()
    lf2_var1.set('0')
    lf2_cb1 = tk.Checkbutton(lf2_frm1, text='隐藏', font=mid_font, variable=lf2_var1, onvalue='1', offvalue='0',
                             command=change_lf2_entry1_show)
    lf2_cb1.grid(row=1, column=2, padx=5)
    lf2_entry1 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=lf2_drag)
    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()
    lf2_button3 = tk.Button(lf2_frm3, text='重置', font=mid_font, command=lf2_reset1)
    lf2_button3.grid(row=1, column=1, padx=20)
    lf2_button4 = tk.Button(lf2_frm3, text='确定', font=mid_font, command=lf2_confirm1)
    lf2_button4.grid(row=1, column=2, padx=20)
    lf2_label2 = tk.Label(labelframe2, text='该私钥的内容为：', font=mid_font)
    lf2_label2.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=13, font=mid_font, state='disabled')
    lf2_text1.pack()
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_label3 = tk.Label(lf2_frm2, text='请输入旧密码：', font=mid_font)
    lf2_label3.grid(row=1, column=1, padx=5)
    lf2_var2 = tk.StringVar()
    lf2_var2.set('1')
    lf2_cb2 = tk.Checkbutton(lf2_frm2, text='隐藏', font=mid_font, variable=lf2_var2, onvalue='1', offvalue='0',
                             command=change_lf2_entry2_show)
    lf2_cb2.grid(row=1, column=2, padx=5)
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font, show='*')
    lf2_entry2.pack()
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_frm4.pack()
    lf2_label4 = tk.Label(lf2_frm4, text='请输入新密码：', font=mid_font)
    lf2_label4.grid(row=1, column=1, padx=5)
    lf2_var3 = tk.StringVar()
    lf2_var3.set('1')
    lf2_cb3 = tk.Checkbutton(lf2_frm4, text='隐藏', font=mid_font, variable=lf2_var3, onvalue='1', offvalue='0',
                             command=change_lf2_entry3_show)
    lf2_cb3.grid(row=1, column=2, padx=5)
    lf2_entry3 = tk.Entry(labelframe2, width=43, font=mid_font, show='*')
    lf2_entry3.pack()
    lf2_frm5 = tk.Frame(labelframe2)
    lf2_frm5.pack()
    lf2_button5 = tk.Button(lf2_frm5, text='重置', font=mid_font, command=lf2_reset2)
    lf2_button5.grid(row=1, column=1, padx=20)
    lf2_button6 = tk.Button(lf2_frm5, text='确定', font=mid_font, command=lf2_confirm2)
    lf2_button6.grid(row=1, column=2, padx=20)
    lf2_label5 = tk.Label(labelframe2, text='   ', font=mid_font, fg=colors[ind])
    lf2_label5.pack()


def ecc_word():
    up_frm = tk.Frame(frm)
    up_frm.pack()
    uf_frm1 = tk.Frame(up_frm)
    uf_frm1.pack()

    def change_uf_entry1_show():
        Tools.change_entry_show(uf_var1, uf_entry1)

    def uf_drag1(files):
        Tools.dragged_files(files, uf_entry1)

    def change_uf_entry2_show():
        Tools.change_entry_show(uf_var2, uf_entry2)

    def uf_drag2(files):
        Tools.dragged_files(files, uf_entry2)

    def change_uf_entry3_show():
        Tools.change_entry_show(uf_var3, uf_entry3)

    uf_label1 = tk.Label(uf_frm1, text='请拖入对方的公钥或输入地址：', font=mid_font)
    uf_label1.grid(row=1, column=1, padx=5)
    uf_var1 = tk.StringVar()
    uf_var1.set('0')
    uf_cb1 = tk.Checkbutton(uf_frm1, text='隐藏', variable=uf_var1, onvalue='1', offvalue='0', command=change_uf_entry1_show, font=mid_font)
    uf_cb1.grid(row=1, column=2, padx=5)
    uf_entry1 = tk.Entry(up_frm, font=mid_font, width=59)
    uf_entry1.pack()
    hook_dropfiles(uf_entry1, func=uf_drag1)
    uf_frm2 = tk.Frame(up_frm)
    uf_frm2.pack()
    uf_frm3 = tk.Frame(uf_frm2)
    uf_frm3.grid(row=1, column=1, padx=15)
    uf_label2 = tk.Label(uf_frm3, text='请拖入自己的私钥或输入地址：', font=mid_font)
    uf_label2.grid(row=1, column=1, padx=5)
    uf_var2 = tk.StringVar()
    uf_var2.set('0')
    uf_cb2 = tk.Checkbutton(uf_frm3, text='隐藏', variable=uf_var2, onvalue='1', offvalue='0', command=change_uf_entry2_show, font=mid_font)
    uf_cb2.grid(row=1, column=2, padx=5)
    uf_entry2 = tk.Entry(uf_frm2, font=mid_font, width=36)
    uf_entry2.grid(row=2, column=1, padx=15)
    hook_dropfiles(uf_entry2, func=uf_drag2)
    uf_frm4 = tk.Frame(uf_frm2)
    uf_frm4.grid(row=1, column=2, padx=15)
    uf_label3 = tk.Label(uf_frm4, text='请输入私钥的使用密码：', font=mid_font)
    uf_label3.grid(row=1, column=1, padx=5)
    uf_var3 = tk.StringVar()
    uf_var3.set('1')
    uf_cb3 = tk.Checkbutton(uf_frm4, text='隐藏', variable=uf_var3, onvalue='1', offvalue='0', command=change_uf_entry3_show, font=mid_font)
    uf_cb3.grid(row=1, column=2, padx=5)
    uf_entry3 = tk.Entry(uf_frm2, font=mid_font, width=30, show='*')
    uf_entry3.grid(row=2, column=2, padx=15)
    base64_or_emoji_frm = tk.Frame(up_frm)
    base64_or_emoji_frm.pack()
    be_frm_label1 = tk.Label(base64_or_emoji_frm, text='请选择密文的编码方式：', font=mid_font)
    be_frm_label1.grid(row=1, column=1, padx=10)
    base64_or_emoji = tk.StringVar()
    base64_or_emoji.set('base64')
    base64_rb = tk.Radiobutton(base64_or_emoji_frm, text='base64编码', variable=base64_or_emoji, value='base64', font=mid_font)
    base64_rb.grid(row=1, column=2, padx=10)
    emoji_rb = tk.Radiobutton(base64_or_emoji_frm, text='emoji编码', variable=base64_or_emoji, value='emoji', font=mid_font)
    emoji_rb.grid(row=1, column=3, padx=10)
    intro_emoji_button = tk.Button(base64_or_emoji_frm, text='说明', font=mid_font, command=Tools.intro_emoji, bd=0, fg='blue')
    intro_emoji_button.grid(row=1, column=4, padx=10)
    down_frm = tk.Frame(frm)
    down_frm.pack()

    # 加密（左边的labelframe）
    labelframe1 = tk.LabelFrame(down_frm, text='ECC加密文字', height=560, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    lf1_text1 = tk.Text(labelframe1, font=mid_font, width=43, height=9)
    lf1_text1.pack()

    def enc(*args):
        if lf1_var1.get() == '0' and args:
            return 0
        Tools.reset(lf1_text2)
        window.update()
        # 通过对方的公钥和自己的私钥生成aes密钥
        aes_key = Tools.get_aes_key_from_ecc_keys(uf_entry1, uf_entry2, uf_entry3)
        if aes_key == 0:
            return 0
        # 再对文字进行加密
        ontology_sec = b''
        with open('_temp1.txt', 'w', encoding='utf-8') as f:
            f.write(lf1_text1.get(1.0, 'end').rstrip('\n'))
        with open('_temp1.txt', 'rb') as f:
            content = f.read(16)
            while content:
                if len(content) < 16:
                    content = Tools.pkcs7_padding(content)
                en_text = aes_key.encrypt(content)
                ontology_sec += en_text
                content = f.read(16)
        os.remove('_temp1.txt')
        lf1_text2.delete(1.0, 'end')
        res = base64.b64encode(ontology_sec).decode('utf-8')
        if base64_or_emoji.get() == 'base64':
            lf1_text2.insert('end', res)
        elif base64_or_emoji.get() == 'emoji':
            lf1_text2.insert('end', Tools.translate_base64_to_emoji(res))

    def lf1_reset():
        Tools.reset(lf1_text1)
        Tools.reset(lf1_text2)

    def lf1_copy():
        Tools.copy(lf1_text2, lf1_button3)

    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()
    lf1_var1 = tk.StringVar()
    lf1_var1.set('0')
    lf1_cb1 = tk.Checkbutton(lf1_frm1, font=mid_font, text='实时计算', variable=lf1_var1, onvalue='1', offvalue='0')
    lf1_cb1.grid(row=1, column=1, padx=15)
    lf1_button1 = tk.Button(lf1_frm1, font=mid_font, text='重置', command=lf1_reset)
    lf1_button1.grid(row=1, column=2, padx=15)
    lf1_button2 = tk.Button(lf1_frm1, font=mid_font, text='加密', command=enc)
    lf1_button2.grid(row=1, column=3, padx=15)
    lf1_button3 = tk.Button(lf1_frm1, font=mid_font, text='复制密文', command=lf1_copy, fg=colors[ind])
    lf1_button3.grid(row=1, column=4, padx=15)
    lf1_text2 = tk.Text(labelframe1, font=mid_font, width=43, height=9)
    lf1_text2.pack()
    lf1_text1.bind("<KeyRelease>", enc)

    # 解密（右边的labelframe)
    labelframe2 = tk.LabelFrame(down_frm, text='ECC解密文字', height=560, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_text1 = tk.Text(labelframe2, font=mid_font, width=43, height=9)
    lf2_text1.pack()

    def dec(*args):
        if lf2_var1.get() == '0' and args:
            return 0
        Tools.reset(lf2_text2)
        window.update()
        # 通过对方的公钥和自己的私钥生成aes密钥
        aes_key = Tools.get_aes_key_from_ecc_keys(uf_entry1, uf_entry2, uf_entry3)
        if aes_key == 0:
            return 0
        # 再对文字进行解密
        info = lf2_text1.get(1.0, 'end').strip('\n')
        try:
            if base64_or_emoji.get() == 'base64':
                ontology_sec = base64.b64decode(info)
            elif base64_or_emoji.get() == 'emoji':
                ontology_sec = base64.b64decode(Tools.translate_emoji_to_base64(info))
        except Exception:
            if base64_or_emoji.get() == 'base64':
                messagebox.showerror(title='密文格式错误', message="不是正确的base64编码，密文是否为emoji编码？")
            elif base64_or_emoji.get() == 'emoji':
                messagebox.showerror(title='密文格式错误', message="无法将输入的emoji字符转为base64编码")
            return 0
        ontology = b''
        with open('_temp2.txt', 'wb') as f:
            f.write(ontology_sec)
        with open('_temp2.txt', 'rb') as f:
            content = f.read(16)
            while content:
                try:
                    de_text = aes_key.decrypt(content)
                except Exception:
                    messagebox.showerror(title='解密失败', message="解密失败，可能是密文信息被删改")
                    return 0
                else:
                    next = f.read(16)
                    if len(next) == 0:
                        de_text = Tools.de_padding(de_text, 'pkcs7 padding')
                    ontology += de_text
                    content = next
        os.remove('_temp2.txt')
        try:
            ontology = ontology.decode('utf-8')
        except Exception as e:
            print('Error:', e)
            messagebox.showinfo(title='解密失败', message='密钥或密文可能不正确')
        else:
            lf2_text2.delete(1.0, 'end')
            lf2_text2.insert('end', str(ontology))

    def lf2_reset():
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)

    def lf2_copy():
        Tools.copy(lf2_text2, lf2_button3)

    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_var1 = tk.StringVar()
    lf2_var1.set('1')
    lf2_cb1 = tk.Checkbutton(lf2_frm1, font=mid_font, text='实时计算', variable=lf2_var1, onvalue='1', offvalue='0')
    lf2_cb1.grid(row=1, column=1, padx=15)
    lf2_button1 = tk.Button(lf2_frm1, font=mid_font, text='重置', command=lf2_reset)
    lf2_button1.grid(row=1, column=2, padx=15)
    lf2_button2 = tk.Button(lf2_frm1, font=mid_font, text='加密', command=dec)
    lf2_button2.grid(row=1, column=3, padx=15)
    lf2_button3 = tk.Button(lf2_frm1, font=mid_font, text='复制密文', command=lf2_copy, fg=colors[ind])
    lf2_button3.grid(row=1, column=4, padx=15)
    lf2_text2 = tk.Text(labelframe2, font=mid_font, width=43, height=9)
    lf2_text2.pack()
    lf2_text1.bind("<KeyRelease>", dec)


def ecc_file():
    up_frm = tk.Frame(frm)
    up_frm.pack()
    uf_frm1 = tk.Frame(up_frm)
    uf_frm1.pack()

    def change_uf_entry1_show():
        Tools.change_entry_show(uf_var1, uf_entry1)

    def uf_drag1(files):
        Tools.dragged_files(files, uf_entry1)

    def change_uf_entry2_show():
        Tools.change_entry_show(uf_var2, uf_entry2)

    def uf_drag2(files):
        Tools.dragged_files(files, uf_entry2)

    def change_uf_entry3_show():
        Tools.change_entry_show(uf_var3, uf_entry3)

    uf_label1 = tk.Label(uf_frm1, text='请拖入对方的公钥或输入地址：', font=mid_font)
    uf_label1.grid(row=1, column=1, padx=5)
    uf_var1 = tk.StringVar()
    uf_var1.set('0')
    uf_cb1 = tk.Checkbutton(uf_frm1, text='隐藏', variable=uf_var1, onvalue='1', offvalue='0', command=change_uf_entry1_show, font=mid_font)
    uf_cb1.grid(row=1, column=2, padx=5)
    uf_entry1 = tk.Entry(up_frm, font=mid_font, width=59)
    uf_entry1.pack()
    hook_dropfiles(uf_entry1, func=uf_drag1)
    uf_frm2 = tk.Frame(up_frm)
    uf_frm2.pack()
    uf_frm3 = tk.Frame(uf_frm2)
    uf_frm3.grid(row=1, column=1, padx=15)
    uf_label2 = tk.Label(uf_frm3, text='请拖入自己的私钥或输入地址：', font=mid_font)
    uf_label2.grid(row=1, column=1, padx=5)
    uf_var2 = tk.StringVar()
    uf_var2.set('0')
    uf_cb2 = tk.Checkbutton(uf_frm3, text='隐藏', variable=uf_var2, onvalue='1', offvalue='0', command=change_uf_entry2_show, font=mid_font)
    uf_cb2.grid(row=1, column=2, padx=5)
    uf_entry2 = tk.Entry(uf_frm2, font=mid_font, width=36)
    uf_entry2.grid(row=2, column=1, padx=15)
    hook_dropfiles(uf_entry2, func=uf_drag2)
    uf_frm4 = tk.Frame(uf_frm2)
    uf_frm4.grid(row=1, column=2, padx=15)
    uf_label3 = tk.Label(uf_frm4, text='请输入私钥的使用密码：', font=mid_font)
    uf_label3.grid(row=1, column=1, padx=5)
    uf_var3 = tk.StringVar()
    uf_var3.set('1')
    uf_cb3 = tk.Checkbutton(uf_frm4, text='隐藏', variable=uf_var3, onvalue='1', offvalue='0', command=change_uf_entry3_show, font=mid_font)
    uf_cb3.grid(row=1, column=2, padx=5)
    uf_entry3 = tk.Entry(uf_frm2, font=mid_font, width=30, show='*')
    uf_entry3.grid(row=2, column=2, padx=15)
    frm_of_labelframe = tk.Frame(frm)
    frm_of_labelframe.pack()

    # 加密（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm_of_labelframe, text='ECC加密文件（夹）', height=606, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def drag2(files):
        Tools.dragged_files(files, lf1_entry2)
        Tools.clean_all_widget(frm4)

    def _enter_length(*args):
        Tools.enter_length(_size, _entry1, _label1, frm4, zebra_frm, lf1_button3)

    lf1_label2 = tk.Label(labelframe1, text='请拖入需要加密的文件（夹）或输入地址：', font=mid_font)
    lf1_label2.pack()
    lf1_entry2 = tk.Entry(labelframe1, show=None, width=43, font=mid_font)
    lf1_entry2.pack()
    hook_dropfiles(lf1_entry2, func=drag2)
    delete_origin = tk.StringVar()
    delete_origin.set('0')
    delete_origin_cb = tk.Checkbutton(labelframe1, text='加密完后删除原文件', font=mid_font, variable=delete_origin, onvalue='1', offvalue='0')
    delete_origin_cb.pack()
    _frm7 = tk.Frame(labelframe1)
    _frm7.pack()
    frm7 = tk.Frame(_frm7)
    frm7.pack()
    lf1_label6 = tk.Label(frm7, text="请选择加密的大小：", font=mid_font)
    lf1_label6.grid(row=1, column=1)
    _size = tk.StringVar()
    _size.set("完整文件")
    option_menu3 = tk.OptionMenu(frm7, _size, *("完整文件", "1单位", "10单位", "516单位", "5160单位", "其他长度", "斑马线加密法"),
                                 command=_enter_length)
    option_menu3.config(font=mid_font)
    option_menu3.grid(row=1, column=2)
    _entry1 = tk.Entry(frm7, width=5, font=mid_font)
    _label1 = tk.Label(frm7, text='单位', font=mid_font)
    intro_button = tk.Button(frm7, text="说明", font=mid_font, command=Tools.intro_enc_head, bd=0, fg='blue')
    intro_button.grid(row=1, column=5)
    zebra_frm = tk.Frame(_frm7)
    zfrm1 = tk.Frame(zebra_frm)
    zfrm1.grid(row=1)
    zlabel1 = tk.Label(zfrm1, text='位置的显示方式：', font=mid_font)
    zlabel1.grid(row=1, column=1, padx=10)
    show_method = tk.StringVar()
    show_method.set('1')

    def change_show_method():
        zentry1.delete(0, 'end')
        zentry4.delete(0, 'end')
        if show_method.get() == '2':
            zlabel3.config(text=' kb ')
            zlabel7.config(text=' kb ')
            zscale1.grid_forget()
            zscale2.grid_forget()
        elif show_method.get() == '1':
            zlabel3.config(text=' %  ')
            zlabel7.config(text='%')
            begin.set(0)
            end.set(100)
            zentry1.insert('end', '0')
            zentry4.insert('end', '100')
            zscale1.grid(row=3)
            zscale2.grid(row=5)

    def change_zentry1(value):
        Tools.change_zentry(value, zentry1)

    def change_zentry4(value):
        Tools.change_zentry(value, zentry4)

    def change_zscale1(*args):
        Tools.change_zscale(show_method, zentry1, begin)

    def change_zscale2(*args):
        Tools.change_zscale(show_method, zentry4, end)

    zrb1 = tk.Radiobutton(zfrm1, text='百分比', font=mid_font, variable=show_method, value='1', command=change_show_method)
    zrb1.grid(row=1, column=2, padx=10)
    zrb2 = tk.Radiobutton(zfrm1, text='绝对值', font=mid_font, variable=show_method, value='2', command=change_show_method)
    zrb2.grid(row=1, column=3, padx=10)
    zfrm2 = tk.Frame(zebra_frm)
    zfrm2.grid(row=2)
    zlabel2 = tk.Label(zfrm2, text='第一根黑线的起始位置：  ', font=mid_font)
    zlabel2.grid(row=1, column=1)
    zentry1 = tk.Entry(zfrm2, width=5, font=mid_font)
    zentry1.grid(row=1, column=2)
    zentry1.insert('end', '0')
    zentry1.bind('<KeyRelease>', change_zscale1)
    zlabel3 = tk.Label(zfrm2, text=' %  ', font=mid_font)
    zlabel3.grid(row=1, column=3)
    begin = tk.IntVar()
    begin.set(0)
    zscale1 = tk.Scale(zebra_frm, from_=0, to=100, orient=tk.HORIZONTAL, length=400, tickinterval=10, resolution=1,
                       showvalue=0, variable=begin, command=change_zentry1)
    zscale1.grid(row=3)
    zfrm4 = tk.Frame(zebra_frm)
    zfrm4.grid(row=4)
    zlabel4 = tk.Label(zfrm4, text='黑线的宽度：            ', font=mid_font)
    zlabel4.grid(row=1, column=1)
    zentry2 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry2.grid(row=1, column=2)
    zlabel8 = tk.Label(zfrm4, text='单位', font=mid_font)
    zlabel8.grid(row=1, column=3)
    zlabel5 = tk.Label(zfrm4, text='黑线的根数：            ', font=mid_font)
    zlabel5.grid(row=2, column=1)
    zentry3 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry3.grid(row=2, column=2)
    zlabel9 = tk.Label(zfrm4, text='根', font=mid_font)
    zlabel9.grid(row=2, column=3)
    zlabel6 = tk.Label(zfrm4, text='最后一根黑线的末尾位置：', font=mid_font)
    zlabel6.grid(row=3, column=1)
    zentry4 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry4.grid(row=3, column=2)
    zentry4.insert('end', '100')
    zentry4.bind('<KeyRelease>', change_zscale2)
    zlabel7 = tk.Label(zfrm4, text=' %  ', font=mid_font)
    zlabel7.grid(row=3, column=3)
    end = tk.IntVar()
    end.set(100)
    zscale2 = tk.Scale(zebra_frm, from_=0, to=100, orient=tk.HORIZONTAL, length=400, tickinterval=10, resolution=1,
                       showvalue=0, variable=end, command=change_zentry4)
    zscale2.grid(row=5)

    def process():
        Tools.clean_all_widget(frm4)
        # 先通过对方的公钥和自己的私钥计算出共享AES密钥
        aes = Tools.get_aes_key_from_ecc_keys(uf_entry1, uf_entry2, uf_entry3)
        if aes == 0:
            return 0
        # 再判断要加密的文件（夹）是否存在
        ontology_path = Tools.get_path_from_entry(lf1_entry2)
        if not os.path.exists(ontology_path):
            tk.messagebox.showerror(title='路径错误', message='待加密的文件地址不正确，请重新输入')
            return 0
        # 为了防止在运行过程中，用户改变_size的值，这里需要先固定这个值
        size = Tools.get_correct_size(_size, _entry1)
        if size == 0:
            return 0
        _begin, width, number, _end = Tools.get_correct_zebra_parameter(size, show_method, zentry1, zentry2, zentry3, zentry4)
        if _begin is False:
            return 0
        setting_of_delete_origin = delete_origin.get()  # 用来保存是否要删除原文件
        if os.path.isfile(ontology_path):
            label5 = tk.Label(frm4, font=mid_font, text='处理时间可能会较长，请耐心等待')
            label5.pack()
            window.update()
            label5.destroy()
            # 再处理要加密的文件
            base, suffix = os.path.splitext(ontology_path)
            ontology_sec_path = base + '_ECC_Encrypted' + suffix
            Tools.aes_enc_file(aes, 'pkcs7 padding', ontology_path, ontology_sec_path, size, _begin, width, number, _end)
            if setting_of_delete_origin == '1':
                Tools.delete_file(ontology_path)
                label9 = tk.Label(frm4, text='加密成功并已删除原文件，\n文件保存至原文件所在文件夹中的', font=mid_font)
            else:
                label9 = tk.Label(frm4, text='加密成功，文件保存至原文件所在文件夹中的', font=mid_font)
            label9.pack()
            entry4 = tk.Entry(frm4, width=43, font=mid_font)
            entry4.insert('end', os.path.basename(ontology_sec_path))
            entry4.pack()
        elif os.path.isdir(ontology_path):
            # 定义进度条
            progress_bar = ttk.Progressbar(frm4)
            progress_bar['length'] = 200
            progress_bar['value'] = 0
            files = os.listdir(ontology_path)
            out_dir = os.path.join(ontology_path, 'ECC_Encrypted')
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            cleaned_files = []  # 只将files里的纯文件的绝对路径保存到这里，其他的，比如文件夹会删掉
            for file in files:
                file_path = os.path.join(ontology_path, file)
                if os.path.isfile(file_path):
                    cleaned_files.append(file_path)
            progress_bar['maximum'] = len(cleaned_files)  # 这里定义进度条的总长度
            progress_bar.pack(pady=10)  # 再放置进度条
            window.update()  # 这里的窗口更新很重要，因为如果第一个文件处理完了再更新窗口，用户会觉得卡顿
            for file_path in cleaned_files:
                out_path = os.path.join(out_dir, os.path.basename(file_path))
                Tools.aes_enc_file(aes, 'pkcs7 padding', file_path, out_path, size, _begin, width, number, _end)
                # 每次加密完后都需要重新设定aes
                aes = Tools.get_aes_key_from_ecc_keys(uf_entry1, uf_entry2, uf_entry3)
                if setting_of_delete_origin == '1':
                    Tools.delete_file(file_path)
                progress_bar['value'] += 1
                window.update()
            if setting_of_delete_origin == '1':
                label9 = tk.Label(frm4, text='加密成功并已删除原文件，文件保存至\n原文件夹中新建的 ECC_Encrypted 文件夹中', font=mid_font)
            else:
                label9 = tk.Label(frm4, text='加密成功，文件保存至原文件夹中\n新建的 ECC_Encrypted 文件夹中', font=mid_font)
            label9.pack()
        else:
            tk.messagebox.showerror(title='路径错误', message='待加密的文件（夹）地址不正确，请重新输入')
            return 0

    def _reset():
        Tools.reset(lf1_entry2)
        Tools.clean_all_widget(frm4)

    frm2 = tk.Frame(labelframe1)
    frm2.pack()
    lf1_button1 = tk.Button(frm2, font=mid_font, text='重置', command=_reset)
    lf1_button1.grid(row=1, column=1, padx=20)
    lf1_button2 = tk.Button(frm2, font=mid_font, text='加密', command=process)
    lf1_button2.grid(row=1, column=2, padx=20)
    lf1_button3 = tk.Button(frm2, text='设置', font=mid_font, command=Tools.setting, fg='blue', bd=0)
    frm4 = tk.Frame(labelframe1)
    frm4.pack()

    # 解密（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm_of_labelframe, text='ECC解密文件（夹）', height=606, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变

    def lf2_drag1(files):
        Tools.dragged_files(files, lf2_entry2)
        Tools.clean_all_widget(lf2_frm4)

    def decrypt():
        Tools.clean_all_widget(lf2_frm4)
        # 先处理密钥
        aes = Tools.get_aes_key_from_ecc_keys(uf_entry1, uf_entry2, uf_entry3)
        if aes == 0:
            return 0
        # 再处理要解密的文件
        ontology_sec_path = Tools.get_path_from_entry(lf2_entry2)
        if not os.path.exists(ontology_sec_path):
            tk.messagebox.showerror(title='路径错误', message='待解密的文件地址不正确，请重新输入')
            return 0
        # 为了防止在运行过程中，用户改变var1, entry1, ...的值，所以这里就需要先固定住这两个值
        setting_of_delete_sec = delete_sec.get()  # 保存是否删除原文件
        _var3 = tk.StringVar()  # 保存是否是临时解密
        _var3.set(lf2_var1.get())
        if os.path.isfile(ontology_sec_path):
            lf2_label3 = tk.Label(lf2_frm4, text='处理时间可能会较长，请耐心等待', font=mid_font)
            lf2_label3.pack()
            window.update()
            lf2_label3.destroy()
            # 再处理解密的文件
            base, suffix = os.path.splitext(ontology_sec_path)
            if _var3.get() == '1':
                ontology_path = base + '_ECC_Decrypted' + suffix
            elif _var3.get() == '2':
                ontology_path = base + '_temp' + suffix
            process_succeed = Tools.aes_dec_file(aes, 'pkcs7 padding', ontology_sec_path, ontology_path)
            if process_succeed:
                if setting_of_delete_sec == '1':
                    Tools.delete_file(ontology_sec_path)
                    lf2_label4 = tk.Label(lf2_frm4, text='解密成功并已删除密文文件，\n文件保存至原文件所在文件夹中的', font=mid_font)
                else:
                    lf2_label4 = tk.Label(lf2_frm4, text='解密成功，文件保存至原文件所在文件夹中的', font=mid_font)
                lf2_label4.pack()
                lf2_entry3 = tk.Entry(lf2_frm4, width=43, font=mid_font)
                lf2_entry3.insert('end', os.path.basename(ontology_path))
                lf2_entry3.pack()
                if _var3.get() == '2':

                    def save():
                        answer = messagebox.askyesno(title='提示', message='请确认修改内容已保存，并且临时文件名称没有修改')
                        if answer:
                            if os.path.exists(ontology_path):
                                lf2_label9 = tk.Label(lf2_frm4, text='处理时间可能会较长，请耐心等待', font=mid_font)
                                lf2_label9.pack()
                                window.update()
                                lf2_label9.destroy()
                                # 这里需要重新新建一个aes
                                aes = Tools.get_aes_key_from_ecc_keys(uf_entry1, uf_entry2, uf_entry3)
                                Tools.aes_enc_file(aes, 'pkcs7 padding', ontology_path, ontology_sec_path)
                                lf2_label10 = tk.Label(lf2_frm4, text='加密成功，文件保存至原文件所在文件夹中的', font=mid_font)
                                lf2_label10.pack()
                                lf2_entry4 = tk.Entry(lf2_frm4, width=43, font=mid_font)
                                lf2_entry4.pack()
                                lf2_entry4.insert('end', os.path.basename(ontology_sec_path))
                                os.remove(ontology_path)
                            else:
                                messagebox.showerror(title='路径错误', message='找不到临时文件了')

                    lf2_button4 = tk.Button(lf2_frm4, text='重新加密', font=mid_font, command=save)
                    lf2_button4.pack()
                elif _var3.get() == '1':

                    def _remove():
                        Tools.remove_file_or_dir(ontology_path, lf2_frm8)

                    lf2_frm7 = tk.Frame(lf2_frm4)
                    lf2_frm7.pack()
                    destroy_button = tk.Button(lf2_frm7, text='阅后即焚', font=mid_font, command=_remove)
                    destroy_button.grid(row=1, column=1, padx=10)
                    intro_destroy_button = tk.Button(lf2_frm7, text='说明', font=mid_font, fg='blue', bd=0,
                                                     command=Tools.intro_destroy)
                    intro_destroy_button.grid(row=1, column=2, padx=10)
                    lf2_frm8 = tk.Frame(lf2_frm4)
                    lf2_frm8.pack()
            else:
                os.remove(ontology_path)  # 这里不需要弹窗报错了，因为_aes_dec_file函数中已经报错了
        elif os.path.isdir(ontology_sec_path):
            # 定义进度条
            progress_bar = ttk.Progressbar(lf2_frm4)
            progress_bar['length'] = 200
            progress_bar['value'] = 0
            files = os.listdir(ontology_sec_path)
            if _var3.get() == '1':
                out_dir = os.path.join(ontology_sec_path, 'ECC_Decrypted')
            elif _var3.get() == '2':
                out_dir = os.path.join(ontology_sec_path, 'temp')
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            cleaned_files = []  # 只将files里的纯文件的绝对路径保存到这里，其他的比如文件夹会删掉
            for file in files:
                file_path = os.path.join(ontology_sec_path, file)
                if os.path.isfile(file_path):
                    cleaned_files.append(file_path)
            progress_bar['maximum'] = len(cleaned_files)  # 这里定义进度条的总长度
            progress_bar.pack(pady=10)  # 再放置进度条
            window.update()
            failed_files = []
            for file_path in cleaned_files:
                out_path = os.path.join(out_dir, os.path.basename(file_path))
                process_success = Tools.aes_dec_file(aes, 'pkcs7 padding', file_path, out_path, show_error=False)
                # 每次解密完后都需要重新设定aes
                aes = Tools.get_aes_key_from_ecc_keys(uf_entry1, uf_entry2, uf_entry3)
                if not process_success:
                    os.remove(out_path)
                    failed_files.append(os.path.basename(file_path))
                else:
                    if setting_of_delete_sec == '1':
                        Tools.delete_file(file_path)
                progress_bar['value'] += 1
                window.update()
            if _var3.get() == '1':
                lf2_label5 = tk.Label(lf2_frm4, text='解密完成，文件保存至\n原文件夹中新建的 ECC_Decrypted 文件夹中', font=mid_font)
            elif _var3.get() == '2':
                lf2_label5 = tk.Label(lf2_frm4, text='解密完成，文件保存至\n原文件夹中新建的 temp 文件夹中', font=mid_font)
            lf2_label5.pack()
            if failed_files:
                lf2_text = tk.Text(lf2_frm4, width=43, font=mid_font, height=6)
                lf2_text.insert('end', f'其中，{len(failed_files)}个文件解密失败，分别为：\n' + '\n'.join(failed_files))
                lf2_text.pack()
            if _var3.get() == '2':

                def save():
                    answer = messagebox.askyesno(title='提示', message='请确认修改内容已保存，并且临时文件名称没有修改')
                    if answer:
                        if os.path.exists(out_dir):
                            # 定义进度条
                            progress_bar2 = ttk.Progressbar(lf2_frm4)
                            progress_bar2['length'] = 200
                            progress_bar2['value'] = 0
                            files2 = os.listdir(out_dir)
                            cleaned_files2 = []
                            for file2 in files2:
                                file_path2 = os.path.join(out_dir, file2)
                                if os.path.isfile(file_path2):
                                    cleaned_files2.append(file_path2)
                            if len(cleaned_files2) == 0:
                                progress_bar2['maximum'] = 1
                                progress_bar2['value'] = 1
                            else:
                                progress_bar2['maximum'] = len(cleaned_files2)  # 这里定义进度条的总长度
                            progress_bar2.pack(pady=10)  # 再放置进度条
                            window.update()
                            for file_path2 in cleaned_files2:
                                origin_path = os.path.join(ontology_sec_path, os.path.basename(file_path2))
                                # 每次加密前都需要重新设定aes
                                aes = Tools.get_aes_key_from_ecc_keys(uf_entry1, uf_entry2, uf_entry3)
                                Tools.aes_enc_file(aes, 'pkcs7 padding', file_path2, origin_path)
                                progress_bar2['value'] += 1
                                window.update()
                            lf2_label6 = tk.Label(lf2_frm4, text='已重新加密回原文件夹', font=mid_font)
                            lf2_label6.pack()
                            shutil.rmtree(out_dir)
                        else:
                            messagebox.showerror(title='路径错误', message='找不到临时文件夹了')

                lf2_button4 = tk.Button(lf2_frm4, text='重新加密', font=mid_font, command=save)
                lf2_button4.pack()

            elif _var3.get() == '1':

                def _remove():
                    Tools.remove_file_or_dir(out_dir, lf2_frm6)

                lf2_frm5 = tk.Frame(lf2_frm4)
                lf2_frm5.pack()
                destroy_button = tk.Button(lf2_frm5, text='阅后即焚', font=mid_font, command=_remove)
                destroy_button.grid(row=1, column=1, padx=10)
                intro_destroy_button = tk.Button(lf2_frm5, text='说明', font=mid_font, fg='blue', bd=0,
                                                 command=Tools.intro_destroy)
                intro_destroy_button.grid(row=1, column=2, padx=10)
                lf2_frm6 = tk.Frame(lf2_frm4)
                lf2_frm6.pack()
        else:
            tk.messagebox.showerror(title='路径错误', message='待解密的文件（夹）地址不正确，请重新输入')
            return 0

    def lf2_reset():
        Tools.reset(lf2_entry2)
        Tools.clean_all_widget(lf2_frm4)

    def tell_difference():
        tell_window = tk.Toplevel(window)
        tell_window.geometry('636x758')
        tell_window.title('说明')
        tell_window.iconbitmap(icon_path)
        tw_text = tk.Text(tell_window, width=46, height=28, font=mid_font)
        tw_text.pack()
        word = '''    1. 如果你仅需要浏览解密后的内容，使用普通解密功能即可，在解密完成后，可以使用阅后即焚功能，来删除解密的文件，这样删除的文件不会在回收站内被找到。

        2. 如果你需要编辑解密后的内容，并在编辑完成后，快速实现重新加密，建议使用临时解密功能，修改后的文件会取代被修改前的文件。
    注意：临时文件的文件名需要保持原样。以及重新加密的方法是全文加密。'''
        tw_text.insert('end', word)

    lf2_label2 = tk.Label(labelframe2, text='请拖入需要解密的文件（夹）或输入地址：', font=mid_font)
    lf2_label2.pack()
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry2.pack()
    hook_dropfiles(lf2_entry2, func=lf2_drag1)
    delete_sec = tk.StringVar()
    delete_sec.set('0')
    delete_sec_cb = tk.Checkbutton(labelframe2, text='解密完后删除密文文件', font=mid_font, variable=delete_sec, onvalue='1',
                                   offvalue='0')
    delete_sec_cb.pack()
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_var1 = tk.StringVar()
    lf2_var1.set('1')
    lf2_rb1 = tk.Radiobutton(lf2_frm1, text='普通解密', font=mid_font, variable=lf2_var1, value='1')
    lf2_rb1.grid(row=1, column=1, padx=15)
    lf2_rb2 = tk.Radiobutton(lf2_frm1, text='临时解密', font=mid_font, variable=lf2_var1, value='2')
    lf2_rb2.grid(row=1, column=2, padx=15)
    lf2_button1 = tk.Button(lf2_frm1, text='说明', font=mid_font, fg='blue', bd=0, command=tell_difference)
    lf2_button1.grid(row=1, column=3, padx=15)
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_button2 = tk.Button(lf2_frm2, font=mid_font, text='重置', command=lf2_reset)
    lf2_button2.grid(row=1, column=1, padx=20)
    lf2_button3 = tk.Button(lf2_frm2, font=mid_font, text='解密', command=decrypt)
    lf2_button3.grid(row=1, column=2, padx=20)
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_frm4.pack()


def ecc_sign_and_verify():
    # 数字签名（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='ECC数字签名', height=741, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    frm1 = tk.Frame(labelframe1)
    frm1.pack()

    def change_entry1_show():
        Tools.change_entry_show(var1, entry1)

    def drag1(files):
        Tools.clean_all_widget(frm4)
        Tools.reset(text2)
        Tools.dragged_files(files, entry1)

    label1 = tk.Label(frm1, text='请拖入私钥或输入地址：', font=mid_font)
    label1.grid(row=1, column=1, padx=5)
    var1 = tk.StringVar()
    var1.set('0')
    cb1 = tk.Checkbutton(frm1, text='隐藏', variable=var1, onvalue='1', offvalue='0', command=change_entry1_show,
                         font=mid_font)
    cb1.grid(row=1, column=2, padx=5)
    entry1 = tk.Entry(labelframe1, font=mid_font, width=43)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)

    def change_target():
        Tools.clean_all_widget(frm4)
        frm3.pack_forget()
        Tools.reset(text2)
        if target.get() == 'file':
            label2.config(text='请拖入需要签名的文件或输入地址：')
            text1.pack_forget()
            entry2.pack()
            frm4.pack()
        elif target.get() == 'word':
            label2.config(text='请输入需要签名的文字：')
            entry2.pack_forget()
            text1.pack()
            frm4.pack_forget()
        frm3.pack()

    def drag2(files):
        Tools.clean_all_widget(frm4)
        Tools.reset(text2)
        Tools.dragged_files(files, entry2)

    def change_pwd_entry_show():
        Tools.change_entry_show(pwd_var, pwd_entry)

    pwd_frm = tk.Frame(labelframe1)
    pwd_frm.pack()
    pwd_label = tk.Label(pwd_frm, text='请输入该私钥的使用密码：', font=mid_font)
    pwd_label.grid(row=1, column=1, padx=5)
    pwd_var = tk.StringVar()
    pwd_var.set('1')
    pwd_cb = tk.Checkbutton(pwd_frm, text='隐藏', font=mid_font, variable=pwd_var, onvalue='1', offvalue='0',
                            command=change_pwd_entry_show)
    pwd_cb.grid(row=1, column=2, padx=5)
    pwd_entry = tk.Entry(labelframe1, width=43, font=mid_font, show='*')
    pwd_entry.pack()
    target_frm = tk.Frame(labelframe1)
    target_frm.pack()
    target = tk.StringVar()
    target.set('word')
    rb1 = tk.Radiobutton(target_frm, text='签名文字', font=mid_font, variable=target, value='word', command=change_target)
    rb1.grid(row=1, column=1, padx=15)
    rb2 = tk.Radiobutton(target_frm, text='签名文件', font=mid_font, variable=target, value='file', command=change_target)
    rb2.grid(row=1, column=2, padx=15)
    label2 = tk.Label(labelframe1, text='请输入需要签名的文字：', font=mid_font)
    label2.pack()
    text1 = tk.Text(labelframe1, width=43, height=9, font=mid_font)
    text1.pack()
    entry2 = tk.Entry(labelframe1, width=43, font=mid_font)
    hook_dropfiles(entry2, func=drag2)

    def process():
        global ind
        Tools.clean_all_widget(frm4)
        Tools.reset(text2)
        # 先处理私钥
        privkey_signer = Tools.get_key(entry1, method='signer', pwd_entry=pwd_entry, is_ecc=True)
        if privkey_signer == 0:
            return 0
        ind = (ind + 1) % 6
        hasher = hashes.Hash(hashes.SHA384(), backend=default_backend())
        if target.get() == 'word':
            hasher.update(text1.get(1.0, 'end').rstrip("\n").encode('utf-8'))
            word_hash = hasher.finalize()
            try:
                signature = base64.b64encode(privkey_signer.sign(word_hash, ec.ECDSA(hashes.SHA384())))
            except Exception:
                Tools.reset(text2)
                text2.insert('end', '签名出错，密钥可能有问题')
                return 0
        elif target.get() == 'file':
            ontology_path = Tools.get_path_from_entry(entry2)
            if os.path.exists(ontology_path) and os.path.isfile(ontology_path):
                with open(ontology_path, 'rb') as f:
                    block_size = 33554432
                    fb = f.read(block_size)
                    while fb:
                        hasher.update(fb)
                        fb = f.read(block_size)
                    file_hash = hasher.finalize()
                ontology_sec_path = ontology_path + '.sign'
                process_succeed = True
                try:
                    signature = base64.b64encode(privkey_signer.sign(file_hash, ec.ECDSA(hashes.SHA384())))
                except Exception:
                    text2.insert('end', '签名出错，请检查密钥与文件')
                    process_succeed = False
                else:
                    with open(ontology_sec_path, 'wb') as outfile:
                        outfile.write(signature)
                    label4 = tk.Label(frm4, text='签名成功，其中信息摘要采用SHA-384算法', font=mid_font, fg=colors[ind])
                    label4.pack()
                    label5 = tk.Label(frm4, text='数字签名文件保存至原文件所在文件夹中的', font=mid_font, fg=colors[ind])
                    label5.pack()
                    entry3 = tk.Entry(frm4, width=43, font=mid_font, fg=colors[ind])
                    entry3.insert('end', os.path.basename(ontology_sec_path))
                    entry3.pack()
                if not process_succeed:
                    os.remove(ontology_sec_path)
            else:
                text2.insert('end', '待签名的文件地址不正确，请重新输入')
                return 0
        text2.insert('end', signature)

    def _reset():
        Tools.clean_all_widget(frm4)
        Tools.reset(text1)
        Tools.reset(text2)

    def _copy():
        Tools.copy(text2, button3)

    frm3 = tk.Frame(labelframe1)
    frm3.pack(pady=5)
    frm2 = tk.Frame(frm3)
    frm2.pack()
    button1 = tk.Button(frm2, text='重置', font=mid_font, command=_reset)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm2, text='签名', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=20)
    button3 = tk.Button(frm2, font=mid_font, text='复制签名', command=_copy, fg=colors[ind])
    button3.grid(row=1, column=3, padx=20)
    label3 = tk.Label(frm3, text='签名结果为：', font=mid_font)
    label3.pack()
    text2 = tk.Text(frm3, width=43, height=7, font=mid_font)
    text2.pack()
    frm4 = tk.Frame(frm3)

    # 验证签名（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='ECC验证签名', height=741, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()

    def change_lf2_entry1_show():
        Tools.change_entry_show(lf2_var1, lf2_entry1)

    def drag2(files):
        Tools.clean_all_widget(lf2_frm4)
        Tools.dragged_files(files, lf2_entry1)

    lf2_label1 = tk.Label(lf2_frm1, text='请拖入签名发送方的公钥或输入地址：', font=mid_font)
    lf2_label1.grid(row=1, column=1, padx=5)
    lf2_var1 = tk.StringVar()
    lf2_var1.set('0')
    lf2_cb1 = tk.Checkbutton(lf2_frm1, text='隐藏', variable=lf2_var1, onvalue='1', offvalue='0', command=change_lf2_entry1_show, font=mid_font)
    lf2_cb1.grid(row=1, column=2, padx=5)
    lf2_entry1 = tk.Entry(labelframe2, font=mid_font, width=43)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=drag2)

    def change_check():
        Tools.clean_all_widget(lf2_frm4)
        lf2_frm7.pack_forget()
        if check_mode.get() == 'file':
            lf2_text2.pack_forget()
            lf2_entry3.pack()
        elif check_mode.get() == 'word':
            lf2_entry3.pack_forget()
            lf2_text2.pack()
        lf2_frm7.pack()

    def change_target2():
        Tools.clean_all_widget(lf2_frm4)
        check_mode.set('word')
        change_check()
        lf2_frm5.pack_forget()
        lf2_frm6.pack_forget()
        if target2.get() == 'file':
            lf2_label2.config(text='请拖入需要验签的文件或输入地址：')
            lf2_text1.pack_forget()
            lf2_entry2.pack()
            lf2_label3.grid_forget()
            lf2_rb3.grid(row=1, column=1, padx=15)
            lf2_rb4.grid(row=1, column=2, padx=15)
        elif target2.get() == 'word':
            lf2_label2.config(text='请输入需要验签的文字：')
            lf2_text1.pack()
            lf2_entry2.pack_forget()
            lf2_label3.grid(row=1, column=1)
            lf2_rb3.grid_forget()
            lf2_rb4.grid_forget()
        lf2_frm5.pack()
        lf2_frm6.pack()

    def drag3(files):
        Tools.clean_all_widget(lf2_frm4)
        Tools.dragged_files(files, lf2_entry2)

    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()
    target2 = tk.StringVar()
    target2.set('word')
    lf2_rb1 = tk.Radiobutton(lf2_frm3, text='验证文字', font=mid_font, variable=target2, value='word', command=change_target2)
    lf2_rb1.grid(row=1, column=1, padx=15)
    lf2_rb2 = tk.Radiobutton(lf2_frm3, text='验证文件', font=mid_font, variable=target2, value='file', command=change_target2)
    lf2_rb2.grid(row=1, column=2, padx=15)
    lf2_label2 = tk.Label(labelframe2, text='请输入需要验签的文字：', font=mid_font)
    lf2_label2.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=9, font=mid_font)
    lf2_text1.pack()
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font)
    hook_dropfiles(lf2_entry2, func=drag3)
    lf2_frm5 = tk.Frame(labelframe2)
    lf2_frm5.pack()
    check_mode = tk.StringVar()
    check_mode.set('word')
    lf2_label3 = tk.Label(lf2_frm5, text='请输入数字签名：', font=mid_font)
    lf2_label3.grid(row=1, column=1)
    lf2_rb3 = tk.Radiobutton(lf2_frm5, text='输入数字签名', font=mid_font, variable=check_mode, value='word', command=change_check)
    lf2_rb4 = tk.Radiobutton(lf2_frm5, text='拖入签名文件', font=mid_font, variable=check_mode, value='file', command=change_check)

    def verify():
        global ind
        Tools.clean_all_widget(lf2_frm4)
        # 先处理公钥
        pubkey_verifier = Tools.get_key(lf2_entry1, method='verifier', is_ecc=True)
        if pubkey_verifier == 0:
            return 0
        ind = (ind + 1) % 6
        hasher = hashes.Hash(hashes.SHA384(), backend=default_backend())
        if target2.get() == 'word':
            hasher.update(lf2_text1.get(1.0, 'end').rstrip("\n").encode('utf-8'))
            word_hash = hasher.finalize()
            try:
                signature = base64.b64decode(lf2_text2.get(1.0, 'end').rstrip("\n"))
            except Exception:
                lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名编码有误', fg=colors[ind])
                lf2_label4.pack()
            else:
                try:
                    pubkey_verifier.verify(signature, word_hash, ec.ECDSA(hashes.SHA384()))
                    lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名验证通过', fg=colors[ind])
                    lf2_label4.pack()
                    lf2_label5 = tk.Label(lf2_frm4, font=mid_font, text='原信息的SHA-384数字摘要与数字签名内容一致', fg=colors[ind])
                    lf2_label5.pack()
                except Exception:
                    lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名验证未能通过', fg=colors[ind])
                    lf2_label4.pack()
                    lf2_label5 = tk.Label(lf2_frm4, font=mid_font, text='原信息的SHA-384数字摘要与数字签名内容不一致', fg=colors[ind])
                    lf2_label5.pack()
        elif target2.get() == 'file':
            if check_mode.get() == 'file':
                signature_path = Tools.get_path_from_entry(lf2_entry3)
                try:
                    with open(signature_path, 'rb') as signature_file:
                        signature = base64.b64decode(signature_file.read())
                except Exception:
                    lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名文件路径错误', fg=colors[ind])
                    lf2_label4.pack()
                    return 0
            elif check_mode.get() == 'word':
                try:
                    signature = base64.b64decode(lf2_text2.get(1.0, 'end').rstrip("\n"))
                except Exception:
                    lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名编码有误', fg=colors[ind])
                    lf2_label4.pack()
                    return 0
            # 然后处理原始文件的地址
            message_path = Tools.get_path_from_entry(lf2_entry2)
            if (not os.path.exists(message_path)) or (not os.path.isfile(message_path)):
                lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='需要验签的文件路径错误', fg=colors[ind])
                lf2_label4.pack()
                return 0
            # 最后检查原始文件的摘要和数字签名是否一致
            with open(message_path, 'rb') as f:
                block_size = 33554432
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                file_hash = hasher.finalize()
            try:
                pubkey_verifier.verify(signature, file_hash, ec.ECDSA(hashes.SHA384()))
                lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名验证通过', fg=colors[ind])
                lf2_label4.pack()
                lf2_entry4 = tk.Entry(lf2_frm4, font=mid_font, width=43, fg=colors[ind])
                lf2_entry4.insert('end', os.path.basename(message_path))
                lf2_entry4.pack()
                lf2_label5 = tk.Label(lf2_frm4, font=mid_font, text='的SHA-384数字摘要与数字签名内容一致', fg=colors[ind])
                lf2_label5.pack()
            except Exception:
                lf2_label4 = tk.Label(lf2_frm4, font=mid_font, text='数字签名验证未能通过', fg=colors[ind])
                lf2_label4.pack()
                lf2_entry4 = tk.Entry(lf2_frm4, font=mid_font, width=43, fg=colors[ind])
                lf2_entry4.insert('end', os.path.basename(message_path))
                lf2_entry4.pack()
                lf2_label5 = tk.Label(lf2_frm4, font=mid_font, text='的SHA-384数字摘要与数字签名内容不一致', fg=colors[ind])
                lf2_label5.pack()

    def reset2():
        Tools.clean_all_widget(lf2_frm4)
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)
        Tools.reset(lf2_entry2)
        Tools.reset(lf2_entry3)

    def drag4(files):
        Tools.clean_all_widget(lf2_frm4)
        Tools.dragged_files(files, lf2_entry3)

    lf2_frm6 = tk.Frame(labelframe2)
    lf2_frm6.pack()
    lf2_text2 = tk.Text(lf2_frm6, width=43, height=7, font=mid_font)
    lf2_text2.pack()
    lf2_entry3 = tk.Entry(lf2_frm6, width=43, font=mid_font)
    hook_dropfiles(lf2_entry3, func=drag4)
    lf2_frm7 = tk.Frame(lf2_frm6)
    lf2_frm7.pack()
    lf2_frm2 = tk.Frame(lf2_frm7)
    lf2_frm2.pack()
    lf2_button1 = tk.Button(lf2_frm2, text='重置', font=mid_font, command=reset2)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm2, text='验签', font=mid_font, command=verify)
    lf2_button2.grid(row=1, column=2, padx=20)
    lf2_frm4 = tk.Frame(lf2_frm7)
    lf2_frm4.pack()


def create_aes_key_by_hash_digest():

    def drag(files):
        Tools.dragged_files(files, entry1)
        process()

    label2 = tk.Label(frm, text='通过信息摘要生成AES 256位密钥', font=mid_font)
    label2.pack()
    frm1 = tk.Frame(frm)
    frm1.pack()

    def change_entry():
        frm2.pack_forget()
        label1.pack_forget()
        text.pack_forget()
        frm4.pack_forget()
        if var1.get() == '1':
            entry1.pack()
            text1.pack_forget()
        elif var1.get() == '2':
            entry1.pack_forget()
            text1.pack()
        frm2.pack()
        label1.pack()
        text.pack()
        frm4.pack()

    var1 = tk.StringVar()
    var1.set('1')
    rb1 = tk.Radiobutton(frm1, text='摘要文件', font=mid_font, variable=var1, value='1', command=change_entry)
    rb1.pack(side='left', padx=15)
    rb2 = tk.Radiobutton(frm1, text='摘要文字', font=mid_font, variable=var1, value='2', command=change_entry)
    rb2.pack(side='right', padx=15)
    entry1 = tk.Entry(frm, font=mid_font, width=59)
    entry1.pack()
    text1 = tk.Text(frm, font=mid_font, width=59, height=10)
    hook_dropfiles(entry1, func=drag)

    def _reset():
        Tools.reset(entry1)
        Tools.reset(text1)
        Tools.reset(text)

    def process(*args):
        Tools.clean_all_widget(frm4)
        window.update()
        if var1.get() == '1':
            block_size = 33554432  # 每一次读取的长度为32mb
            hasher = hashlib.sha256()
            path = Tools.get_path_from_entry(entry1)
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, 'rb') as f:
                    fb = f.read(block_size)
                    while fb:
                        hasher.update(fb)
                        fb = f.read(block_size)
                digest = hasher.digest()
            else:
                messagebox.showerror(title='路径错误', message='文件路径不对哦')
                return 0
        else:
            digest = Tools.get_hash_digest_of_word(text1.get(1.0, 'end'))
        Tools.reset(text)
        text.insert('end', str(digest))
        # 获取完摘要后，就要进行保存
        global ind
        ind = (1 + ind) % 6
        current_path = os.getcwd()
        key_path = current_path + '\\keys'
        if not os.path.exists(key_path):
            os.mkdir(key_path)
        with open(key_path + '\\aes_key_digest.aes', 'wb') as f:
            f.write(digest)
        label3 = tk.Label(frm4, text='256位 AES 密钥已保存至：', font=mid_font, fg=colors[ind])
        label3.pack()
        entry2 = tk.Entry(frm4, width=59, font=mid_font)
        entry2.pack()
        entry2.insert('end', f'{key_path}')
        entry2.config(fg=colors[ind])
        label4 = tk.Label(frm4, text='中的 aes_key_digest.aes 文件内', font=mid_font, fg=colors[ind])
        label4.pack()
        label5 = tk.Label(frm4, text='注意：新生成的密钥会替换文件夹内同名的旧密钥', font=mid_font, fg='red')
        label5.pack()

        def open_dir():
            os.system(f'explorer {key_path}')

        button3 = tk.Button(frm4, text='打开密钥保存的文件夹', font=mid_font, command=open_dir)
        button3.pack()

    frm2 = tk.Frame(frm)
    frm2.pack()
    button1 = tk.Button(frm2, text='重置', font=mid_font, command=_reset)
    button1.pack(side='left', padx=15)
    button2 = tk.Button(frm2, text='确认', font=mid_font, command=process)
    button2.pack(side='right', padx=15)
    label1 = tk.Label(frm, text='摘要结果为：', font=mid_font)
    label1.pack()
    text = tk.Text(frm, font=mid_font, width=59, height=3)
    text.pack()
    frm4 = tk.Frame(frm)
    frm4.pack()


def create_aes_key(length):
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

    key = ''
    for i in range(length):
        key += _chr(randint(0, 94))
    label1 = tk.Label(frm, text=f'{length*8}位的密钥生成成功', font=mid_font)
    label1.pack()
    label2 = tk.Label(frm, text='密钥：' + str(key), font=mid_font)
    label2.pack()
    current_path = os.getcwd()
    key_path = current_path + '\\keys'
    if not os.path.exists(key_path):
        os.mkdir(key_path)
    with open(key_path + f'\\aes_key_{length*8}.aes', 'wb') as f:
        f.write(bytes(key, encoding='utf-8'))
    label3 = tk.Label(frm, text='密钥已经保存至', font=mid_font)
    label3.pack()
    entry1 = tk.Entry(frm, width=59, font=mid_font)
    entry1.pack()
    entry1.insert(0, key_path)
    label4 = tk.Label(frm, text=f'文件夹中的aes_key_{length*8}.aes文件内', font=mid_font)
    label4.pack()
    label5 = tk.Label(frm, text='注意：新生成的密钥会替换文件夹内同名的旧密钥', font=mid_font, fg='red')
    label5.pack()

    def open_dir():
        os.system(f'explorer {key_path}')

    button1 = tk.Button(frm, text='打开密钥保存的文件夹', font=mid_font, command=open_dir)
    button1.pack()


def aes_word():
    frm3 = tk.Frame(frm)
    frm3.pack()

    def change_entry1_show():
        Tools.change_entry_show(var2, entry1)

    def set_var2_to_0():
        var2.set("0")
        change_entry1_show()

    def set_var2_to_1():
        var2.set("1")
        change_entry1_show()

    def drag(files):
        Tools.dragged_files(files, entry1)

    var1 = tk.StringVar()
    var1.set('1')
    rb1 = tk.Radiobutton(frm3, text='拖入密钥文件：', variable=var1, value='1', font=mid_font, command=set_var2_to_0)
    rb1.grid(row=1, column=1, padx=5)
    rb2 = tk.Radiobutton(frm3, text='手动输入密钥：', variable=var1, value='2', font=mid_font, command=set_var2_to_1)
    rb2.grid(row=1, column=2, padx=5)
    var2 = tk.StringVar()
    var2.set('0')
    cb1 = tk.Checkbutton(frm3, text='隐藏', variable=var2, onvalue='1', offvalue='0', command=change_entry1_show,
                         font=mid_font)
    cb1.grid(row=1, column=3, padx=5)
    entry1 = tk.Entry(frm, font=mid_font, width=59)
    entry1.pack()
    hook_dropfiles(entry1, func=drag)
    frm1 = tk.Frame(frm)
    frm1.pack()
    label1 = tk.Label(frm1, text='模式：', font=mid_font)
    label1.grid(row=1, column=1, padx=10)
    mode = tk.StringVar()
    mode.set('CBC')
    option_menu1 = tk.OptionMenu(frm1, mode, *("CBC", "ECB"))
    option_menu1.config(font=mid_font)
    option_menu1.grid(row=1, column=2)
    label2 = tk.Label(frm1, text='填充方式：', font=mid_font)
    label2.grid(row=1, column=3, padx=10)
    padding = tk.StringVar()
    padding.set("pkcs7 padding")
    option_menu2 = tk.OptionMenu(frm1, padding, *('pkcs7 padding', "iso 10126 padding", 'zero padding'))
    option_menu2.config(font=mid_font)
    option_menu2.grid(row=1, column=4)
    label3 = tk.Label(frm1, text='请输入偏移量：（ECB模式不需要）', font=mid_font)
    label3.grid(row=1, column=5, padx=10)
    button1 = tk.Button(frm1, text='说明', bd=0, fg='blue', command=Tools.intro_iv, font=mid_font)
    button1.grid(row=1, column=6, padx=10)
    entry2 = tk.Entry(frm, width=59, font=mid_font)
    entry2.pack()
    base64_or_emoji_frm = tk.Frame(frm)
    base64_or_emoji_frm.pack()
    be_frm_label1 = tk.Label(base64_or_emoji_frm, text='请选择密文的编码方式：', font=mid_font)
    be_frm_label1.grid(row=1, column=1, padx=10)
    base64_or_emoji = tk.StringVar()
    base64_or_emoji.set('base64')
    base64_rb = tk.Radiobutton(base64_or_emoji_frm, text='base64编码', variable=base64_or_emoji, value='base64', font=mid_font)
    base64_rb.grid(row=1, column=2, padx=10)
    emoji_rb = tk.Radiobutton(base64_or_emoji_frm, text='emoji编码', variable=base64_or_emoji, value='emoji', font=mid_font)
    emoji_rb.grid(row=1, column=3, padx=10)
    intro_emoji_button = tk.Button(base64_or_emoji_frm, text='说明', font=mid_font, command=Tools.intro_emoji, bd=0, fg='blue')
    intro_emoji_button.grid(row=1, column=4, padx=10)
    frm_of_labelframe = tk.Frame(frm)
    frm_of_labelframe.pack()

    # 加密（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm_of_labelframe, text='AES加密文字', height=560, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    text1 = tk.Text(labelframe1, font=mid_font, width=43, height=9)
    text1.pack()

    def process(*args):
        if var3.get() == "0" and args:
            return 0
        Tools.reset(text2)
        window.update()
        # 先处理密钥
        aes = Tools.get_aes_key(var1, entry1, mode=mode.get(), iv=entry2.get())
        if aes == 0:
            return 0
        # 对文字进行处理
        ontology_sec = b''
        with open('_temp.txt', 'w', encoding='utf-8') as f:
            f.write(text1.get(1.0, 'end').rstrip('\n'))
        with open('_temp.txt', 'rb') as f:
            content = f.read(16)
            while content:
                if len(content) < 16:
                    if padding.get() == 'zero padding':
                        content = Tools.add_to_16(content)  # 使用自建的add_to_16（ZeroPadding）补充方式
                    elif padding.get() == 'iso 10126 padding':
                        content = Tools.iso_padding(content)  # 使用自建的 iso padding 模式
                    elif padding.get() == 'pkcs7 padding':
                        content = Tools.pkcs7_padding(content)
                en_text = aes.encrypt(content)
                ontology_sec += en_text
                content = f.read(16)
        os.remove('_temp.txt')
        text2.delete(1.0, 'end')
        res = base64.b64encode(ontology_sec).decode('utf-8')
        if base64_or_emoji.get() == 'base64':
            text2.insert('end', res)
        elif base64_or_emoji.get() == 'emoji':
            text2.insert('end', Tools.translate_base64_to_emoji(res))

    def reset():
        Tools.reset(text1)
        Tools.reset(text2)

    def copy_():
        Tools.copy(text2, button4)

    frm2 = tk.Frame(labelframe1)
    frm2.pack()
    var3 = tk.StringVar()
    var3.set('0')
    cb2 = tk.Checkbutton(frm2, font=mid_font, text='实时计算', variable=var3, onvalue='1', offvalue='0')
    cb2.grid(row=1, column=1, padx=15)
    button2 = tk.Button(frm2, font=mid_font, text='重置', command=reset)
    button2.grid(row=1, column=2, padx=15)
    button3 = tk.Button(frm2, font=mid_font, text='加密', command=process)
    button3.grid(row=1, column=3, padx=15)
    button4 = tk.Button(frm2, font=mid_font, text='复制密文', command=copy_, fg=colors[ind])
    button4.grid(row=1, column=4, padx=15)
    text2 = tk.Text(labelframe1, font=mid_font, width=43, height=9)
    text2.pack()
    text1.bind("<KeyRelease>", process)

    # 解密（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm_of_labelframe, text='AES解密文字', height=560, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变

    def reset2():
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)

    def copy2():
        Tools.copy(lf2_text2, lf2_button3)

    def decrypt(*args):
        if (live_cal.get() == '0' and args) or (not lf2_text1.get(1.0, 'end').replace('\n', '').replace(' ', '')):
            return 0
        Tools.reset(lf2_text2)
        window.update()
        # 先对密钥进行处理
        aes = Tools.get_aes_key(var1, entry1, mode=mode.get(), iv=entry2.get())
        if aes == 0:
            return 0
        # 再对文字进行处理
        info = lf2_text1.get(1.0, 'end').strip('\n')
        try:
            if base64_or_emoji.get() == 'base64':
                ontology_sec = base64.b64decode(info)
            elif base64_or_emoji.get() == 'emoji':
                ontology_sec = base64.b64decode(Tools.translate_emoji_to_base64(info))
        except Exception:
            if base64_or_emoji.get() == 'base64':
                messagebox.showerror(title='密文格式错误', message="不是正确的base64编码，密文是否为emoji编码？")
            elif base64_or_emoji.get() == 'emoji':
                messagebox.showerror(title='密文格式错误', message="无法将输入的emoji字符转为base64编码")
            return 0
        ontology = b''
        with open('_temp.txt', 'wb') as f:
            f.write(ontology_sec)
        with open('_temp.txt', 'rb') as f:
            content = f.read(16)
            while content:
                try:
                    de_text = aes.decrypt(content)
                except Exception:
                    messagebox.showerror(title='解密失败', message="解密失败，可能是密文信息被删改")
                    return 0
                else:
                    next = f.read(16)
                    if len(next) == 0:
                        de_text = Tools.de_padding(de_text, padding.get())
                    ontology += de_text
                    content = next
        os.remove('_temp.txt')
        try:
            ontology = ontology.decode('utf-8')
        except Exception as e:
            print('Error:', e)
            messagebox.showinfo(title='解密失败', message='密钥或密文可能不正确')
        else:
            lf2_text2.delete(1.0, 'end')
            lf2_text2.insert('end', str(ontology))

    lf2_text1 = tk.Text(labelframe2, font=mid_font, width=43, height=9)
    lf2_text1.pack()
    lf2_text1.bind('<KeyRelease>', decrypt)
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    live_cal = tk.StringVar()
    live_cal.set('1')
    lf2_cb1 = tk.Checkbutton(lf2_frm1, font=mid_font, text='实时计算', variable=live_cal, onvalue='1', offvalue='0')
    lf2_cb1.grid(row=1, column=1, padx=15)
    lf2_button1 = tk.Button(lf2_frm1, font=mid_font, text='重置', command=reset2)
    lf2_button1.grid(row=1, column=2, padx=15)
    lf2_button2 = tk.Button(lf2_frm1, font=mid_font, text='解密', command=decrypt)
    lf2_button2.grid(row=1, column=3, padx=15)
    lf2_button3 = tk.Button(lf2_frm1, font=mid_font, text='复制明文', command=copy2, fg=colors[ind])
    lf2_button3.grid(row=1, column=4, padx=15)
    lf2_text2 = tk.Text(labelframe2, width=43, height=9, font=mid_font)
    lf2_text2.pack()


def aes_file():
    frm3 = tk.Frame(frm)
    frm3.pack()

    def change_entry1_show():
        Tools.change_entry_show(var2, entry1)

    def _enter_length(*args):
        Tools.enter_length(_size, _entry1, _label1, frm4, zebra_frm, lf1_button3)

    def set_var2_to_0():
        var2.set("0")
        change_entry1_show()

    def set_var2_to_1():
        var2.set("1")
        change_entry1_show()

    def drag1(files):
        Tools.dragged_files(files, entry1)
        Tools.clean_all_widget(frm4)

    var1 = tk.StringVar()
    var1.set('1')
    rb1 = tk.Radiobutton(frm3, text='拖入密钥文件：', variable=var1, value='1', font=mid_font, command=set_var2_to_0)
    rb1.grid(row=1, column=1, padx=5)
    rb2 = tk.Radiobutton(frm3, text='手动输入密钥：', variable=var1, value='2', font=mid_font, command=set_var2_to_1)
    rb2.grid(row=1, column=2, padx=5)
    var2 = tk.StringVar()
    var2.set('0')
    cb1 = tk.Checkbutton(frm3, text='隐藏', variable=var2, onvalue='1', offvalue='0', command=change_entry1_show,
                         font=mid_font)
    cb1.grid(row=1, column=3, padx=5)
    entry1 = tk.Entry(frm, font=mid_font, width=59)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)
    frm5 = tk.Frame(frm)
    frm5.pack()
    label7 = tk.Label(frm5, text='模式:', font=mid_font)
    label7.grid(row=1, column=1, padx=10)
    _mode = tk.StringVar()
    _mode.set("CBC")
    option_menu1 = tk.OptionMenu(frm5, _mode, *("CBC", "ECB"))
    option_menu1.config(font=mid_font)
    option_menu1.grid(row=1, column=2)
    label8 = tk.Label(frm5, text='填充方式:', font=mid_font)
    label8.grid(row=1, column=3, padx=10)
    _padding = tk.StringVar()
    _padding.set("pkcs7 padding")
    option_menu2 = tk.OptionMenu(frm5, _padding, *('pkcs7 padding', "iso 10126 padding", 'zero padding'))
    option_menu2.config(font=mid_font)
    option_menu2.grid(row=1, column=4)
    label3 = tk.Label(frm5, text='请输入偏移量：（ECB模式不需要）', font=mid_font)
    label3.grid(row=1, column=5, padx=10)
    button3 = tk.Button(frm5, text='说明', font=mid_font, bd=0, fg='blue', command=Tools.intro_iv)
    button3.grid(row=1, column=6, padx=10)
    entry3 = tk.Entry(frm, font=mid_font, width=59)
    entry3.pack()
    frm_of_labelframe = tk.Frame(frm)
    frm_of_labelframe.pack()

    # 加密（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm_of_labelframe, text='AES加密文件（夹）', height=606, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def drag2(files):
        Tools.dragged_files(files, lf1_entry2)
        Tools.clean_all_widget(frm4)

    lf1_label2 = tk.Label(labelframe1, text='请拖入需要加密的文件（夹）或输入地址：', font=mid_font)
    lf1_label2.pack()
    lf1_entry2 = tk.Entry(labelframe1, show=None, width=43, font=mid_font)
    lf1_entry2.pack()
    hook_dropfiles(lf1_entry2, func=drag2)
    delete_origin = tk.StringVar()
    delete_origin.set('0')
    delete_origin_cb = tk.Checkbutton(labelframe1, text='加密完后删除原文件', font=mid_font, variable=delete_origin, onvalue='1', offvalue='0')
    delete_origin_cb.pack()
    _frm7 = tk.Frame(labelframe1)
    _frm7.pack()
    frm7 = tk.Frame(_frm7)
    frm7.pack()
    lf1_label6 = tk.Label(frm7, text="请选择加密的大小：", font=mid_font)
    lf1_label6.grid(row=1, column=1)
    _size = tk.StringVar()
    _size.set("完整文件")
    option_menu3 = tk.OptionMenu(frm7, _size, *("完整文件", "1单位", "10单位", "516单位", "5160单位", "其他长度", "斑马线加密法"),
                                 command=_enter_length)
    option_menu3.config(font=mid_font)
    option_menu3.grid(row=1, column=2)
    _entry1 = tk.Entry(frm7, width=5, font=mid_font)
    _label1 = tk.Label(frm7, text='单位', font=mid_font)
    intro_button = tk.Button(frm7, text="说明", font=mid_font, command=Tools.intro_enc_head, bd=0, fg='blue')
    intro_button.grid(row=1, column=5)
    zebra_frm = tk.Frame(_frm7)
    zfrm1 = tk.Frame(zebra_frm)
    zfrm1.grid(row=1)
    zlabel1 = tk.Label(zfrm1, text='位置的显示方式：', font=mid_font)
    zlabel1.grid(row=1, column=1, padx=10)
    show_method = tk.StringVar()
    show_method.set('1')

    def change_show_method():
        zentry1.delete(0, 'end')
        zentry4.delete(0, 'end')
        if show_method.get() == '2':
            zlabel3.config(text=' kb ')
            zlabel7.config(text=' kb ')
            zscale1.grid_forget()
            zscale2.grid_forget()
        elif show_method.get() == '1':
            zlabel3.config(text=' %  ')
            zlabel7.config(text='%')
            begin.set(0)
            end.set(100)
            zentry1.insert('end', '0')
            zentry4.insert('end', '100')
            zscale1.grid(row=3)
            zscale2.grid(row=5)

    def change_zentry1(value):
        Tools.change_zentry(value, zentry1)

    def change_zentry4(value):
        Tools.change_zentry(value, zentry4)

    def change_zscale1(*args):
        Tools.change_zscale(show_method, zentry1, begin)

    def change_zscale2(*args):
        Tools.change_zscale(show_method, zentry4, end)

    zrb1 = tk.Radiobutton(zfrm1, text='百分比', font=mid_font, variable=show_method, value='1', command=change_show_method)
    zrb1.grid(row=1, column=2, padx=10)
    zrb2 = tk.Radiobutton(zfrm1, text='绝对值', font=mid_font, variable=show_method, value='2', command=change_show_method)
    zrb2.grid(row=1, column=3, padx=10)
    zfrm2 = tk.Frame(zebra_frm)
    zfrm2.grid(row=2)
    zlabel2 = tk.Label(zfrm2, text='第一根黑线的起始位置：  ', font=mid_font)
    zlabel2.grid(row=1, column=1)
    zentry1 = tk.Entry(zfrm2, width=5, font=mid_font)
    zentry1.grid(row=1, column=2)
    zentry1.insert('end', '0')
    zentry1.bind('<KeyRelease>', change_zscale1)
    zlabel3 = tk.Label(zfrm2, text=' %  ', font=mid_font)
    zlabel3.grid(row=1, column=3)
    begin = tk.IntVar()
    begin.set(0)
    zscale1 = tk.Scale(zebra_frm, from_=0, to=100, orient=tk.HORIZONTAL, length=400, tickinterval=10, resolution=1,
                       showvalue=0, variable=begin, command=change_zentry1)
    zscale1.grid(row=3)
    zfrm4 = tk.Frame(zebra_frm)
    zfrm4.grid(row=4)
    zlabel4 = tk.Label(zfrm4, text='黑线的宽度：            ', font=mid_font)
    zlabel4.grid(row=1, column=1)
    zentry2 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry2.grid(row=1, column=2)
    zlabel8 = tk.Label(zfrm4, text='单位', font=mid_font)
    zlabel8.grid(row=1, column=3)
    zlabel5 = tk.Label(zfrm4, text='黑线的根数：            ', font=mid_font)
    zlabel5.grid(row=2, column=1)
    zentry3 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry3.grid(row=2, column=2)
    zlabel9 = tk.Label(zfrm4, text='根', font=mid_font)
    zlabel9.grid(row=2, column=3)
    zlabel6 = tk.Label(zfrm4, text='最后一根黑线的末尾位置：', font=mid_font)
    zlabel6.grid(row=3, column=1)
    zentry4 = tk.Entry(zfrm4, width=5, font=mid_font)
    zentry4.grid(row=3, column=2)
    zentry4.insert('end', '100')
    zentry4.bind('<KeyRelease>', change_zscale2)
    zlabel7 = tk.Label(zfrm4, text=' %  ', font=mid_font)
    zlabel7.grid(row=3, column=3)
    end = tk.IntVar()
    end.set(100)
    zscale2 = tk.Scale(zebra_frm, from_=0, to=100, orient=tk.HORIZONTAL, length=400, tickinterval=10, resolution=1,
                       showvalue=0, variable=end, command=change_zentry4)
    zscale2.grid(row=5)

    def process():
        Tools.clean_all_widget(frm4)
        # 先处理密钥
        aes = Tools.get_aes_key(var1, entry1, mode=_mode.get(), iv=entry3.get())
        if aes == 0:
            return 0
        # 再判断要加密的文件（夹）是否存在
        ontology_path = Tools.get_path_from_entry(lf1_entry2)
        if not os.path.exists(ontology_path):
            tk.messagebox.showerror(title='路径错误', message='待加密的文件地址不正确，请重新输入')
            return 0
        # 为了防止在运行过程中，用户改变_size的值，这里需要先固定这个值
        size = Tools.get_correct_size(_size, _entry1)
        if size == 0:
            return 0
        _begin, width, number, _end = Tools.get_correct_zebra_parameter(size, show_method, zentry1, zentry2, zentry3, zentry4)
        if _begin is False:
            return 0
        _var1 = tk.StringVar()  # 用来保存密钥的类型
        _var1.set(var1.get())
        hidden_entry1 = tk.Entry(frm)  # 用来保存密钥
        hidden_entry1.insert('end', entry1.get())
        mode = _mode.get()
        iv = entry3.get()
        padding = _padding.get()
        setting_of_delete_origin = delete_origin.get()
        if os.path.isfile(ontology_path):
            label5 = tk.Label(frm4, font=mid_font, text='处理时间可能会较长，请耐心等待')
            label5.pack()
            window.update()
            label5.destroy()
            # 再处理要加密的文件
            base, suffix = os.path.splitext(ontology_path)
            ontology_sec_path = base + '_AES_Encrypted' + suffix
            Tools.aes_enc_file(aes, padding, ontology_path, ontology_sec_path, size, _begin, width, number, _end)
            if setting_of_delete_origin == '1':
                Tools.delete_file(ontology_path)
                label9 = tk.Label(frm4, text='加密成功并已删除原文件，\n文件保存至原文件所在文件夹中的', font=mid_font)
            else:
                label9 = tk.Label(frm4, text='加密成功，文件保存至原文件所在文件夹中的', font=mid_font)
            label9.pack()
            entry4 = tk.Entry(frm4, width=43, font=mid_font)
            entry4.insert('end', os.path.basename(ontology_sec_path))
            entry4.pack()
        elif os.path.isdir(ontology_path):
            # 定义进度条
            progress_bar = ttk.Progressbar(frm4)
            progress_bar['length'] = 200
            progress_bar['value'] = 0
            files = os.listdir(ontology_path)
            out_dir = os.path.join(ontology_path, 'AES_Encrypted')
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            cleaned_files = []  # 只将files里的纯文件的绝对路径保存到这里，其他的，比如文件夹会删掉
            for file in files:
                file_path = os.path.join(ontology_path, file)
                if os.path.isfile(file_path):
                    cleaned_files.append(file_path)
            progress_bar['maximum'] = len(cleaned_files)  # 这里定义进度条的总长度
            progress_bar.pack(pady=10)  # 再放置进度条
            window.update()  # 这里的窗口更新很重要，因为如果第一个文件处理完了再更新窗口，用户会觉得卡顿
            for file_path in cleaned_files:
                out_path = os.path.join(out_dir, os.path.basename(file_path))
                Tools.aes_enc_file(aes, padding, file_path, out_path, size, _begin, width, number, _end)
                # 每次加密完后都需要重新设定aes
                aes = Tools.get_aes_key(_var1, hidden_entry1, mode=mode, iv=iv)
                if setting_of_delete_origin == '1':
                    Tools.delete_file(file_path)
                progress_bar['value'] += 1
                window.update()
            if setting_of_delete_origin == '1':
                label9 = tk.Label(frm4, text='加密成功并已删除原文件，文件保存至\n原文件夹中新建的 AES_Encrypted 文件夹中', font=mid_font)
            else:
                label9 = tk.Label(frm4, text='加密成功，文件保存至原文件夹中\n新建的 AES_Encrypted 文件夹中', font=mid_font)
            label9.pack()
        else:
            tk.messagebox.showerror(title='路径错误', message='待加密的文件（夹）地址不正确，请重新输入')
            return 0

    def _reset():
        Tools.reset(lf1_entry2)
        Tools.clean_all_widget(frm4)

    frm2 = tk.Frame(labelframe1)
    frm2.pack()
    lf1_button1 = tk.Button(frm2, font=mid_font, text='重置', command=_reset)
    lf1_button1.grid(row=1, column=1, padx=20)
    lf1_button2 = tk.Button(frm2, font=mid_font, text='加密', command=process)
    lf1_button2.grid(row=1, column=2, padx=20)
    lf1_button3 = tk.Button(frm2, text='设置', font=mid_font, command=Tools.setting, fg='blue', bd=0)
    frm4 = tk.Frame(labelframe1)
    frm4.pack()

    # 解密（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm_of_labelframe, text='AES解密文件（夹）', height=606, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变

    def lf2_drag1(files):
        Tools.dragged_files(files, lf2_entry2)
        Tools.clean_all_widget(lf2_frm4)

    def decrypt():
        Tools.clean_all_widget(lf2_frm4)
        # 先处理密钥
        aes = Tools.get_aes_key(var1, entry1, mode=_mode.get(), iv=entry3.get())
        if aes == 0:
            return 0
        # 再处理要解密的文件
        ontology_sec_path = Tools.get_path_from_entry(lf2_entry2)
        if not os.path.exists(ontology_sec_path):
            tk.messagebox.showerror(title='路径错误', message='待解密的文件地址不正确，请重新输入')
            return 0
        # 为了防止在运行过程中，用户改变var1, entry1, ...的值，所以这里就需要先固定住这两个值
        setting_of_delete_sec = delete_sec.get()
        _var1 = tk.StringVar()  # 保存密钥的类型
        _var1.set(var1.get())
        _var3 = tk.StringVar()  # 保存是否是临时解密
        _var3.set(lf2_var1.get())
        hidden_entry = tk.Entry(frm)  # 保存密钥
        hidden_entry.delete(0, 'end')
        hidden_entry.insert('end', entry1.get())
        mode = _mode.get()
        iv = entry3.get()
        padding = _padding.get()
        if os.path.isfile(ontology_sec_path):
            lf2_label3 = tk.Label(lf2_frm4, text='处理时间可能会较长，请耐心等待', font=mid_font)
            lf2_label3.pack()
            window.update()
            lf2_label3.destroy()
            # 再处理解密的文件
            base, suffix = os.path.splitext(ontology_sec_path)
            if _var3.get() == '1':
                ontology_path = base + '_AES_Decrypted' + suffix
            elif _var3.get() == '2':
                ontology_path = base + '_temp' + suffix
            process_succeed = Tools.aes_dec_file(aes, padding, ontology_sec_path, ontology_path)
            if process_succeed:
                if setting_of_delete_sec == '1':
                    Tools.delete_file(ontology_sec_path)
                    lf2_label4 = tk.Label(lf2_frm4, text='解密成功并已删除密文文件，\n文件保存至原文件所在文件夹中的', font=mid_font)
                else:
                    lf2_label4 = tk.Label(lf2_frm4, text='解密成功，文件保存至原文件所在文件夹中的', font=mid_font)
                lf2_label4.pack()
                lf2_entry3 = tk.Entry(lf2_frm4, width=43, font=mid_font)
                lf2_entry3.insert('end', os.path.basename(ontology_path))
                lf2_entry3.pack()
                if _var3.get() == '2':

                    def save():
                        answer = messagebox.askyesno(title='提示', message='请确认修改内容已保存，并且临时文件名称没有修改')
                        if answer:
                            if os.path.exists(ontology_path):
                                lf2_label9 = tk.Label(lf2_frm4, text='处理时间可能会较长，请耐心等待', font=mid_font)
                                lf2_label9.pack()
                                window.update()
                                lf2_label9.destroy()
                                # 这里需要重新新建一个aes
                                aes = Tools.get_aes_key(_var1, hidden_entry, mode=mode, iv=iv)
                                Tools.aes_enc_file(aes, padding, ontology_path, ontology_sec_path)
                                lf2_label10 = tk.Label(lf2_frm4, text='加密成功，文件保存至原文件所在文件夹中的', font=mid_font)
                                lf2_label10.pack()
                                lf2_entry4 = tk.Entry(lf2_frm4, width=43, font=mid_font)
                                lf2_entry4.pack()
                                lf2_entry4.insert('end', os.path.basename(ontology_sec_path))
                                os.remove(ontology_path)
                            else:
                                messagebox.showerror(title='路径错误', message='找不到临时文件了')

                    lf2_button4 = tk.Button(lf2_frm4, text='重新加密', font=mid_font, command=save)
                    lf2_button4.pack()
                elif _var3.get() == '1':

                    def _remove():
                        Tools.remove_file_or_dir(ontology_path, lf2_frm8)

                    lf2_frm7 = tk.Frame(lf2_frm4)
                    lf2_frm7.pack()
                    destroy_button = tk.Button(lf2_frm7, text='阅后即焚', font=mid_font, command=_remove)
                    destroy_button.grid(row=1, column=1, padx=10)
                    intro_destroy_button = tk.Button(lf2_frm7, text='说明', font=mid_font, fg='blue', bd=0,
                                                     command=Tools.intro_destroy)
                    intro_destroy_button.grid(row=1, column=2, padx=10)
                    lf2_frm8 = tk.Frame(lf2_frm4)
                    lf2_frm8.pack()
            else:
                os.remove(ontology_path)  # 这里不需要弹窗报错了，因为_aes_dec_file函数中已经报错了
        elif os.path.isdir(ontology_sec_path):
            # 定义进度条
            progress_bar = ttk.Progressbar(lf2_frm4)
            progress_bar['length'] = 200
            progress_bar['value'] = 0
            files = os.listdir(ontology_sec_path)
            if _var3.get() == '1':
                out_dir = os.path.join(ontology_sec_path, 'AES_Decrypted')
            elif _var3.get() == '2':
                out_dir = os.path.join(ontology_sec_path, 'temp')
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            cleaned_files = []  # 只将files里的纯文件的绝对路径保存到这里，其他的比如文件夹会删掉
            for file in files:
                file_path = os.path.join(ontology_sec_path, file)
                if os.path.isfile(file_path):
                    cleaned_files.append(file_path)
            progress_bar['maximum'] = len(cleaned_files)  # 这里定义进度条的总长度
            progress_bar.pack(pady=10)  # 再放置进度条
            window.update()
            failed_files = []
            for file_path in cleaned_files:
                out_path = os.path.join(out_dir, os.path.basename(file_path))
                process_success = Tools.aes_dec_file(aes, padding, file_path, out_path, show_error=False)
                # 每次解密完后都需要重新设定aes
                aes = Tools.get_aes_key(_var1, hidden_entry, mode=mode, iv=iv)
                if not process_success:
                    os.remove(out_path)
                    failed_files.append(os.path.basename(file_path))
                else:
                    if setting_of_delete_sec == '1':
                        Tools.delete_file(file_path)
                progress_bar['value'] += 1
                window.update()
            if _var3.get() == '1':
                lf2_label5 = tk.Label(lf2_frm4, text='解密完成，文件保存至\n原文件夹中新建的 AES_Decrypted 文件夹中', font=mid_font)
            elif _var3.get() == '2':
                lf2_label5 = tk.Label(lf2_frm4, text='解密完成，文件保存至\n原文件夹中新建的 temp 文件夹中', font=mid_font)
            lf2_label5.pack()
            if failed_files:
                lf2_text = tk.Text(lf2_frm4, width=43, font=mid_font, height=6)
                lf2_text.insert('end', f'其中，{len(failed_files)}个文件解密失败，分别为：\n' + '\n'.join(failed_files))
                lf2_text.pack()
            if _var3.get() == '2':

                def save():
                    answer = messagebox.askyesno(title='提示', message='请确认修改内容已保存，并且临时文件名称没有修改')
                    if answer:
                        if os.path.exists(out_dir):
                            # 定义进度条
                            progress_bar2 = ttk.Progressbar(lf2_frm4)
                            progress_bar2['length'] = 200
                            progress_bar2['value'] = 0
                            files2 = os.listdir(out_dir)
                            cleaned_files2 = []
                            for file2 in files2:
                                file_path2 = os.path.join(out_dir, file2)
                                if os.path.isfile(file_path2):
                                    cleaned_files2.append(file_path2)
                            if len(cleaned_files2) == 0:
                                progress_bar2['maximum'] = 1
                                progress_bar2['value'] = 1
                            else:
                                progress_bar2['maximum'] = len(cleaned_files2)  # 这里定义进度条的总长度
                            progress_bar2.pack(pady=10)  # 再放置进度条
                            window.update()
                            for file_path2 in cleaned_files2:
                                origin_path = os.path.join(ontology_sec_path, os.path.basename(file_path2))
                                # 每次加密前都需要重新设定aes
                                aes = Tools.get_aes_key(_var1, hidden_entry, mode=mode, iv=iv)
                                Tools.aes_enc_file(aes, padding, file_path2, origin_path)
                                progress_bar2['value'] += 1
                                window.update()
                            lf2_label6 = tk.Label(lf2_frm4, text='已重新加密回原文件夹', font=mid_font)
                            lf2_label6.pack()
                            shutil.rmtree(out_dir)
                        else:
                            messagebox.showerror(title='路径错误', message='找不到临时文件夹了')

                lf2_button4 = tk.Button(lf2_frm4, text='重新加密', font=mid_font, command=save)
                lf2_button4.pack()

            elif _var3.get() == '1':

                def _remove():
                    Tools.remove_file_or_dir(out_dir, lf2_frm6)

                lf2_frm5 = tk.Frame(lf2_frm4)
                lf2_frm5.pack()
                destroy_button = tk.Button(lf2_frm5, text='阅后即焚', font=mid_font, command=_remove)
                destroy_button.grid(row=1, column=1, padx=10)
                intro_destroy_button = tk.Button(lf2_frm5, text='说明', font=mid_font, fg='blue', bd=0,
                                                 command=Tools.intro_destroy)
                intro_destroy_button.grid(row=1, column=2, padx=10)
                lf2_frm6 = tk.Frame(lf2_frm4)
                lf2_frm6.pack()
        else:
            tk.messagebox.showerror(title='路径错误', message='待解密的文件（夹）地址不正确，请重新输入')
            return 0

    def lf2_reset():
        Tools.reset(lf2_entry2)
        Tools.clean_all_widget(lf2_frm4)

    def tell_difference():
        tell_window = tk.Toplevel(window)
        tell_window.geometry('636x758')
        tell_window.title('说明')
        tell_window.iconbitmap(icon_path)
        tw_text = tk.Text(tell_window, width=46, height=28, font=mid_font)
        tw_text.pack()
        word = '''    1. 如果你仅需要浏览解密后的内容，使用普通解密功能即可，在解密完成后，可以使用阅后即焚功能，来删除解密的文件，这样删除的文件不会在回收站内被找到。

    2. 如果你需要编辑解密后的内容，并在编辑完成后，快速实现重新加密，建议使用临时解密功能，修改后的文件会取代被修改前的文件。
注意：临时文件的文件名需要保持原样。以及重新加密的方法是全文加密。'''
        tw_text.insert('end', word)

    lf2_label2 = tk.Label(labelframe2, text='请拖入需要解密的文件（夹）或输入地址：', font=mid_font)
    lf2_label2.pack()
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry2.pack()
    hook_dropfiles(lf2_entry2, func=lf2_drag1)
    delete_sec = tk.StringVar()
    delete_sec.set('0')
    delete_sec_cb = tk.Checkbutton(labelframe2, text='解密完后删除密文文件', font=mid_font, variable=delete_sec, onvalue='1',
                                   offvalue='0')
    delete_sec_cb.pack()
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_var1 = tk.StringVar()
    lf2_var1.set('1')
    lf2_rb1 = tk.Radiobutton(lf2_frm1, text='普通解密', font=mid_font, variable=lf2_var1, value='1')
    lf2_rb1.grid(row=1, column=1, padx=15)
    lf2_rb2 = tk.Radiobutton(lf2_frm1, text='临时解密', font=mid_font, variable=lf2_var1, value='2')
    lf2_rb2.grid(row=1, column=2, padx=15)
    lf2_button1 = tk.Button(lf2_frm1, text='说明', font=mid_font, fg='blue', bd=0, command=tell_difference)
    lf2_button1.grid(row=1, column=3, padx=15)
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_button2 = tk.Button(lf2_frm2, font=mid_font, text='重置', command=lf2_reset)
    lf2_button2.grid(row=1, column=1, padx=20)
    lf2_button3 = tk.Button(lf2_frm2, font=mid_font, text='解密', command=decrypt)
    lf2_button3.grid(row=1, column=2, padx=20)
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_frm4.pack()


def create_ckks_key():
    frm_of_labelframe = tk.Frame(frm)
    frm_of_labelframe.pack()
    # 随机生成CKKS同态加密对称加密密钥
    labelframe1 = tk.LabelFrame(frm_of_labelframe, text='随机生成CKKS同态加密对称加密密钥', height=457, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    label1 = tk.Label(labelframe1, text='请选择全局缩放因子的大小\n值越大精度越高，但计算消耗更大：', font=mid_font)
    label1.pack()

    def start(*args):
        Tools.clean_all_widget(frm3)
        global_scale = var1.get()
        label2 = tk.Label(frm3, text='程序正在进行中，请稍候...', font=mid_font)
        label2.pack()
        window.update()
        label2.destroy()
        # 生成对称密钥（把公钥和私钥合在一起）
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        context.generate_galois_keys()
        context.global_scale = 2 ** global_scale
        # 由于ckks的密钥太长，所以用base85编码，这样比base64编码更节约空间
        serialized_context = base64.b85encode(context.serialize(save_public_key=True, save_secret_key=True,
                                                                save_galois_keys=True, save_relin_keys=True))
        label3 = tk.Label(frm3, text='密钥生成成功', font=mid_font)
        label3.pack()
        label4 = tk.Label(frm3, text='密钥：' + serialized_context[:5].decode() + '...' + serialized_context[-20:].decode(), font=mid_font)
        label4.pack()
        # 对称加密的密钥文件头和文件尾为：-----BEGIN CKKS KEY-----; -----END CKKS KEY-----
        key = b'-----BEGIN CKKS KEY-----\n' + serialized_context + b'\n-----END CKKS KEY-----'
        current_path = os.getcwd()
        key_path = current_path + '\\keys'
        if not os.path.exists(key_path):
            os.mkdir(key_path)
        with open(key_path + f'\\CKKS_key_{global_scale}.he', 'wb') as f:
            f.write(key)
        label5 = tk.Label(frm3, text='密钥已经保存至', font=mid_font)
        label5.pack()
        entry1 = tk.Entry(frm3, width=43, font=mid_font)
        entry1.pack()
        entry1.insert(0, key_path)
        label6 = tk.Label(frm3, text=f'文件夹中的CKKS_key_{global_scale}.he文件内', font=mid_font)
        label6.pack()
        label7 = tk.Label(frm3, text='注意：新生成的密钥会替换文件夹内同名的旧密钥', font=mid_font, fg='red')
        label7.pack()

    var1 = tk.IntVar()
    var1.set(30)
    rb2 = tk.Radiobutton(labelframe1, variable=var1, text='2^30（兼顾精度与速度）', font=mid_font, value=30)
    rb2.pack()
    button1 = tk.Button(labelframe1, text='开始生成', font=mid_font, command=start)
    button1.pack()
    frm3 = tk.Frame(labelframe1)
    frm3.pack()

    # 随机生成CKKS同态加密非对称加密密钥
    labelframe2 = tk.LabelFrame(frm_of_labelframe, text='随机生成CKKS同态加密非对称加密密钥', height=457, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变

    lf2_label2 = tk.Label(labelframe2, text='请选择全局缩放因子的大小\n值越大精度越高，但计算消耗更大：', font=mid_font)
    lf2_label2.pack()

    def lf2_start(*args):
        Tools.clean_all_widget(lf2_frm3)
        global_scale = lf2_var1.get()
        label2 = tk.Label(lf2_frm3, text='程序正在进行中，请稍候...', font=mid_font)
        label2.pack()
        window.update()
        label2.destroy()
        # 生成非对称密钥
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        context.generate_galois_keys()
        context.global_scale = 2 ** global_scale
        # 由于ckks的密钥太长，所以用base85编码，这样比base64编码更节约空间
        serialized_pk = base64.b85encode(context.serialize(save_public_key=True, save_secret_key=False,
                                                                save_galois_keys=True, save_relin_keys=True))
        serialized_sk = base64.b85encode(context.serialize(save_public_key=False, save_secret_key=True,
                                                           save_galois_keys=True, save_relin_keys=True))
        label3 = tk.Label(lf2_frm3, text='密钥生成成功', font=mid_font)
        label3.pack()
        label_pk = tk.Label(lf2_frm3, text='公钥：' + serialized_pk[:5].decode() + '...' + serialized_pk[-20:].decode(), font=mid_font)
        label_pk.pack()
        label_sk = tk.Label(lf2_frm3, text='私钥：' + serialized_sk[:5].decode() + '...' + serialized_sk[-20:].decode(), font=mid_font)
        label_sk.pack()
        # 公钥文件头和文件尾为：-----BEGIN CKKS KEY-----; -----END CKKS KEY-----
        pk = b'-----BEGIN CKKS PUBLIC KEY-----\n' + serialized_pk + b'\n-----END CKKS PUBLIC KEY-----'
        sk = b'-----BEGIN CKKS PRIVATE KEY-----\n' + serialized_sk + b'\n-----END CKKS PRIVATE KEY-----'
        current_path = os.getcwd()
        key_path = current_path + '\\keys'
        if not os.path.exists(key_path):
            os.mkdir(key_path)
        with open(key_path + f'\\CKKS_public_key_{global_scale}.hepk', 'wb') as pkf, open(key_path + f'\\CKKS_private_key_{global_scale}.hesk', 'wb') as skf:
            pkf.write(pk)
            skf.write(sk)
        label5 = tk.Label(lf2_frm3, text='密钥已经保存至', font=mid_font)
        label5.pack()
        entry1 = tk.Entry(lf2_frm3, width=43, font=mid_font)
        entry1.pack()
        entry1.insert(0, key_path)
        label6 = tk.Label(lf2_frm3, text=f'文件夹中的.hepk和.hesk文件内', font=mid_font)
        label6.pack()
        label7 = tk.Label(lf2_frm3, text='注意：新生成的密钥会替换文件夹内同名的旧密钥', font=mid_font, fg='red')
        label7.pack()

    lf2_var1 = tk.IntVar()
    lf2_var1.set(30)
    lf2_rb2 = tk.Radiobutton(labelframe2, variable=lf2_var1, text='2^30（兼顾精度与速度）', font=mid_font, value=30)
    lf2_rb2.pack()
    lf2_button1 = tk.Button(labelframe2, text='开始生成', font=mid_font, command=lf2_start)
    lf2_button1.pack()
    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()

    def open_dir():
        keys_dir_path = os.path.join(os.getcwd(), 'keys')
        if not os.path.exists(keys_dir_path):
            os.mkdir(keys_dir_path)
        os.system(f"explorer {os.path.join(os.getcwd(), 'keys')}")

    open_dir_button = tk.Button(frm, text='打开密钥保存的文件夹', font=mid_font, command=open_dir)
    open_dir_button.pack()


def set_pwd_of_ckks_privkey():
    # 添加密码或去除密码（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='为CKKS私钥添加或去除使用密码', height=741, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()

    def change_lf1_entry1_show():
        Tools.change_entry_show(lf1_var1, lf1_entry1)

    def change_lf1_entry2_show():
        Tools.change_entry_show(lf1_var2, lf1_entry2)

    def lf1_confirm():
        lf1_label4.config(text='   ')
        lf1_text1.config(state='normal')
        Tools.reset(lf1_text1)
        key_path = Tools.get_path_from_entry(lf1_entry1)
        if os.path.exists(key_path):
            with open(Tools.get_path_from_entry(lf1_entry1), 'r', encoding='utf-8') as f:
                key = f.read()
                if "-----BEGIN CKKS PRIVATE KEY-----" in key:
                    lf1_text1.insert('end', '\n'.join([key[:500], '由于私钥过长，部分已省略', "-----END CKKS PRIVATE KEY-----"]))
                else:
                    lf1_text1.insert('end', '这不是正确的私钥')
        else:
            lf1_text1.insert('end', '私钥地址错误')
        lf1_text1.config(state='disabled')

    def lf1_drag(files):
        Tools.dragged_files(files, lf1_entry1)
        lf1_confirm()

    def lf1_reset():
        Tools.reset(lf1_entry1)
        Tools.reset(lf1_entry2)
        lf1_text1.config(state='normal')
        Tools.reset(lf1_text1)
        lf1_text1.config(state='disabled')
        lf1_label4.config(text='   ')

    lf1_label1 = tk.Label(lf1_frm1, text='请拖入您的私钥或输入地址：', font=mid_font)
    lf1_label1.grid(row=1, column=1, padx=5)
    lf1_var1 = tk.StringVar()
    lf1_var1.set('0')
    lf1_cb1 = tk.Checkbutton(lf1_frm1, text='隐藏', font=mid_font, variable=lf1_var1, onvalue='1', offvalue='0',
                             command=change_lf1_entry1_show)
    lf1_cb1.grid(row=1, column=2, padx=5)
    lf1_entry1 = tk.Entry(labelframe1, width=43, font=mid_font)
    lf1_entry1.pack()
    hook_dropfiles(lf1_entry1, func=lf1_drag)
    lf1_frm3 = tk.Frame(labelframe1)
    lf1_frm3.pack()
    lf1_button3 = tk.Button(lf1_frm3, text='重置', font=mid_font, command=lf1_reset)
    lf1_button3.grid(row=1, column=1, padx=20)
    lf1_button4 = tk.Button(lf1_frm3, text='确定', font=mid_font, command=lf1_confirm)
    lf1_button4.grid(row=1, column=2, padx=20)
    lf1_label2 = tk.Label(labelframe1, text='该私钥的内容为：', font=mid_font)
    lf1_label2.pack()
    lf1_text1 = tk.Text(labelframe1, width=43, height=16, font=mid_font, state='disabled')
    lf1_text1.pack()
    lf1_frm4 = tk.Frame(labelframe1)
    lf1_frm4.pack()
    lf1_label3 = tk.Label(lf1_frm4, text='请输入私钥的使用密码：', font=mid_font)
    lf1_label3.grid(row=1, column=1, padx=5)
    lf1_var2 = tk.StringVar()
    lf1_var2.set('1')
    lf1_cb2 = tk.Checkbutton(lf1_frm4, text='隐藏', font=mid_font, variable=lf1_var2, onvalue='1', offvalue='0',
                             command=change_lf1_entry2_show)
    lf1_cb2.grid(row=1, column=2, padx=5)
    lf1_entry2 = tk.Entry(labelframe1, width=43, font=mid_font, show='*')
    lf1_entry2.pack()
    lf1_frm2 = tk.Frame(labelframe1)
    lf1_frm2.pack()

    def encrypt():
        global ind
        lf1_confirm()
        ind = (ind + 1) % 6
        lf1_label4.config(fg=colors[ind])
        lf1_text1.config(state='normal')
        if lf1_text1.get(1.0, 'end').strip('\n') == '这不是正确的私钥' or lf1_text1.get(1.0, 'end').strip('\n') == '私钥地址错误':
            lf1_text1.config(state='disabled')
            lf1_label4.config(text='无法加密')
            return 0
        elif not lf1_entry2.get().strip(' '):
            lf1_label4.config(text='密码不能为空')
            return 0
        else:
            with open(Tools.get_path_from_entry(lf1_entry1), 'r', encoding='utf-8') as f:
                privkey = f.read()
            enc_key = Tools.encrypt_privkey(privkey.encode('utf-8'), lf1_entry2.get(), is_ckks=True)
            if enc_key == b'':
                lf1_label4.config(text='已经加密过，无法再次加密')
                return 0
            with open(Tools.get_path_from_entry(lf1_entry1), 'wb') as f:
                f.write(enc_key)
            lf1_label4.config(text='加密成功')
            lf1_text1.config(state='normal')
            Tools.reset(lf1_text1)
            lf1_text1.insert('end', '\n'.join([enc_key.decode()[:500], '由于私钥过长，部分已省略', "-----END CKKS PRIVATE KEY-----"]))
            lf1_text1.config(state='disabled')

    def decrypt():
        global ind
        lf1_confirm()
        ind = (ind + 1) % 6
        lf1_label4.config(fg=colors[ind])
        lf1_text1.config(state='normal')
        if lf1_text1.get(1.0, 'end').strip('\n') == '这不是正确的私钥' or lf1_text1.get(1.0, 'end').strip('\n') == '私钥地址错误':
            lf1_text1.config(state='disabled')
            lf1_label4.config(text='无法解密')
            return 0
        elif not lf1_entry2.get().strip(' '):
            lf1_label4.config(text='密码不能为空')
            return 0
        else:
            with open(Tools.get_path_from_entry(lf1_entry1), 'r', encoding='utf-8') as f:
                privkey = f.read()
            dec_key = Tools.decrypt_privkey(privkey.encode('utf-8'), lf1_entry2.get(), is_ckks=True)
            if dec_key == b'':
                lf1_label4.config(text='私钥的使用密码错误')
                return 0
            elif dec_key == b'1':
                lf1_label4.config(text='已经去除过密码，无法再次去除')
                return 0
            with open(Tools.get_path_from_entry(lf1_entry1), 'wb') as f:
                f.write(dec_key)
            lf1_label4.config(text='已去除密码')
            lf1_text1.config(state='normal')
            Tools.reset(lf1_text1)
            lf1_text1.insert('end', '\n'.join([dec_key.decode()[:500], '由于私钥过长，部分已省略', "-----END CKKS PRIVATE KEY-----"]))
            lf1_text1.config(state='disabled')

    lf1_button1 = tk.Button(lf1_frm2, text='去除密码', font=mid_font, command=decrypt)
    lf1_button1.grid(row=1, column=1, padx=20)
    lf1_button2 = tk.Button(lf1_frm2, text='添加密码', font=mid_font, command=encrypt)
    lf1_button2.grid(row=1, column=2, padx=20)
    lf1_label4 = tk.Label(labelframe1, text='   ', font=mid_font, fg=colors[ind])
    lf1_label4.pack()

    # 修改密码（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='为CKKS私钥修改使用密码', height=741, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()

    def change_lf2_entry1_show():
        Tools.change_entry_show(lf2_var1, lf2_entry1)

    def change_lf2_entry2_show():
        Tools.change_entry_show(lf2_var2, lf2_entry2)

    def change_lf2_entry3_show():
        Tools.change_entry_show(lf2_var3, lf2_entry3)

    def lf2_drag(files):
        Tools.dragged_files(files, lf2_entry1)
        lf2_confirm1()

    def lf2_reset1():
        Tools.reset(lf2_entry1)
        lf2_label5.config(text='   ')
        lf2_text1.config(state='normal')
        Tools.reset(lf2_text1)
        lf2_text1.config(state='disabled')
        lf2_reset2()

    def lf2_confirm1():
        lf2_label5.config(text='   ')
        lf2_text1.config(state='normal')
        Tools.reset(lf2_text1)
        key_path = Tools.get_path_from_entry(lf2_entry1)
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                key = f.read()
                if bytes("-----BEGIN CKKS PRIVATE KEY-----\nEncrypted:".encode('utf-8')) in key:
                    lf2_text1.insert('end', '\n'.join([key.decode()[:500], '由于私钥过长，部分已省略', "-----END CKKS PRIVATE KEY-----"]))
                else:
                    lf2_text1.insert('end', '这不是已加密的私钥')
        else:
            lf2_text1.insert('end', '私钥地址错误')
        lf2_text1.config(state='disabled')

    def lf2_reset2():
        Tools.reset(lf2_entry2)
        Tools.reset(lf2_entry3)
        lf2_label5.config(text='   ')

    def lf2_confirm2():
        global ind
        lf2_confirm1()
        ind = (ind + 1) % 6
        lf2_label5.config(fg=colors[ind])
        lf2_text1.config(state='normal')
        if lf2_text1.get(1.0, 'end').strip('\n') == '这不是已加密的私钥' or lf2_text1.get(1.0, 'end').strip('\n') == '私钥地址错误':
            lf2_text1.config(state='disabled')
            lf2_label5.config(text='无法修改密码')
            return 0
        elif not lf2_entry2.get().strip('') or not lf2_entry3.get().strip(''):
            lf2_label5.config(text='密码不能为空')
            return 0
        else:
            with open(Tools.get_path_from_entry(lf2_entry1), 'r', encoding='utf-8') as f:
                enc_key = f.read()
            dec_key = Tools.decrypt_privkey(enc_key.encode('utf-8'), lf2_entry2.get(), is_ckks=True)
            if dec_key == b'':
                lf2_label5.config(text='旧密码错误')
                return 0
            enc_key = Tools.encrypt_privkey(dec_key, lf2_entry3.get(), is_ckks=True)
            with open(Tools.get_path_from_entry(lf2_entry1), 'wb') as f:
                f.write(enc_key)
            lf2_label5.config(text='修改成功')
            lf2_text1.config(state='normal')
            Tools.reset(lf2_text1)
            lf2_text1.insert('end', '\n'.join([enc_key.decode()[:500], '由于私钥过长，部分已省略', "-----END CKKS PRIVATE KEY-----"]))
            lf2_text1.config(state='disabled')

    lf2_label1 = tk.Label(lf2_frm1, text='请拖入被加密的私钥或输入地址：', font=mid_font)
    lf2_label1.grid(row=1, column=1, padx=5)
    lf2_var1 = tk.StringVar()
    lf2_var1.set('0')
    lf2_cb1 = tk.Checkbutton(lf2_frm1, text='隐藏', font=mid_font, variable=lf2_var1, onvalue='1', offvalue='0',
                             command=change_lf2_entry1_show)
    lf2_cb1.grid(row=1, column=2, padx=5)
    lf2_entry1 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=lf2_drag)
    lf2_frm3 = tk.Frame(labelframe2)
    lf2_frm3.pack()
    lf2_button3 = tk.Button(lf2_frm3, text='重置', font=mid_font, command=lf2_reset1)
    lf2_button3.grid(row=1, column=1, padx=20)
    lf2_button4 = tk.Button(lf2_frm3, text='确定', font=mid_font, command=lf2_confirm1)
    lf2_button4.grid(row=1, column=2, padx=20)
    lf2_label2 = tk.Label(labelframe2, text='该私钥的内容为：', font=mid_font)
    lf2_label2.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=13, font=mid_font, state='disabled')
    lf2_text1.pack()
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_label3 = tk.Label(lf2_frm2, text='请输入旧密码：', font=mid_font)
    lf2_label3.grid(row=1, column=1, padx=5)
    lf2_var2 = tk.StringVar()
    lf2_var2.set('1')
    lf2_cb2 = tk.Checkbutton(lf2_frm2, text='隐藏', font=mid_font, variable=lf2_var2, onvalue='1', offvalue='0',
                             command=change_lf2_entry2_show)
    lf2_cb2.grid(row=1, column=2, padx=5)
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font, show='*')
    lf2_entry2.pack()
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_frm4.pack()
    lf2_label4 = tk.Label(lf2_frm4, text='请输入新密码：', font=mid_font)
    lf2_label4.grid(row=1, column=1, padx=5)
    lf2_var3 = tk.StringVar()
    lf2_var3.set('1')
    lf2_cb3 = tk.Checkbutton(lf2_frm4, text='隐藏', font=mid_font, variable=lf2_var3, onvalue='1', offvalue='0',
                             command=change_lf2_entry3_show)
    lf2_cb3.grid(row=1, column=2, padx=5)
    lf2_entry3 = tk.Entry(labelframe2, width=43, font=mid_font, show='*')
    lf2_entry3.pack()
    lf2_frm5 = tk.Frame(labelframe2)
    lf2_frm5.pack()
    lf2_button5 = tk.Button(lf2_frm5, text='重置', font=mid_font, command=lf2_reset2)
    lf2_button5.grid(row=1, column=1, padx=20)
    lf2_button6 = tk.Button(lf2_frm5, text='确定', font=mid_font, command=lf2_confirm2)
    lf2_button6.grid(row=1, column=2, padx=20)
    lf2_label5 = tk.Label(labelframe2, text='   ', font=mid_font, fg=colors[ind])
    lf2_label5.pack()


def ckks_word():
    frm2 = tk.Frame(frm)
    frm2.pack()
    frm1 = tk.Frame(frm2)
    frm1.pack()

    def change_pack():
        if var1.get() == 1:
            up_frm.pack_forget()
            up_frm2.pack()
        elif var1.get() == 2:
            up_frm2.pack_forget()
            up_frm.pack()

    var1 = tk.IntVar()
    var1.set(2)
    rb1 = tk.Radiobutton(frm1, variable=var1, text='对称加密', font=mid_font, value=1, command=change_pack)
    rb1.grid(row=1, column=1, padx=20)
    rb2 = tk.Radiobutton(frm1, variable=var1, text='非对称加密', font=mid_font, value=2, command=change_pack)
    rb2.grid(row=1, column=2, padx=20)
    # up_frm里放非对称加密的密钥布局
    up_frm = tk.Frame(frm2)
    up_frm.pack()
    uf_frm1 = tk.Frame(up_frm)
    uf_frm1.pack()

    def change_uf_entry1_show():
        Tools.change_entry_show(uf_var1, uf_entry1)

    def uf_drag1(files):
        Tools.dragged_files(files, uf_entry1)

    def change_uf_entry2_show():
        Tools.change_entry_show(uf_var2, uf_entry2)

    def uf_drag2(files):
        Tools.dragged_files(files, uf_entry2)

    def change_uf_entry3_show():
        Tools.change_entry_show(uf_var3, uf_entry3)

    uf_label1 = tk.Label(uf_frm1, text='请拖入用于加密数据的CKKS公钥或输入地址：', font=mid_font)
    uf_label1.grid(row=1, column=1, padx=5)
    uf_var1 = tk.StringVar()
    uf_var1.set('0')
    uf_cb1 = tk.Checkbutton(uf_frm1, text='隐藏', variable=uf_var1, onvalue='1', offvalue='0',
                            command=change_uf_entry1_show, font=mid_font)
    uf_cb1.grid(row=1, column=2, padx=5)
    uf_entry1 = tk.Entry(up_frm, font=mid_font, width=59)
    uf_entry1.pack()
    hook_dropfiles(uf_entry1, func=uf_drag1)
    uf_frm2 = tk.Frame(up_frm)
    uf_frm2.pack()
    uf_frm3 = tk.Frame(uf_frm2)
    uf_frm3.grid(row=1, column=1, padx=15)
    uf_label2 = tk.Label(uf_frm3, text='请拖入用于解密数据的私钥或输入地址：', font=mid_font)
    uf_label2.grid(row=1, column=1, padx=5)
    uf_var2 = tk.StringVar()
    uf_var2.set('0')
    uf_cb2 = tk.Checkbutton(uf_frm3, text='隐藏', variable=uf_var2, onvalue='1', offvalue='0',
                            command=change_uf_entry2_show, font=mid_font)
    uf_cb2.grid(row=1, column=2, padx=5)
    uf_entry2 = tk.Entry(uf_frm2, font=mid_font, width=36)
    uf_entry2.grid(row=2, column=1, padx=15)
    hook_dropfiles(uf_entry2, func=uf_drag2)
    uf_frm4 = tk.Frame(uf_frm2)
    uf_frm4.grid(row=1, column=2, padx=15)
    uf_label3 = tk.Label(uf_frm4, text='请输入私钥的使用密码：', font=mid_font)
    uf_label3.grid(row=1, column=1, padx=5)
    uf_var3 = tk.StringVar()
    uf_var3.set('1')
    uf_cb3 = tk.Checkbutton(uf_frm4, text='隐藏', variable=uf_var3, onvalue='1', offvalue='0',
                            command=change_uf_entry3_show, font=mid_font)
    uf_cb3.grid(row=1, column=2, padx=5)
    uf_entry3 = tk.Entry(uf_frm2, font=mid_font, width=30, show='*')
    uf_entry3.grid(row=2, column=2, padx=15)
    # up_frm2里放对称加密的密钥布局
    up_frm2 = tk.Frame(frm2)
    uf2_frm1 = tk.Frame(up_frm2)
    uf2_frm1.pack()

    def change_uf2_entry1_show():
        Tools.change_entry_show(uf2_var1, uf2_entry1)

    def uf2_drag1(files):
        Tools.dragged_files(files, uf2_entry1)

    uf2_label1 = tk.Label(uf2_frm1, text='请拖入CKKS对称加密密钥或输入地址：', font=mid_font)
    uf2_label1.grid(row=1, column=1, padx=5)
    uf2_var1 = tk.StringVar()
    uf2_var1.set('0')
    uf2_cb1 = tk.Checkbutton(uf_frm1, text='隐藏', variable=uf2_var1, onvalue='1', offvalue='0',
                            command=change_uf2_entry1_show, font=mid_font)
    uf2_cb1.grid(row=1, column=2, padx=5)
    uf2_entry1 = tk.Entry(up_frm2, font=mid_font, width=59)
    uf2_entry1.pack()
    hook_dropfiles(uf2_entry1, func=uf2_drag1)
    uf2_label2 = tk.Label(up_frm2, text='   ', font=mid_font)
    uf2_label2.pack(pady=6)
    uf2_label3 = tk.Label(up_frm2, text='   ', font=mid_font)
    uf2_label3.pack()

    # down_frm用来布置加密和解密区域
    down_frm = tk.Frame(frm)
    down_frm.pack()

    def open_dir():
        dir_path = os.path.join(os.getcwd(), 'CKKS_Vectors')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        os.system(f"explorer {os.path.join(os.getcwd(), 'CKKS_Vectors')}")

    df_frm1 = tk.Frame(down_frm)
    df_frm1.grid(row=1, column=1)

    def df1_drag(files):
        Tools.dragged_files(files, df1_text2)

    def df1_copy1():
        Tools.copy(df1_text1, df1_button1)

    def df1_reset1():
        Tools.reset(df1_text1)
        df1_label3.config(text=f'V1的长度为：0（须等于V2）')

    def df1_reset2():
        Tools.reset(df1_text2)

    def df1_cal():
        print('计算HE(V1)')
        Tools.reset(df1_text2)
        df1_text2.insert('end', '处理时间可能较长，请稍候')
        window.update()
        Tools.reset(df1_text2)
        # 先处理公钥或对称加密密钥
        if var1.get() == 1:
            if uf2_entry1.get().strip() == "":
                messagebox.showerror(title='缺少对称加密密钥', message='缺少对称加密密钥')
                return 0
            context = Tools.get_ckks_context(uf2_entry1)
            if context == 0:
                return 0
        elif var1.get() == 2:
            if uf_entry1.get().strip() == "":
                messagebox.showerror(title='缺少非对称加密公钥', message='缺少非对称加密公钥')
                return 0
            context = Tools.get_ckks_context(uf_entry1, method='pk')
            if context == 0:
                return 0
        # 再对明文V1进行处理
        v1 = Tools.text2vector(df1_text1.get(1.0, 'end').rstrip('\n').strip())
        print(f'向量化的V1为：{v1}，长度为：{len(v1)}')
        try:
            enc_v1 = ts.ckks_vector(context, v1)
        except Exception:
            messagebox.showerror(title='密钥错误', message='密钥错误，无法加密')
            return 0
        # 保存enc_v1
        dir_path = os.path.join(os.getcwd(), 'CKKS_Vectors')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        out_path = dir_path + '\\HE(V1).txt'
        with open(out_path, 'wb') as f:
            f.write(base64.b85encode(enc_v1.serialize()))
        df1_text2.insert(1.0, out_path)

    def cal_len_v1(*args):
        len_v1 = len(Tools.text2vector(df1_text1.get(1.0, 'end').rstrip('\n').strip()))
        df1_label3.config(text=f'V1的长度为：{len_v1}（须等于V2）')

    df1_frm1 = tk.Frame(df_frm1)
    df1_frm1.pack()
    df1_label1 = tk.Label(df1_frm1, text='输入或计算明文V1：', font=mid_font)
    df1_label1.grid(row=1, column=1, padx=5)
    df1_button1 = tk.Button(df1_frm1, text='复制', font=mid_font, fg=colors[ind], command=df1_copy1)
    df1_button1.grid(row=1, column=2, padx=5)
    df1_button2 = tk.Button(df1_frm1, text='重置', font=mid_font, command=df1_reset1)
    df1_button2.grid(row=1, column=3, padx=5)
    df1_label3 = tk.Label(df_frm1, text='V1的长度为：0（须等于V2）', font=mid_font)
    df1_label3.pack()
    df1_text1 = tk.Text(df_frm1, width=30, font=mid_font, height=12)
    df1_text1.pack()
    df1_text1.bind('<KeyRelease>', cal_len_v1)
    df1_button3 = tk.Button(df_frm1, text='计算HE(V1)↓', font=mid_font, command=df1_cal)
    df1_button3.pack()
    df1_frm2 = tk.Frame(df_frm1)
    df1_frm2.pack()
    df1_label2 = tk.Label(df1_frm2, text='V1的加密结果为：', font=mid_font)
    df1_label2.grid(row=1, column=1, padx=5)
    df1_button4 = tk.Button(df1_frm2, text='打开', font=mid_font, command=open_dir)
    df1_button4.grid(row=1, column=2, padx=5)
    df1_button5 = tk.Button(df1_frm2, text='重置', font=mid_font, command=df1_reset2)
    df1_button5.grid(row=1, column=3, padx=5)
    df1_text2 = tk.Text(df_frm1, width=30, font=mid_font, height=4)
    df1_text2.pack()
    df1_text2.insert(1.0, '处理结果以文件形式保存，您也可以拖入相应文件到此处进行后续处理')
    hook_dropfiles(df1_text2, func=df1_drag)

    df_frm2 = tk.Frame(down_frm)
    df_frm2.grid(row=1, column=2)

    def df2_cal1():
        print('计算(V1+V2)-V2')
        df1_reset1()
        try:
            v1_plus_v2 = Tools.ascii_str_to_int_list(df5_text1.get(1.0, 'end').rstrip('\n').strip())
        except Exception:
            messagebox.showerror('(V1+V2)输入有误', '(V1+V2)输入有误，无法处理')
            return 0
        print(f'V1+V2的向量化结果为: {v1_plus_v2}，长度为：{len(v1_plus_v2)}')
        v2 = Tools.text2vector(df3_text1.get(1.0, 'end').rstrip('\n').strip())
        print(f'v2的向量化结果为: {v2}，长度为：{len(v2)}')
        v1_vector = Tools.subtract_lists(v1_plus_v2, v2)
        print(f'V2-V1的向量化结果为：{v1_vector}，长度为：{len(v1_vector)}')
        try:
            v1 = Tools.vector2text(v1_vector)
        except Exception as e:
            print(e)
            messagebox.showerror('计算失败', '计算失败，可能是(V1+V2)或v1输入有误')
            return 0
        df1_text1.insert(1.0, v1)
        cal_len_v1()

    df2_button1 = tk.Button(df_frm2, text='计算\n(V1+V2)-V2\n←', font=mid_font, command=df2_cal1)
    df2_button1.grid(row=1, column=1, pady=100)
    df2_label1 = tk.Label(df_frm2, text='\n\n\n', font=mid_font)
    df2_label1.grid(row=2, column=1, pady=100)

    df_frm3 = tk.Frame(down_frm)
    df_frm3.grid(row=1, column=3)

    def df3_drag(files):
        Tools.dragged_files(files, df3_text2)

    def df3_copy1():
        Tools.copy(df3_text1, df3_button1)

    def df3_reset1():
        Tools.reset(df3_text1)
        df3_label3.config(text=f'V2的长度为：0（须等于V1）')

    def df3_reset2():
        Tools.reset(df3_text2)

    def df3_cal():
        print('计算HE(V2)')
        Tools.reset(df3_text2)
        df3_text2.insert('end', '处理时间可能较长，请稍候')
        window.update()
        Tools.reset(df3_text2)
        # 先处理公钥或对称加密密钥
        if var1.get() == 1:
            if uf2_entry1.get().strip() == "":
                messagebox.showerror(title='缺少对称加密密钥', message='缺少对称加密密钥')
                return 0
            context = Tools.get_ckks_context(uf2_entry1)
            if context == 0:
                return 0
        elif var1.get() == 2:
            if uf_entry1.get().strip() == "":
                messagebox.showerror(title='缺少非对称加密公钥', message='缺少非对称加密公钥')
                return 0
            context = Tools.get_ckks_context(uf_entry1, method='pk')
            if context == 0:
                return 0
        # 再对明文V2进行处理
        v2 = Tools.text2vector(df3_text1.get(1.0, 'end').rstrip('\n').strip())
        print(f'向量化的V2为：{v2}，长度为：{len(v2)}')
        try:
            enc_v2 = ts.ckks_vector(context, v2)
        except Exception:
            messagebox.showerror(title='密钥错误', message='密钥错误，无法加密')
            return 0
        # 保存enc_v2
        dir_path = os.path.join(os.getcwd(), 'CKKS_Vectors')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        out_path = dir_path + '\\HE(V2).txt'
        with open(out_path, 'wb') as f:
            f.write(base64.b85encode(enc_v2.serialize()))
        df3_text2.insert(1.0, out_path)

    def cal_len_v2(*args):
        len_v2 = len(Tools.text2vector(df3_text1.get(1.0, 'end').rstrip('\n').strip()))
        df3_label3.config(text=f'V2的长度为：{len_v2}（须等于V1）')

    df3_frm1 = tk.Frame(df_frm3)
    df3_frm1.pack()
    df3_label1 = tk.Label(df3_frm1, text='输入或计算明文V2：', font=mid_font)
    df3_label1.grid(row=1, column=1, padx=5)
    df3_button1 = tk.Button(df3_frm1, text='复制', font=mid_font, fg=colors[ind], command=df3_copy1)
    df3_button1.grid(row=1, column=2, padx=5)
    df3_button2 = tk.Button(df3_frm1, text='重置', font=mid_font, command=df3_reset1)
    df3_button2.grid(row=1, column=3, padx=5)
    df3_label3 = tk.Label(df_frm3, text='V2的长度为：0（须等于V1）', font=mid_font)
    df3_label3.pack()
    df3_text1 = tk.Text(df_frm3, width=30, font=mid_font, height=12)
    df3_text1.pack()
    df3_text1.bind('<KeyRelease>', cal_len_v2)
    df3_button3 = tk.Button(df_frm3, text='计算HE(V2)↓', font=mid_font, command=df3_cal)
    df3_button3.pack()
    df3_frm2 = tk.Frame(df_frm3)
    df3_frm2.pack()
    df3_label2 = tk.Label(df3_frm2, text='V2的加密结果为：', font=mid_font)
    df3_label2.grid(row=1, column=1, padx=5)
    df3_button4 = tk.Button(df3_frm2, text='打开', font=mid_font, command=open_dir)
    df3_button4.grid(row=1, column=2, padx=5)
    df3_button5 = tk.Button(df3_frm2, text='重置', font=mid_font, command=df3_reset2)
    df3_button5.grid(row=1, column=3, padx=5)
    df3_text2 = tk.Text(df_frm3, width=30, font=mid_font, height=4)
    df3_text2.pack()
    df3_text2.insert(1.0, '处理结果以文件形式保存，您也可以拖入相应文件到此处进行后续处理')
    hook_dropfiles(df3_text2, func=df3_drag)

    df_frm4 = tk.Frame(down_frm)
    df_frm4.grid(row=1, column=4)

    def df4_cal1():
        print('计算(V1+V2)-V1')
        df3_reset1()
        try:
            v1_plus_v2 = Tools.ascii_str_to_int_list(df5_text1.get(1.0, 'end').rstrip('\n').strip())
        except Exception:
            messagebox.showerror('(V1+V2)输入有误', '(V1+V2)输入有误，无法处理')
            return 0
        print(f'V1+V2的向量化结果为: {v1_plus_v2}，长度为：{len(v1_plus_v2)}')
        v1 = Tools.text2vector(df1_text1.get(1.0, 'end').rstrip('\n').strip())
        print(f'v1的向量化结果为: {v1}，长度为：{len(v1)}')
        v2_vector = Tools.subtract_lists(v1_plus_v2, v1)
        print(f'V2-V1的向量化结果为：{v2_vector}，长度为：{len(v2_vector)}')
        try:
            v2 = Tools.vector2text(v2_vector)
        except Exception as e:
            print(e)
            messagebox.showerror('计算失败', '计算失败，可能是(V1+V2)或v1输入有误')
            return 0
        df3_text1.insert(1.0, v2)
        cal_len_v2()

    def df4_cal2():
        print('计算V1+V2')
        df5_reset1()
        v1 = Tools.text2vector(df1_text1.get(1.0, 'end').rstrip('\n').strip())
        print(f'v1的向量化结果为: {v1}，长度为：{len(v1)}')
        v2 = Tools.text2vector(df3_text1.get(1.0, 'end').rstrip('\n').strip())
        print(f'v2的向量化结果为: {v2}，长度为：{len(v2)}')
        v1_plus_v2_vector = Tools.add_lists(v1, v2)
        print(f'V1+V2的向量化结果为：{v1_plus_v2_vector}，长度为：{len(v1_plus_v2_vector)}')
        v1_plus_v2 = Tools.float_list_to_ascii_str(v1_plus_v2_vector)
        df5_text1.insert(1.0, v1_plus_v2)
        cal_len_v1_plus_v2()

    def df4_cal3():
        print('计算HE(V1)+HE(V2)')
        Tools.reset(df5_text2)
        df5_text2.insert(1.0, '处理时间可能较长，请稍候')
        window.update()
        Tools.reset(df5_text2)
        # 先处理提取向量的对称密钥或公钥
        if var1.get() == 1:  # 对称加解密
            if uf2_entry1.get().strip() == "":
                return 0
            context = Tools.get_ckks_context(uf2_entry1)
            if context == 0:
                return 0
        elif var1.get() == 2:  # 非对称加解密
            if uf_entry1.get().strip() == "":
                messagebox.showerror(title='请拖入公钥', message='请拖入公钥\n密文相加时也需要输入公钥')
                return 0
            context = Tools.get_ckks_context(uf_entry1, method='pk')
            if context == 0:
                return 0
        # 再对密文HE(V1)和HE(V2)进行处理
        he_v1 = Tools.get_encrypted_vectors_form_path(df1_text2, context)
        if he_v1 == 0:
            return 0
        he_v2 = Tools.get_encrypted_vectors_form_path(df3_text2, context)
        if he_v2 == 0:
            return 0
        result = he_v1 + he_v2
        # 处理完之后对解密的信息进行保存和展示
        dir_path = os.path.join(os.getcwd(), 'CKKS_Vectors')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        out_path = dir_path + '\\HE(V1)_plus_HE(V2).txt'
        with open(out_path, 'wb') as f:
            f.write(base64.b85encode(result.serialize()))
        df5_text2.insert(1.0, out_path)
        print('计算HE(V1)+HE(V2)完成')

    df4_button1 = tk.Button(df_frm4, text='计算\n(V1+V2)-V1\n←', font=mid_font, command=df4_cal1)
    df4_button1.grid(row=1, column=1, pady=5)
    df4_button2 = tk.Button(df_frm4, text='计算\n  V1+V2   \n→', font=mid_font, command=df4_cal2)
    df4_button2.grid(row=2, column=1, pady=5)
    df4_label1 = tk.Label(df_frm4, text='\n\n\n\n\n', font=mid_font)
    df4_label1.grid(row=3, column=1, pady=5)
    df4_button3 = tk.Button(df_frm4, text='计算\nHE(V1)+HE(V2)\n→', font=mid_font, command=df4_cal3)
    df4_button3.grid(row=4, column=1, pady=5)

    df_frm5 = tk.Frame(down_frm)
    df_frm5.grid(row=1, column=5)

    def df5_drag(files):
        Tools.dragged_files(files, df5_text2)

    def df5_copy1():
        Tools.copy(df5_text1, df5_button1)

    def df5_reset1():
        Tools.reset(df5_text1)
        df5_label3.config(text='V1+V2的长度为：0')

    def df5_reset2():
        Tools.reset(df5_text2)

    def df5_cal():
        print('解密[HE(V1)+HE(V2)]')
        df5_reset1()
        df5_text1.insert('end', '处理时间可能较长，请稍候')
        window.update()
        Tools.reset(df5_text1)
        # 先处理私钥或对称加密密钥用于解密以及公钥用于提取[HE(V1)+HE(V2)]
        if var1.get() == 1:  # 对称加解密
            if uf2_entry1.get().strip() == "":
                messagebox.showerror(title='缺少对称加密密钥', message='缺少对称加密密钥')
                return 0
            context = Tools.get_ckks_context(uf2_entry1)
            if context == 0:
                return 0
            # 再对密文HE(V1)+HE(V2)进行处理
            he_v1_plus_he_v2 = Tools.get_encrypted_vectors_form_path(df5_text2, context)
            try:
                result = he_v1_plus_he_v2.decrypt()
            except Exception:
                messagebox.showerror(title='密钥错误', message='密钥错误，无法解密')
                return 0
        elif var1.get() == 2:  # 非对称加解密
            if uf_entry1.get().strip() == "":
                messagebox.showerror(title='请拖入公钥', message='请拖入公钥\n解密时也需要输入公钥')
                return 0
            pk = Tools.get_ckks_context(uf_entry1, method='pk')
            if pk == 0:
                return 0
            if uf_entry2.get().strip() == "":
                messagebox.showerror(title='缺少非对称加密私钥', message='缺少非对称加密私钥')
                return 0
            sk = Tools.get_ckks_context(uf_entry2, method='sk', pwd_entry=uf_entry3)
            if sk == 0:
                return 0
            # 再对密文HE(V1)+HE(V2)进行处理
            he_v1_plus_he_v2 = Tools.get_encrypted_vectors_form_path(df5_text2, pk)
            try:
                result = he_v1_plus_he_v2.decrypt(sk)
            except Exception:
                messagebox.showerror(title='私钥错误', message='私钥错误，无法解密')
                return 0
        # 处理完之后对解密的信息进行展示
        print(f'解密[HE(V1)+HE(V2)]的向量化结果为：{np.round(result)}，长度为：{len(result)}')
        try:
            ans = Tools.float_list_to_ascii_str(result)
        except Exception:
            messagebox.showerror(title='解密失败', message='解密失败，可能是解密的私钥与加密的公钥不匹配')
            return 0
        df5_text1.insert(1.0, ans)
        cal_len_v1_plus_v2()

    def cal_len_v1_plus_v2(*args):
        len_v1_plus_v2 = len(df5_text1.get(1.0, 'end').rstrip('\n').strip())
        df5_label3.config(text=f'V1+V2的长度为：{len_v1_plus_v2}')

    df5_frm1 = tk.Frame(df_frm5)
    df5_frm1.pack()
    df5_label1 = tk.Label(df5_frm1, text='输入或计算V1+V2：', font=mid_font)
    df5_label1.grid(row=1, column=1, padx=5)
    df5_button1 = tk.Button(df5_frm1, text='复制', font=mid_font, fg=colors[ind], command=df5_copy1)
    df5_button1.grid(row=1, column=2, padx=5)
    df5_button2 = tk.Button(df5_frm1, text='重置', font=mid_font, command=df5_reset1)
    df5_button2.grid(row=1, column=3, padx=5)
    df5_label3 = tk.Label(df_frm5, text='V1+V2的长度为：0', font=mid_font)
    df5_label3.pack()
    df5_text1 = tk.Text(df_frm5, width=30, font=mid_font, height=11)
    df5_text1.pack()
    df5_text1.bind('<KeyRelease>', cal_len_v1_plus_v2)
    df5_button3 = tk.Button(df_frm5, text='解密[HE(V1)+HE(V2)]↑', font=mid_font, command=df5_cal)
    df5_button3.pack()
    df5_frm2 = tk.Frame(df_frm5)
    df5_frm2.pack(pady=4)
    df5_label2 = tk.Label(df5_frm2, text='输入或计算\n[HE(V1)+HE(V2)]：', font=mid_font)
    df5_label2.grid(row=1, column=1, padx=5)
    df5_button4 = tk.Button(df5_frm2, text='打开', font=mid_font, command=open_dir)
    df5_button4.grid(row=1, column=2, padx=5)
    df5_button5 = tk.Button(df5_frm2, text='重置', font=mid_font, command=df5_reset2)
    df5_button5.grid(row=1, column=3, padx=5)
    df5_text2 = tk.Text(df_frm5, width=30, font=mid_font, height=4)
    df5_text2.pack()
    df5_text2.insert(1.0, '处理结果以文件形式保存，您也可以拖入相应文件到此处进行后续处理')
    hook_dropfiles(df5_text2, func=df5_drag)


def hash_word():
    # 哈希计算（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='哈希计算', height=741, width=606, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def process(*args):
        if var1.get() == "utf-8":
            value = bytes(text1.get(1.0, 'end').rstrip("\n").encode("UTF-8"))
        elif var1.get() == "gbk":
            value = bytes(text1.get(1.0, 'end').rstrip("\n").encode("GBK"))
        text2.delete(1.0, 'end')
        hash_value = None
        method = method_var.get()
        if method == 'MD4':
            hasher = MD4.new()
            hasher.update(value)
            hash_value = hasher.hexdigest()
        elif method == 'MD5':
            hash_value = hashlib.md5(value).hexdigest()
            if var2.get() == '16位':
                hash_value = str(hash_value)[8: -8]
        elif method == "CRC32":
            if var2.get() == "十六进制":
                # hash_value = hex(binascii.crc32(value))  # 默认带16进制前缀“0x”
                hash_value = str(hex(binascii.crc32(value))).lstrip("0x")  # 去掉前缀
            elif var2.get() == "十进制":
                hash_value = binascii.crc32(value)
            elif var2.get() == "二进制":
                hash_value = str(bin(binascii.crc32(value))).lstrip("0b")  # 去掉前缀
        elif method == 'SHA-1':
            hash_value = hashlib.sha1(value).hexdigest()
        elif method == 'SHA-256':
            hash_value = hashlib.sha256(value).hexdigest()
        elif method == 'SHA-384':
            hash_value = hashlib.sha384(value).hexdigest()
        elif method == 'SHA-512':
            hash_value = hashlib.sha512(value).hexdigest()
        elif method == 'BLAKE2B':
            hash_value = hashlib.blake2b(value).hexdigest()
        elif method == 'RipeMD160':
            hasher = RIPEMD160.new()
            hasher.update(value)
            hash_value = hasher.hexdigest()
        elif method == 'SHA-224':
            hash_value = hashlib.sha3_224(value).hexdigest()
        if var3.get() == '1':
            hash_value = str(hash_value).upper()
        text2.insert('end', hash_value)

    frm3 = tk.Frame(labelframe1)
    frm3.pack()
    label1 = tk.Label(frm3, text='请选择文字的编码方式：', font=mid_font)
    label1.grid(row=1, column=1)
    var1 = tk.StringVar()
    var1.set("utf-8")
    option_menu1 = tk.OptionMenu(frm3, var1, *("utf-8", "gbk"), command=process)
    option_menu1.config(font=mid_font)
    option_menu1.grid(row=1, column=2)
    text1 = tk.Text(labelframe1, width=43, height=15, font=mid_font)
    text1.pack()

    def _reset():
        Tools.reset(text1)
        Tools.reset(text2)

    def _copy():
        Tools.copy(text2, button3)

    def change_grid(*args):
        option_menu2.grid_forget()
        option_menu3.grid_forget()
        if method_var.get() == "CRC32":
            var2.set("十六进制")
            option_menu2.grid(row=1, column=4, padx=5)
        elif method_var.get() == 'MD5':
            var2.set("32位")
            option_menu3.grid(row=1, column=4, padx=5)
        process()

    frm2 = tk.Frame(labelframe1)
    frm2.pack(pady=5)
    button1 = tk.Button(frm2, text='重置文字', font=mid_font, command=_reset)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm2, text='哈希计算', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=20)
    button3 = tk.Button(frm2, text='复制结果', font=mid_font, command=_copy, fg=colors[ind])
    button3.grid(row=1, column=3, padx=20)
    frm1 = tk.Frame(labelframe1)
    frm1.pack()
    var3 = tk.StringVar()
    var3.set("1")
    cb1 = tk.Checkbutton(frm1, text='大写', font=mid_font, variable=var3, onvalue='1', offvalue='0', command=process)
    cb1.grid(row=1, column=1, padx=10)
    method_var = tk.StringVar()
    method_var.set('CRC32')
    method_option = tk.OptionMenu(frm1, method_var, *('CRC32', 'MD4', 'MD5', 'SHA-1', 'SHA-256', 'SHA-384', 'SHA-512', 'SHA-224', 'BLAKE2B', 'RipeMD160'), command=change_grid)
    method_option.grid(row=1, column=2)
    method_option.config(font=mid_font)
    label2 = tk.Label(frm1, text='结果为：', font=mid_font)
    label2.grid(row=1, column=3)
    var2 = tk.StringVar()  # 这个是结果的表示方式
    var2.set("十六进制")
    option_menu2 = tk.OptionMenu(frm1, var2, *("十六进制", "十进制", "二进制"), command=process)
    option_menu2.config(font=mid_font)
    option_menu2.grid(row=1, column=4, padx=5)
    option_menu3 = tk.OptionMenu(frm1, var2, *("32位", "16位"), command=process)
    option_menu3.config(font=mid_font)
    text2 = tk.Text(labelframe1, width=43, height=6, font=mid_font)
    text2.pack()
    text1.bind("<KeyRelease>", process)

    # 哈希校验（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='哈希校验', height=741, width=606, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)
    lf2_label1 = tk.Label(labelframe2, text='请输入哈希值1：', font=mid_font)
    lf2_label1.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=11, font=mid_font)
    lf2_text1.pack()

    def reset1():
        Tools.reset(lf2_text1)
        compare()

    def reset2():
        Tools.reset(lf2_text2)
        compare()

    def compare(*args):
        global ind
        ind = (ind + 1) % 6
        lf2_entry1.config(state='normal')
        Tools.reset(lf2_entry1)
        if lf2_text1.get(1.0, 'end').upper().replace(' ', '').replace('\n', '') == lf2_text2.get(1.0, 'end').upper().replace(' ', '').replace('\n', ''):
            lf2_entry1.insert('end', '一致')
        else:
            lf2_entry1.insert('end', '不一致')
        lf2_entry1.config(fg=colors[ind], state='readonly')

    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack(pady=5)
    lf2_button1 = tk.Button(lf2_frm1, text='重置1', font=mid_font, command=reset1)
    lf2_button1.grid(row=1, column=1, padx=15)
    lf2_button2 = tk.Button(lf2_frm1, text='重置2', font=mid_font, command=reset2)
    lf2_button2.grid(row=1, column=2, padx=15)
    lf2_button3 = tk.Button(lf2_frm1, text='比较', font=mid_font, command=compare)
    lf2_button3.grid(row=1, column=3, padx=15)
    lf2_entry1 = tk.Entry(lf2_frm1, width=6, font=mid_font, fg=colors[ind])
    lf2_entry1.insert('end', '一致')
    lf2_entry1.config(state='readonly')
    lf2_entry1.grid(row=1, column=4, padx=15)
    lf2_label2 = tk.Label(labelframe2, text='请输入哈希值2：', font=mid_font)
    lf2_label2.pack()
    lf2_text2 = tk.Text(labelframe2, width=43, height=11, font=mid_font)
    lf2_text2.pack()
    lf2_text1.bind('<KeyRelease>', compare)
    lf2_text2.bind('<KeyRelease>', compare)


def hash_file():

    def change_grid(*args):
        option_menu1.grid_forget()
        option_menu2.grid_forget()
        if method_var.get() == 'CRC32':
            var1.set('十六进制')
            option_menu1.grid(row=1, column=3, padx=5)
        elif method_var.get() == 'MD5':
            var1.set('32位')
            option_menu2.grid(row=1, column=3, padx=5)
        process()

    def get_hash(filename, method):
        with open(filename, "rb") as f:
            if method == 'MD5':
                hasher = hashlib.md5()  # 创建md5对象
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    hasher.update(data)  # 更新md5对象
                hash_value = hasher.hexdigest()  # 返回md5值
                if var1.get() == '16位':
                    hash_value = str(hash_value)[8: -8]
            elif method == "CRC32":
                data = f.read()
                if var1.get() == '十六进制':
                    hash_value = str(hex(zlib.crc32(data))).lstrip("0x")
                elif var1.get() == '十进制':
                    hash_value = zlib.crc32(data)
                elif var1.get() == '二进制':
                    hash_value = str(bin(zlib.crc32(data))).lstrip("0b")
            elif method == 'SHA-1':
                block_size = 33554432  # 每一次读取的长度为32mb
                hasher = hashlib.sha1()
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                hash_value = hasher.hexdigest()
            elif method == 'SHA-256':
                block_size = 33554432  # 每一次读取的长度为32mb
                hasher = hashlib.sha256()
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                hash_value = hasher.hexdigest()
            elif method == 'SHA-384':
                block_size = 33554432  # 每一次读取的长度为32mb
                hasher = hashlib.sha384()
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                hash_value = hasher.hexdigest()
            elif method == 'SHA-512':
                block_size = 33554432  # 每一次读取的长度为32mb
                hasher = hashlib.sha512()
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                hash_value = hasher.hexdigest()
            elif method == 'BLAKE2B':
                block_size = 33554432  # 每一次读取的长度为32mb
                hasher = hashlib.blake2b()
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                hash_value = hasher.hexdigest()
            elif method == 'SHA-224':
                block_size = 33554432  # 每一次读取的长度为32mb
                hasher = hashlib.sha3_224()
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                hash_value = hasher.hexdigest()
            elif method == 'RipeMD160':
                block_size = 33554432  # 每一次读取的长度为32mb
                hasher = RIPEMD160.new()
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                hash_value = hasher.hexdigest()
            elif method == 'MD4':
                block_size = 33554432  # 每一次读取的长度为32mb
                hasher = MD4.new()
                fb = f.read(block_size)
                while fb:
                    hasher.update(fb)
                    fb = f.read(block_size)
                hash_value = hasher.hexdigest()
            if capital.get() == '1':
                hash_value = str(hash_value).upper()
        return hash_value

    def process(*args):
        global ind
        file1 = Tools.get_path_from_entry(entry1)
        if os.path.exists(file1) and os.path.isfile(file1):
            Tools.reset(text1)
            text1.insert('end', get_hash(file1, method_var.get()))
        elif file1.replace(' ', '').replace('\n', ''):  # 如果输入了文件路径，但路径错误
            Tools.reset(text1)
            text1.insert('end', '文件1路径错误')
        file2 = Tools.get_path_from_entry(entry3)
        if os.path.exists(file2) and os.path.isfile(file2):
            Tools.reset(text2)
            text2.insert('end', get_hash(file2, method_var.get()))
        elif file2.replace(' ', '').replace('\n', ''):
            Tools.reset(text2)
            text2.insert('end', '文件2路径错误')
        entry2.config(state='normal')
        Tools.reset(entry2)
        if text1.get(1.0, 'end').replace(' ', '').replace('\n', '').upper() == text2.get(1.0, 'end').replace(' ', '').replace('\n', '').upper():
            entry2.insert('end', '一致')
        else:
            entry2.insert('end', '不一致')
        ind = (ind + 1) % 6
        entry2.config(state='readonly', fg=colors[ind])

    def drag1(files):
        Tools.dragged_files(files, entry1)
        process()

    def drag2(files):
        Tools.dragged_files(files, entry3)
        process()

    def reset1():
        Tools.reset(entry1)
        Tools.reset(text1)
        entry2.config(state='normal')
        Tools.reset(entry2)
        entry2.config(state='readonly')

    def reset2():
        Tools.reset(entry3)
        Tools.reset(text2)
        entry2.config(state='normal')
        Tools.reset(entry2)
        entry2.config(state='readonly')

    def copy1():
        Tools.copy(text1, button_3)

    def copy2():
        Tools.copy(text2, button_6)

    def reset_all():
        reset1()
        reset2()

    def small_window():
        def _reset1():
            Tools.reset(_entry1)
            Tools.reset(_text1)

        def _reset2():
            Tools.reset(_entry2)
            Tools.reset(_text2)

        def check(*args):
            global ind
            path1 = Tools.get_path_from_entry(_entry1)
            if os.path.exists(path1) and os.path.isfile(path1):
                Tools.reset(_text1)
                _text1.insert('end', get_hash(path1, _var1.get()))
            elif path1:
                Tools.reset(_text1)
                _text1.insert('end', '文件1路径错误')
            path2 = _entry2.get().strip().strip("\"").lstrip("“").rstrip("”")
            if os.path.exists(path2) and os.path.isfile(path2):
                Tools.reset(_text2)
                _text2.insert('end', get_hash(path2, _var1.get()))
            elif path2:
                Tools.reset(_text2)
                _text2.insert('end', '文件2路径错误')
            _entry3.config(state='normal')
            Tools.reset(_entry3)
            if _text1.get(1.0, 'end').replace(' ', '').replace('\n', '').upper() == _text2.get(1.0, 'end').replace(' ', '').replace('\n', '').upper():
                _entry3.insert('end', '一致')
            else:
                _entry3.insert('end', '不一致')
            ind = (ind + 1) % 6
            _entry3.config(state='readonly', fg=colors[ind])

        def inner_drag1(files):
            Tools.dragged_files(files, _entry1)
            check()

        def inner_drag2(files):
            Tools.dragged_files(files, _entry2)
            check()

        com_window = tk.Toplevel()
        com_window.title("哈希计算与校验")
        com_window.geometry("595x515")
        com_window.iconbitmap(icon_path)
        _label1 = tk.Label(com_window, text='请拖入文件1或输入地址：', font=mid_font)
        _label1.pack()
        _entry1 = tk.Entry(com_window, font=mid_font, width=44)
        _entry1.pack()
        hook_dropfiles(_entry1, func=inner_drag1)
        _label2 = tk.Label(com_window, text='文件1的哈希值为：', font=mid_font)
        _label2.pack()
        _text1 = tk.Text(com_window, width=44, height=5, font=mid_font)
        _text1.pack()
        frm1 = tk.Frame(com_window)
        frm1.pack()
        _var1 = tk.StringVar()
        _var1.set("CRC32")
        option_menu = tk.OptionMenu(frm1, _var1, *('CRC32', 'MD4', 'MD5', 'SHA-1', 'SHA-256', 'SHA-384', 'SHA-512', 'SHA-224', 'BLAKE2B', 'RipeMD160'), command=check)
        option_menu.config(font=mid_font)
        option_menu.grid(row=1, column=1, padx=5)
        _button1 = tk.Button(frm1, text='重置1', font=mid_font, command=_reset1)
        _button1.grid(row=1, column=2, padx=5)
        _button2 = tk.Button(frm1, text='重置2', font=mid_font, command=_reset2)
        _button2.grid(row=1, column=3, padx=5)
        _button3 = tk.Button(frm1, text='比较', font=mid_font, command=check)
        _button3.grid(row=1, column=4, padx=5)
        _entry3 = tk.Entry(frm1, width=6, font=mid_font, state='readonly', fg=colors[ind])
        _entry3.grid(row=1, column=5, padx=5)
        _label3 = tk.Label(com_window, text='请拖入文件2或输入地址：', font=mid_font)
        _label3.pack()
        _entry2 = tk.Entry(com_window, width=44, font=mid_font)
        _entry2.pack()
        hook_dropfiles(_entry2, func=inner_drag2)
        _label4 = tk.Label(com_window, text='文件2的哈希值为：', font=mid_font)
        _label4.pack()
        _text2 = tk.Text(com_window, width=44, height=5, font=mid_font)
        _text2.pack()

    label1 = tk.Label(frm, text='请拖入文件1或输入地址：', font=mid_font)
    label1.pack()
    frame1 = tk.Frame(frm)
    frame1.pack()
    entry1 = tk.Entry(frame1, width=59, font=mid_font)
    entry1.grid(row=1, column=1, padx=5)
    hook_dropfiles(entry1, func=drag1)
    button_2 = tk.Button(frame1, text='确定', font=mid_font, command=process)
    button_2.grid(row=1, column=2, padx=5)
    label2 = tk.Label(frm, text='文件1的哈希值为（此处也可手动填入哈希值）：', font=mid_font)
    label2.pack()
    frame2 = tk.Frame(frm)
    frame2.pack()
    text1 = tk.Text(frame2, width=59, height=8, font=mid_font)
    text1.grid(row=1, column=1, padx=5)
    frame3 = tk.Frame(frame2)
    frame3.grid(row=1, column=2, padx=5)
    button_1 = tk.Button(frame3, text='重置', font=mid_font, command=reset1)
    button_1.grid(row=1, column=1, pady=5)
    button_3 = tk.Button(frame3, text='复制', font=mid_font, command=copy1, fg=colors[ind])
    button_3.grid(row=2, column=1, pady=5)
    frm2 = tk.Frame(frm)
    frm2.pack()
    label5 = tk.Label(frm2, text='请设置哈希值的计算方式：', font=mid_font)
    label5.grid(row=1, column=1, padx=5)
    method_var = tk.StringVar()
    method_var.set('CRC32')
    method_option = tk.OptionMenu(frm2, method_var, *(
    'CRC32', 'MD4', 'MD5', 'SHA-1', 'SHA-256', 'SHA-384', 'SHA-512', 'SHA-224', 'BLAKE2B', 'RipeMD160'),
                                  command=change_grid)
    method_option.grid(row=1, column=2, padx=5)
    method_option.config(font=mid_font)
    var1 = tk.StringVar()
    var1.set("十六进制")
    option_menu1 = tk.OptionMenu(frm2, var1, *("十六进制", "十进制", "二进制"), command=process)
    option_menu1.config(font=mid_font)
    option_menu1.grid(row=1, column=3, padx=5)
    option_menu2 = tk.OptionMenu(frm2, var1, *("32位", "16位"), command=process)
    option_menu2.config(font=mid_font)
    capital = tk.StringVar()
    capital.set('1')
    cb1 = tk.Checkbutton(frm2, text='大写', font=mid_font, variable=capital, onvalue='1', offvalue='0', command=process)
    cb1.grid(row=1, column=4, padx=5)
    frm1 = tk.Frame(frm)
    frm1.pack()
    button1 = tk.Button(frm1, text='重置全部', font=mid_font, command=reset_all)
    button1.grid(row=1, column=1, padx=10)
    button3 = tk.Button(frm1, text='计算并校验', font=mid_font, command=process)
    button3.grid(row=1, column=2, padx=10)
    entry2 = tk.Entry(frm1, width=6, font=mid_font, fg=colors[ind])
    entry2.grid(row=1, column=3, padx=10)
    entry2.insert('end', '一致')
    entry2.config(state='readonly')
    button4 = tk.Button(frm1, text='小窗模式', font=mid_font, command=small_window)
    button4.grid(row=1, column=4, padx=10)
    label3 = tk.Label(frm, text='请拖入文件2或输入地址：', font=mid_font)
    label3.pack()
    frame4 = tk.Frame(frm)
    frame4.pack()
    entry3 = tk.Entry(frame4, width=59, font=mid_font)
    entry3.grid(row=1, column=1, padx=5)
    button_4 = tk.Button(frame4, font=mid_font, text='确定', command=process)
    button_4.grid(row=1, column=2, padx=5)
    hook_dropfiles(entry3, func=drag2)
    label4 = tk.Label(frm, text='文件2的哈希值为（此处也可手动填入哈希值）：', font=mid_font)
    label4.pack()
    frame5 = tk.Frame(frm)
    frame5.pack()
    text2 = tk.Text(frame5, width=59, height=8, font=mid_font)
    text2.grid(row=1, column=1, padx=5)
    frame6 = tk.Frame(frame5)
    frame6.grid(row=1, column=2, padx=5)
    button_5 = tk.Button(frame6, text='重置', font=mid_font, command=reset2)
    button_5.grid(row=1, column=1, pady=5)
    button_6 = tk.Button(frame6, text='复制', font=mid_font, command=copy2, fg=colors[ind])
    button_6.grid(row=2, column=1, pady=5)
