#### [安装Anaconda](https://www.anaconda.com/)以及对[Anaconde的简单入门](https://www.leipengkai.com/article/28/)
```bash
# 查看是否成功安装
conda --version
# 在base环境中安装包
pip3 install -U -r requirements.txt
```

### [常用的网页分析库](./parse_tool)

## Scrapy框架

![Scrapy框架](https://ws3.sinaimg.cn/large/006tKfTcgy1g0jw3iz9j4j318q0u0anj.jpg)

- Scrapy架构概览的名词理解
  - **Scrapy Engine**:引擎负责控制数据流在系统中所有组件中流动,并在相应动作发生时触发事件,整个爬虫的调度中心.

  - **调度器(Scheduler)**:调度器从引擎接受request并将他们入队,以便之后引擎请求他们时提供给引擎

  - **下载器(Downloader)**:下载器负责获取页面数据并提供给引擎,而后提供给spider

  * [**Spiders**](#Spiders):Spider是Scrapy用户编写用于分析response并提取item并额外跟进URL以及返回request和item的类
  - **Item**: 定义爬取的数据结构
  * [**Item Pipeline**](#Item-Pipeline):负责处理被spider提取出来的item.典型的处理有清理,验证及持久化(例如存取到数据库中).

  * [**下载器中间件(Downloader middlewares)**](#Downloader-middlewares):下载器中间件是在引擎及下载器之间的特定钩子(specific hook),处理Downloader的输入(request)和输出(response). 其提供了一个简便的机制,通过插入自定义代码来扩展Scrapy功能

  - **Spider中间件(Spider middlewares)**:在引擎及Spider之间的特定钩子(specific hook),处理spider的输入(response)和输出(items及requests)

  * **数据流(Data flow)**
    - 引擎打开一个网站(open a domain),找到处理该网站的Spider并向该spider请求第一个要爬取的URL(s)

    - 引擎从Spider中获取到第一个要爬取的URL并在调度器(Scheduler)以Request调度

    - 引擎向调度器请求下一个要爬取的URL

    - 调度器返回下一个要爬取的URL给引擎,引擎将URL通过下载中间件(请求(request)方向)转发给下载器(Downloader)

    - 一旦页面下载完毕,下载器生成一个该页面的Response,并将其通过下载中间件(返回(response)方向)发送给引擎

    - 引擎从下载器中接收到Response并通过Spider中间件(输入方向)发送给Spider处理

    - Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎

    - 引擎将(Spider返回的)爬取到的Item给Item Pipeline,将(Spider返回的)Request给调度器

    - (从第二步)重复直到调度器中没有更多地request,引擎关闭该网站
- [Scrapy文档](http://scrapy-chs.readthedocs.io/zh_CN/latest/),[english](https://docs.scrapy.org/en/latest/index.html)
- [Scrapy命令行工具](#Scrapy命令行):用于管理Scrapy项目的命令行工具
- [Spiders中的提取数据选择器](./xpath.md)
- [之前的Scrapy理解图](./scrapy.png)

## 爬虫思路顺序
- 新建项目(scrapy startproject xxx):新建一个新的爬虫项目
- 明确目标(编写items.py):明确你想要抓取的目标
- 存储内容(pipelines.py):设计管道存储爬取内容
- 制作爬虫(spiders/xxspider.py):制作爬虫开始爬取网页

## 用到的技术,(xmind中)加上本地的教程
- [mysql数据库以及ORM:SQLAlchemy的使用](./database/learn_mysql/)
- 模块功能清楚分明,逻辑结构清晰,可扩展性强
    - [免费代理ip(元类,redis,aiohttp检测代理ip的可用性)](./tool/free_ip_pool/)
    - [cookies池登录](./tool/cookies_pool/)
- 付费代理ip的使用思路

## 项目介绍
- [usernmae项目](./username/):爬取网名,用来创造虚拟用户


### [Spiders](https://scrapy.readthedocs.io/en/latest/topics/spiders.html)
- 编写爬取网站的规则,来完成爬虫的逻辑,进行网页数据的解析
- 每个spider负责处理一个特定(或一些)网站.其包含了一个用于下载的初始URL如何跟进网页中的链接以及如何分析页面中的内容,提取生成 item 的方法

- name: 用于区别Spider. 该名字必须是唯一的,您不可以为不同的Spider设定相同的名字

- start_urls: 包含了Spider在启动时进行爬取的url列表. 因此,第一个被获取到的页面将是其中之一. 后续的URL则从初始的URL获取到的数据中提取

- start_requests():spider中初始的request是通过调用start_requests()来获取的.start_requests()读取start_urls中的URL,并以parse为回调函数生成 Request.当该request下载完毕并返回时，将生成response，并作为参数传给该回调函数

- parse() 是spider默认的回调函数. 被调用时,每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数. 该方法负责解析返回的数据(response data),提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象

### [Item Pipeline](https://scrapy.readthedocs.io/en/latest/topics/item-pipeline.html)
- 当页面被爬虫解析所需的数据存入Item后,将被发送到项目管道(Pipeline),并经过几个特定的次序处理数据,最后存入本地文件或存入数据库.
- Item Pipeline: 后处理(Post-process),存储爬取的数据,当我们抓取到Item之后,需要进行对它的进一步的处理(指定多个Pipline的先后来层层处理)
- Pipeline的作用:验证或清理爬取的数据,查重,存入数据库
- 每个管道组件的类中的方法:
    - process_item(self, item, spider):必须实现
    - open_spider(self, spider)
    - close_spider(self, spider)
    - from_crawler(cls, crawler)
- 本地[pipelines.py](./quoteturorial/quoteturorial/pipelines.py)文件,包括数据修改,去重,保存到mysql,mongo,以及图片保存

### [Downloader middlewares](https://scrapy.readthedocs.io/en/latest/topics/downloader-middleware.html)
- 下载器中间件按照优先级被调用的：当request从引擎向下载器传递时，数字小的下载器中间件先执行，数字大的后执行；当下载器将response向引擎传递，数字大的下载器中间件先执行，小的后执行。
- 通过设置下载器中间件可以实现爬虫自动更换user-agent,IP,[设置代理](https://www.jianshu.com/p/a94d7de5560f)等功能
- 下载器中间件是个类,类里可以定义方法,例如process_request(),process_response(),process_exception()
    - 参数:process_request(self, request, spider), process_response(self,request, response, spider)
    - 返回值:必须是Response、Request或IgnoreRequest异常(异常的话会由此方法处理:process_exception())
- process_request(self, request, spider)
    - 参数request是个字典,字典里包含了headers、url等信息,可修改User-agent、变换代理
    - 如果根据参数request里的url直接就去做抓取,返回response对象,返回的response对象就会不经过剩下的下载器中间件,直接返回到引擎,然后在spider中做处理
    - 如果对请求做了修改,返回的是request对象,就会(将一次或多次修改后的request对象)重新发回到调度器,等待调度
- 本地[middlewares.py](./quoteturorial/quoteturorial/middlewares.py)文件

### Scrapy命令行
 -  创建项目.抓取目标网站:http://quotes.toscrape.com/

        # scrapy startproject [项目名]
	    scrapy startproject quotetutorial
	    cd quotetutorial
 - 创建spider

        # 创建Spider模板: scrapy genspider + 文件名(爬虫名) + 网址域名
	    scrapy genspider quotes quotes.toscrape.com
        # 创建CrawlSpider模板:它是Spider的子类(派生类)
        # scrapy genspider -t crawl quotes quotes.toscrape.com


 - list返回项目所有spider名称

        scrapy list
 - 编写爬虫规则

	    vim quotetutorial/spiders/quotes.py
 - check检查错误

        scrapy check
 - 查看所有下载的中间件

        scrapy settings --get=DOWNLOADER_MIDDLEWARES
 - 运行爬虫

    	scrapy crawl quotes
        # 也可以指定文件名爬取
        scrapy runspider spiders/quotes.py
 - 定义好Item,Spider后,保存抓取的内容

	    scrapy crawl quotes -o quotes.json # 可以导出多种格式, .jl, .csv, .xml
	    scrapy crawl quotes -o ftp://user:passwd@ip/path/quotes.csv  # 也可以通过ftp服务导出
 - 交互的调试效果:在交互环境中测试提取数据的代码

	    scrapy shell quotes.toscrape.com
		quotes = response.css('.quote')
	    quotes[0]
		quotes[0].css('.text')
		quotes[0].css('.text::text')
		quotes[0].css('.text::text').extract_first()
		response.css('a::attr(href)')
        response.css('a::text')
        response.css('a[href*=image]::text').re_first('Name(.*)')
        response.css('a[href*=image] img::attr(src)').extract()

        # scrapy Selector用法
        response.xpath('//a/text()')
        response.xpath('//a/@href')
        response.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')
 - scrapy 选择器(Selectors): 使用XPath提取网页的数据

        proxychains4  scrapy shell http://doc.scrapy.org/en/latest/_static/selectors-sample1.html
        response.xpath("//a[contains(@href,'image')]")
        response.xpath("//a[contains(@href,'html')]")
        response.xpath("//a[contains(@href,'html')]/@href")
        response.xpath("//a[contains(@href,'image')]/text()")
        response.xpath("//a[contains(@href,'image')]/text()").re('Name:\s*(.*)')
        response.xpath('//*[@class="even"]')

当在一个项目中,有多个爬虫时,要注释掉其它的ITEM_PIPELINES,其它setting.py中的内容好像也要做点改变
