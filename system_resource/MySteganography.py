import base64
import copy
import math
import os
import re
import time
import tkinter as tk
from math import floor
from random import randint
from tkinter import messagebox
from tkinter import ttk
import cv2
import numpy as np
import pyperclip
from windnd import hook_dropfiles
from moviepy.editor import VideoFileClip, AudioFileClip
import zero_width_lib as zwlib
import jieba
from reedsolo import RSCodec
from blind_watermark import WaterMark
from system_resource.ToolKit import Tools

temp_video_path = temp_outvideo_path = temp_video_saving_path = 'N/A'
base64dic = Tools.base64dic
alive = False  # 控制线程是否存活的变量
window = frm = mid_font = icon_path = colors = ind = zoom = ...


def initiation(_window, _frm, _mid_font, _icon_path, _colors, _ind, _zoom):
    global window, frm, mid_font, icon_path, colors, ind, zoom
    window = _window
    frm = _frm
    mid_font = _mid_font
    icon_path = _icon_path
    colors = _colors
    ind = _ind
    zoom = _zoom


def video_logo():
    # 请输入隐写对象（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='输入隐写的内容', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()

    def change_grid_of_labelframe1(*args):
        lf1_frm3.pack_forget()
        lf1_frm4.pack_forget()
        if lf1_stega_object.get() == '文件':
            lf1_label1.grid_forget()
            lf1_optionmenu2.grid_forget()
            lf1_frm2.pack_forget()
            lf1_frm5.pack()
            lf1_frm3.pack()
            lf1_frm6.pack()
            lf1_frm7.pack()
            if file_part.get() == '部分文件':
                lf1_frm8.pack()
            lf1_frm4.pack()
        elif lf1_stega_object.get() == '文字':
            lf1_label1.grid(row=1, column=2)
            lf1_optionmenu2.grid(row=1, column=3)
            lf1_frm5.pack_forget()
            lf1_frm6.pack_forget()
            lf1_frm7.pack_forget()
            lf1_frm8.pack_forget()
            lf1_frm2.pack()
            lf1_frm3.pack()
            lf1_frm4.pack()
        lf1_entry2.config(state='normal')
        Tools.reset(lf1_entry2)
        lf1_entry2.config(state='readonly')

    def change_pack_of_lf1_frm8(*args):
        lf1_frm4.pack_forget()
        if file_part.get() == '部分文件':
            lf1_frm8.pack()
        elif file_part.get() == '完整文件':
            lf1_frm8.pack_forget()
        lf1_frm4.pack()
        calculate_information_size()

    def reset_lf1_text1_or_lf1_entry1():
        if lf1_stega_object.get() == '文字':
            Tools.reset(lf1_text1)
        elif lf1_stega_object.get() == '文件':
            Tools.reset(lf1_entry1)
            lf1_entry2.config(state='normal')
            Tools.reset(lf1_entry2)
            lf1_entry2.config(state='readonly')
            Tools.reset(lf1_entry4)
            Tools.reset(lf1_entry5)
        Tools.delete_file('_temp_file.txt')
        lf1_entry3.config(state='normal')
        Tools.reset(lf1_entry3)
        lf1_entry3.config(state='readonly')

    def calculate_information_size(*args):
        global ind
        ind = (ind + 1) % 6
        lf1_entry2.config(fg=colors[ind], state='normal')
        Tools.reset(lf1_entry2)
        try:
            total_size = os.path.getsize('_temp_file.txt')
        except Exception:
            total_size = 0
        if lf1_stega_object.get() == '文字':
            lf1_entry2.insert(0, total_size)
        elif lf1_stega_object.get() == '文件':
            if lf1_entry3.get() == '路径错误':
                lf1_entry2.insert(0, '路径错误')
            elif lf1_entry3.get() == '':
                lf1_entry3.insert(0, '')
            else:
                if file_part.get() == '完整文件':
                    lf1_entry2.insert(0, total_size)
                elif file_part.get() == '部分文件':
                    try:
                        end = eval(lf1_entry5.get())
                        assert isinstance(end, int) and total_size >= end >= 1
                        begin = eval(lf1_entry4.get())
                        assert isinstance(begin, int) and total_size >= begin >= 1 and end >= begin
                        partial_size = end - begin + 1  # 包含头尾
                        lf1_entry2.insert(0, partial_size)
                    except Exception:
                        lf1_entry2.insert(0, '输入错误')
        lf1_entry2.config(state='readonly')

    def lf1_confirm(*args):
        # 把文字或文件以base64编码保存在程序所在文件夹中的_temp_file.txt
        if lf1_stega_object.get() == '文字':
            global ind
            ind = (ind + 1) % 6
            word = lf1_text1.get(1.0, 'end').rstrip('\n')
            if word_encoding.get() == 'base64':
                word_set = set(word)
                for i in word_set:
                    if i not in base64dic.keys():
                        lf1_entry2.config(fg=colors[ind], state='normal')
                        Tools.reset(lf1_entry2)
                        lf1_entry2.insert(0, '编码错误')
                        lf1_entry2.config(state='readonly')
                        return 0
                with open('_temp_file.txt', 'wb') as outfile:
                    outfile.write(word.encode('utf-8'))
            elif word_encoding.get() == '字节码':
                try:
                    byte = eval(word)
                    assert isinstance(byte, bytes)
                except Exception:
                    lf1_entry2.config(fg=colors[ind], state='normal')
                    Tools.reset(lf1_entry2)
                    lf1_entry2.insert(0, '编码错误')
                    lf1_entry2.config(state='readonly')
                    return 0
                with open('_temp_file.txt', 'wb') as outfile:
                    outfile.write(base64.b64encode(byte))
            else:
                with open('_temp_file.txt', 'wb') as outfile:
                    outfile.write(base64.b64encode(word.encode(word_encoding.get())))  # 将文字转为base64编码后写入临时文件
        elif lf1_stega_object.get() == '文件':
            file_path = Tools.get_path_from_entry(lf1_entry1)
            lf1_entry3.config(state='normal')
            Tools.reset(lf1_entry3)
            if os.path.exists(file_path):
                with open('_temp_file.txt', 'wb') as outfile, open(file_path, 'rb') as infile:
                    while True:
                        block = infile.read(600)
                        if block:
                            outfile.write(base64.b64encode(block))
                        else:
                            break
                lf1_entry3.insert(0, os.path.getsize('_temp_file.txt'))
            else:
                lf1_entry3.insert(0, '路径错误')
            lf1_entry3.config(state='readonly')
        calculate_information_size()

    def drag1(files):
        Tools.dragged_files(files, lf1_entry1)
        lf1_confirm()

    # 如果用户选择隐写文字所展示的布局
    lf1_stega_object = tk.StringVar()
    lf1_stega_object.set('文字')
    lf1_optionmenu1 = tk.OptionMenu(lf1_frm1, lf1_stega_object, *('文字', '文件'), command=change_grid_of_labelframe1)
    lf1_optionmenu1.grid(row=1, column=1)
    lf1_optionmenu1.config(font=mid_font)
    lf1_label1 = tk.Label(lf1_frm1, text=' 请选择文字的编码方式：', font=mid_font)
    lf1_label1.grid(row=1, column=2)
    word_encoding = tk.StringVar()
    word_encoding.set('utf-8')
    lf1_optionmenu2 = tk.OptionMenu(lf1_frm1, word_encoding, *('utf-8', 'gbk', 'base64', '字节码'), command=lf1_confirm)
    lf1_optionmenu2.grid(row=1, column=3)
    lf1_optionmenu2.config(font=mid_font)
    lf1_frm2 = tk.Frame(labelframe1)
    lf1_frm2.pack()
    lf1_label2 = tk.Label(lf1_frm2, text='请下方输入需要隐写的文字：', font=mid_font)
    lf1_label2.pack()
    lf1_text1 = tk.Text(lf1_frm2, width=43, height=21, font=mid_font)
    lf1_text1.pack()
    lf1_text1.bind('<KeyRelease>', lf1_confirm)
    lf1_frm3 = tk.Frame(labelframe1)
    lf1_frm3.pack()
    lf1_button1 = tk.Button(lf1_frm3, text='重置', font=mid_font, command=reset_lf1_text1_or_lf1_entry1)
    lf1_button1.grid(row=1, column=1, padx=20)
    lf1_button2 = tk.Button(lf1_frm3, text='确定', font=mid_font, command=lf1_confirm)
    lf1_button2.grid(row=1, column=2, padx=20)
    lf1_frm4 = tk.Frame(labelframe1)
    lf1_frm4.pack()
    lf1_label3 = tk.Label(lf1_frm4, text="信息大小（base64字节）：", font=mid_font)
    lf1_label3.grid(row=1, column=1)
    lf1_entry2 = tk.Entry(lf1_frm4, width=8, font=mid_font)
    lf1_entry2.grid(row=1, column=2)
    lf1_entry2.insert('end', '0')
    lf1_entry2.config(state='readonly')
    # 如果用户选择隐写文件所展示的布局
    lf1_frm5 = tk.Frame(labelframe1)
    lf1_label4 = tk.Label(lf1_frm5, text='请拖入需要隐写的文件或输入地址：', font=mid_font)
    lf1_label4.grid(row=1, column=1)
    lf1_entry1 = tk.Entry(lf1_frm5, width=43, font=mid_font)
    lf1_entry1.grid(row=2, column=1)
    lf1_entry1.bind('<KeyRelease>', lf1_confirm)
    hook_dropfiles(lf1_entry1, func=drag1)
    lf1_frm6 = tk.Frame(labelframe1)
    lf1_label5 = tk.Label(lf1_frm6, text='文件的总大小（base64字节）：', font=mid_font)
    lf1_label5.grid(row=1, column=1)
    lf1_entry3 = tk.Entry(lf1_frm6, width=8, font=mid_font, state='readonly')
    lf1_entry3.grid(row=1, column=2)
    lf1_frm7 = tk.Frame(labelframe1)
    lf1_label6 = tk.Label(lf1_frm7, text='请选择隐写的部分：', font=mid_font)
    lf1_label6.grid(row=1, column=1)
    file_part = tk.StringVar()
    file_part.set('完整文件')
    lf1_optionmenu3 = tk.OptionMenu(lf1_frm7, file_part, *('完整文件', '部分文件'), command=change_pack_of_lf1_frm8)
    lf1_optionmenu3.grid(row=1, column=2)
    lf1_optionmenu3.config(font=mid_font)
    lf1_frm8 = tk.Frame(labelframe1)
    lf1_label7 = tk.Label(lf1_frm8, text='第', font=mid_font)
    lf1_label7.grid(row=1, column=1)
    lf1_entry4 = tk.Entry(lf1_frm8, width=8, font=mid_font)
    lf1_entry4.grid(row=1, column=2)
    lf1_entry4.bind('<KeyRelease>', calculate_information_size)
    lf1_label8 = tk.Label(lf1_frm8, text='至 第', font=mid_font)
    lf1_label8.grid(row=1, column=3)
    lf1_entry5 = tk.Entry(lf1_frm8, width=8, font=mid_font)
    lf1_entry5.grid(row=1, column=4)
    lf1_entry5.bind('<KeyRelease>', calculate_information_size)
    lf1_label9 = tk.Label(lf1_frm8, text='base64字节（含头尾）', font=mid_font)
    lf1_label9.grid(row=1, column=5)

    # 设置隐写的参数（右边的labelframe）

    def drag2(files):
        Tools.dragged_files(files, lf2_entry1)

    def drag3(files):
        Tools.dragged_files(files, lf2_entry2)

    def reset_lf2_entry1_and_lf2_entry2():
        Tools.reset(lf2_entry1)
        Tools.reset(lf2_entry2)

    def lf2_confirm():

        def back_to_first():
            global alive
            alive = False
            time.sleep(0.1)
            # 还要删除临时视频
            Tools.delete_file(temp_video_path)
            try:
                lf2_second_frm.pack_forget()
                lf2_first_frm.pack()
            except Exception:
                pass

        lf2_frm9.pack_forget()
        Tools.reset(lf2_entry9)
        # 首先检查一下视频与logo是否正确，不用检查要隐写的内容，那些可以等到完成之前再确认
        logo_path = Tools.get_path_from_entry(lf2_entry2)
        if os.path.exists(logo_path):
            temp_logo_path = f'_temp_logo{os.path.splitext(logo_path)[-1]}'
            Tools.read_all_and_write_all(logo_path, temp_logo_path)
            try:
                logo_img = cv2.imread(temp_logo_path)
                cv2.imshow('image', logo_img)
            except Exception:
                Tools.delete_file(temp_logo_path)
                messagebox.showerror('图片格式错误', 'logo 图片的格式不正确')
                return 0
            os.remove(temp_logo_path)
            cv2.destroyAllWindows()
        else:
            messagebox.showerror('logo错误', 'logo地址错误')
            return 0

        video_path = Tools.get_path_from_entry(lf2_entry1)
        if os.path.exists(video_path):
            global temp_video_path
            temp_video_path = f'_temp_video{os.path.splitext(video_path)[-1]}'
            Tools.read_all_and_write_all(video_path, temp_video_path)  # 将原视频拷贝一份至程序所在路径下的temp_video_path
            applied = False
            saving = False
            logo_fg = np.zeros(shape=(1, 1, 1))
            mask = np.zeros(shape=(1, 1))
            # 50是根据interval_between_frames是50毫秒定的，其他的变量设定什么初始值是无所谓的
            logo_center_x = logo_center_y = amplitude = interval_between_frames = bg_rows = bg_cols = start = end = time_of_saving_start = 50
            time_used_for_saving_audio = 0

            # 用户点击“应用”或点击视频画面时会调用这个函数
            def apply():
                # 此函数会对logo进行处理得到logo_fg和用于处理frame的mask
                nonlocal applied, logo_fg, mask, logo_center_x, logo_center_y, amplitude, interval_between_frames
                # 获取一下用户设定的中心点
                try:
                    logo_center_x = eval(lf2_entry4.get())
                    assert isinstance(logo_center_x, int) and 0 <= logo_center_x <= bg_cols
                except Exception:
                    Tools.reset(lf2_entry4)
                    logo_center_x = round(bg_cols / 2)
                    lf2_entry4.insert(0, logo_center_x)
                try:
                    logo_center_y = eval(lf2_entry5.get())
                    assert isinstance(logo_center_y, int) and 0 <= logo_center_y <= bg_rows
                except Exception:
                    Tools.reset(lf2_entry5)
                    logo_center_y = round(bg_rows / 2)
                    lf2_entry5.insert(0, logo_center_y)
                # 再处理一下用户设定的缩放程度
                try:
                    set_resize = eval(lf2_entry6.get())
                    assert (isinstance(set_resize, int) or isinstance(set_resize, float)) and 0 <= set_resize
                except Exception:
                    Tools.reset(lf2_entry6)
                    lf2_entry6.insert(0, '1.0')
                    set_resize = 1.0
                # 再根据用户设定的阈值处理好logo_fg和mask
                if threshold_method.get() == '背景阈值':
                    try:
                        set_threshold = eval(lf2_threshold_entry1.get())
                        assert isinstance(set_threshold, int) and 0 <= set_threshold <= 255
                    except Exception:
                        Tools.reset(lf2_threshold_entry1)
                        lf2_threshold_entry1.insert(0, '230')
                        set_threshold = eval(lf2_threshold_entry1.get())
                    logo_fg, mask = Tools.process_logo_img_according_to_parameters(logo_img, set_resize,
                                                                                   threshold=set_threshold)
                elif threshold_method.get() == '原图':
                    logo_fg, mask = Tools.process_logo_img_according_to_parameters(logo_img, set_resize,
                                                                                   origin=True)
                elif threshold_method.get() == '自适应阈值':
                    adaptiveMethod = cv2.ADAPTIVE_THRESH_MEAN_C if adaptive_method.get() == '平均值' else cv2.ADAPTIVE_THRESH_GAUSSIAN_C
                    thresholdType = cv2.THRESH_BINARY if threshold_type.get() == '二值化' else cv2.THRESH_BINARY_INV
                    try:
                        blockSize = eval(lf2_threshold_entry2.get())
                        assert isinstance(blockSize, int) and blockSize > 0 and blockSize % 2 == 1
                    except Exception:
                        Tools.reset(lf2_threshold_entry2)
                        lf2_threshold_entry2.insert(0, '11')
                        blockSize = eval(lf2_threshold_entry2.get())
                    try:
                        C = eval(lf2_threshold_entry3.get())
                        assert isinstance(C, int)
                    except Exception:
                        Tools.reset(lf2_threshold_entry3)
                        lf2_threshold_entry3.insert(0, '2')
                        C = eval(lf2_threshold_entry3.get())
                    logo_fg, mask = Tools.process_logo_img_according_to_parameters(logo_img, set_resize,
                                                                                   adaptive_method=adaptiveMethod,
                                                                                   threshold_type=thresholdType,
                                                                                   block_size=blockSize, C=C)
                elif threshold_method.get() == "Otsu's二值化算法":
                    if otsu_part.get() == '亮部':
                        logo_fg, mask = Tools.process_logo_img_according_to_parameters(logo_img, set_resize,
                                                                                       Otsus=True,
                                                                                       bright=True)
                    elif otsu_part.get() == '暗部':
                        logo_fg, mask = Tools.process_logo_img_according_to_parameters(logo_img, set_resize,
                                                                                       Otsus=True,
                                                                                       bright=False)
                elif threshold_method.get() == 'logo HSV范围':
                    try:
                        hmin = eval(lf2_threshold_entry4.get())
                        assert isinstance(hmin, int) and 0 <= hmin <= 180
                    except Exception:
                        Tools.reset(lf2_threshold_entry4)
                        lf2_threshold_entry4.insert(0, '26')
                        hmin = eval(lf2_threshold_entry4.get())
                    try:
                        smin = eval(lf2_threshold_entry5.get())
                        assert isinstance(smin, int) and 0 <= smin <= 255
                    except Exception:
                        Tools.reset(lf2_threshold_entry5)
                        lf2_threshold_entry5.insert(0, '43')
                        smin = eval(lf2_threshold_entry5.get())
                    try:
                        vmin = eval(lf2_threshold_entry6.get())
                        assert isinstance(vmin, int) and 0 <= vmin <= 255
                    except Exception:
                        Tools.reset(lf2_threshold_entry6)
                        lf2_threshold_entry6.insert(0, '46')
                        vmin = eval(lf2_threshold_entry6.get())
                    try:
                        hmax = eval(lf2_threshold_entry7.get())
                        assert isinstance(hmax, int) and hmin <= hmax <= 180
                    except Exception:
                        Tools.reset(lf2_threshold_entry7)
                        lf2_threshold_entry7.insert(0, '180')  # 这里不能再填充‘34’了，因为可能会小于hmin
                        hmax = eval(lf2_threshold_entry7.get())
                    try:
                        smax = eval(lf2_threshold_entry8.get())
                        assert isinstance(smax, int) and smin <= smax <= 255
                    except Exception:
                        Tools.reset(lf2_threshold_entry8)
                        lf2_threshold_entry8.insert(0, '255')
                        smax = eval(lf2_threshold_entry8.get())
                    try:
                        vmax = eval(lf2_threshold_entry9.get())
                        assert isinstance(vmax, int) and smin <= vmax <= 255
                    except Exception:
                        Tools.reset(lf2_threshold_entry9)
                        lf2_threshold_entry9.insert(0, '255')
                        vmax = eval(lf2_threshold_entry9.get())
                    lower_threshold = np.array([hmin, smin, vmin])
                    upper_threshold = np.array([hmax, smax, vmax])
                    logo_fg, mask = Tools.process_logo_img_according_to_parameters(logo_img, set_resize,
                                                                                   lower_threshold=lower_threshold,
                                                                                   upper_threshold=upper_threshold)
                # 获取一下用户设定的振幅，可以为0
                try:
                    amplitude = eval(lf2_entry7.get())
                    assert isinstance(amplitude, int) and 5 >= amplitude >= 0
                except Exception:
                    Tools.reset(lf2_entry7)
                    lf2_entry7.insert(0, '2')
                    amplitude = eval(lf2_entry7.get())
                # 处理一下用户设定的播放速度
                if not saving:
                    try:
                        speed = eval(lf2_entry8.get())
                        assert isinstance(speed, int) and 1000 >= speed > 0
                    except Exception:
                        lf2_entry8.insert(0, '20')
                        interval_between_frames = 50
                    else:
                        interval_between_frames = 1000 // speed
                else:
                    interval_between_frames = 1  # 如果处于保存状态，则将帧与帧之间的时间间隔设为1（注意，不能设为0，因为0代表一直等待）

                applied = True

            @Tools.run_as_thread
            def show_video():
                cap = cv2.VideoCapture(temp_video_path)
                retval, frame = cap.read()
                if retval:  # 如果能够正确读取
                    global alive, temp_outvideo_path
                    nonlocal bg_rows, bg_cols, outvideo_path

                    def change_logo_position_and_apply(event, x, y, flags, param):
                        if event == cv2.EVENT_LBUTTONDOWN and not saving:
                            Tools.reset(lf2_entry4)
                            Tools.reset(lf2_entry5)
                            lf2_entry4.insert(0, x)
                            lf2_entry5.insert(0, y)
                            apply()

                    total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 总帧数是从0开始计数的，这有点特别
                    progress_bar['maximum'] = total_frame_count
                    lf2_entry3.config(state='normal')
                    lf2_entry3.insert(0, floor((total_frame_count - 36) / 2))  # 经过测试，这里确实是减36
                    lf2_entry3.config(state='readonly')
                    frame_counter = 0
                    bg_rows, bg_cols, _ = frame.shape
                    # 视频必须先保存在程序所在文件夹，因为opencv不允许路径中含有中文
                    temp_outvideo_path = f'Video_WithLogo.{video_format.get()}'  # 这里是结果视频的临时保存路径
                    if video_format.get() == 'mp4':
                        fourcc = 'mp4v'
                    # elif video_format.get() == 'avi':  # avi格式的视频在音频处理时不支持
                    #     fourcc = 'XVID'
                    outwriter = cv2.VideoWriter(temp_outvideo_path, cv2.VideoWriter_fourcc(*fourcc),
                                                cap.get(cv2.CAP_PROP_FPS), (bg_cols, bg_rows))
                    jumped_to_begin = False
                    alive = True
                    cv2.namedWindow('Video')
                    cv2.setMouseCallback('Video', change_logo_position_and_apply)
                    while alive and retval:
                        if applied:  # 如果用户按下“应用”键，就要对帧添加logo
                            if saving:
                                if not jumped_to_begin:  # 点击保存后，要跳转到第一帧以进行处理和保存
                                    # 不用再检查参数了，因为用户点击保存时已经检查过了
                                    frame_counter = 0
                                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 将当前帧设为第0帧
                                    retval, frame = cap.read()
                                    jumped_to_begin = True
                                    # 将视频跳转到第一帧，然后开始录制。跳转完成后，这一段代码就不需要再执行了
                                if jumped_to_begin:  # 注意这里不能用else
                                    if file_part.get() == '完整文件':
                                        vibration_x, vibration_y = Tools.get_vibration_information(frame_counter,
                                                                                                   amplitude)
                                    elif file_part.get() == '部分文件':
                                        vibration_x, vibration_y = Tools.get_vibration_information(frame_counter,
                                                                                                   amplitude, start,
                                                                                                   end)
                                    Tools.put_logo_according_to_parameters(frame, logo_fg, mask,
                                                                           logo_center_x + vibration_x,
                                                                           logo_center_y + vibration_y)
                                    outwriter.write(frame)
                                    progress_bar['value'] += 1
                                    time_used = round(time.time() - time_of_saving_start)  # 精确到秒
                                    minutes = time_used // 60
                                    seconds = time_used % 60
                                    time_label1.config(text=f"图像：{minutes}分{seconds}秒")
                                    window.update()
                            else:  # 不在saving状态下，默认从头读取隐写信息
                                vibration_x, vibration_y = Tools.get_vibration_information(frame_counter, amplitude)
                                Tools.put_logo_according_to_parameters(frame, logo_fg, mask,
                                                                       logo_center_x + vibration_x,
                                                                       logo_center_y + vibration_y)
                        cv2.imshow('Video', frame)
                        frame_counter += 1
                        retval, frame = cap.read()
                        if not retval:  # 如果已经读到最后一帧可读帧
                            if not saving:
                                frame_counter = 0  # 就从头开始
                                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 将当前帧设为第0帧，用于循环播放视频
                                print('跳转到第一帧')
                                retval, frame = cap.read()
                            else:
                                # 如果处于保存状态，并且保存到最后一帧可读帧的话，就退出视频播放，并且添加音频和把视频移动到用户选择的文件夹下
                                outwriter.release()
                                cv2.destroyAllWindows()
                                audio_label.config(text='正在提取原视频中的音频文件')
                                window.update()

                                @Tools.run_as_thread
                                def counting_time_for_saving_audio():
                                    nonlocal time_used_for_saving_audio
                                    while alive:
                                        time.sleep(1)
                                        time_used_for_saving_audio += 1
                                        minutes = time_used_for_saving_audio // 60
                                        seconds = time_used_for_saving_audio % 60
                                        time_label2.config(text=f'音频：{minutes}分{seconds}秒')

                                counting_time_for_saving_audio()
                                audio_clip = AudioFileClip(temp_video_path)  # temp_video_path = f'_temp_video{os.path.splitext(video_path)[-1]}'
                                audio_clip.write_audiofile('my_audio.wav')  # 将原视频中的音频临时保存在my_audio.wav中
                                dst_video = VideoFileClip(temp_outvideo_path)  # temp_outvideo_path = f'Video_WithLogo.{video_format.get()}'
                                dst_video = dst_video.set_audio(AudioFileClip('my_audio.wav'))  # 为临时结果视频添加音频
                                audio_label.config(text='已完成音频文件的提取，正在合成视频\n等待时间约为上方进度条走过的时间的1.5倍\n时间过长则意味着音频处理可能出错')
                                window.update()
                                if save_path.get() == 'logo图片所在文件夹':
                                    save_dir = os.path.dirname(logo_path)
                                elif save_path.get() == '背景视频所在文件夹':
                                    save_dir = os.path.dirname(video_path)
                                current_time = time.localtime()
                                outvideo_path = ''.join([save_dir, rf"\{os.path.splitext(os.path.basename(video_path))[0][:8].replace('.', '')}..._WithLogo_", str(current_time.tm_mon), 'm', str(current_time.tm_mday), 'd', str(current_time.tm_hour), 'h', str(current_time.tm_min), 'm', str(current_time.tm_sec), 's', '.', video_format.get()])
                                dst_video.write_videofile(outvideo_path, audio_codec='aac')  # 保存合成视频，注意加上参数audio_codec='aac'，否则音频无声音
                                Tools.delete_file(temp_outvideo_path)
                                Tools.delete_file('my_audio.wav')
                                lf2_label16.config(text=f'视频保存在{save_path.get()}中的：')
                                lf2_entry9.insert(0, os.path.basename(outvideo_path))
                                lf2_frm9.pack()
                                break
                        if cv2.waitKey(interval_between_frames) == ord('q') or cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) != 1:
                            outwriter.release()
                            Tools.delete_file(temp_outvideo_path)
                            break
                    print(f'线程进入结束状态alive: {alive}, saving: {saving}')
                    cap.release()
                    cv2.destroyAllWindows()
                    back_to_first()
                else:  # 如果不能正确读取
                    cap.release()
                    back_to_first()
                    messagebox.showerror('视频读取错误', '无法正确读取视频文件')

        else:
            messagebox.showerror('视频错误', '视频地址错误')
            return 0

        def change_grid_of_threshold_parameter_frm(*args):
            stop_apply()
            lf2_threshold_entry1.grid_forget()
            lf2_threshold_optionmenu4.grid_forget()
            adaptive_threshold_frm.grid_forget()
            hsv_threshold_frm.grid_forget()
            hsv_threshold_frm2.grid_forget()
            if threshold_method.get() == '背景阈值':
                lf2_threshold_entry1.grid(row=1, column=2, padx=20)
            elif threshold_method.get() == '原图':
                # 如果是原图的话，就不要进行布局
                pass
            elif threshold_method.get() == '自适应阈值':
                adaptive_threshold_frm.grid(row=2, column=1)
            elif threshold_method.get() == "Otsu's二值化算法":
                lf2_threshold_optionmenu4.grid(row=1, column=2)
            elif threshold_method.get() == 'logo HSV范围':
                hsv_threshold_frm2.grid(row=2, column=1)
                hsv_threshold_frm.grid(row=3, column=1)

        def stop_apply(*args):
            if not saving:  # 如果用户点击了保存，就不要理会用户对参数的修改
                nonlocal applied
                applied = False

        def save():
            nonlocal saving, interval_between_frames, start, end, time_of_saving_start
            # 进行额外的检查，包括信息容量的检查
            try:
                info_size = eval(lf1_entry2.get())
                assert isinstance(info_size, int) and info_size <= eval(lf2_entry3.get())
            except Exception:
                messagebox.showerror('隐写信息不正确', '被隐写的信息大小超过隐写容量或没有输入要隐写的信息')
                return 0
            if file_part.get() == '部分文件':
                start = eval(lf1_entry4.get())  # 这里不用断言了，因为info_size正确的话，start和end肯定都正确
                end = eval(lf1_entry5.get())  # 如果start和end不正确的话，info_size一定不正确
            saving = True
            time_of_saving_start = time.time()
            apply()
            # 然后布局"正在保存"的有关信息
            lf2_frm7.pack_forget()
            lf2_frm8.pack()

        lf2_first_frm.pack_forget()
        lf2_second_frm = tk.Frame(labelframe2)
        lf2_second_frm.pack()
        lf2_frm2 = tk.Frame(lf2_second_frm)
        lf2_frm2.pack()
        lf2_label3 = tk.Label(lf2_frm2, text='隐写容量（base64字节）：', font=mid_font)
        lf2_label3.grid(row=1, column=1)
        lf2_entry3 = tk.Entry(lf2_frm2, width=8, font=mid_font, state='readonly')
        lf2_entry3.grid(row=1, column=2)
        lf2_label4 = tk.Label(lf2_second_frm, text='请在视频上单击logo放置的位置', fg='red', font=mid_font)
        lf2_label4.pack()
        lf2_label5 = tk.Label(lf2_second_frm, text='logo中心点的位置（左上角为原点）：', font=mid_font)
        lf2_label5.pack()
        lf2_frm3 = tk.Frame(lf2_second_frm)
        lf2_frm3.pack()
        lf2_label6 = tk.Label(lf2_frm3, text='x：', font=mid_font)
        lf2_label6.grid(row=1, column=1)
        lf2_entry4 = tk.Entry(lf2_frm3, width=4, font=mid_font)
        lf2_entry4.grid(row=1, column=2)
        lf2_entry4.bind('<KeyRelease>', stop_apply)
        lf2_label7 = tk.Label(lf2_frm3, text='像素  y：', font=mid_font)
        lf2_label7.grid(row=1, column=3)
        lf2_entry5 = tk.Entry(lf2_frm3, width=4, font=mid_font)
        lf2_entry5.grid(row=1, column=4)
        lf2_entry5.bind('<KeyRelease>', stop_apply)
        lf2_label8 = tk.Label(lf2_frm3, text='像素', font=mid_font)
        lf2_label8.grid(row=1, column=5)

        def intro_demarcation():
            intro_window = tk.Toplevel()
            intro_window.geometry(Tools.zoom_size('636x758', zoom))
            intro_window.title('背景与主体的划分方式介绍')
            intro_window.iconbitmap(icon_path)
            iw_text = tk.Text(intro_window, width=46, height=28, font=mid_font)
            iw_text.pack()
            word = '''这是一个抠图功能，可以帮助您快速实现把logo主体从背景上抠下来，这里提供了四种方式可供选择。此外，您也可以选择“原图”选项，从而不进行抠图。

一、背景阈值
    您可以设定一个亮度阈值（取值范围：[0, 255]），所有高于该亮度值的像素点会被抠掉，而低于该亮度值的像素点则会被保留。例如要去除白色背景，则可以把背景阈值设为230左右。

二、自适应阈值
    此方法会将整个图像分为若干个自适应区域，然后在每一个自适应区域内通过平均值或高斯加权计算阈值，如果想要保留每个自适应区域内的亮部，则选用“反向二值化”方法，反之则选用“二值化”方法。
    注意自适应区域的大小必须为奇数。

三、Otsu's二值化算法
    此方法适用于明暗反差较强的图片，此方法会自动找到划分明暗的阈值，你只需要根据需求选择保留亮部或暗部即可

四、logo HSV范围（即logo主体的色相、饱和度、亮度的取值范围）
    此方法适用于logo主体颜色较为单一或亮度较为相近的情况，您可以通过设定要保留的HSV范围，来抠取想要的图像。软件里提供了常见颜色的HSV范围，您可以一键调用它们。\
您也可以在“工具箱”中的“获取图片像素点的HSV值/范围”来获取几种颜色的HSV范围，并把它复制下来，然后通过“一键粘贴”功能使用选择好的范围'''
            iw_text.insert('end', word)

        lf2_frm4 = tk.Label(lf2_second_frm)
        lf2_frm4.pack()
        lf2_label9 = tk.Label(lf2_frm4, text='选择logo主体与背景的划分方式：', font=mid_font)
        lf2_label9.grid(row=1, column=1, padx=5)
        lf2_button3 = tk.Button(lf2_frm4, text='说明', font=mid_font, fg='blue', bd=0, command=intro_demarcation)
        lf2_button3.grid(row=1, column=2, padx=5)
        lf2_frm5 = tk.Frame(lf2_second_frm)
        lf2_frm5.pack()
        threshold_method = tk.StringVar()
        threshold_method.set('背景阈值')
        lf2_threshold_optionmenu1 = tk.OptionMenu(lf2_frm5, threshold_method,
                                                  *('背景阈值', '自适应阈值', "Otsu's二值化算法", 'logo HSV范围', '原图'),
                                                  command=change_grid_of_threshold_parameter_frm)
        lf2_threshold_optionmenu1.grid(row=1, column=1)
        lf2_threshold_optionmenu1.config(font=mid_font)
        # 下面是用户选择‘背景阈值’的界面布局
        lf2_threshold_entry1 = tk.Entry(lf2_frm5, width=3, font=mid_font)
        lf2_threshold_entry1.grid(row=1, column=2, padx=20)
        lf2_threshold_entry1.insert(0, '230')
        lf2_threshold_entry1.bind('<KeyRelease>', stop_apply)
        # 下面是用户选择‘自适应阈值’的界面布局
        adaptive_threshold_frm = tk.Frame(lf2_frm5)  # adaptive_threshold_frm.grid(row=2, column=1)
        lf2_threshold_label1 = tk.Label(adaptive_threshold_frm, text='自适应方法：', font=mid_font)
        lf2_threshold_label1.grid(row=1, column=1)
        adaptive_method = tk.StringVar()
        adaptive_method.set('平均值')
        lf2_threshold_optionmenu2 = tk.OptionMenu(adaptive_threshold_frm, adaptive_method, *('平均值', '高斯加权'),
                                                  command=stop_apply)
        lf2_threshold_optionmenu2.grid(row=1, column=2)
        lf2_threshold_optionmenu2.config(font=mid_font)
        lf2_threshold_label2 = tk.Label(adaptive_threshold_frm, text='阈值类型：', font=mid_font)
        lf2_threshold_label2.grid(row=2, column=1)
        threshold_type = tk.StringVar()
        threshold_type.set('二值化')
        lf2_threshold_optionmenu3 = tk.OptionMenu(adaptive_threshold_frm, threshold_type, *('二值化', '反向二值化'),
                                                  command=stop_apply)
        lf2_threshold_optionmenu3.grid(row=2, column=2)
        lf2_threshold_optionmenu3.config(font=mid_font)
        lf2_threshold_label3 = tk.Label(adaptive_threshold_frm, text='自适应区域的大小：', font=mid_font)
        lf2_threshold_label3.grid(row=3, column=1)
        lf2_threshold_entry2 = tk.Entry(adaptive_threshold_frm, width=3, font=mid_font)
        lf2_threshold_entry2.grid(row=3, column=2)
        lf2_threshold_entry2.bind('<KeyRelease>', stop_apply)
        lf2_threshold_entry2.insert(0, '11')
        lf2_threshold_label4 = tk.Label(adaptive_threshold_frm, text='均值下调值：', font=mid_font)
        lf2_threshold_label4.grid(row=4, column=1)
        lf2_threshold_entry3 = tk.Entry(adaptive_threshold_frm, width=3, font=mid_font)
        lf2_threshold_entry3.grid(row=4, column=2)
        lf2_threshold_entry3.insert(0, '2')
        lf2_threshold_entry3.bind('<KeyRelease>', stop_apply)
        # 下面是用户选择‘Otsu's’二值化算法
        otsu_part = tk.StringVar()
        otsu_part.set('亮部')
        lf2_threshold_optionmenu4 = tk.OptionMenu(lf2_frm5, otsu_part, *('亮部', '暗部'), command=stop_apply)
        lf2_threshold_optionmenu4.config(font=mid_font)  # lf2_threshold_optionmenu4.grid(row=1, column=2)
        # 下面是用户选择‘logo HSV范围’的界面布局
        hsv_threshold_frm2 = tk.Frame(lf2_frm5)  # hsv_threshold_frm2.grid(row=2, column=1)

        def change_hsv(*args):
            stop_apply()
            Tools.reset(lf2_threshold_entry4)
            Tools.reset(lf2_threshold_entry5)
            Tools.reset(lf2_threshold_entry6)
            Tools.reset(lf2_threshold_entry7)
            Tools.reset(lf2_threshold_entry8)
            Tools.reset(lf2_threshold_entry9)
            if color_name.get() == '黄':
                hmin, hmax, smin, smax, vmin, vmax = 26, 34, 43, 255, 46, 255
            elif color_name.get() == '黑':
                hmin, hmax, smin, smax, vmin, vmax = 0, 180, 0, 255, 0, 46
            elif color_name.get() == '灰':
                hmin, hmax, smin, smax, vmin, vmax = 0, 180, 0, 43, 46, 220
            elif color_name.get() == '白':
                hmin, hmax, smin, smax, vmin, vmax = 0, 180, 0, 30, 221, 255
            elif color_name.get() == '红1':
                hmin, hmax, smin, smax, vmin, vmax = 0, 10, 43, 255, 46, 255
            elif color_name.get() == '红2':
                hmin, hmax, smin, smax, vmin, vmax = 156, 180, 43, 255, 46, 255
            elif color_name.get() == '橙':
                hmin, hmax, smin, smax, vmin, vmax = 11, 25, 43, 255, 46, 255
            elif color_name.get() == '绿':
                hmin, hmax, smin, smax, vmin, vmax = 35, 77, 43, 255, 46, 255
            elif color_name.get() == '青':
                hmin, hmax, smin, smax, vmin, vmax = 78, 99, 43, 255, 46, 255
            elif color_name.get() == '蓝':
                hmin, hmax, smin, smax, vmin, vmax = 100, 124, 43, 255, 46, 255
            elif color_name.get() == '紫':
                hmin, hmax, smin, smax, vmin, vmax = 125, 155, 43, 255, 46, 255
            elif color_name.get() == '一键粘贴':
                try:
                    data = pyperclip.paste()
                    pattern = re.findall('\d{1,3},\d{1,3},\d{1,3}~\d{1,3},\d{1,3},\d{1,3}', data)[0]
                    assert len(pattern) == len(data)
                    hmin, smin, vmin, hmax, smax, vmax = data.replace('~', ',').split(',')
                except Exception:
                    messagebox.showerror('读取错误', '无法从剪贴板中读取正确的信息，请使用工具箱中的读取HSV功能')
                    return 0
            lf2_threshold_entry4.insert(0, hmin)
            lf2_threshold_entry5.insert(0, smin)
            lf2_threshold_entry6.insert(0, vmin)
            lf2_threshold_entry7.insert(0, hmax)
            lf2_threshold_entry8.insert(0, smax)
            lf2_threshold_entry9.insert(0, vmax)

        lf2_threshold_label11 = tk.Label(hsv_threshold_frm2, text='可一键调用常见颜色的HSV范围：', font=mid_font)
        lf2_threshold_label11.grid(row=1, column=1)
        color_name = tk.StringVar()
        color_name.set('黄')
        lf2_threshold_optionmenu5 = tk.OptionMenu(hsv_threshold_frm2, color_name,
                                                  *('黄', '黑', '灰', '白', '红1', '红2', '橙', '绿', '青', '蓝', '紫', '一键粘贴'),
                                                  command=change_hsv)
        lf2_threshold_optionmenu5.grid(row=1, column=2)
        lf2_threshold_optionmenu5.config(font=mid_font)
        hsv_threshold_frm = tk.Frame(lf2_frm5)  # hsv_threshold_frm.grid(row=3, column=1)
        lf2_threshold_label5 = tk.Label(hsv_threshold_frm, text='下阈值 H：', font=mid_font)
        lf2_threshold_label5.grid(row=1, column=1)
        lf2_threshold_entry4 = tk.Entry(hsv_threshold_frm, width=3, font=mid_font)
        lf2_threshold_entry4.grid(row=1, column=2)
        lf2_threshold_entry4.insert(0, '26')
        lf2_threshold_label6 = tk.Label(hsv_threshold_frm, text=' S：', font=mid_font)
        lf2_threshold_label6.grid(row=1, column=3)
        lf2_threshold_entry5 = tk.Entry(hsv_threshold_frm, width=3, font=mid_font)
        lf2_threshold_entry5.grid(row=1, column=4)
        lf2_threshold_entry5.insert(0, '43')
        lf2_threshold_label7 = tk.Label(hsv_threshold_frm, text=' V：', font=mid_font)
        lf2_threshold_label7.grid(row=1, column=5)
        lf2_threshold_entry6 = tk.Entry(hsv_threshold_frm, width=3, font=mid_font)
        lf2_threshold_entry6.grid(row=1, column=6)
        lf2_threshold_entry6.insert(0, '46')
        lf2_threshold_label8 = tk.Label(hsv_threshold_frm, text='上阈值 H：', font=mid_font)
        lf2_threshold_label8.grid(row=2, column=1)
        lf2_threshold_entry7 = tk.Entry(hsv_threshold_frm, width=3, font=mid_font)
        lf2_threshold_entry7.grid(row=2, column=2)
        lf2_threshold_entry7.insert(0, '34')
        lf2_threshold_label9 = tk.Label(hsv_threshold_frm, text=' S：', font=mid_font)
        lf2_threshold_label9.grid(row=2, column=3)
        lf2_threshold_entry8 = tk.Entry(hsv_threshold_frm, width=3, font=mid_font)
        lf2_threshold_entry8.grid(row=2, column=4)
        lf2_threshold_entry8.insert(0, '255')
        lf2_threshold_label10 = tk.Label(hsv_threshold_frm, text=' V: ', font=mid_font)
        lf2_threshold_label10.grid(row=2, column=5)
        lf2_threshold_entry9 = tk.Entry(hsv_threshold_frm, width=3, font=mid_font)
        lf2_threshold_entry9.grid(row=2, column=6)
        lf2_threshold_entry9.insert(0, '255')

        lf2_frm6 = tk.Frame(lf2_second_frm)
        lf2_frm6.pack()
        lf2_label10 = tk.Label(lf2_frm6, text='选择logo缩放的程度：', font=mid_font)
        lf2_label10.grid(row=1, column=1)
        lf2_entry6 = tk.Entry(lf2_frm6, width=4, font=mid_font)
        lf2_entry6.grid(row=1, column=2)
        lf2_entry6.insert(0, '1.0')
        lf2_entry6.bind('<KeyRelease>', stop_apply)
        lf2_label11 = tk.Label(lf2_frm6, text='选择logo的振幅：', font=mid_font)
        lf2_label11.grid(row=2, column=1)
        lf2_entry7 = tk.Entry(lf2_frm6, width=4, font=mid_font)
        lf2_entry7.grid(row=2, column=2)
        lf2_entry7.insert(0, '2')
        lf2_entry7.bind('<KeyRelease>', stop_apply)
        lf2_label12 = tk.Label(lf2_frm6, text='像素', font=mid_font)
        lf2_label12.grid(row=2, column=3)
        lf2_label13 = tk.Label(lf2_frm6, text='视频播放速度：', font=mid_font)
        lf2_label13.grid(row=3, column=1)
        lf2_entry8 = tk.Entry(lf2_frm6, width=4, font=mid_font)
        lf2_entry8.grid(row=3, column=2)
        lf2_entry8.insert(0, '20')
        lf2_entry8.bind('<KeyRelease>', stop_apply)
        lf2_label14 = tk.Label(lf2_frm6, text='帧/秒', font=mid_font)
        lf2_label14.grid(row=3, column=3)
        lf2_frm7 = tk.Frame(lf2_second_frm)
        lf2_frm7.pack()
        lf2_button4 = tk.Button(lf2_frm7, text='放弃(Q)', font=mid_font, command=back_to_first)
        lf2_button4.grid(row=1, column=1, padx=10)
        lf2_button5 = tk.Button(lf2_frm7, text='应用', font=mid_font, command=apply)
        lf2_button5.grid(row=1, column=2, padx=10)
        lf2_button6 = tk.Button(lf2_frm7, text='保存', font=mid_font, command=save)
        lf2_button6.grid(row=1, column=3, padx=10)
        lf2_frm8 = tk.Frame(lf2_second_frm)
        lf2_label15 = tk.Label(lf2_frm8, text='正在保存中，请勿进行其他操作\n进度条走完后，还需为视频处理音频\n关闭软件可能造成程序所在文件夹内多出垃圾文件', font=mid_font, fg='red')
        lf2_label15.pack()
        # 再加一个进度条
        progress_frm = tk.Frame(lf2_frm8)
        progress_frm.pack()
        time_label1 = tk.Label(progress_frm, text='图像：0分0秒', font=mid_font)  # 这个Label是为了存每一帧的累计耗时用的
        time_label1.grid(row=1, column=1)
        progress_bar = ttk.Progressbar(progress_frm)
        progress_bar['length'] = 200
        progress_bar['value'] = 0
        progress_bar.grid(row=1, column=2)
        time_label2 = tk.Label(progress_frm, text='音频：0分0秒', font=mid_font)  # 这个Label是为了展示存声音的耗时用的
        time_label2.grid(row=1, column=3)
        audio_label = tk.Label(lf2_frm8, text=' ', font=mid_font)  # 这个label是为了展示音频保存进度的
        audio_label.pack()

        show_video()

    def open_outvideo():
        if os.path.exists(outvideo_path):
            os.system('start ' + outvideo_path)
        else:
            messagebox.showerror('视频不存在', '结果已被删除或移动')

    outvideo_path = 'N/A'
    labelframe2 = tk.LabelFrame(frm, text='设置隐写的参数', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_first_frm = tk.Frame(labelframe2)
    lf2_first_frm.pack()
    lf2_label1 = tk.Label(lf2_first_frm, text='请拖入背景视频或输入地址：', font=mid_font)
    lf2_label1.pack()
    lf2_entry1 = tk.Entry(lf2_first_frm, width=43, font=mid_font)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=drag2)
    lf2_label2 = tk.Label(lf2_first_frm, text='请拖入logo图片或输入地址：', font=mid_font)
    lf2_label2.pack()
    lf2_entry2 = tk.Entry(lf2_first_frm, width=43, font=mid_font)
    lf2_entry2.pack()
    hook_dropfiles(lf2_entry2, func=drag3)
    lf2_frm11 = tk.Frame(lf2_first_frm)
    lf2_frm11.pack()
    lf2_label17 = tk.Label(lf2_frm11, text='请选择结果的保存格式：', font=mid_font)
    lf2_label17.grid(row=1, column=1)
    video_format = tk.StringVar()
    video_format.set('mp4')
    lf2_optionmenu1 = tk.OptionMenu(lf2_frm11, video_format, 'mp4')  # 目前测试只发现了支持mp4格式
    lf2_optionmenu1.grid(row=1, column=2)
    lf2_optionmenu1.config(font=mid_font)
    lf2_label18 = tk.Label(lf2_frm11, text='请选择结果的保存位置：', font=mid_font)
    lf2_label18.grid(row=2, column=1)
    save_path = tk.StringVar()
    save_path.set('背景视频所在文件夹')
    lf2_optionmenu2 = tk.OptionMenu(lf2_frm11, save_path, *('背景视频所在文件夹', 'logo图片所在文件夹'))
    lf2_optionmenu2.grid(row=2, column=2)
    lf2_optionmenu2.config(font=mid_font)
    lf2_frm1 = tk.Frame(lf2_first_frm)
    lf2_frm1.pack()
    lf2_button1 = tk.Button(lf2_frm1, text='重置', font=mid_font, command=reset_lf2_entry1_and_lf2_entry2)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm1, text='确定', font=mid_font, command=lf2_confirm)
    lf2_button2.grid(row=1, column=2, padx=20)
    lf2_frm9 = tk.Frame(lf2_first_frm)
    lf2_label16 = tk.Label(lf2_frm9, text='结果保存至...所在文件夹中的', font=mid_font)  # 省略号的内容会根据用户的选择改变
    lf2_label16.pack()
    lf2_entry9 = tk.Entry(lf2_frm9, width=43, font=mid_font)
    lf2_entry9.pack()
    lf2_button7 = tk.Button(lf2_frm9, text='浏览视频', command=open_outvideo, font=mid_font)
    lf2_button7.pack()


def nearest_neighbor():
    # 隐写（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='最近邻插值法隐写图片', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def drag1(files):
        Tools.dragged_files(files, entry1)
        label3.pack_forget()
        frm3.pack_forget()

    def drag2(files):
        Tools.dragged_files(files, entry2)
        label3.pack_forget()
        frm3.pack_forget()

    def lf1_copy():
        Tools.copy(entry4, button5)

    def reset():
        Tools.reset(entry1)
        Tools.reset(entry2)
        label3.pack_forget()
        frm3.pack_forget()

    def confirm():
        nonlocal outpath
        path1 = Tools.get_path_from_entry(entry1)  # 1号代表被隐写的图片
        path2 = Tools.get_path_from_entry(entry2)  # 2号代表载体图片
        frm3.pack_forget()
        if os.path.exists(path1) and os.path.exists(path2):
            label3.config(text='正在处理中，请稍候...')
            label3.pack()
            window.update()
            temp_path1 = f'_temp_path1{os.path.splitext(path1)[-1]}'
            temp_path2 = f'_temp_path2{os.path.splitext(path2)[-1]}'
            Tools.read_all_and_write_all(path1, temp_path1)
            Tools.read_all_and_write_all(path2, temp_path2)
            try:
                pic1 = cv2.imread(temp_path1)
                pic2 = cv2.imread(temp_path2)
                y1, x1, _ = pic1.shape
                y2, x2, _ = pic2.shape
            except Exception:
                Tools.delete_file(temp_path1)
                Tools.delete_file(temp_path2)
                label3.pack_forget()
                messagebox.showerror('图像处理失败', '无法正确读取图片或尺寸不满足要求')
                return 0
            finally:
                Tools.delete_file(temp_path1)
                Tools.delete_file(temp_path2)
            if var1.get() == '1':  # 自动微调尺寸，确保载体图片为隐藏图片的宽高的奇数整数倍，且至少为3倍
                if y2 <= y1:
                    y2 = 3 * y1
                else:
                    y2 = floor(y2 / y1) * y1 if floor(y2 / y1) % 2 == 1 else math.ceil(y2 / y1) * y1
                    if y2 == y1:
                        y2 = 3 * y1
                if x2 <= x1:
                    x2 = 3 * x1
                else:
                    x2 = floor(x2 / x1) * x1 if floor(x2 / x1) % 2 == 1 else math.ceil(x2 / x1) * x1
                    if x2 == x1:
                        x2 = 3 * x1
                pic2 = cv2.resize(pic2, (x2, y2))
            elif var1.get() == '0':  # 如果不微调尺寸，则需要判断一下尺寸是否符合要求
                if x2 < x1 or y2 < y1:
                    label3.pack_forget()
                    messagebox.showerror('载体图片过小', '载体图片太小，无法隐藏需要隐藏的图片')
                    return 0
            step_x, step_y = x2 / x1, y2 / y1
            for i in range(0, x1):
                for j in range(0, y1):  # 遍历小图片的每一个像素
                    x, y = int(i * step_x + step_x * 0.5), int(j * step_y + step_y * 0.5)
                    # 找到隐藏图片的某一个像素点应该放在载体图片的哪一个位置
                    pic2[y, x] = pic1[j, i]
            temp_outpath = f'_{x1}_{y1}_hidden_pixel{os.path.splitext(path2)[-1]}'
            Tools.reset(entry3)
            cv2.imwrite(temp_outpath, pic2)  # 先写入软件所在文件夹
            outpath = os.path.join(os.path.splitext(path2)[0]+temp_outpath)  # 再将结果保存至载体图片所在文件夹中
            Tools.read_all_and_write_all(temp_outpath, outpath)
            Tools.delete_file(temp_outpath)
            label3.config(text=f'结果保存至载体图片所在文件夹中的：')
            entry3.insert('end', os.path.basename(outpath))
            entry4.config(state='normal')
            Tools.reset(entry4)
            entry4.insert('end', f'{x1}*{y1}')
            entry4.config(state='readonly')
            frm3.pack()
        else:
            label3.pack_forget()
            messagebox.showerror('图像读取失败', '图像地址不正确，无法读取')

    def open_pic():
        if os.path.exists(outpath):
            os.system(outpath)
        else:
            messagebox.showerror('图片不存在', '结果已被删除或移动')

    def intro_resize():
        intro_window = tk.Toplevel()
        intro_window.title("自动微调尺寸介绍")
        intro_window.geometry(Tools.zoom_size('636x758', zoom))
        intro_window.iconbitmap(icon_path)
        iw_text = tk.Text(intro_window, width=46, height=28, font=mid_font)
        iw_text.pack()
        word = '''    由于载体图片的宽高是隐藏图片宽高的奇数整数倍时，可以减少解读时的图片失真情况。

    所以您可以选择勾选自动微调尺寸。软件会自动微调载体图片的尺寸，使得载体图片的宽高为待隐藏图片宽高的奇数整数倍，且至少为3倍。'''
        iw_text.insert('end', word)

    outpath = 'N/A'
    label1 = tk.Label(labelframe1, text='请拖入需要被隐藏的图片或输入地址：', font=mid_font)
    label1.pack()
    entry1 = tk.Entry(labelframe1, width=43, font=mid_font)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)
    label2 = tk.Label(labelframe1, text='请拖入一张载体图片来隐藏上面的图片：', font=mid_font)
    label2.pack()
    entry2 = tk.Entry(labelframe1, width=43, font=mid_font)
    entry2.pack()
    hook_dropfiles(entry2, func=drag2)
    frm1 = tk.Frame(labelframe1)
    frm1.pack()
    var1 = tk.StringVar()
    var1.set('1')
    cb1 = tk.Checkbutton(frm1, text='自动微调尺寸', variable=var1, onvalue='1', offvalue='0', font=mid_font)
    cb1.grid(row=1, column=1)
    intro_button = tk.Button(frm1, text='说明', fg='blue', command=intro_resize, bd=0, font=mid_font)
    intro_button.grid(row=1, column=2)
    frm2 = tk.Frame(labelframe1)
    frm2.pack()
    button1 = tk.Button(frm2, text='重置', font=mid_font, command=reset)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm2, text='确定', font=mid_font, command=confirm)
    button2.grid(row=1, column=2, padx=20)
    label3 = tk.Label(labelframe1, text='   ', font=mid_font)
    frm3 = tk.Frame(labelframe1)
    entry3 = tk.Entry(frm3, width=43, font=mid_font)
    entry3.pack()
    frm4 = tk.Frame(frm3)
    frm4.pack()
    label4 = tk.Label(frm4, text='恢复被隐藏图片的密码为：', font=mid_font)
    label4.grid(row=1, column=1, padx=5)
    button5 = tk.Button(frm4, text='复制', font=mid_font, fg=colors[ind], command=lf1_copy)
    button5.grid(row=1, column=2, padx=5)
    entry4 = tk.Entry(frm3, width=43, font=mid_font, state='readonly')
    entry4.pack()
    button4 = tk.Button(frm3, text='浏览结果', font=mid_font, command=open_pic)
    button4.pack()

    # 读取（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='最近邻插值法读取图片', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变

    def lf2_drag1(files):
        Tools.dragged_files(files, lf2_entry1)
        lf2_label3.pack_forget()
        lf2_frm2.pack_forget()
        Tools.clean_all_widget(lf2_frm2_2)

    def lf2_reset():
        Tools.reset(lf2_entry1)
        Tools.reset(lf2_entry2)
        lf2_label3.pack_forget()
        lf2_frm2.pack_forget()
        Tools.clean_all_widget(lf2_frm2_2)

    def lf2_confirm(*args):
        nonlocal out_path2
        pic_path = Tools.get_path_from_entry(lf2_entry1)
        lf2_frm2.pack_forget()
        if os.path.exists(pic_path):
            lf2_label3.config(text='正在处理中，请稍候...')
            lf2_label3.pack()
            window.update()
            temp_pic_path = f'_temp_pic_path{os.path.splitext(pic_path)[-1]}'
            Tools.read_all_and_write_all(pic_path, temp_pic_path)
            pwd = lf2_entry2.get().strip()
            try:
                pic = cv2.imread(temp_pic_path)
                pic_height, pic_width, _ = pic.shape
                assert re.match(r'^\d+\*\d+$', pwd)
                x, y = [int(i) for i in pwd.split('*')]
                assert x < pic_width and y < pic_height
                dst = cv2.resize(pic, (x, y), interpolation=cv2.INTER_LINEAR)
                temp_outpath = f'temp{os.path.splitext(pic_path)[-1]}'
                cv2.imwrite(temp_outpath, dst)
                out_path2 = os.path.splitext(pic_path)[0]+'_revealed'+os.path.splitext(pic_path)[-1]
                Tools.read_all_and_write_all(temp_outpath, out_path2)
                Tools.delete_file(temp_outpath)
                lf2_label3.config(text='结果保存至载体图片所在文件夹中的：')
                Tools.reset(lf2_entry3)
                lf2_entry3.insert('end', os.path.basename(out_path2))
                lf2_frm2.pack()
                Tools.clean_all_widget(lf2_frm2_2)
                window.update()
                lf2_open_pic()
            except Exception:
                lf2_label3.pack_forget()
                messagebox.showerror('解读失败', '密码格式不正确或该图片的尺寸无法被解读')
            finally:
                Tools.delete_file(temp_pic_path)
        else:
            lf2_label3.pack_forget()
            messagebox.showerror('图像读取失败', '图像地址不正确，无法读取')

    def lf2_open_pic():
        if os.path.exists(out_path2):
            os.system(out_path2)
        else:
            messagebox.showerror('图片不存在', '结果已被删除或移动')

    def lf2_remove_result():
        Tools.remove_file_or_dir(out_path2, lf2_frm2_2)

    out_path2 = 'N/A'
    lf2_label1 = tk.Label(labelframe2, text='请拖入需要解读的图片或输入地址：', font=mid_font)
    lf2_label1.pack()
    lf2_entry1 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=lf2_drag1)
    lf2_label2 = tk.Label(labelframe2, text='请输入恢复被隐藏图片的密码：', font=mid_font)
    lf2_label2.pack()
    lf2_entry2 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry2.pack()
    lf2_entry2.bind('<Return>', lf2_confirm)
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_button2 = tk.Button(lf2_frm1, text='重置', command=lf2_reset, font=mid_font)
    lf2_button2.grid(row=1, column=1, padx=20)
    lf2_button3 = tk.Button(lf2_frm1, text='确定', command=lf2_confirm, font=mid_font)
    lf2_button3.grid(row=1, column=2, padx=20)
    lf2_label3 = tk.Label(labelframe2, text='   ', font=mid_font)
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_entry3 = tk.Entry(lf2_frm2, width=43, font=mid_font)
    lf2_entry3.pack()
    lf2_frm2_1 = tk.Frame(lf2_frm2)
    lf2_frm2_1.pack()
    lf2_button5 = tk.Button(lf2_frm2_1, text='浏览结果', font=mid_font, command=lf2_open_pic)
    lf2_button5.grid(row=1, column=1, padx=10)
    lf2_button6 = tk.Button(lf2_frm2_1, text='阅后即焚', font=mid_font, command=lf2_remove_result)
    lf2_button6.grid(row=1, column=2, padx=10)
    lf2_frm2_2 = tk.Frame(lf2_frm2)
    lf2_frm2_2.pack()


def read_video_logo():
    # 定位识别对象（左边的labelframe）
    labelframe1 = tk.LabelFrame(frm, text='定位识别对象', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()

    def drag1(files):
        Tools.dragged_files(files, lf1_frm1_entry1)

    def reset_lf1_entry1():
        Tools.reset(lf1_frm1_entry1)

    def lf1_frm1_confirm():
        global temp_video_path

        def back_to_first():
            global alive
            alive = False
            time.sleep(0.2)  # 等待0.2秒是为了解除对temp_video_path文件的占用
            # 还要删除临时视频
            Tools.delete_file(temp_video_path)
            try:
                lf1_frm2.pack_forget()
                lf1_frm1.pack()
            except Exception:
                pass

        # 先检查一下视频是否正确
        video_path = Tools.get_path_from_entry(lf1_frm1_entry1)
        if os.path.exists(video_path):
            temp_video_path = f'_temp_video{os.path.splitext(video_path)[-1]}'
            Tools.read_all_and_write_all(video_path, temp_video_path)
            Tools.reset(lf2_text1)
            logo_selected = False
            logo = np.zeros((1, 1, 1))  # 用户框选出来的logo图片

            @Tools.run_as_thread
            def show_video():
                cap = cv2.VideoCapture(temp_video_path)
                retval, frame = cap.read()
                if retval:
                    global alive
                    alive = True
                    inv_base64dic = {'[(0, -1), (0, -1)]': '0', '[(0, -1), (-1, -1)]': '1',
                                     '[(0, -1), (-1, 0)]': '2',
                                     '[(0, -1), (-1, 1)]': '3', '[(0, -1), (0, 1)]': '4', '[(0, -1), (1, 1)]': '5',
                                     '[(0, -1), (1, 0)]': '6', '[(0, -1), (1, -1)]': '7',
                                     '[(-1, -1), (0, -1)]': '8',
                                     '[(-1, -1), (-1, -1)]': '9', '[(-1, -1), (-1, 0)]': 'A',
                                     '[(-1, -1), (-1, 1)]': 'B',
                                     '[(-1, -1), (0, 1)]': 'C', '[(-1, -1), (1, 1)]': 'D',
                                     '[(-1, -1), (1, 0)]': 'E',
                                     '[(-1, -1), (1, -1)]': 'F', '[(-1, 0), (0, -1)]': 'G',
                                     '[(-1, 0), (-1, -1)]': 'H',
                                     '[(-1, 0), (-1, 0)]': 'I', '[(-1, 0), (-1, 1)]': 'J', '[(-1, 0), (0, 1)]': 'K',
                                     '[(-1, 0), (1, 1)]': 'L', '[(-1, 0), (1, 0)]': 'M', '[(-1, 0), (1, -1)]': 'N',
                                     '[(-1, 1), (0, -1)]': 'O', '[(-1, 1), (-1, -1)]': 'P',
                                     '[(-1, 1), (-1, 0)]': 'Q',
                                     '[(-1, 1), (-1, 1)]': 'R', '[(-1, 1), (0, 1)]': 'S', '[(-1, 1), (1, 1)]': 'T',
                                     '[(-1, 1), (1, 0)]': 'U', '[(-1, 1), (1, -1)]': 'V', '[(0, 1), (0, -1)]': 'W',
                                     '[(0, 1), (-1, -1)]': 'X', '[(0, 1), (-1, 0)]': 'Y', '[(0, 1), (-1, 1)]': 'Z',
                                     '[(0, 1), (0, 1)]': 'a',
                                     '[(0, 1), (1, 1)]': 'b', '[(0, 1), (1, 0)]': 'c', '[(0, 1), (1, -1)]': 'd',
                                     '[(1, 1), (0, -1)]': 'e',
                                     '[(1, 1), (-1, -1)]': 'f', '[(1, 1), (-1, 0)]': 'g', '[(1, 1), (-1, 1)]': 'h',
                                     '[(1, 1), (0, 1)]': 'i',
                                     '[(1, 1), (1, 1)]': 'j', '[(1, 1), (1, 0)]': 'k', '[(1, 1), (1, -1)]': 'l',
                                     '[(1, 0), (0, -1)]': 'm',
                                     '[(1, 0), (-1, -1)]': 'n', '[(1, 0), (-1, 0)]': 'o', '[(1, 0), (-1, 1)]': 'p',
                                     '[(1, 0), (0, 1)]': 'q',
                                     '[(1, 0), (1, 1)]': 'r', '[(1, 0), (1, 0)]': 's', '[(1, 0), (1, -1)]': 't',
                                     '[(1, -1), (0, -1)]': 'u',
                                     '[(1, -1), (-1, -1)]': 'v', '[(1, -1), (-1, 0)]': 'w',
                                     '[(1, -1), (-1, 1)]': 'x',
                                     '[(1, -1), (0, 1)]': 'y', '[(1, -1), (1, 1)]': 'z', '[(1, -1), (1, 0)]': '+',
                                     '[(1, -1), (1, -1)]': '/', '[(0, 0), (1, 1)]': '=', '[(0, 0), (0, 0)]': ''}
                    frame_rows, frame_cols, _ = frame.shape
                    x_start = y_start = row_begin = row_end = col_begin = col_end = -1
                    frame_copy = copy.deepcopy(frame)

                    def select_location_of_logo(event, x, y, flags, param):
                        nonlocal x_start, y_start, row_begin, row_end, col_begin, col_end, frame_copy, logo
                        if event == cv2.EVENT_LBUTTONDOWN:
                            x_start, y_start = x, y
                        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
                            frame_copy = copy.deepcopy(frame)
                            cv2.rectangle(frame_copy, (x_start, y_start), (x, y),
                                          (randint(0, 255), randint(0, 255), randint(0, 255)), 1)
                        elif event == cv2.EVENT_LBUTTONUP:
                            row_begin = min(y_start, y)
                            row_end = max(y_start, y)
                            col_begin = min(x_start, x)
                            col_end = max(x_start, x)
                            logo = frame_copy[row_begin: row_end, col_begin: col_end]
                            # print(row_begin, row_end, col_begin, col_end)
                            # 接下来是设定要在哪个范围寻找logo
                            row_begin = max(row_begin - 10, 0)
                            row_end = min(row_end + 10, frame_rows)
                            col_begin = max(col_begin - 10, 0)
                            col_end = min(col_end + 10, frame_cols)

                    cv2.namedWindow('Video')
                    cv2.setMouseCallback('Video', select_location_of_logo)
                    frame_count = 1
                    c_mean = n_mean = nw_mean = w_mean = sw_mean = s_mean = se_mean = e_mean = ne_mean = (0, 0)
                    directions = []
                    progress_bar['maximum'] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    while alive and retval:
                        if not logo_selected:
                            cv2.imshow('Video', frame_copy)
                        else:
                            cv2.imshow('Video', frame)
                            print('frame count: ', frame_count)
                            # 注意这里的(x, y)顺序
                            position = Tools.get_logo_position_from_frame(frame, logo,
                                                                          constraint=[(col_begin, row_begin),
                                                                                      (col_end, row_end)])
                            print('position: ', position)
                            # 前36帧负责定位9个方位的位置均值
                            if frame_count <= 36:  # 注意：这里的frame_count是从1开始数的
                                if frame_count % 9 == 1:
                                    c_mean = (c_mean[0] + position[0], c_mean[1] + position[1])
                                elif frame_count % 9 == 2:
                                    n_mean = (n_mean[0] + position[0], n_mean[1] + position[1])
                                elif frame_count % 9 == 3:
                                    nw_mean = (nw_mean[0] + position[0], nw_mean[1] + position[1])
                                elif frame_count % 9 == 4:
                                    w_mean = (w_mean[0] + position[0], w_mean[1] + position[1])
                                elif frame_count % 9 == 5:
                                    sw_mean = (sw_mean[0] + position[0], sw_mean[1] + position[1])
                                elif frame_count % 9 == 6:
                                    s_mean = (s_mean[0] + position[0], s_mean[1] + position[1])
                                elif frame_count % 9 == 7:
                                    se_mean = (se_mean[0] + position[0], se_mean[1] + position[1])
                                elif frame_count % 9 == 8:
                                    e_mean = (e_mean[0] + position[0], e_mean[1] + position[1])
                                elif frame_count % 9 == 0:
                                    ne_mean = (ne_mean[0] + position[0], ne_mean[1] + position[1])
                                if frame_count == 36:
                                    c_mean = (c_mean[0] / 4, c_mean[1] / 4)
                                    n_mean = (n_mean[0] / 4, n_mean[1] / 4)
                                    nw_mean = (nw_mean[0] / 4, nw_mean[1] / 4)
                                    w_mean = (w_mean[0] / 4, w_mean[1] / 4)
                                    sw_mean = (sw_mean[0] / 4, sw_mean[1] / 4)
                                    s_mean = (s_mean[0] / 4, s_mean[1] / 4)
                                    se_mean = (se_mean[0] / 4, se_mean[1] / 4)
                                    e_mean = (e_mean[0] / 4, e_mean[1] / 4)
                                    ne_mean = (ne_mean[0] / 4, ne_mean[1] / 4)
                                    print(c_mean, n_mean, nw_mean, w_mean, sw_mean, s_mean, se_mean, e_mean, ne_mean)
                                    # break
                            # 后面的帧负责读取有效信息
                            else:
                                direction = Tools.close_to_which(position, c_mean, n_mean, nw_mean, w_mean, sw_mean,
                                                                 s_mean, se_mean, e_mean, ne_mean)
                                print('direction: ', direction)
                                if len(directions) == 0:  # 只有directions中一个数据都没有的时候，直接往里加数据即可
                                    directions.append(direction)
                                else:  # 如果directions中有一个数据，那么需要再往里加一个，并进行查表，最后再对directions进行清空
                                    directions.append(direction)
                                    try:
                                        base64char = inv_base64dic[str(directions)]
                                    except Exception:
                                        base64char = '?'
                                    # print(base64char)
                                    lf2_text1.insert('end', base64char)
                                    directions = []
                            retval, frame = cap.read()
                            frame_count += 1
                            progress_bar['value'] += 1
                            window.update()
                        cv2.waitKey(1)
                        if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) != 1:
                            break
                    cv2.destroyAllWindows()
                    cap.release()
                    back_to_first()
                else:
                    cap.release()
                    back_to_first()
                    messagebox.showerror('视频读取错误', '无法正确读取视频文件')

            show_video()

        else:
            messagebox.showerror('视频错误', '视频地址错误')
            return 0

        def lf1_frm2_confirm():
            nonlocal logo_selected
            logo_selected = True
            lf1_frm2_3.pack()

        lf1_frm1.pack_forget()
        lf1_frm2 = tk.Frame(labelframe1)
        lf1_frm2.pack()
        lf1_frm2_label1 = tk.Label(lf1_frm2, text='请框选logo的位置（框住的logo背景越少越好）', font=mid_font, fg='red')
        lf1_frm2_label1.pack()
        lf1_frm2_2 = tk.Frame(lf1_frm2)
        lf1_frm2_2.pack()
        lf1_frm2_button1 = tk.Button(lf1_frm2_2, text='返回上一步', font=mid_font, command=back_to_first)
        lf1_frm2_button1.grid(row=1, column=1, padx=20)
        lf1_frm2_button2 = tk.Button(lf1_frm2_2, text='确定', font=mid_font, command=lf1_frm2_confirm)
        lf1_frm2_button2.grid(row=1, column=2, padx=20)
        lf1_frm2_3 = tk.Frame(lf1_frm2)
        lf1_frm2_label2 = tk.Label(lf1_frm2_3, text='正在识别中，请稍候……', font=mid_font)
        lf1_frm2_label2.pack()
        # 再加一个进度条
        progress_bar = ttk.Progressbar(lf1_frm2_3)
        progress_bar['length'] = 300
        progress_bar['value'] = 1  # 这里直接设为1即可，因为第一帧已经让用户进行设定了
        progress_bar.pack()

    lf1_frm1_label1 = tk.Label(lf1_frm1, text='请拖入需要识别的视频或输入地址：', font=mid_font)
    lf1_frm1_label1.pack()
    lf1_frm1_entry1 = tk.Entry(lf1_frm1, width=43, font=mid_font)
    lf1_frm1_entry1.pack()
    hook_dropfiles(lf1_frm1_entry1, func=drag1)
    lf1_frm1_2 = tk.Frame(lf1_frm1)
    lf1_frm1_2.pack()
    lf1_frm1_button1 = tk.Button(lf1_frm1_2, text='重置', font=mid_font, command=reset_lf1_entry1)
    lf1_frm1_button1.grid(row=1, column=1, padx=20)
    lf1_frm1_button2 = tk.Button(lf1_frm1_2, text='确定', font=mid_font, command=lf1_frm1_confirm)
    lf1_frm1_button2.grid(row=1, column=2, padx=20)

    # 获取到的隐写信息（右边的labelframe）

    def change_format():
        change_window = tk.Toplevel()
        change_window.geometry('1272x758')
        change_window.title('格式转换')
        change_window.iconbitmap(icon_path)

        # 左边的labelframe
        cw_labelframe1 = tk.LabelFrame(change_window, text='需要转换格式的信息：', height=741, width=606, font=mid_font)
        cw_labelframe1.pack(side='left', padx=15, pady=5)
        cw_labelframe1.pack_propagate(0)
        cw_lf1_text1 = tk.Text(cw_labelframe1, width=43, height=27, font=mid_font)
        cw_lf1_text1.pack()
        cw_lf1_text1.insert(1.0, lf2_text1.get(1.0, 'end'))

        # 右边的labelframe
        cw_labelframe2 = tk.LabelFrame(change_window, text='选择转换的格式', height=741, width=606, font=mid_font)
        cw_labelframe2.pack(side='right', padx=15, pady=5)
        cw_labelframe2.pack_propagate(0)
        cw_lf2_frm1 = tk.Frame(cw_labelframe2)
        cw_lf2_frm1.pack()

        def change_pack_of_cw_labelframe2(*args):
            if choice.get() == '文字':
                cw_lf2_label1.grid(row=1, column=2)
                cw_lf2_label2.grid_forget()
                cw_lf2_option_menu2.grid(row=1, column=3)
                cw_lf2_entry1.grid_forget()
                cw_lf2_frm2.pack(pady=9)
                cw_lf2_text1.pack()
                cw_lf2_label3.pack_forget()
                cw_lf2_entry2.pack_forget()
                cw_lf2_button2.pack_forget()
            elif choice.get() == '文件':
                cw_lf2_label1.grid_forget()
                cw_lf2_label2.grid(row=1, column=2)
                cw_lf2_option_menu2.grid_forget()
                cw_lf2_entry1.grid(row=1, column=3)
                cw_lf2_frm2.pack_forget()
                cw_lf2_text1.pack_forget()

        def confirm(*args):
            Tools.reset(cw_lf2_text1)
            cw_lf2_label3.pack_forget()
            cw_lf2_entry2.pack_forget()
            cw_lf2_button2.pack_forget()
            try:
                if rs.get() == '1' and choice.get() == '文字':
                    data_bytes = base64.b64decode(bytes(cw_lf1_text1.get(1.0, 'end').rstrip('\n').replace('?', 'x'), 'utf-8'))
                else:
                    data_bytes = base64.b64decode(bytes(cw_lf1_text1.get(1.0, 'end').rstrip('\n'), 'utf-8'))
            except Exception:
                messagebox.showerror('base64格式错误', '输入的不是正确的base64编码')
                return 0
            if choice.get() == '文字':
                if rs.get() == '0':
                    try:
                        word = data_bytes.decode(encode_format.get())
                    except Exception:
                        word = '转码失败'
                else:
                    re_length = cw_lf1_entry1.get()
                    try:
                        re_length = eval(re_length)
                        assert isinstance(re_length, int) and re_length > 0
                    except Exception:
                        word = '纠错码长度错误，纠错码长度应为正整数'
                        cw_lf2_text1.insert(1.0, word)
                        return 0
                    try:
                        rsc = RSCodec(re_length)
                        decoded_text = rsc.decode(data_bytes)[0]
                    except Exception:
                        cw_lf2_text1.insert('end', '纠错码长度有误或错误过多，无法纠错')
                        return 0
                    try:
                        word = decoded_text.decode(encode_format.get())
                    except Exception:
                        word = '编码错误'
                cw_lf2_text1.insert('end', word)
            elif choice.get() == '文件':
                outpath = f"outcome.{cw_lf2_entry1.get().lstrip('.')}"
                with open(outpath, 'wb') as f:
                    f.write(data_bytes)
                Tools.reset(cw_lf2_entry2)
                cw_lf2_entry2.insert('end', outpath)
                cw_lf2_label3.pack()
                cw_lf2_entry2.pack()
                cw_lf2_button2.pack()

        def open_outcome_dir():
            os.system('start ' + os.getcwd())

        choice = tk.StringVar()
        choice.set('文字')
        cw_lf2_option_menu1 = tk.OptionMenu(cw_lf2_frm1, choice, *('文字', '文件'), command=change_pack_of_cw_labelframe2)
        cw_lf2_option_menu1.config(font=mid_font)
        cw_lf2_option_menu1.grid(row=1, column=1)
        cw_lf2_label1 = tk.Label(cw_lf2_frm1, text='文字的编码方式：', font=mid_font)
        cw_lf2_label1.grid(row=1, column=2)
        cw_lf2_label2 = tk.Label(cw_lf2_frm1, text='文件的后缀名：', font=mid_font)
        encode_format = tk.StringVar()
        encode_format.set('utf-8')
        cw_lf2_option_menu2 = tk.OptionMenu(cw_lf2_frm1, encode_format, *('utf-8', 'gbk'), command=confirm)
        cw_lf2_option_menu2.config(font=mid_font)
        cw_lf2_option_menu2.grid(row=1, column=3)
        cw_lf2_entry1 = tk.Entry(cw_lf2_frm1, width=4, font=mid_font)
        cw_lf2_entry1.bind('<Return>', confirm)
        cw_lf2_button1 = tk.Button(cw_lf2_frm1, text='确定', font=mid_font, command=confirm)
        cw_lf2_button1.grid(row=1, column=4, padx=15)
        cw_lf2_frm2 = tk.Frame(cw_labelframe2)
        cw_lf2_frm2.pack(pady=9)
        rs = tk.StringVar()
        rs.set('0')
        cw_lf1_cb1 = tk.Checkbutton(cw_lf2_frm2, text='去除纠错码', font=mid_font, variable=rs, onvalue='1', offvalue='0')
        cw_lf1_cb1.grid(row=1, column=1, padx=15)
        cw_lf1_label1 = tk.Label(cw_lf2_frm2, text='纠错码长度：', font=mid_font)
        cw_lf1_label1.grid(row=1, column=2)
        cw_lf1_entry1 = tk.Entry(cw_lf2_frm2, width=4, font=mid_font)
        cw_lf1_entry1.grid(row=1, column=3)
        cw_lf1_entry1.bind('<Return>', confirm)
        cw_lf2_text1 = tk.Text(cw_labelframe2, width=43, height=23, font=mid_font)
        cw_lf2_text1.pack()
        cw_lf2_label3 = tk.Label(cw_labelframe2, text='结果保存至程序所在文件夹中的：', font=mid_font)
        cw_lf2_entry2 = tk.Entry(cw_labelframe2, width=43, font=mid_font)
        cw_lf2_button2 = tk.Button(cw_labelframe2, text='打开结果所在的文件夹', font=mid_font, command=open_outcome_dir)
        confirm()

    def copy_result():
        Tools.copy(lf2_text1, lf2_button2)

    labelframe2 = tk.LabelFrame(frm, text='获取到的隐写信息（base64格式）', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)  # 使组件大小不变
    lf2_text1 = tk.Text(labelframe2, width=43, height=25, font=mid_font)
    lf2_text1.pack()
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_button1 = tk.Button(lf2_frm1, text='格式转换', font=mid_font, command=change_format)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm1, text='复制结果', font=mid_font, command=copy_result, fg=colors[ind])
    lf2_button2.grid(row=1, column=2, padx=20)


def get_hsv_value():

    def reset_ff_entry1():
        Tools.reset(ff_entry1)

    def drag1(files):
        Tools.dragged_files(files, ff_entry1)

    def ff_confirm():
        hmin_of_get = smin_of_get = vmin_of_get = hmin_of_discard = smin_of_discard = vmin_of_discard = 255
        hmax_of_get = smax_of_get = vmax_of_get = hmax_of_discard = smax_of_discard = vmax_of_discard = 0
        pic_path = Tools.get_path_from_entry(ff_entry1)
        if os.path.exists(pic_path):
            temp_pic_path = f'_temp_pic{os.path.splitext(pic_path)[-1]}'
            Tools.read_all_and_write_all(pic_path, temp_pic_path)
            cv2.namedWindow('image')
            try:
                pic_img = cv2.imread(temp_pic_path)
                pic_rows, pic_cols, _ = pic_img.shape
                if pic_rows > 900 or pic_cols > 900:
                    zoom = min(900 / pic_rows, 900 / pic_cols)  # 对过大的图片进行缩放
                    pic_img = cv2.resize(pic_img, None, fx=zoom, fy=zoom, interpolation=cv2.INTER_AREA)
                cv2.imshow('image', pic_img)
            except Exception:
                cv2.destroyAllWindows()
                os.remove(temp_pic_path)
                messagebox.showerror('图片格式错误', '图片的格式不正确')
                return 0
            pic_img = cv2.cvtColor(pic_img, cv2.COLOR_BGR2HSV)
            os.remove(temp_pic_path)
        else:
            messagebox.showerror('图片错误', '图片地址错误')
            return 0

        def back_to_first():
            global alive
            alive = False
            cv2.destroyAllWindows()
            try:
                second_frm.pack_forget()
                first_frm.pack()
            except Exception:
                pass

        def clear_record():
            nonlocal hmin_of_get, smin_of_get, vmin_of_get, hmin_of_discard, smin_of_discard, vmin_of_discard, hmax_of_get, smax_of_get, vmax_of_get, hmax_of_discard, smax_of_discard, vmax_of_discard
            hmin_of_get = smin_of_get = vmin_of_get = hmin_of_discard = smin_of_discard = vmin_of_discard = 255
            hmax_of_get = smax_of_get = vmax_of_get = hmax_of_discard = smax_of_discard = vmax_of_discard = 0
            sf_entry2.config(state='normal')
            sf_entry3.config(state='normal')
            sf_entry4.config(state='normal')
            Tools.reset(sf_entry2)
            Tools.reset(sf_entry3)
            Tools.reset(sf_entry4)
            sf_entry2.config(state='readonly')
            sf_entry3.config(state='readonly')
            sf_entry4.config(state='readonly')

        def copy_record():
            Tools.copy(sf_entry2, sf_button3)

        @Tools.run_as_thread
        def listen_closing_img_window():
            while alive:
                if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) != 1:
                    back_to_first()
                time.sleep(0.1)

        global alive
        alive = True
        listen_closing_img_window()
        first_frm.pack_forget()
        second_frm = tk.Frame(frm)
        second_frm.pack()
        sf_label1 = tk.Label(second_frm, text='请在图片上左键点击需要采集的像素点，右键点击需要排除的像素点', font=mid_font, fg='red')
        sf_label1.pack()
        sf_frm1 = tk.Frame(second_frm)
        sf_frm1.pack()
        sf_label2 = tk.Label(sf_frm1, text='当前像素点的HSV值：', font=mid_font)
        sf_label2.grid(row=1, column=1)
        sf_entry1 = tk.Entry(sf_frm1, width=11, font=mid_font, state='readonly')
        sf_entry1.grid(row=1, column=2)
        sf_frm2 = tk.Frame(second_frm)
        sf_frm2.pack()
        sf_frm3 = tk.Frame(sf_frm2)
        sf_frm3.grid(row=1, column=1, padx=10)
        sf_label3 = tk.Label(sf_frm3, text='采集到的像素点的HSV范围：', font=mid_font)
        sf_label3.pack()
        sf_entry2 = tk.Entry(sf_frm3, width=23, font=mid_font, state='readonly')
        sf_entry2.pack()
        sf_frm4 = tk.Frame(sf_frm2)
        sf_frm4.grid(row=1, column=2, padx=10)
        sf_label4 = tk.Label(sf_frm4, text='排除掉的像素点的HSV范围：', font=mid_font)
        sf_label4.pack()
        sf_entry3 = tk.Entry(sf_frm4, width=23, font=mid_font, state='readonly')
        sf_entry3.pack()
        sf_frm5 = tk.Frame(second_frm)
        sf_frm5.pack()
        sf_label5 = tk.Label(sf_frm5, text='采集与排除的区间是否重合：', font=mid_font)
        sf_label5.grid(row=1, column=1)
        sf_entry4 = tk.Entry(sf_frm5, width=10, font=mid_font, state='readonly')
        sf_entry4.grid(row=1, column=2)
        sf_frm6 = tk.Frame(second_frm)
        sf_frm6.pack()
        sf_button1 = tk.Button(sf_frm6, text='返回上一层', command=back_to_first, font=mid_font)
        sf_button1.grid(row=1, column=1, padx=15)
        sf_button2 = tk.Button(sf_frm6, text='清空当前记录', command=clear_record, font=mid_font)
        sf_button2.grid(row=1, column=2, padx=15)
        sf_button3 = tk.Button(sf_frm6, text='复制采集的区间', command=copy_record, font=mid_font, fg=colors[ind])
        sf_button3.grid(row=1, column=3, padx=15)

        def get_hsv_of_pixel(event, x, y, flag, param):
            if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
                h, s, v = pic_img[y, x]
                sf_entry1.config(state='normal')
                Tools.reset(sf_entry1)
                sf_entry1.insert(0, f'{h},{s},{v}')
                sf_entry1.config(state='readonly')
                if event == cv2.EVENT_LBUTTONDOWN:
                    nonlocal hmin_of_get, smin_of_get, vmin_of_get, hmax_of_get, smax_of_get, vmax_of_get
                    hmin_of_get = min(hmin_of_get, h)
                    smin_of_get = min(smin_of_get, s)
                    vmin_of_get = min(vmin_of_get, v)
                    hmax_of_get = max(hmax_of_get, h)
                    smax_of_get = max(smax_of_get, s)
                    vmax_of_get = max(vmax_of_get, v)
                    sf_entry2.config(state='normal')
                    Tools.reset(sf_entry2)
                    sf_entry2.insert(0,
                                     f'{hmin_of_get},{smin_of_get},{vmin_of_get}~{hmax_of_get},{smax_of_get},{vmax_of_get}')
                    sf_entry2.config(state='readonly')
                elif event == cv2.EVENT_RBUTTONDOWN:
                    nonlocal hmin_of_discard, smin_of_discard, vmin_of_discard, hmax_of_discard, smax_of_discard, vmax_of_discard
                    hmin_of_discard = min(hmin_of_discard, h)
                    smin_of_discard = min(smin_of_discard, s)
                    vmin_of_discard = min(vmin_of_discard, v)
                    hmax_of_discard = max(hmax_of_discard, h)
                    smax_of_discard = max(smax_of_discard, s)
                    vmax_of_discard = max(vmax_of_discard, v)
                    sf_entry3.config(state='normal')
                    Tools.reset(sf_entry3)
                    sf_entry3.insert(0,
                                     f'{hmin_of_discard},{smin_of_discard},{vmin_of_discard}~{hmax_of_discard},{smax_of_discard},{vmax_of_discard}')
                    sf_entry3.config(state='readonly')
                if sf_entry3.get() and sf_entry2.get():
                    sf_entry4.config(state='normal')
                    Tools.reset(sf_entry4)
                    if (hmax_of_get < hmin_of_discard or hmax_of_discard < hmin_of_get) and (
                            smax_of_get < smin_of_discard or smax_of_discard < smin_of_get) and (
                            vmax_of_get < vmin_of_discard or vmax_of_discard < vmin_of_get):
                        sf_entry4.insert(0, '区间不重合')
                    else:
                        sf_entry4.insert(0, '区间重合')
                    sf_entry4.config(state='readonly')

        cv2.setMouseCallback('image', get_hsv_of_pixel)

    first_frm = tk.Frame(frm)
    first_frm.pack()
    ff_label1 = tk.Label(first_frm, text='请拖入需要获取HSV值/范围的图片或输入地址：', font=mid_font)
    ff_label1.pack()
    ff_entry1 = tk.Entry(first_frm, width=59, font=mid_font)
    ff_entry1.pack()
    hook_dropfiles(ff_entry1, func=drag1)
    ff_frm1 = tk.Frame(first_frm)
    ff_frm1.pack()
    ff_button1 = tk.Button(ff_frm1, text='重置', command=reset_ff_entry1, font=mid_font)
    ff_button1.grid(row=1, column=1, padx=20)
    ff_button2 = tk.Button(ff_frm1, text='确定', command=ff_confirm, font=mid_font)
    ff_button2.grid(row=1, column=2, padx=20)


def hide_zip():
    def drag1(files):
        Tools.dragged_files(files, entry1)

    def drag2(files):
        Tools.dragged_files(files, entry2)

    label1 = tk.Label(frm, text='请拖入图片或输入地址：', font=mid_font)
    label1.pack()
    entry1 = tk.Entry(frm, width=59, font=mid_font)
    entry1.pack()
    hook_dropfiles(entry1, func=drag1)
    label2 = tk.Label(frm, text='请拖入.zip压缩包或输入地址：', font=mid_font)
    label2.pack()
    entry2 = tk.Entry(frm, width=59, font=mid_font)
    entry2.pack()
    hook_dropfiles(entry2, func=drag2)
    frm1 = tk.Frame(frm)
    frm1.pack()
    label3 = tk.Label(frm1, text='请选择结果保存的目录：', font=mid_font)
    label3.grid(row=1, column=1, padx=10)
    option = tk.StringVar()
    option.set('图片所在文件夹')
    option_menu = tk.OptionMenu(frm1, option, *('图片所在文件夹', '压缩包所在文件夹'))
    option_menu.config(font=mid_font)
    option_menu.grid(row=1, column=2, padx=10)
    frm3 = tk.Frame(frm)
    frm3.pack()

    def _reset():
        Tools.reset(entry1)
        Tools.reset(entry2)

    def process():
        Tools.clean_all_widget(frm4)
        label4 = tk.Label(frm4, text='处理时间可能会较长，请耐心等待', font=mid_font)
        label4.pack()
        window.update()
        label4.destroy()
        pic_path = Tools.get_path_from_entry(entry1)
        zip_path = Tools.get_path_from_entry(entry2)
        if not os.path.exists(pic_path):
            tk.messagebox.showerror(title='路径错误', message='图片地址不正确，请重新输入')
        elif not os.path.exists(zip_path):
            tk.messagebox.showerror(title='路径错误', message='压缩包地址不正确，请重新输入')
        else:
            if option.get() == '图片所在文件夹':
                out_dir = os.path.dirname(pic_path)
            elif option.get() == '压缩包所在文件夹':
                out_dir = os.path.dirname(zip_path)
            pic_basename = os.path.basename(pic_path)
            out_basename = pic_basename[:pic_basename.rindex('.')] + '_WithSecret' + pic_basename[
                                                                                     pic_basename.rindex('.'):]
            out_path = out_dir + '\\' + out_basename
            pic_size = os.path.getsize(pic_path)
            zip_size = os.path.getsize(zip_path)
            with open(pic_path, 'rb') as pic, open(zip_path, 'rb') as zip, open(out_path, 'wb') as outfile:
                Tools.read_and_write(pic, outfile, pic_size)
                Tools.read_and_write(zip, outfile, zip_size)
            label5 = tk.Label(frm4, text=f'隐藏成功，结果保存至{option.get()}内的：', font=mid_font)
            label5.pack()
            entry3 = tk.Entry(frm4, width=59, font=mid_font)
            entry3.insert('end', out_basename)
            entry3.pack()

    button1 = tk.Button(frm3, text='重置文件', font=mid_font, command=_reset)
    button1.grid(row=1, column=1, padx=20)
    button2 = tk.Button(frm3, text='开始隐藏', font=mid_font, command=process)
    button2.grid(row=1, column=2, padx=20)
    frm4 = tk.Frame(frm)
    frm4.pack()


def zero_width_ste():
    # 生成（左边的labelframe)
    labelframe1 = tk.LabelFrame(frm, text='生成', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def cal_len_of_text1(*args):
        lf1_label1.config(text='请输入显示的文字：（长度：{}）'.format(len(lf1_text1.get(1.0, 'end').rstrip('\n'))))

    def cal_len_of_text2(*args):
        lf1_label2.config(text="请输入隐藏的文字：（隐藏后长度：{}）".format(len(zwlib.t2z(lf1_text2.get(1.0, 'end').rstrip('\n')))))

    lf1_label1 = tk.Label(labelframe1, text='请输入显示的文字：（长度：0）', font=mid_font)
    lf1_label1.pack()
    lf1_text1 = tk.Text(labelframe1, width=43, height=7, font=mid_font)
    lf1_text1.pack()
    lf1_text1.bind('<KeyRelease>', cal_len_of_text1)
    lf1_label2 = tk.Label(labelframe1, text='请输入隐藏的文字：（隐藏后长度：0）', font=mid_font)
    lf1_label2.pack()
    lf1_text2 = tk.Text(labelframe1, width=43, height=7, font=mid_font)
    lf1_text2.pack()
    lf1_text2.bind('<KeyRelease>', cal_len_of_text2)
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()
    interval = 5

    def reset1():
        Tools.reset(lf1_text1)
        lf1_label1.config(text='请输入显示的文字：（长度：0）')
        Tools.reset(lf1_text2)
        lf1_label2.config(text='请输入隐藏的文字：（隐藏后长度：0）')
        Tools.reset(lf1_text3)
        lf1_label3.config(text='生成的结果为：（长度：0）')

    def generate():
        Tools.reset(lf1_text3)
        visible = lf1_text1.get(1.0, 'end').rstrip('\n')
        hidden = lf1_text2.get(1.0, 'end').rstrip('\n')
        if mode.get() == '隐写':
            encoded = zwlib.encode(visible, hidden)
        elif mode.get() == '保护':
            window.update()
            hidden2z = zwlib.t2z(hidden)
            word_list = jieba.lcut(visible)
            print('word_list:', word_list)
            start, end = 0, interval
            res_word_list = []
            group = word_list[start: end]
            while group:
                res_word_list.append(''.join(group))
                start += interval
                end += interval
                group = word_list[start: end]
            print('res_word_list:', res_word_list)
            if len(res_word_list) > 1:
                encoded = hidden2z.join(res_word_list)
            else:
                encoded = res_word_list[0] + hidden2z
        lf1_label3.config(text='生成的结果为：（长度：{}）'.format(len(encoded)))
        lf1_text3.insert('end', encoded)

    def copy1():
        Tools.copy(lf1_text3, lf1_button3)

    def intro_mode():
        intro_window2 = tk.Toplevel()
        intro_window2.title("隐写模式介绍")
        intro_window2.geometry(Tools.zoom_size('636x758', zoom))
        intro_window2.iconbitmap(icon_path)
        iw_text = tk.Text(intro_window2, width=46, height=17, font=mid_font)
        iw_text.pack()
        word = f'''    这是在文章中插入零宽度字符的两种不同方式。

    隐写模式：这种模式只会将用于隐写的零宽度字符全都放在第一个明文字符后面。
    
    保护模式：这个模式是用来对文章进行版权保护的，它会在文章中按照设定的规则插入零宽度字符，比如每隔{interval}个中文词组或英文单词插入一次隐写的内容。具体的间隔数量可以在下方设置（要求：正整数），默认为{interval}，注意：空格、换行、标点都算一个词组或单词。这种方法类似与在文章中打上隐形水印，在别人直接照搬文章时，就会留下证据。这种方法的缺点是：由于要进行分词，所以处理较慢。'''
        iw_text.insert('end', word)
        iw_frm1 = tk.Frame(intro_window2)
        iw_frm1.pack()
        iw_label1 = tk.Label(iw_frm1, text='隐写字符之间的间隔词组/单词数量：', font=mid_font)
        iw_label1.grid(row=1, column=1)
        iw_entry1 = tk.Entry(iw_frm1, width=4, font=mid_font)
        iw_entry1.grid(row=1, column=2)
        iw_entry1.insert('end', interval)
        iw_frm2 = tk.Frame(intro_window2)
        iw_frm2.pack()

        def changed(*args):
            global ind
            iw_entry2.config(state='normal')
            Tools.reset(iw_entry2)
            iw_entry2.insert('end', '未保存')
            ind = (ind + 1) % 6
            iw_entry2.config(fg=colors[ind], state='readonly')

        def save():
            global ind
            nonlocal interval
            try:
                interval = eval(iw_entry1.get())
                assert isinstance(interval, int) and interval > 0
            except Exception:
                interval = 5
                Tools.reset(iw_entry1)
                iw_entry1.insert('end', interval)
            iw_entry2.config(state='normal')
            Tools.reset(iw_entry2)
            iw_entry2.insert('end', '已保存')
            ind = (ind + 1) % 6
            iw_entry2.config(fg=colors[ind], state='readonly')

        iw_entry1.bind("<KeyRelease>", changed)
        iw_entry2 = tk.Entry(iw_frm2, width=6, font=mid_font, fg=colors[ind])
        iw_entry2.insert('end', '已保存')
        iw_entry2.config(state='readonly')
        iw_entry2.grid(row=1, column=1, padx=10)
        iw_button1 = tk.Button(iw_frm2, text='确认', font=mid_font, command=save)
        iw_button1.grid(row=1, column=2, padx=10)

    mode = tk.StringVar()
    mode.set('隐写')
    lf1_rb1 = tk.Radiobutton(lf1_frm1, text='隐写', font=mid_font, variable=mode, value='隐写')
    lf1_rb1.grid(row=1, column=1, padx=5)
    lf1_rb2 = tk.Radiobutton(lf1_frm1, text='保护', font=mid_font, variable=mode, value='保护')
    lf1_rb2.grid(row=1, column=2, padx=5)
    lf1_button4 = tk.Button(lf1_frm1, text='说明', bd=0, fg='blue', command=intro_mode, font=mid_font)
    lf1_button4.grid(row=1, column=3, padx=5)
    lf1_button1 = tk.Button(lf1_frm1, text='重置', font=mid_font, command=reset1)
    lf1_button1.grid(row=1, column=4, padx=10)
    lf1_button2 = tk.Button(lf1_frm1, text='生成', font=mid_font, command=generate)
    lf1_button2.grid(row=1, column=5, padx=10)
    lf1_button3 = tk.Button(lf1_frm1, text='复制', font=mid_font, command=copy1, fg=colors[ind])
    lf1_button3.grid(row=1, column=6, padx=10)

    lf1_label3 = tk.Label(labelframe1, text='生成的结果为：（长度：0）', font=mid_font)
    lf1_label3.pack()
    lf1_text3 = tk.Text(labelframe1, width=43, height=7, font=mid_font)
    lf1_text3.pack()

    # 解析（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='解析', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)
    lf2_label1 = tk.Label(labelframe2, text='请输入需要解析的文字', font=mid_font)
    lf2_label1.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=11, font=mid_font)
    lf2_text1.pack()
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack(pady=5)

    def reset2():
        Tools.reset(lf2_text1)
        Tools.reset(lf2_text2)

    def analysis(*args):
        Tools.reset(lf2_text2)
        text = lf2_text1.get(1.0, 'end').rstrip('\n') + 'a'
        zero_width_list = ['‌', '‍', '​', '﻿', '‎', '‏']
        for i in range(len(text)):  # 将文章开头的零宽度字符去掉，因为这些字符可能已经不再完整
            if text[i] not in zero_width_list:
                text = text[i:]
                break
        while True:
            try:
                decoded = zwlib.decode(text)
                assert len(decoded)
            except Exception:
                text = text[1:]
                if not len(text):
                    decoded = '未发现隐写信息'
                    break
            else:
                break
        lf2_text2.insert('end', decoded)

    def copy2():
        Tools.copy(lf2_text2, lf2_button3)

    lf2_button1 = tk.Button(lf2_frm1, text='重置', font=mid_font, command=reset2)
    lf2_button1.grid(row=1, column=1, padx=15)
    lf2_button2 = tk.Button(lf2_frm1, text='解析', font=mid_font, command=analysis)
    lf2_button2.grid(row=1, column=2, padx=15)
    lf2_button3 = tk.Button(lf2_frm1, text='复制', font=mid_font, command=copy2, fg=colors[ind])
    lf2_button3.grid(row=1, column=3, padx=15)
    lf2_label2 = tk.Label(labelframe2, text='解析的结果为：', font=mid_font)
    lf2_label2.pack()
    lf2_text2 = tk.Text(labelframe2, width=43, height=11, font=mid_font)
    lf2_text2.pack()
    lf2_text1.bind("<KeyRelease>", analysis)


def fourier_word():
    # 隐写文字（左边的labelframe)
    labelframe1 = tk.LabelFrame(frm, text='盲水印法隐写文字', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def lf1_drag1(files):
        Tools.dragged_files(files, lf1_entry1)

    def lf1_reset():
        Tools.reset(lf1_entry1)
        Tools.reset(lf1_entry2)
        lf1_entry3.config(state='normal')
        Tools.reset(lf1_entry3)
        lf1_entry3.config(state='readonly')
        Tools.reset(lf1_text1)
        lf1_label3.pack_forget()
        lf1_entry2.pack_forget()
        lf1_frm2.pack_forget()

    def lf1_copy():
        Tools.copy(lf1_entry3, lf1_button3)

    def ste():
        lf1_label3.pack_forget()
        lf1_entry2.pack_forget()
        lf1_frm2.pack_forget()
        back_pic_path = Tools.get_path_from_entry(lf1_entry1)
        if not os.path.exists(back_pic_path):
            messagebox.showerror('地址错误', '图片地址不存在')
            return 0
        temp_path = 'temp_pic' + os.path.splitext(back_pic_path)[-1]
        Tools.read_all_and_write_all(back_pic_path, temp_path)
        bwm1 = WaterMark(password_img=1, password_wm=1)
        try:
            bwm1.read_img(temp_path)
        except Exception:
            Tools.delete_file(temp_path)
            messagebox.showerror('图片错误', '不是正确的图片')
            return 0
        lf1_label3.config(text='正在处理中，请稍候...')
        lf1_label3.pack()
        window.update()
        bwm1.read_wm(lf1_text1.get(1.0, 'end').rstrip('\n'), mode='str')
        temp_out_pic_path = 'embedded.png'
        bwm1.embed(temp_out_pic_path)
        len_wm = len(bwm1.wm_bit)
        out_pic_path = os.path.splitext(back_pic_path)[0]+f'_{len_wm}_embedded'+os.path.splitext(back_pic_path)[-1]
        Tools.read_all_and_write_all(temp_out_pic_path, out_pic_path)
        lf1_label3.config(text='结果已经保存至载体图片所在文件夹中的：')
        Tools.reset(lf1_entry2)
        lf1_entry2.insert('end', os.path.basename(out_pic_path))
        lf1_entry2.pack()
        lf1_frm2.pack()
        lf1_entry3.config(state='normal')
        Tools.reset(lf1_entry3)
        lf1_entry3.insert('end', len_wm)
        lf1_entry3.config(state='readonly')
        Tools.delete_file(temp_path)
        Tools.delete_file(temp_out_pic_path)

    lf1_label1 = tk.Label(labelframe1, text='请拖入一张用于隐藏文字的载体图片或输入地址：', font=mid_font)
    lf1_label1.pack()
    lf1_entry1 = tk.Entry(labelframe1, width=43, font=mid_font)
    lf1_entry1.pack()
    hook_dropfiles(lf1_entry1, func=lf1_drag1)
    lf1_label2 = tk.Label(labelframe1, text='请输入要隐写的文字：', font=mid_font)
    lf1_label2.pack()
    lf1_text1 = tk.Text(labelframe1, width=43, height=17, font=mid_font)
    lf1_text1.pack()
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()
    lf1_button1 = tk.Button(lf1_frm1, text='重置', font=mid_font, command=lf1_reset)
    lf1_button1.grid(row=1, column=1, padx=20)
    lf1_button2 = tk.Button(lf1_frm1, text='隐写', font=mid_font, command=ste)
    lf1_button2.grid(row=1, column=2, padx=20)
    lf1_label3 = tk.Label(labelframe1, text='   ', font=mid_font)
    lf1_entry2 = tk.Entry(labelframe1, width=43, font=mid_font)
    lf1_frm2 = tk.Frame(labelframe1)
    lf1_label4 = tk.Label(lf1_frm2, text='请记住信息提取密码：', font=mid_font)
    lf1_label4.grid(row=1, column=1, padx=5)
    lf1_entry3 = tk.Entry(lf1_frm2, width=8, font=mid_font, state='readonly')
    lf1_entry3.grid(row=1, column=2, padx=5)
    lf1_button3 = tk.Button(lf1_frm2, text='复制', font=mid_font, command=lf1_copy, fg=colors[ind])
    lf1_button3.grid(row=1, column=3, padx=5)

    # 解析（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='盲水印法读取文字', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)

    def lf2_drag1(files):
        Tools.dragged_files(files, lf2_entry1)
        Tools.reset(lf2_text1)

    def lf2_reset():
        Tools.reset(lf2_entry1)
        Tools.reset(lf2_entry2)
        Tools.reset(lf2_text1)

    def lf2_copy():
        Tools.copy(lf2_text1, lf2_button3)

    def extract(*args):
        lf2_label3.config(text='正在提取中，请稍候...')
        Tools.reset(lf2_text1)
        window.update()
        pic_path = Tools.get_path_from_entry(lf2_entry1)
        if not os.path.exists(pic_path):
            lf2_label3.config(text='提取到的信息为：')
            messagebox.showerror('地址错误', '图片地址不存在')
            return 0
        pwd = lf2_entry2.get()
        try:
            pwd = eval(pwd)
            assert isinstance(pwd, int)
        except Exception:
            lf2_label3.config(text='提取到的信息为：')
            messagebox.showerror('信息提取密码格式错误', '信息提取密码格式错误')
            return 0
        bwm1 = WaterMark(password_wm=1, password_img=1)
        temp_path = 'embedded' + os.path.splitext(pic_path)[-1]
        Tools.read_all_and_write_all(pic_path, temp_path)
        try:
            wm_extract = bwm1.extract(temp_path, wm_shape=pwd, mode='str')
        except Exception:
            Tools.delete_file(temp_path)
            lf2_label3.config(text='提取到的信息为：')
            messagebox.showerror('图片错误', '不是正确的图片')
            return 0
        lf2_text1.insert('end', wm_extract)
        Tools.delete_file(temp_path)
        lf2_label3.config(text='提取到的信息为：')

    lf2_label1 = tk.Label(labelframe2, text='请拖入需要解读的图片或输入地址：', font=mid_font)
    lf2_label1.pack()
    lf2_entry1 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=lf2_drag1)
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_label2 = tk.Label(lf2_frm1, text='请输入信息提取密码：', font=mid_font)
    lf2_label2.grid(row=1, column=1, padx=5)
    lf2_entry2 = tk.Entry(lf2_frm1, width=8, font=mid_font)
    lf2_entry2.grid(row=1, column=2, padx=5)
    lf2_entry2.bind('<Return>', extract)
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_button1 = tk.Button(lf2_frm2, text='重置', font=mid_font, command=lf2_reset)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm2, text='提取', font=mid_font, command=extract)
    lf2_button2.grid(row=1, column=2, padx=20)
    lf2_button3 = tk.Button(lf2_frm2, text='复制结果', font=mid_font, command=lf2_copy, fg=colors[ind])
    lf2_button3.grid(row=1, column=3, padx=20)
    lf2_label3 = tk.Label(labelframe2, text='提取到的信息为：', font=mid_font)
    lf2_label3.pack()
    lf2_text1 = tk.Text(labelframe2, width=43, height=20, font=mid_font)
    lf2_text1.pack()


def fourier_pic():
    # 隐写图片（左边的labelframe)
    labelframe1 = tk.LabelFrame(frm, text='盲水印法隐写图片', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe1.pack(side='left', padx=5, pady=5)
    labelframe1.pack_propagate(0)  # 使组件大小不变

    def lf1_drag1(files):
        Tools.dragged_files(files, lf1_entry1)
        lf1_label3.pack_forget()
        lf1_frm2.pack_forget()

    def lf1_drag2(files):
        Tools.dragged_files(files, lf1_entry2)
        lf1_label3.pack_forget()
        lf1_frm2.pack_forget()

    def lf1_reset():
        Tools.reset(lf1_entry1)
        Tools.reset(lf1_entry2)
        Tools.reset(lf1_entry3)
        lf1_entry4.config(state='normal')
        Tools.reset(lf1_entry4)
        lf1_entry4.config(state='readonly')
        lf1_label3.pack_forget()
        lf1_frm2.pack_forget()

    def lf1_copy():
        Tools.copy(lf1_entry4, lf1_button3)

    def open_pic1():
        if os.path.exists(out_path1):
            os.system(out_path1)
        else:
            messagebox.showerror('图片不存在', '结果已被删除或移动')

    def ste():
        nonlocal out_path1
        lf1_label3.pack_forget()
        lf1_frm2.pack_forget()
        back_pic_path = Tools.get_path_from_entry(lf1_entry1)
        if not os.path.exists(back_pic_path):
            messagebox.showerror('地址错误', '载体图片地址不存在')
            return 0
        ste_pic_path = Tools.get_path_from_entry(lf1_entry2)
        if not os.path.exists(ste_pic_path):
            messagebox.showerror('地址错误', '待隐写的图片地址不存在')
            return 0
        bwm1 = WaterMark(password_img=1, password_wm=1)
        temp_path1 = 'temp_pic1' + os.path.splitext(back_pic_path)[-1]
        Tools.read_all_and_write_all(back_pic_path, temp_path1)
        try:
            bwm1.read_img(temp_path1)
        except Exception:
            Tools.delete_file(temp_path1)
            messagebox.showerror('载体图片错误', '不是正确的载体图片')
            return 0
        temp_path2 = 'temp_pic2' + os.path.splitext(ste_pic_path)[-1]
        Tools.read_all_and_write_all(ste_pic_path, temp_path2)
        try:
            bwm1.read_wm(temp_path2)
            height, weight, _ = cv2.imread(temp_path2).shape
        except Exception:
            Tools.delete_file(temp_path1)
            Tools.delete_file(temp_path2)
            messagebox.showerror('待隐写的图片错误', '不是正确的待隐写的图片')
            return 0
        lf1_label3.config(text='正在处理中，请稍候...')
        lf1_label3.pack()
        window.update()
        temp_out_pic_path = f'embedded{os.path.splitext(back_pic_path)[-1]}'
        try:
            bwm1.embed(temp_out_pic_path)
        except Exception as e:
            Tools.delete_file(temp_path1)
            Tools.delete_file(temp_path2)
            Tools.delete_file(temp_out_pic_path)
            lf1_label3.pack_forget()
            messagebox.showerror('超出隐写容量', e)
            return 0
        out_path1 = os.path.splitext(back_pic_path)[0]+f'_{height}_{weight}_embedded'+os.path.splitext(back_pic_path)[-1]
        Tools.read_all_and_write_all(temp_out_pic_path, out_path1)
        lf1_label3.config(text='结果已经保存至载体图片所在文件夹中的：')
        Tools.reset(lf1_entry3)
        lf1_entry3.insert('end', os.path.basename(out_path1))
        lf1_frm2.pack()
        lf1_entry4.config(state='normal')
        Tools.reset(lf1_entry4)
        lf1_entry4.insert('end', f'{height}*{weight}')
        lf1_entry4.config(state='readonly')
        Tools.delete_file(temp_path1)
        Tools.delete_file(temp_path2)
        Tools.delete_file(temp_out_pic_path)

    out_path1 = 'N/A'
    lf1_label2 = tk.Label(labelframe1, text='请拖入需要被隐写的图片或输入地址：', font=mid_font)
    lf1_label2.pack()
    lf1_entry2 = tk.Entry(labelframe1, width=43, font=mid_font)
    lf1_entry2.pack()
    hook_dropfiles(lf1_entry2, func=lf1_drag2)
    lf1_label1 = tk.Label(labelframe1, text='请拖入一张载体图片来隐藏上面的图片：', font=mid_font)
    lf1_label1.pack()
    lf1_entry1 = tk.Entry(labelframe1, width=43, font=mid_font)
    lf1_entry1.pack()
    hook_dropfiles(lf1_entry1, func=lf1_drag1)
    lf1_frm1 = tk.Frame(labelframe1)
    lf1_frm1.pack()
    lf1_button1 = tk.Button(lf1_frm1, text='重置', font=mid_font, command=lf1_reset)
    lf1_button1.grid(row=1, column=1, padx=20)
    lf1_button2 = tk.Button(lf1_frm1, text='隐写', font=mid_font, command=ste)
    lf1_button2.grid(row=1, column=2, padx=20)
    lf1_label3 = tk.Label(labelframe1, text='   ', font=mid_font)
    lf1_frm2 = tk.Frame(labelframe1)
    lf1_entry3 = tk.Entry(lf1_frm2, width=43, font=mid_font)
    lf1_entry3.pack()
    lf1_frm2_1 = tk.Frame(lf1_frm2)
    lf1_frm2_1.pack()
    lf1_label4 = tk.Label(lf1_frm2_1, text='请记住信息提取密码：', font=mid_font)
    lf1_label4.grid(row=1, column=1, padx=5)
    lf1_entry4 = tk.Entry(lf1_frm2_1, width=12, font=mid_font, state='readonly')
    lf1_entry4.grid(row=1, column=2, padx=5)
    lf1_button3 = tk.Button(lf1_frm2_1, text='复制', font=mid_font, command=lf1_copy, fg=colors[ind])
    lf1_button3.grid(row=1, column=3, padx=5)
    lf1_button4 = tk.Button(lf1_frm2, text='浏览结果', font=mid_font, command=open_pic1)
    lf1_button4.pack()

    # 解析（右边的labelframe）
    labelframe2 = tk.LabelFrame(frm, text='盲水印法读取图片', height=Tools().height, width=Tools().width, font=mid_font)
    labelframe2.pack(side='right', padx=5, pady=5)
    labelframe2.pack_propagate(0)
    out_pic_path = ...

    def lf2_drag1(files):
        Tools.dragged_files(files, lf2_entry1)
        lf2_label3.pack_forget()
        lf2_frm4.pack_forget()
        Tools.clean_all_widget(lf2_frm4_1)

    def lf2_reset():
        Tools.reset(lf2_entry1)
        Tools.reset(lf2_entry2)
        lf2_label3.pack_forget()
        lf2_frm4.pack_forget()
        Tools.clean_all_widget(lf2_frm4_1)

    def open_pic2():
        if os.path.exists(out_pic_path):
            os.system(out_pic_path)
        else:
            messagebox.showerror('图片不存在', '图片不存在或已被移动')

    def lf2_remove_result():
        Tools.remove_file_or_dir(out_pic_path, lf2_frm4_1)

    def extract(*args):
        nonlocal out_pic_path
        lf2_label3.config(text='正在提取中，请稍候...')
        lf2_label3.pack()
        lf2_frm4.pack_forget()
        Tools.clean_all_widget(lf2_frm4_1)
        window.update()
        pic_path = Tools.get_path_from_entry(lf2_entry1)
        if not os.path.exists(pic_path):
            lf2_label3.pack_forget()
            messagebox.showerror('地址错误', '图片地址不存在')
            return 0
        try:
            pwd = lf2_entry2.get()
            assert re.match(r'^\d+\*\d+$', pwd)
            height, width = [eval(i) for i in pwd.split('*')]
            assert isinstance(height, int) and isinstance(width, int)
        except Exception:
            lf2_label3.pack_forget()
            messagebox.showerror('信息提取密码格式错误', '信息提取密码格式应为“数字*数字”')
            return 0
        temp_path = 'embedded' + os.path.splitext(pic_path)[-1]
        Tools.read_all_and_write_all(pic_path, temp_path)
        temp_out_path = 'extracted' + os.path.splitext(pic_path)[-1]
        bwm1 = WaterMark(password_img=1, password_wm=1)
        try:
            bwm1.extract(filename=temp_path, wm_shape=(height, width), out_wm_name=temp_out_path)
        except Exception:
            lf2_label3.pack_forget()
            Tools.delete_file(temp_path)
            Tools.delete_file(temp_out_path)
            messagebox.showerror('图片错误', '不是正确的图片')
            return 0
        out_pic_path = os.path.join(os.path.splitext(pic_path)[0]+'_extracted'+os.path.splitext(pic_path)[-1])
        Tools.read_all_and_write_all(temp_out_path, out_pic_path)
        Tools.delete_file(temp_path)
        Tools.delete_file(temp_out_path)
        lf2_label3.config(text='图片已提取至载体图片所在文件夹中的：')
        Tools.reset(lf2_entry3)
        lf2_entry3.insert('end', os.path.basename(out_pic_path))
        lf2_frm4.pack()
        window.update()
        open_pic2()

    lf2_label1 = tk.Label(labelframe2, text='请拖入需要解读的图片或输入地址：', font=mid_font)
    lf2_label1.pack()
    lf2_entry1 = tk.Entry(labelframe2, width=43, font=mid_font)
    lf2_entry1.pack()
    hook_dropfiles(lf2_entry1, func=lf2_drag1)
    lf2_frm1 = tk.Frame(labelframe2)
    lf2_frm1.pack()
    lf2_label2 = tk.Label(lf2_frm1, text='请输入信息提取密码：', font=mid_font)
    lf2_label2.grid(row=1, column=1, padx=5)
    lf2_entry2 = tk.Entry(lf2_frm1, width=12, font=mid_font)
    lf2_entry2.grid(row=1, column=2, padx=5)
    lf2_entry2.bind('<Return>', extract)
    lf2_frm2 = tk.Frame(labelframe2)
    lf2_frm2.pack()
    lf2_button1 = tk.Button(lf2_frm2, text='重置', font=mid_font, command=lf2_reset)
    lf2_button1.grid(row=1, column=1, padx=20)
    lf2_button2 = tk.Button(lf2_frm2, text='提取', font=mid_font, command=extract)
    lf2_button2.grid(row=1, column=2, padx=20)
    lf2_label3 = tk.Label(labelframe2, text='   ', font=mid_font)
    lf2_frm4 = tk.Frame(labelframe2)
    lf2_entry3 = tk.Entry(lf2_frm4, width=43, font=mid_font)
    lf2_entry3.pack()
    lf2_frm5 = tk.Frame(lf2_frm4)
    lf2_frm5.pack()
    lf2_button4 = tk.Button(lf2_frm5, text='浏览结果', font=mid_font, command=open_pic2)
    lf2_button4.grid(row=1, column=1, padx=10)
    lf2_button5 = tk.Button(lf2_frm5, text='阅后即焚', font=mid_font, command=lf2_remove_result)
    lf2_button5.grid(row=1, column=2, padx=10)
    lf2_frm4_1 = tk.Frame(lf2_frm4)
    lf2_frm4_1.pack()
