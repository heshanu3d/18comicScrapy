from PIL import Image
from comic18Scrapy.settings import IMAGES_STORE_DIR_NAME
import os
from os.path import abspath, dirname

class ImgSpice:
    path = ""
    spice_num = 10
    pic_type = 'JPEG'
    suffix = '.jpg'
    save_path = ''
    width = 0
    height = 0
    def __init__(self, img_path):
        self.path = img_path

    def open_img(self, img_path):
        img = Image.open(img_path)
        self.width, self.height = img.size
        return img

    def save_img(self, img):
        img.save(self.save_path, self.pic_type)

    def paste_img(self, list):
        if len(list) == 0:
            return
        new_img = Image.new('RGB', (self.width, self.height))
        index = 0
        paste_height = 0
        for img in list:
            w, h = img.size
            new_img.paste(img, (0, paste_height, w, paste_height + h))
            paste_height += h
        self.save_img(new_img)

    def cut_img(self, img):
        width, height = img.size
        item_height = int(height / self.spice_num)
        box_list = []
        for i in range(0, self.spice_num):
            if i != self.spice_num-1:
                box_list.append((0, i * item_height, width, (i + 1) * item_height))
            else:
                box_list.append((0, i * item_height, width, height))
        image_list = [img.crop(box) for box in box_list]
        return image_list

    def generate_save_path(self):
        name_flag = False
        new_path = ''
        for p in self.path.split('\\'):
            if p.rfind(self.suffix) > 0:
                page = p[0:p.rfind(self.suffix)]
                p = '%03d' % int(page) + self.suffix
            new_path += p
            if name_flag == True:
                new_path += '-new'
                name_flag = False
            new_path += '\\'
            if p == IMAGES_STORE_DIR_NAME:
                name_flag = True
        new_path = new_path[:-1]
        self.save_path = new_path
        save_dir = self.save_path[:self.save_path.rfind('\\')]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def spice(self):
        img = self.open_img(self.path)
        img_list = self.cut_img(img)
        img_list.reverse()
        self.generate_save_path()
        self.paste_img(img_list)

# album_dir_path : "D:\\PycharmProjects\\comic18ScrapyOut\\弱點弱点"
class AlbumSpice:
    path = ''
    def __init__(self, album_dir_path):
        self.path = album_dir_path

    def spice(self):
        for p in os.listdir(self.path):
            chapter_path = self.path + '\\' + p
            print(chapter_path)
            chapter = ChapterSpice(chapter_path)
            chapter.spice()

# chp_dir_path : "D:\\PycharmProjects\\comic18ScrapyOut\\弱點弱点\\第57話91"
class ChapterSpice:
    path = ''
    def __init__(self, chp_dir_path):
        self.path = chp_dir_path

    def spice(self):
        for p in os.listdir(self.path):
            img_path = self.path + '\\' + p
            img = ImgSpice(img_path)
            img.spice()

if __name__ == "__main__":
    path = "D:\\PycharmProjects\\comic18ScrapyOut\\弱點弱点"
    instance  = AlbumSpice(path)
    instance.spice()

