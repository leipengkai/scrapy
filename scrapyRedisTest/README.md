分布式爬虫的优点
- 充分利用多机器的宽带加速攫取
- 充分利用多机的ip加速攫取速度

需要解决:
- requests队列集中管理
- 去重集中管理

[scrapy-redis](https://github.com/rmax/scrapy-redis)

    pip install redis
    scrapy startproject scrapyRedisTest
    cd scrapyRedisTest
    wget https://github.com/rmax/scrapy-redis/tree/master/src/scrapy_redis

    # 运行爬虫 或者使用pycharm运行main.py，等待输入start_url
    scrapy runspider main.py
    # 再进入rdis客户端,设置start_url
    docker exec -it scrapy_redis_1 bash 
    redis-cli 
    lpush instagram:start_urls https://www.instagram.com/explore/tags/nois7/

    ZRANGEBYSCORE instagram:reqeuests 0 100

    # 暂停与重启
    kill -f xx # 会向进程改善 Kill 信号
    scrapy crawl lagou -s JOBDIR=job_info/001

    telnet 127.0.0.1 6623
    est()
