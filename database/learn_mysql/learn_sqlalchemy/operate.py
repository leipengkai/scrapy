from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey ,Column,Integer,String,create_engine
from sqlalchemy.orm import relationship,sessionmaker,undefer,aliased
from sqlalchemy.sql import func

from  models import *


# 创建一个带连接池的引擎 (初始化数据库连接):
# engine = create_engine('mysql+pymysql://root:123456@0.0.0.0/scrapy?charset=utf8mb4',echo=True)
engine = create_engine('mysql+pymysql://root:123456@0.0.0.0:3307/scrapy?charset=utf8mb4')
# engine = create_engine('mysql+pymysql://root:123456@0.0.0.0:3307/scrapy?charset=utf8mb4', echo=True)

# 创建DBSession类型
db_pool = sessionmaker(bind=engine) # 负责执行内存中的对象和数据库表之间的同步工作
session = db_pool() # 先使用工程类来创建一个session
# 当使用session后就显示地调用session.close(),也不能把连接关闭,连接由QueuePool连接池管理并复用


# 插入数据,必须指明字段名title
# s1 = Subjects(title='python爬虫')
# session.add(s1)

# 查询对象方法(Query object),https://docs.sqlalchemy.org/en/latest/orm/query.html
# 如果在查询中不写这些方法,查出来的就是sql语句
# print(session.query(Subjects).first()) # 返回第一个查询对象,或者没有则返回None
# print(session.query(Subjects).get(2))  # 按主键值查询
# print(session.query(Subjects).filter_by(title="python爬虫").one()) # 仅仅查询到一个才用one(),如果多个或者没有都会抛出异常
# print(session.query(Subjects).all())  # 表中所有数据,返回查询对象列表


# 多表查询
# print(session.query(Stu).join(Scores).all()) 
'''
# 相当于内连接
select stu.name,scores.score from stu
    inner join scores on scores.stuid=stu.id;
'''
#在上面的例子中由于只存在一个ForeignKey,Query.join知道如何选取合适的列进行JOIN.如果没有定义ForeignKey,或者存在多个,此时你需要手动指明你参与JOIN的列.Query.join()以如下方式进行:
	# query.join(Scores, Stu.id==Scores.stuid)    # explicit condition
	# query.join(Scores, Stu.score)              # same, with explicit target
	# query.join('score') 
	# query.join(Stu.score)                       # specify relationship from left to right
# print(session.query(Stu).join(Scores,Stu.id==Scores.stuid).all()) 
# print(session.query(Stu).join(Scores, Stu.score).all()) 
# print(session.query(Stu).join('score').all()) 

print(session.query(Scores).join(Stu,Stu.id==Scores.stuid).all())  

############################  创建
# 创建用户,user1
# add1 = Address(location="北海")
# phn1 = PhoneNum(number="18977941970")
# user1 = User(name="femn",addresses=add1, phonenums=phn1)

# session.add(add1)
# session.add(phn1)
# session.add(user1)


# 再为user1添加一个新手机号
# user1 = session.query(User).filter(User.name=="femn").all()[0]
# print(user1)
# phn1 = session.query(PhoneNum).filter(PhoneNum.number=="18977941970").all()[0]

# phn2 = PhoneNum(number="15107792139")

# user1.phonenums = [phn1, phn2]

# session.add(phn2)
# session.add(user1)

############################### 查询
# https://www.jianshu.com/p/8d085e2f2657
user1 = session.query(User).filter(User.name=="femn").all()[0]
print(user1)

for phone_id, number in session.query(PhoneNum.id, PhoneNum.number):
    print(phone_id,number)

for p in session.query(PhoneNum).order_by(PhoneNum.id)[1:]:
    print(p)



# 提交事务,保存用户
session.commit()
print("ok")
