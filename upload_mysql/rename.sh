#!/bin/bash

# 查看某目录的文件个数
# ls -l |grep "^-"|wc -l
# 0  1985+1825=3810 3810+1788=5598
# 注意要在abspath中执行 按数字重命名某个目录下所有.jpg文件
abspath='/home/femn/Downloads/sync1/test'

num=3810
for i in `ls $abspath |grep '\.jpg'`
do
	num=`expr $num + 1`;
	mv $i $num.jpg
done
