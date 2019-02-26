在本目录下执行
```bash
jupyter notebook –ip=127.0.0.1 &
```

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
