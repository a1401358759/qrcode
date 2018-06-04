#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import shutil
import qrcode

from PIL import Image
from reportlab.lib.pagesizes import A3, portrait
from reportlab.pdfgen import canvas


# 将二维码附着在base_img上 并输出PDF文件
def generatorQrcode(inPath, outPath):
    BASE_DIR = os.path.dirname(__file__)
    IN_DIR = BASE_DIR + '/' + inPath
    OUT_DIR = BASE_DIR + '/' + outPath

    # 删除output文件夹, 并重新创建
    if os.path.exists(outPath):
        shutil.rmtree(outPath)
    os.mkdir(OUT_DIR)

    # 生成canvas画布
    (width, high) = portrait(A3)
    c = canvas.Canvas('./output.pdf', pagesize=portrait(A3))
    x = 0
    y = high - 130

    files = os.listdir(IN_DIR)
    base_img = Image.open('./base.png')
    region_resize = (120, 120)  # 重新定义二维码尺寸(width, height)
    left = int((base_img.size[0] - region_resize[0]) / 2)
    top = int((base_img.size[1] - region_resize[1]) / 2)
    # left为二维码距离base_image左边的距离, top为上边距, 如果上下不居中 需要手动调整top的值
    box = (left, 110)
    for f in files:
        path = IN_DIR + '/' + f
        if os.path.isfile(path):
            # name = os.path.splitext(f)[0]
            with open(path, 'r') as open_file:
                while True:
                    info = open_file.readline()
                    info = info.strip('\n')
                    if not info:
                        break
                    # 生成二维码
                    qr = qrcode.QRCode(
                        version=None,  # 二维码的大小, int, 1-40(最小值是1，是个12×12的矩阵), 如果让程序自动生成，将值设置为None并使用fit=True参数
                        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 二维码的纠错范围，可以选择4个常量, 默认ERROR_CORRECT_M
                        box_size=10,  # 每个点(方块)中的像素个数
                        border=0  # 二维码距图像外围边框距离, 默认为4
                    )
                    qr.add_data(info)
                    qr.make(fit=True)
                    img = qr.make_image()

                    # 将二维码保存并重新设置大小
                    name = info.split('q=')[1]
                    img_path = OUT_DIR + '/' + name + '.png'  # 图片存储路径
                    img.save(img_path)
                    img = Image.open(img_path)
                    region = img
                    region = region.resize(region_resize)

                    # 将二维码附着在图片上
                    base_img.paste(region, box)
                    base_img.save(img_path)

                    # 图片写入PDF文件
                    x += 5
                    c.drawImage(img_path, x, y, 80, 130)
                    if x > 680:
                        x = 0
                        y -= 135
                    else:
                        x += 80

                    if y < 0:
                        c.showPage()
                        y = high - 130
                    os.remove(img_path)  # 图片写入完成后删除

                c.save()


# 附: 生成二维码时error_correction参数选项及说明
# ERROR_CORRECT_L 7%以下的错误会被纠正
# ERROR_CORRECT_M (default) 15%以下的错误会被纠正
# ERROR_CORRECT_Q 25%以下的错误会被纠正
# ERROR_CORRECT_H. 30%以下的错误会被纠正


# def convert_images_to_pdf(img_path, pdf_path):
#     (width, high) = portrait(A3)
#     c = canvas.Canvas(pdf_path, pagesize=portrait(A3))
#     img_name_list = os.listdir(img_path)
#     x = 0
#     y = high - 130
#     for img_name in img_name_list:
#         x += 5
#         img_file = img_path + os.sep + str(img_name)
#         c.drawImage(img_file, x, y, 80, 130)
#         if x > 680:
#             x = 0
#             y -= 135
#         else:
#             x += 80
#
#         if y < 0:
#             c.showPage()
#             y = high - 130
#     c.save()


if __name__ == '__main__':
    generatorQrcode('input', 'output')
    # convert_images_to_pdf('./output', './output.pdf')
    print 'ok! done!'
