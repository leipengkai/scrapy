### 检验对应网址,用户名+密码的这种,是否能正确登录
- 单独运行对应网址目录下的cookies.py文件,可进行检验
- 正在登录获取cookies以及保存cookies,都是在login目录下对应网址的[cookies.py](./cookiespool/login/)

### 基本思路
- 找到登录url(可能会变)
- 输入用户名,密码,捕获成功或不成功的登录标记元素(可能会变)
- 验证身份:点击按钮,拖图,看图识图,图片验证码(字符:).(可能会变)
    - 拖图:先截验证图,再用验证图和本地的图片做匹配,做完匹配之后,再进行移动
    - 而且移动的距离是以及本地图片名为依据的
    - 比较难实现的原因:需要下载好模板图片
## 其它方法
- [超级鹰识码平台](http://www.chaojiying.com/)
- 卷积神经网络
- tesserocr

### 具体操作
[微博登录](./weibo/cookies.py)
