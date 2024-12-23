# 信安工具箱简介

这是我在大学期间开发的一款课程项目，这款程序中包括了隐写术、RSA、ECC非对称加解密、数字签名、AES对称加解密、DH密钥交换算法、Shamir秘密共享算法、CKKS同态加密以及哈希计算等多种功能。这个软件使用方便、上手简单、使用逻辑清晰，旨在为用户提供一系列方便、安全和可靠的数据保护解决方案。

这款加密软件是一款完全脱离网络的应用，这意味着在进行加密之前，数据不会离开您的设备，也不会被传输到任何其他地方。这种安全性确保了您的数据不会被黑客窃取或被其他人访问。因此，无论您是在家里还是在公共场所，您都可以使用这款软件来加密您的数据，确保它们的安全性和隐私性。

程序会经常更新，建议您通过git工具将项目clone到本地，这样可以方便更新。您也可以通过在我的github上（ https://github.com/CrownYou/Information-Security-Toolbox ）留言，或添加我的联系方式（QQ：1147978107）或QQ交流群：745373067，对软件未来的更新与发展提出您宝贵的建议。

下载exe文件的途径：目前由于代码量过大，编译exe时总是报错，暂无exe文件提供，请直接使用源代码。

# 使用时注意

1. 注意请不要弄乱文件的相对位置，否则软件运行不了哦。

2. 需要的python环境：经过测试，发现在python3.7解释器上运行时，文本框内无法正确显示emoji符号。但是影响不是很大，其他功能均可正常使用。在python3.11解释器上也没法运行旧版的OpenCV库。**运行建议使用python3.9解释器**。

3. 安装所需的库：进入 "main.py"所在文件夹，在地址栏输入cmd，按回车，输入下面的指令：

   ```cmd
   pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

4. 配置好环境后，直接运行 “main.py” 或者点击 “信安工具箱.bat” 即可。您可以为 “信安工具箱.bat” 创建一个快捷方式，这样就可以方便地打开它了。此外，软件内还提供了一个名为“快捷方式图标.ico”的文件，您可以用它作为快捷方式的图标。

5. 程序启动成功后，需要输入登录密码，**初始密码为空，直接点击确认即可登录**，登录成功后可以修改登录密码。

# 信安工具箱功能介绍

## RSA非对称加密（公钥加密，私钥解密）

可自定义RSA密钥生成的长度；可加解密文字、任意文件、文件夹；可自定义加密文档中的某一部分以实现快速加密。

## RSA数字签名（私钥签名，公钥验签）
可以对文件或文字进行签名，签名的结果可以保存为文件或文字。收件人可以通过数字签名判断发件人的身份。

## ECC非对称加密
这是一种比RSA算法更加高效、安全的非对称加密算法。

## ECC数字签名（私钥签名，公钥验签）

ECC签名功能和RSA一样，只不过ECC签名需要用ECC的公私钥对。

## AES对称加密
密钥可自定义或随机生成，也可以使用软件内置的**DH密钥交换算法**或**Shamir秘密分享算法**，安全地协商临时会话密钥。与RSA加密一样，均可加解密文字、任意文件、文件夹；可自定义加密文档中的某一部分以实现快速加密。AES加密支持CBC和ECB两种模式，以及pkcs7、iso 10126 和 zero padding三种填充方式。

## CKKS同态加密

CKKS（Cloud Key Encryption and Signing）是一种基于近似学习误差（RLWE）问题的高效同态加密方案，由Cheon等人于2017年提出。它支持浮点向量在密文空间的加减乘运算并保持同态，但只支持有限次乘法的运算。
CKKS同态加密的核心特点:
 \* 近似同态性: 支持浮点向量在密文空间的加减乘运算，但乘法运算存在精度误差，且乘法次数受到限制。
 \* 高计算效率: 基于ring-LWE和BGV方案改进，具有较高的计算效率。
 \* 高安全性: 基于RLWE问题，安全性得到较强的理论证明。
CKKS同态加密的主要应用场景:
 \* 安全多方计算: 支持多个参与者在不共享数据的情况下进行联合计算，保护数据隐私。
 \* 隐私保护机器学习: 支持模型训练和预测过程在加密状态下进行，保护模型和数据隐私。
 \* 云计算安全: 支持云端数据的加密存储和计算，提高数据安全性和隐私性。

## 哈希计算
软件中包含了超级多哈希算法，包括CRC-32、MD4、MD5、SHA-1、SHA-256、SHA-384、SHA-512、BLAKE2B、RipeMD160、SHA-224算法。
可对文件、文字进行哈希计算。

## 隐写术
软件中包含了许多自创隐写方法，总共包括以下几种：
1. logo振动法：通过视频中logo的振动，来隐藏信息，可以隐藏文件或文字信息。
2. 最近邻插值法图像隐写术：将小图片的像素分散排列在大图片中，这样肉眼无法识别小图片的内容，但将大图片缩小至小图片的大小即可观察到小图片。
3. 图片隐藏压缩包：将.zip压缩包藏在图片中，且图片看不出任何问题，但只要将图片的后缀改为.zip就可以读取压缩包中的内容。
4. 透视变换隐藏二维码（人可见，机器不可见）：某些平台限制二维码的传播，那么可以对二维码进行透视变换，使之无法被平台识别，但对方只要从设定的角度和位置观察即可识别图中二维码的内容。
5. 透明度通道隐藏二维码（机器可见，人不可见）：通过对图片的透明度通道和RBG值进行调整，可以使得包含二维码的图片在特定颜色的背景图上无法被肉眼观察到二维码的存在。
6. 表里不一图像隐写术：可以使得一张图片在不同背景颜色下显示出完全不一样的图像。
7. 零宽度字符隐写术：将信息隐藏在零宽度字符中，可用于传递隐秘信息，也可用于版权保护。
8. 图片盲水印（频域变换隐写术）：能够将文字或图片隐藏在图片中，肉眼难以察觉图片中含有隐藏信息。

## 其他工具

1. 获取像素点的HSV值/范围
2. 强密码生成器
3. base64转码器
4. 抗关键字审核工具-零宽度字符、近形字法
5. 抗关键字审核工具-文字纵向排列法
6. 添加/去除RS纠错码
