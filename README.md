### 安装包
    环境:python3.6
    mkvirtualenv scrapy
    workon scrapy
    pip3 install -U -r requirements.txt

### 常用的网页分析库
 - re:Python内置的正则库, [regex简易实例](./regex.ipynb)

 - Urllib:Python内置HTTP库,[urllib简易实例](./urllib.ipynb)

 - Requests:Python实现的简单易用的HTTP库,[requests简易实例](./requests.ipynb)

 - BeautifulSoup:灵活又方便的网页解析库,处理高效,支持多种解析器,利用它有用编写正则表达式即可方便地实现网页信息的提取,[beautifulsoup4简易实例](./beautifulsoup.ipynb)

 - PyQuery:强大又灵活的网页解析库,如果你觉得正则写起来太麻烦,如果你觉得 BeautifulSoup语法太难记,如果你熟悉jQuery语法,那么PyQuery就是你的绝佳选择. [pyquery简易实例](./pyquery.ipynb)

 - lxml:网页DOM选择器,快速定位操作HTML对象,也可以用于XML

 - Selenium:自动化测试工具,支持多种浏览器,爬虫中主要用来解决JavaScript渲染问题以及模拟浏览器点击等事件[selenium简易实例](./selenium.ipynb)

  - 使用selenium需要安装一个对应的浏览器驱动,来模拟真实浏览器加载js,ajax等非静态页面数据


            wget http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
	        unzip chromedriver_linux64.zip
	        chmod +x chromedriver
	        sudo mv -f chromedriver /usr/local/share/chromedriver
	        sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
	        sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

	        # 在ipython3中检查是否安装成功
	        ipython3
	        from selenium import webdriver
	        browser = webdriver.Chrome()
### PySpider框架

	# 安装Pyspider框架
	sudo pip3 install pyspider
	pyspider --help
	# 安装JS渲染的浏览器驱动
	wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
	tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2
	sudo mv  phantomjs-2.1.1-linux-x86_64 /usr/local/share
	sudo ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin
	phantomjs # 在里面编写JS语句

	# 启动pyspider所有组件,并在当前路径下生成data目录
	pyspider all
	# WebUI界面
	http://localhost:5000
	# http://docs.pyspider.org/en/latest/


### Scrapy框架
- [Scrapy文档](http://scrapy-chs.readthedocs.io/zh_CN/latest/),[english](https://docs.scrapy.org/en/latest/index.html)
- [架构概览](./scrapy.png)
  - **Scrapy Engine**:引擎负责控制数据流在系统中所有组件中流动,并在相应动作发生时触发事件,整个爬虫的调度中心.

  - **调度器(Scheduler)**:调度器从引擎接受request并将他们入队,以便之后引擎请求他们时提供给引擎

  - **下载器(Downloader)**:下载器负责获取页面数据并提供给引擎,而后提供给spider

  * **Spiders**:Spider是Scrapy用户编写用于分析response并提取item(即获取到的item)或额外跟进的URL的类.
    - 每个spider负责处理一个特定(或一些)网站.其包含了一个用于下载的初始URL如何跟进网页中的链接以及如何分析页面中的内容,提取生成 item 的方法

    - name: 用于区别Spider. 该名字必须是唯一的,您不可以为不同的Spider设定相同的名字

    - start_urls: 包含了Spider在启动时进行爬取的url列表. 因此,第一个被获取到的页面将是其中之一. 后续的URL则从初始的URL获取到的数据中提取

    - start_requests():spider中初始的request是通过调用start_requests()来获取的.start_requests()读取start_urls中的URL,并以parse为回调函数生成 Request.当该request下载完毕并返回时，将生成response，并作为参数传给该回调函数

    - parse() 是spider默认的回调函数. 被调用时,每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数. 该方法负责解析返回的数据(response data),提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象
  - **Item**: 定义数据结构
  * **Item Pipeline**:负责处理被spider提取出来的item.典型的处理有清理,验证及持久化(例如存取到数据库中).
	- 当页面被爬虫解析所需的数据存入Item后,将被发送到项目管道(Pipeline),并经过几个特定的次序处理数据,最后存入本地文件或存入数据库.

  * **下载器中间件(Downloader middlewares)**:下载器中间件是在引擎及下载器之间的特定钩子(specific hook),处理Downloader传递给引擎的response. 其提供了一个简便的机制,通过插入自定义代码来扩展Scrapy功能
	- 通过设置下载器中间件可以实现爬虫自动更换user-agent,IP,设置代理等功能

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
- 基本概念
  - **命令行工具(Command line tools)**: 学习用于管理Scrapy项目的命令行工具
  - **Items**: 定义爬取的数据
  - **Spiders**: 编写爬取网站的规则,来完成爬虫的逻辑,进行网页数据的解析
  - **选择器(Selectors)**: 使用XPath提取网页的数据
  - **Scrapy终端(Scrapy shell)**: 在交互环境中测试提取数据的代码
  - **Item Loaders**: 使用爬取到的数据填充item
  - **Item Pipeline**: 后处理(Post-process),存储爬取的数据,当我们抓取到Item之后,需要进行对它的进一步的处理(指定多个Pipline的先后来层层处理)

- Scrapy简单命令

 - 抓取目标网站:http://quotes.toscrape.com/. 创建项目

	    scrapy startproject quotetutorial
	    cd quotetutorial
 - 创建spider

	    scrapy genspider quotes quotes.toscrape.com
 - 编写爬虫规则

	    vim quotetutorial/spiders/quotes.py
 - 运行爬虫

    	scrapy crawl quotes
 - 交互的调试效果

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
 - 定义好Item,Spider后,保存抓取的内容

	    scrapy crawl quotes -o quotes.json # 可以导出多种格式, .jl, .csv, .xml
	    scrapy crawl quotes -o ftp://user:passwd@ip/path/quotes.csv  # 也可以通过ftp服务导出
 - 查看所有下载的中间件

        scrapy settings --get=DOWNLOADER_MIDDLEWARES
 - scrapy Selector用法

        proxychains4  scrapy shell http://doc.scrapy.org/en/latest/_static/selectors-sample1.html
        response.xpath("//a[contains(@href,'image')]")
        response.xpath("//a[contains(@href,'html')]")
        response.xpath("//a[contains(@href,'html')]/@href")
        response.xpath("//a[contains(@href,'image')]/text()")
        response.xpath("//a[contains(@href,'image')]/text()").re('Name:\s*(.*)')
        response.xpath('//*[@class="even"]')
