## 模块功能清楚分明,逻辑结构清晰,可扩展性强
### 1.存储模块:[db.py](./cookiespool/db.py)
- 使用[Reids 哈希(HASH)](http://www.runoob.com/redis/redis-hashes.html) ,保存对象
- 数据保存在名为3的数据库中
- 检测数据库配置,录运行db.py脚本时,以'accounts:weibo'为key,'hell2o'为用户名,'sss3s'为对应其用户名的cookies值

### 生成模块:[generator.py](./cookiespool/generator.py)
- 一个key('accounts:<website>'):用名保存用户名和密码(accounts\_db),由api接口增加
- 一个key('cookies:<website>'):用来保存用名和cookies(cookies\_db),由cookies.py增加
- 正在登录,检测是否登录成功,正常登录以及获取cookies和返回cookies,都是在login目录下对应网址的[cookies.py](./cookiespool/login/)中完成的
- 需要注意的是:必须要在先使用'/<website>/add/<username>/<password>'接口,来增加用户,才能去遍历出对应的cookies
    - 在运行项目时
    - 在单独运行此文件时,db为3,key为:'accounts:<website>',要保存有用户名(属性)和密码(值)

### 检测模块:[tester.py](./cookiespool/tester.py)
- 用对应网站的首页+cookies,看看是不是返回200

### 提取以及生成接口:[api.py](./cookiespool/api.py)
- /<website>/random:在对应网址上随机获得一个cookies值
- /<website>/count:在对应网址查看cookies的个数
- /<website>/add/<username>/<password>:用对应网址,增加对应的用户名和密码
    - 会在3数据库中生成一个key为:'accounts:<website>' 属性为:username 值为password
的数据

### 5.调度模块:[scheduler.py](./cookiespool/scheduler.py)

- 使用多进程去分别启动生成模块,检测模块,提取模块

### 6.运行项目:[run.py](./cookiespool/run.py)
- 一定要先启动redis服务器
- 5000端口号
- 先将config.py文件中的GENERATOR_PROCESS和VALID_PROCESS值改成False,再运行

```bash

python3 run.py
# 新增用户,还没有产生cookies
http://0.0.0.0:5000/weibo/add/username/password

# 查看cookies,为0
http://0.0.0.0:5000/weibo/count
```

- 当新增加一个用户后,将GENERATOR_PROCESS和VALID_PROCESS值改成True,再运行
```bash
# 查看cookies,为1
http://0.0.0.0:5000/weibo/count

# 随机得到一个cookies
http://0.0.0.0:5000/weibo/random

```

## 进行扩展
- 1.在login目录下创建对应的网址目录,然后在新创建的网址目录下创建cookies.py文件(验证登录,获得cookies)
- 2.编写[generator.py](./cookiespool/generator.py)中,以CookiesGenerator为父类的对应网址的子类,并从上面的cookies.py中得到cookies值
- 3.将新的写的CookiesGenerator子类[增加配置文件的 GENERATOR_MAP值](./cookiespool/config.py)
- 4.编写[tester.py](./cookiespool/tester.py)中,以ValidTester为父类对应网址的子类,根据username去判断cookies是否有效
- 5.将新编写的ValidTester的子类,添加到配置文件的[TESTER_MAP值中](./cookiespool/config.py)


## 注意
- Pychram运行,run.py时会有问题
- 只用weibo这个网址做的测试,而且只是一个用户
