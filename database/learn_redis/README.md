yum install -y redis
vim /etc/redis.conf
    # 外网也能访问
    #bind 127.0.0.1
    # 关闭保护模式
    protected-mode no 


# 生产环境不能使用
keys *


exists k1 : 判断 1存在,0不存在

del k1 # 1删除成功


查看类型
type k1 :string

成对成对出现

<strong>字符串(string):</strong>
- string类型是二进制安全的.意思是redis的string可以包含任何数据,比如jpg图片或者序列化的对象

set k1 1
get k1


incr k1 : 天然计数器, key的值为数字
type k1
# incr将字符串值解析成整形,将其加1,最后结果保存为新的字符串
incrby k1 100  :刷数据 直接加100

mset k1 v1 k2 v2 :批量插入多个,覆盖之前的k值
mget k1 k2

ttl k2  # 查看过期时间  -1:永不过期 -2:已过期而已删除(没有这个key)
# 没设置过期时间,默认为永不过期

expire k2 10  # 设置10s过期时间
persist k2      # 取消过期时间,为永久不过期 


<strong>列表(list):</strong>

```bash
# 从右往左插入 
# 对应list的尾部,添加字符串元素: ←
rpush list1 1
type list1
rpush list1 2

# 可插入多个
# 从左往右插入
# 头部,添加字符串元素: →
lpush list1 a
lpush list1 b
# 最后插入的,可为最新动态展示

# 查看
llen list1
lrange list1 0 -1  # 所有 b a 1 2
lrange list1 2 2  # 1
lpush list1 c d


# 删除
rpop list1
lpop list1

# 秒杀活动

# 用一个Key保存订单号
lpush tmp_orders orders_sn_1
lpush tmp_orders orders_sn_2
# 返回秒杀数量

lrange tmp_orders 0 -1
1) "orders_sn_2"
2) "orders_sn_1"

# 取出订单号
rpop tmp_orders
"orders_sn_1"

rpop tmp_orders
"orders_sn_2"


# lpush和brpop命令组合可以实现阻塞队列,生产者利用lpush命令从列表左端插入元素，多个消费者使用brpop命令阻塞式的“抢”列表尾部的元素，多个客户端保证了消费的负载均衡和高可用性

```

<strong>哈希(hash):</strong>
- hash是一个string类型的field和value的映射表,hash特别适合用于存储对象
- 缓存

```

hmset user:1 username femn age 28 job it
hget user:1 username
hmget user:1 username age
hgetall user:1
```

<strong>集合(set):</strong>
- set是string类型的无序排列
- 和list类型不同,set集合不允许出现重复元素

```
# 为集合赋值
sadd set1 1 2 3

# 查看集合
smembers set1

# 删除指定值
srem set1 3

# sdiff:以前者key值为准,计算差值
sadd set1 1 2 3 4
sadd set2 1 4 5
sdiff set1 set2
1) "2"
2) "3"

sdiff set2 set1
1) "5"

# sinter: 交集,相同的值(不分先后)
sinter set1 set2
1) "1"
2) "4"

# sunion: 并集,所有的值(不分先后)
sunion set1 set2

```

<strong>集合应用场景: 标签</strong>

```
# 给用户添加多个标签，获取用户共同喜好的标签
127.0.0.1:6379> sadd user:1:tags tag1 tag2 tag5
(integer) 3
127.0.0.1:6379> sadd user:2:tags tag2 tag3 tag5
(integer) 3
127.0.0.1:6379> sadd user:3:tags tag1 tag2 tag4
(integer) 3
127.0.0.1:6379> sinter user:1:tags user:2:tags
1) "tag5"
2) "tag2"

# 给标签添加用户，获取该标签有多少用户喜欢
127.0.0.1:6379> sadd tag1:users user:1 user:2 user:3
(integer) 3
127.0.0.1:6379> sadd tag2:users user:1 user:3
(integer) 2
127.0.0.1:6379> sadd tag3:users user:1 user:2
(integer) 2
127.0.0.1:6379> sinter tag1:users
1) "user:2"
2) "user:1"
3) "user:3"
127.0.0.1:6379> sinter tag2:users
1) "user:1"
2) "user:3"
```

<strong>有序集合(sorted set): </strong>

```
# 说明: zadd key score member

# "femn 1"在期中考试中的成绩是90分
zadd mid_test 90 "femn 1"

zadd mid_test 92 "femn lei"
zadd mid_test 96 "femn parker"

# 从大到小排序,倒序
zrevrange mid_test 0 -1 withscores
# 正序
zrange mid_test 0 -1 withscores

# 分段,倒序统计
zrevrangebyscore mid_test 100 92 withscores
# 分段,正序统计
zrangebyscore mid_test 92 100 withscores


# "femn 1"在期末考试中的成绩是90分
zadd fin_test 90 "femn 1"
zadd fin_test 92 "femn lei"
zadd fin_test 96 "femn parker"
# 新同学
zadd fin_test 100 "xiao fang"

# 交集: zinterstore destination numkeys key [key]
zinterstore sum_point 2 mid_test fin_test

zrevrange sum_point 0 -1 withscores
1) "femn parker"
2) "192"
3) "femn lei"
4) "184"
5) "femn 1"
6) "180"

# A和B中共有的member，会加入到C交集中，其score等于A、B中score之和
# 不同时在A和B的member，不会加到C中
# 所以新同学,没有

# 增加,为小范加10分
zincrby fin_test 10 "xiao fang"
"110"


# 程序员工资
zadd programmer 2000 peter
zadd programmer 3500 jack
zadd programmer 5000 tom

# 经理工资
zadd manager 2000 herry
zadd manager 3500 mary
zadd manager 4000 tom

# 并集
zunionstore salary 2 programmer manager
zrange salary 0 -1 withscores
 1) "herry"
 2) "2000"
 3) "peter"
 4) "2000"
 5) "jack"
 6) "3500"
 7) "mary"
 8) "3500"
 9) "tom"
10) "9000"
# A的所有member会加到C中，其score与A中相等
# B的所有member会加到C中，其score与B中相等
# A和B中共有的member，其score等于A、B中score之和






```



<strong>  :</strong>
<strong>  :</strong>
<strong>  :</strong>


### 持久化


<strong>RDB(Redis DataBase)持久化优缺点:</strong>

- 可以在指定的时间间隔内生成数据集的时间点快照（point-in-time snapshot）
    - 功能核心函数rdbSave(生成RDB文件)和rdbLoad（从文件加载内存）两个函数

- 优点：速度快，适合于用做备份，主从复制也是基于RDB持久化功能实现的
- 缺点：会有数据丢失
- rdb持久化核心配置参数：

```
vim /data/6379/redis.conf
dir /data/6379
dbfilename dump.rdb
save 900 1      #900秒（15分钟）内有1个更改
save 300 10     #300秒（5分钟）内有10个更改
save 60 10000   #60秒内有10000个更改  
```


<strong>AOF持久化(append-only log file)优缺点:</strong>
- 记录服务器执行的所有写操作命令，并在服务器启动时，通过重新执行这些命令来还原数据集
- AOF 文件中的命令全部以 Redis通信协议(RESP)的格式来保存，新命令会被追加到文件的末尾
    - RESP 是redis客户端和服务端之前使用的一种通讯协议
- 每当执行服务器(定时)任务或者函数时flushAppendOnlyFile 函数都会被调用， 这个函数执行以下两个工作
    - WRITE：根据条件，将 aof_buf 中的缓存写入到 AOF 文件
    - SAVE：根据条件，调用 fsync 或 fdatasync 函数，将 AOF 文件保存到磁盘中

- 优点：可以最大程度保证数据不丢
- 缺点：日志记录量级比较大,恢复速度慢
- AOF持久化配置

```
appendonly yes          #是否打开aof日志功能
appendfsync always      #每1个命令,都立即同步到aof
appendfsync everysec    #每秒写1次
appendfsync no          #写入工作交给操作系统,由操作系统判断缓冲区大小,统一写入到aof.

```

<strong>比较  :</strong>
- rdb：基于快照的持久化，速度更快，一般用作备份，主从复制也是依赖于rdb持久化功能
- aof：以追加的方式记录redis操作日志的文件。可以最大程度的保证redis数据安全，类似于mysql的binlog
- aof文件比rdb更新频率高，优先使用aof还原数据
- aof比rdb更安全也更大
- rdb性能比aof好
- 如果两个都配了优先加载AOF







redis很快,只是shell一行一行的执行,shell慢了
vim for.sh

#!/bin/bash

for i in {1..100000}
do
    echo "${i} is ok"
    redis-cli -h db01 set k_${i} v_${i}
done

time bash for.sh



redis> shutdown
shutdwon之前,会先bgsave

kill -9 redis_pid # 数据不会持久化      # 直接把头也砍了,不要用-9.固态硬盘不能恢复数据
kill redis_pid # 数据会持久化 -15 正常退出流程,优雅的关闭


主从复制,哨兵
集群
一个集群里最多有16834个槽位,不管redis节点有多少个,每个节点可以有N个槽位,但整个集群的槽位最多只能有16834个.
重点是槽的数量,而不是序号(0~16833)

只要有一个槽位有问题或者没分配,整个集群都不可使用
hash分槽算法: 平均随机分配到槽位上

集群内的信息是共享的,只要能发现集群中的一台机器,你就能获取集群内的所有成员
只允许同时 挂一台机器,一个机器有主从节点





create databases test default character utf8mb4 collate utf8mb4_unicode_ci;


show index from articles;
set profiling=1;
select * from articles where content like "我们%";
show profiles;


create index index_content on articles(content(50));
show index from articles;
select * from articles where content like "我们%";
show profiles;
drop index index_content;

先aof
面试 圆 总结
不挂不满,监控,数据备份,帮助开发查看数据

