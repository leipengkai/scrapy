爬取用户名,保存为文件和mongodb

    scrapy startproject username
	cd username
	scrapy genspider yimanwu www.yimanwu.com
流程

 - tings.py: mongodb的设置
 - items.py: 定义mongodb的字段
 - pipelines.py: 初始化mongod,解析数据并保存
 - settings: 将pipelines,写入ITEM_PIPELINES设置中
 - 运行爬虫
    	scrapy crawl yimanwu