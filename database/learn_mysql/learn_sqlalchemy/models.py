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
    emp = relationship("Emp", backref="dept")


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



