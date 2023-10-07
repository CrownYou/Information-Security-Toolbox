# 信安工具箱简介

这是我在大学期间开发的一款课程项目，这款程序中包括了RSA非对称加解密、数字签名、AES对称加解密、哈希计算和隐写术等多种功能。这个软件使用方便、上手简单旨在为用户提供一系列方便、安全和可靠的数据保护解决方案。

这款加密软件是一款完全脱离网络的应用，这意味着在进行加密之前，数据不会离开您的设备，也不会被传输到任何其他地方。这种安全性确保了您的数据不会被黑客窃取或被其他人访问。因此，无论您是在家里还是在公共场所，您都可以使用这款软件来加密您的数据，确保它们的安全性和隐私性。

程序会经常更新，建议您通过git工具将项目clone到本地，这样可以方便更新。您也可以通过在我的github上（ https://github.com/CrownYou/Information-Security-Toolbox ）留言，或添加我的联系方式（QQ：1147978107），对软件未来的更新与发展提出您宝贵的建议。

下载exe文件的途径：1. QQ群：745373067。2. github该项目界面中的 Releases 功能里下载。

# 使用时注意

1. 注意请不要弄乱文件的相对位置，否则软件运行不了哦。

2. 需要的python环境：经过测试，发现在python3.7解释器上运行时，文本框内无法正确显示emoji符号。但是影响不是很大，其他功能均可正常使用。在python3.11解释器上也没法运行旧版的OpenCV库。**运行建议使用python3.9解释器。

4. 进入 "start.py"所在文件夹，在地址栏输入cmd，按回车，输入下面的指令：

   ```cmd
   pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

5. 配置好环境后，直接运行 “start.py” 或者 “信安工具箱.bat” 即可。您可以为 “信安工具箱.bat” 创建一个快捷方式，这样就可以方便地打开它了。此外，软件内还提供了一个名为“快捷方式图标.ico”的文件，您可以用它作为快捷方式的图标。

6. 程序启动成功后，需要输入登录密码，初始密码为空，直接点击确认即可登录，登录成功后可以修改登录密码。

# 信安工具箱功能介绍

## RSA非对称加密（公钥加密，私钥解密）

可自定义RSA密钥生成的长度；可加解密文字、任意文件、文件夹；可自定义加密文档中的某一部分以实现快速加密。

## RSA数字签名（私钥签名，公钥验签）
可以对文件或文字进行签名，签名的结果可以保存为文件或文字。收件人可以通过数字签名判断发件人的身份。

## AES对称加密
密钥可自定义或随机生成，也可以使用软件内置的DH密钥交换算法，安全地协商临时会话密钥。与RSA加密一样，均可加解密文字、任意文件、文件夹；可自定义加密文档中的某一部分以实现快速加密。AES加密支持CBC和ECB两种模式，以及pkcs7、iso 10126 和 zero padding三种填充方式。

## 哈希计算
软件中包含了超级多哈希算法，包括CRC-32、MD4、MD5、SHA-1、SHA-256、SHA-384、SHA-512、BLAKE2B、RipeMD160、SHA-224算法。
可对文件、文字进行哈希计算。

## 隐写术
软件中包含了许多自创隐写方法，总共包括以下几种：
1. logo振动法：通过视频中logo的振动，来隐藏信息，可以隐藏文件或文字信息。
2. 大图片包藏小图片：将小图片的像素分散排列在大图片中，这样肉眼无法识别小图片的内容，但将大图片缩小至小图片的大小即可观察到小图片。
3. 图片隐藏压缩包：将.zip压缩包藏在图片中，且图片看不出任何问题，但只要将图片的后缀改为.zip就可以读取压缩包中的内容。
4. 透视变换隐藏法：某些平台限制二维码的传播，那么可以对二维码进行透视变换，使之无法被平台识别，但对方只要从设定的角度和位置观察即可识别图中二维码的内容。
5. 零宽度字符隐写术：将信息隐藏在零宽度字符中，可用于传递隐秘信息，也可用于版权保护。
6. 图片盲水印（频域变换隐写术）：能够将文字或图片隐藏在图片中，肉眼难以察觉图片中含有隐藏信息，

## 其他工具

1. 获取像素点的HSV值/范围
2. 强密码生成器
3. base64转码器
4. 反查重+反和谐神器
5. 添加/去除RS纠错码

# 信安工具箱更新文档

## 2023.03.18 版本更新说明
更新了零宽度字符隐写术和反查重工具

## 2023.03.28 版本更新说明

UI界面大更新

新增了文字版权保护和近形字替换功能

## 2023.04.03 版本更新说明

新增了RS纠错码功能

## 2023.04.10 版本更新说明

新增了DH密钥交换算法功能

## 2023.04.24 版本更新说明

新增了将二维码图片隐藏在载体图片中的功能。可以规避平台对二维码的审核，但收信人只要从特定角度扫描即可识别。

## 2023.05.29 版本更新说明

新增了“私钥使用密码”功能，能够保护私钥安全。

## 2023.10.07 版本更新说明

新增了图片盲水印功能。



