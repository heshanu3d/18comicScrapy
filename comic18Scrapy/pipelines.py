# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import re

class comic18ScrapyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for imgurl in item['imgurl']:
            yield Request(imgurl, priority=item['prior'], meta={'imgname' :item['imgname'],'dirname':item['dirname'],'subdirname':item['subdirname']})

    def file_path(self, request, response=None, info=None):
        # 接收上面meta传递过来的图片名称
        imgname = request.meta['imgname']
        dirname = request.meta['dirname']
        subdirname = request.meta['subdirname']
        # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
        dirname = re.sub(r'[?？\\*|“"<>:/]', '', dirname)
        subdirname = re.sub(r'[?？\\*|“"<>:/]', '', subdirname)
        filename = ""
        if not subdirname:
            # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
            filename = u'{0}/{1}'.format(dirname, imgname)
        else:
            filename = u'{0}/{1}/{2}'.format(dirname, subdirname, imgname)
        return filename