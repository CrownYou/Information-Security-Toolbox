import base64
import copy
import re
import math
from math import ceil
from math import floor
import random
from random import randint
from tkinter import ttk
import numpy as np
from windnd import hook_dropfiles
import matplotlib.pyplot as plt
import sympy as sp
from moviepy.editor import VideoFileClip, AudioFileClip
import pyperclip
import binascii
import hashlib
import shutil  # pip install pytest-shutil
import zlib
from Crypto import Random  # pip install pycryptodome
from Crypto.Hash import SHA384
from Crypto.Hash import MD4
from Crypto.Hash import RIPEMD160
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
import threading
import pyautogui as auto  # pip install pyautogui==0.9.50
from tkinter import messagebox
# 上面的是其他文件需要调用的库，打包文件的时候需要用上
import os
import time
import tkinter as tk
import cv2  # pip install opencv-python==4.5.1.48
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher  # pip install pycryptodome
from Crypto.PublicKey import RSA
# pkg = __import__('system_resource', fromlist=['MyEncryption', 'MySteganography', 'ToolKit', 'ToolBox'])
# kit = pkg.ToolKit
# Tools = kit.Tools
# myenc = pkg.MyEncryption
# myste = pkg.MySteganography
# mybox = pkg.ToolBox
from system_resource import MyEncryption as myenc, MySteganography as myste, ToolKit as kit, ToolBox as mybox
from system_resource.ToolKit import Tools
import main