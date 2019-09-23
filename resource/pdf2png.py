import os
import fitz
import os


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(path + "create successfully")
    else:  # 如果存在就不管他，可以做一个比较优雅的处理，但是我懒啊
        print("existed")
    return path


origin_dir = "../paper-pdf/"
dest_dir = "../paper-png/"

_list = os.listdir(origin_dir)
for item in _list:
    print(origin_dir + item)
    doc = fitz.open(origin_dir + item)
    target_dir = dest_dir + item.split('.')[0]
    mkdir(target_dir)
    for pg in range(doc.pageCount):
        page = doc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
        zoom_x = 2.0
        zoom_y = 2.0
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(target_dir + '/%s.png' % pg)
