```bash
# 查询每个月倒数第 3 天入职的员工的信息
select * from emp where hiredate = last_day(hiredate)-2;

# 查询1981 年来公司的人中所有员工的最高工资的那个员工的信息
select * from emp where mgr =(select max(mgr) from emp where date_format(hiredate,"%Y") = "1981");

# 查询平均工资高于 7800 的部门 id 和它的平均工资
select deptno ,avg(mgr) from emp group by deptno having avg(mgr) > 7800;

# 查询工资最低的员工信息:ename, mgr
select ename,mgr from emp where mgr = (select min(mgr) from emp);

# 查询第3高的工资 n-1 distinct:去重
SELECT distinct(mgr) from emp ORDER BY mgr DESC LIMIT 2,1;

# 查询平均工资最低的部门信息: 子查询:单列、from、orderby等都可以进行子查询
# emp  部门的最低平均工资  ,注意只有在FROM 子句中使用子查询才能使用as e表
select min(e.avgmgr) from (select avg(mgr) as avgmgr from emp group by deptno) as e;
# select min(e.avgmgr) from (select avg(mgr) as avgmgr from emp group by deptno) as e join t1 where e.id=t1.id;

# emp deptno
select deptno from emp group by deptno having avg(mgr)= 
    (select min(e.avgmgr) from (select avg(mgr) as avgmgr from emp group by deptno) as e);
# dept deptno
select * from dept where deptno = 
    (select deptno from emp group by deptno having avg(mgr)= 
        (select min(e.avgmgr) from (select avg(mgr) as avgmgr from emp group by deptno) as e));


# 查询平均工资最低的部门信息以及该部门的平均工资 
select d.* ,(select avg(mgr) from emp where deptno=d.deptno) from dept as d where deptno = 
    (select deptno from emp group by deptno having avg(mgr)= 
        (select min(e.avgmgr) from (select avg(mgr) as avgmgr from emp group by deptno) as e));


# 最高工资中最低的那个部门的最低工资是多少
select min(mgr) from emp where deptno in
    (select deptno from emp group by deptno having max(mgr)= 
        (select min(e.maxmgr) from (select max(mgr) as maxmgr from emp group by deptno) as e));
        
        
# 查询比本部门平均工资高的员工的 ename, deptno, mgr 及平均工资
select e.ename,e.mgr,e.deptno,d.avgmgr 
	from emp as e,(select avg(mgr) as avgmgr ,deptno from emp group by deptno) as d 
		where e.mgr>d.avgmgr and e.deptno=d.deptno;


```
