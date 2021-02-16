- # 特性
`支持断点续爬`

`支持全站crawl`

`支持单一画册crawl`

- # 启动:

```python main.py```

如果使用pycharm可以直接运行main.py下的main函数


- # crawl单独一个画册方法
将以下两句中的 album id均填为需要crawl的画册id，既可crawl单独一个画册：
```Rule(LinkExtractor(allow=r'album/216659'), callback='parse_album', process_request='rule_process_request_modify_prior', follow=True)```

```start_urls = ['https://18comic.org/album/216659/']```

- # crawl全站画册方法

去掉规则中的album id：

```Rule(LinkExtractor(allow=r'album/'), callback='parse_album', process_request='rule_process_request_modify_prior', follow=True)```

- # 切片功能
    【图片级】    
    ```path = "D:\\PycharmProjects\\comic18ScrapyOut\\弱點弱点\\第57話91\\001.jpg"```    
    ```img_spi = ImgSpice(path)```    
    ```img_spi.spice()```
    
    【章节级】    
    ```path = "D:\\PycharmProjects\\comic18ScrapyOut\\弱點弱点\\第57話91"```    
    ```chapter_spi = ChapterSpice(path)```    
    ```chapter_spi.spice()```
    
    【画册级】    
    ```path = "D:\\PycharmProjects\\comic18ScrapyOut\\弱點弱点"```    
    ```album_spi = AlbumSpice(path)```    
    ```album_spi.spice()```    


- # 调试方法

1. run/debug configuration中创建新的配置项

2. script path 中填 scrapy 的cmdline.py路径

    如：D:\Python37\Lib\site-packages\scrapy\cmdline.py

3. Parameters 中填脚本启动命令

    如：crawl comic18

4. Working directory 中填项目根目录
    如：D:\PycharmProjects\comic18Scrapy