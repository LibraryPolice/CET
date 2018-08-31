# coding: utf-8
import os
from PIL import Image
from common import *
from sklearn import svm
from numpy import array
from io import BytesIO
from learn import *

classify_dir = "labeled_images"

def classify_croped_image_to_folder(img_list, img_name):
    """通过文件名将块图片存储至指定文件夹"""
    for n, word in enumerate(img_name[:4]):
        if not os.path.exists(classify_dir):
            os.mkdir(classify_dir)
        file_dir = os.path.join(classify_dir, word)
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        img_list[n].save(os.path.join(classify_dir,word,img_name))

def main():
    name_list = os.listdir("images")
    for name in name_list:
        if not name.endswith(".png"):
            continue
        img = Image.open(os.path.join("images",name))
        piece_img_list =do_image_crop(img.copy())
        classify_croped_image_to_folder(piece_img_list, name)
if __name__ == '__main__':
    main()
