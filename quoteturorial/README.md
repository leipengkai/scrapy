[随机更换User-Agent](https://github.com/hellysmile/fake-useragent)
[tor 隐藏ip](https://stackoverflow.com/questions/45009940/scrapy-with-privoxy-and-tor-how-to-renew-ip)

    pip install toripchanger

使用[scrapyd部署](https://github.com/scrapy/scrapyd)
    
    pip install scrapyd
    pip install scrapyd-client
    vim scrapy.cfg
    启动scrapyd
    cd scrapyd
    scrapyd
    # 查看启动情况
    http://localhost:6800/
    
    #部署Scrapy项目
    cd ../
    scrapyd-deploy instagram -p quoteturorial
    
    # 启动一个爬虫
    curl http://localhost:6800/schedule.json -d project=quoteturorial -d spider=instagram
    # 取消
    curl http://localhost:6800/cancel.json -d project=quoteturorial -d job=fac5bb18d67311e8b5b1f2189813fda2
    curl http://localhost:6800/delproject.json -d project=quoteturorial
[代理ip]
- [scrapy-crawlera](https://github.com/scrapy-plugins/scrapy-crawlera)
- [free-proxy](https://free-proxy-list.net/)
- [西刺代理](http://www.xicidaili.com/)
