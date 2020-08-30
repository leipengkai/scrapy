# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text, ForeignKey, BigInteger, DATE
from sqlalchemy.dialects.mysql import DOUBLE,INTEGER,DECIMAL

from sqlalchemy.orm import relationship
from sqlalchemy.orm import contains_eager, deferred


# 创建对象的基类以及alembic的跟踪Model:
DbBase = declarative_base()


class Stu(DbBase):
    '''
    学生表
    '''
    __tablename__ = 'stu'
    id = Column(INTEGER(11),primary_key=True,autoincrement=True)
    name = Column(String(10),nullable=False)
    birthday = Column(DATE,nullable=True)
    gender = Column(Boolean,unique=False, default=True) # bool类型设置默认值
    isdelete= Column(Boolean,unique=False, default=True)
    # share = Column(String(64), server_default='1') # String设置默认值
    hometown = Column(String(30),nullable=True)
    fscore  = Column(Integer)  # 没有意义,为了说明列不可拆分性
    score = relationship("Scores",backref="stu")

    def __repr__(self):
        return "<Stu(id={},name={},score={})>".format(self.id,self.name,self.score)



class Subjects(DbBase):
    '''
    学科表
    '''
    __tablename__ = 'subjects'
    id = Column(INTEGER(11),primary_key=True,autoincrement=True)
    title = Column(String(10),nullable=False)
    score = relationship("Scores",backref="subjects")

    def __repr__(self):
        return "<Subjects(id={},title={})>".format(self.id,self.title)


class Scores(DbBase):
    '''
    分数表
    '''
    __tablename__ = 'scores'
    id = Column(INTEGER(11),primary_key=True,autoincrement=True)
    stuid = Column(INTEGER(11),ForeignKey('stu.id'))  
    subid = Column(Integer,ForeignKey('subjects.id'))  
    score = Column(DECIMAL(5,2))

    def __repr__(self):
        return "<Scores(id={},sutid={},subid={},score={})>".format(self.id,self.stuid,self.subid,self.score)


class Dept(DbBase):
    '''
    部门表
    '''
    __tablename__ = 'dept'
    deptno = Column(INTEGER(2),primary_key=True)
    dname = Column(String(14))
    loc = Column(String(13))
    # 方便双方引用
    emp = relationship("Emp", backref="dept")
    # relationship是为了简化联合查询join等，创建的两个表之间的虚拟关系，这种关系与标的结构时无关的。他与外键十分相似，确实，他必须在外键的基础上才允许使用


class Emp(DbBase):
    '''
    员工表
    '''
    __tablename__ = 'emp'
    empno = Column(INTEGER(4),primary_key=True)
    ename = Column(String(10))
    job = Column(String(10))
    mgr = Column(INTEGER(4))
    hiredate = Column(DATE, nullable=True)
    sal = Column(DOUBLE(7, 2))  # 工资
    comm = Column(DOUBLE(7, 2))
    deptno = Column(INTEGER(2),ForeignKey('dept.deptno'),nullable=False)
    # SQLAlchemy中定义关系要比Django的ORM要麻烦许多:Django中只需要一行就可以了,不再需要relationship,去显示指明
    # dept = models.ForeignKey(Dept, verbose_name="", related_name="emp",default="")
    # nullable=False表示一对多,等于True时则是多对多


class Salgrade(DbBase):
    '''
    工资等级表
    '''
    __tablename__ = 'salgrade'
    grade = Column(Integer,primary_key=True) # 必须明确一个主键
    losal = Column(Integer)
    hisal = Column(Integer)


class Areas(DbBase):
    '''
    地区表,自关联
    '''
    __tablename__ = 'areas'
    id = Column(INTEGER(11),primary_key=True,autoincrement=True)
    title = Column(String(50))
    pid = Column(INTEGER(11),ForeignKey('areas.id'))



class Address(DbBase):
    __tablename__ = 'address'
    attributes = ['id', 'location', 'user_id']
    detail_attributes = attributes
    summary_attributes = ['location']

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    location = Column(String(255), nullable=False)
    user_id = Column(ForeignKey(u'user.id'), nullable=False)

    # 只是方便引用,写在那边无所谓,单方引用
    user = relationship(u'User')    # , uselist=False
    
    def __repr__(self):
        return "<Address(id={},location={})>".format(self.id,self.location)

class PhoneNum(DbBase):
    __tablename__ = 'phone'
    attributes = ['id', 'number', 'user_id']
    detail_attributes = attributes
    summary_attributes = ['number']

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    number = Column(String(255), nullable=False)
    user_id = Column(ForeignKey(u'user.id'), nullable=False)

    user = relationship(u'User')
    
    def __repr__(self):
        return "<PhoneNum(id={},number={})>".format(self.id,self.number)
    
    
class User(DbBase):
    __tablename__ = 'user'
    attributes = ['id', 'name', 'addresses', 'phonenums']
    detail_attributes = attributes
    summary_attributes = ['name']

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    
    # 只是方便引用,写在那边无所谓,单方引用
    addresses = relationship(u'Address', back_populates=u'user', lazy=False, uselist=True, viewonly=True)
    phonenums = relationship(u'PhoneNum', back_populates=u'user', lazy=False, uselist=True, viewonly=True)
    # lazy=False,一次性加载出来phonenums的值,这样就可以让信息在一次sql查询中加载出来，而不是每次访问外键属性再发起一次查询。问题在于，lazy=False时sql被组合为一个SQL语句，relationship每级嵌套会被展开，实际数据库查询结果将是乘数级
    # uselist=False,addresses=add1可以插入,但为True的话,报错:not list-like
    # uselist=True, 必须以列表的形式添加: user1.phonenums = [phn1, phn2]


    def __repr__(self):
        return "<User(id={},name={},addresses={},phonenums={})>".format(self.id,self.name, self.addresses, self.phonenums)
    
class Tag(DbBase):
    __tablename__ = 'tag'
    attributes = ['id', 'res_id', 'key', 'value']
    detail_attributes = attributes
    summary_attributes = ['key', 'value']

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    res_id = Column(String(36), nullable=False)
    key = Column(String(36), nullable=False)
    value = Column(String(36), nullable=False)

    def __repr__(self):
        return "<Tag(id={},res_id={},key={},value={})>".format(self.id,self.res_id,self.key,self.value)


class Region(DbBase):
    '''
    地区表,一个地区可以有多个标签
    '''
    __tablename__ = 'region'
    attributes = ['id', 'name', 'desc', 'tags', 'user_id', 'user']
    detail_attributes = attributes
    summary_attributes = ['name', 'desc']

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    desc = Column(String(255), nullable=True)
    user_id = Column(ForeignKey(u'user.id'), nullable=True)
    user = relationship(u'User')

    # alembic revision --autogenerate -m "work"
    # 对下面这个没生效
    tags = relationship(u'Tag', primaryjoin='foreign(Region.id) == Tag.res_id',
        lazy=False, viewonly=True, uselist=True)
    # https://www.osgeo.cn/sqlalchemy/orm/join_conditions.html
    def __repr__(self):
        return "<Region(id={},name={},user={},tags={})>".format(self.id,self.name,self.user,self.tags)

class Resource(DbBase):
    '''
    资源表,一个资源可以有多个标签
    '''
    __tablename__ = 'resource'
    attributes = ['id', 'name', 'desc', 'tags', 'user_id', 'user', 'region_id', 'region']
    detail_attributes = attributes
    summary_attributes = ['name', 'desc']

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    desc = Column(String(255), nullable=True)
    user_id = Column(ForeignKey(u'user.id'), nullable=True)
    region_id = Column(ForeignKey(u'region.id'), nullable=True)
    user = relationship(u'User')
    region = relationship(u'Region')

    tags = relationship(u'Tag', primaryjoin='foreign(Resource.id) == Tag.res_id',
        lazy=False, viewonly=True, uselist=True)
    def __repr__(self):
        return "<Resource(id={},name={},user={},region={},tags={})>".format(self.id,self.name,self.user,self.region,self.tags)

