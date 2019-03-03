搭建代理池:proxypool

主要模块：
1 存储（代理池）db.py
2 获取        crawler.py
3 检测        tester.py
4 提取        api.py



1.存储介绍
使用redis的有序集合，有序集合的便利之处是可以给每个ip一个分数；

代理ip的分数体系：
新ip，设为10分
ip检测成功，设为100分
ip检测失败，减1分
ip分数达到最低分，删除