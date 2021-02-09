# -*- coding: utf-8 -*-
from scrapy import cmdline

import sys, os, zipfile,time


def unzip_single(src_file, dest_dir, password = None):
    ''' 解压单个文件到目标文件夹。
    '''
    if password:
        password = password.encode()
    zf = zipfile.ZipFile(src_file)
    try:
        zf.extractall(path=dest_dir, pwd=password)
    except RuntimeError as e:
        print(e)
    zf.close()

def unzip_all(source_dir, dest_dir, password = None):
    if not os.path.isdir(source_dir):    # 如果是单一文件
        unzip_single(source_dir, dest_dir, password)
    else:
        it = os.scandir(source_dir)
        for entry in it:
            if entry.is_file() and os.path.splitext(entry.name)[1]=='.zip' :
                unzip_single(entry.path, dest_dir, password)


if __name__ == "__main__":
    dir_path = os.path.abspath(os.path.join(os.getcwd(), "./Redis-x64-3.2.100"))
    zip_path = os.path.abspath(os.path.join(os.getcwd(), "./Redis-x64-3.2.100.zip"))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        unzip_all(zip_path, dir_path)
    cmd = "start cmd /k %s/redis-server.exe %s/redis.windows.conf" % (dir_path,dir_path)
    os.system(cmd)
    time.sleep(2)
cmdline.execute("scrapy crawl comic18".split())