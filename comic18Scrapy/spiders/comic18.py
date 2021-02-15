# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from comic18Scrapy.items import mangaItem
from scrapy import Request
from fake_useragent import UserAgent
import re


class Comic18Spider(CrawlSpider):
    name = 'comic18'
    # base_website_url = '18comic1.one'
    base_website_url = '18comic.org'
    allowed_domains = [base_website_url]
    # start_urls = ['https://18comic.org/']
    # start_urls = ['https://18comic.org/search/photos?search_query=全彩']
    start_urls = ['https://18comic.org/album/216659/'] #sub
    # start_urls = ['https://18comic.org/album/159976/'] #page
    # start_urls = ['https://18comic.org/photo/143749'] #sub_page

    book_follow_prior = 20000
    pic_download_prior = 0

    rules = (
        # Rule(LinkExtractor(allow=r'18comic.org/search/photos\?search_query=全彩&page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'album/216659'), callback='parse_album', process_request='rule_process_request_modify_prior', follow=True),
        # Rule(LinkExtractor(allow=r'photo/'), callback='parse_subpage', follow=True),
    )

    def parse_album(self, response):
        print(response.url)
        book_name = response.xpath("//div[@itemprop='name']/text()").get().strip()
        if not book_name:
            strtmp = re.findall(r'/album/(\d+)', response.url)
            if strtmp:
                book_name = int(strtmp[0])
        self.logger.debug("book_name:%s\n" % book_name)

        #subname
        subname = response.xpath("//div[@class='episode']//a")
        if len(subname) > 0:
            self.logger.debug("this manga has subpage\n")
            if subname:
                for s in subname:
                    # item = mangaItem()
                    sub_book_name = re.sub('[ \n]','',s.xpath(".//li//text()").get().strip())
                    sub_book_url = s.xpath("./@href").get()
                    self.logger.debug("sub:%s", sub_book_name)
                    self.logger.debug("%s\n", sub_book_url)
                    self.book_follow_prior += 1
                    yield response.follow(sub_book_url, self.parse_subpage, priority = self.book_follow_prior, meta={'dirname':book_name,'subdirname':sub_book_name})
        else:
            # total_page
            total_page = 0
            find_total_page = response.xpath("//div[@class='p-t-5 p-b-5']//text()").getall()
            for t in find_total_page:
                res = re.findall("頁數：(\d+)", t)
                if res:
                    total_page = int(res[0])
                    break
            if total_page == 0:
                self.logger.error("cannot find total_page in %s\n", response.url)
                return
            book_id = re.findall('album/(\d+)', response.url)
            if book_id:
                book_id = book_id[0]
                self.pic_download_prior += 1
                self.logger.info("[%d]%s prior:%d total_page:%s\n" % (int(book_id), book_name, self.pic_download_prior, total_page))
                for i in range(1, total_page + 1):
                    imgurltmp = []
                    imgurltmp.append(
                        "https://img18comic6cgewp.kiseouhgf.info/media/photos/%d/%05d.jpg" % (int(book_id), i))
                    item = mangaItem()
                    item['imgurl'] = imgurltmp
                    item['imgname'] = str(i) + ".jpg"
                    item['dirname'] = book_name
                    item['subdirname'] = ''
                    item['prior'] = self.pic_download_prior
                    yield item
            else:
                self.logger.error("err.cannot find book_id from response.url in %s\n", response.url)
                return

    def parse_subpage(self, response):

        total_page = response.xpath("//div[@id='page_0']//text()").get()
        total_page = int(total_page[total_page.rfind('/')+1:].strip())

        book_id = re.findall('photo/(\d+)',response.url)
        if book_id:
            book_id = int(book_id[0])
        else:
            self.logger.error("err.cannot find book_id from response.url in %s\n", response.url)
            return
        self.pic_download_prior += 1

        print(book_id)
        print(response.meta['dirname'])
        print(self.pic_download_prior)
        print(response.meta['subdirname'])
        print(total_page)

        self.logger.info("[%d]%s/%s prior:%s subpage has %d imgs.\n" % (book_id, response.meta['dirname'], self.pic_download_prior, response.meta['subdirname'], total_page))

        for i in range(1,total_page+1):
            imgurltmp = []
            img_index = "%05d" % i
            img_src_node = response.xpath("//div[@id='%s.jpg']//img" % img_index)
            if img_src_node:
                img_url = img_src_node[0].xpath(".//@data-original").get()
            else:
                print("img_url not found! url:%s, img_index:%d" % (response.url, i))
                continue
            print("img_url : %s" % img_url)
            imgurltmp.append(img_url)

            item = mangaItem()
            item['imgurl'] = imgurltmp
            item['imgname'] = str(i) + ".jpg"
            item['dirname'] = response.meta['dirname']
            item['subdirname'] = response.meta['subdirname']
            item['prior'] = self.pic_download_prior
            yield item

    def rule_process_request_modify_prior(self, request, response):
        self.book_follow_prior += 1
        # request.priority = self.book_follow_prior
        return request