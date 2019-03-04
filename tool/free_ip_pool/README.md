## 搭建代理池:proxypool

## [运用部署](./ProxyPool/proxypool/README.md)

## 主要功能模块介绍：
### 1.存储(代理池)模块:[db.py](./ProxyPool/proxypool/db.py)
- 使用[redis的有序集合](http://www.runoob.com/redis/redis-sorted-sets.html)来存储代理ip
- 有序集合使得ip不允许重复以及可以给每个ip一个分数:
    - 新ip,设为10分
    - ip检测成功,设为100分
    - ip检测失败,减1分
    - ip分数达到最低分,删除
### 2.爬取模块:[crawler.py](./ProxyPool/proxypool/crawler.py)
- 使用元类来创建爬取ip对象
- 将爬取到的代理在未检测的情况下,保存到数据库为2的redis
### 3.检测模块:[tester.py](./ProxyPool/proxypool/tester.py)
- 使用asyncio,aiohttp模块来检测代理ip的可用性
- 只保留可用的
### 4.提取模块:[api.py](./ProxyPool/proxypool/api.py)
- 通过使用Flask,来提取redis中可用的代理ip
- 为提取代理ip提供API接口
- 随机得到一个代理ip: http://0.0.0.0:5555/random
### 5.调度模块:[scheduler.py](./ProxyPool/proxypool/scheduler.py)
- 使用多进程去分别启动爬取模块,检测模块,提取模块
### 6.运行项目:[run.py](./ProxyPool/run.py)



