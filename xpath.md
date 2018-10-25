### Xpath语法笔记

#### 选取节点

| 表达式 | 实例 | 说明 |
| :------: | :------: | :------: |
| /  | xpath('/html/body')  | 从根节点上开始选取,body节点  |
| //  | xpath('//div') | 选取所有的div节点 |
| .  | xpath('./div')  | 选取当前节点下的所有div节点 |
| ..  | xpath('../div')  | 选取父节点下的所有div节点 |
| @ | xpath('../div/@class') | 选取所有div的class属性  |

#### 谓语

谓语被嵌在方括号内，用来查找某个特定的节点或包含某个制定的值的节点

| 实例| 说明 |
| :------: | :------: |
| xpath('/html/body/div/div[1]')  | 获取/html/body/div下的第一个div节点 |
| xpath('/html/body/div/div[last()]') | 最后一个div节点  |
| xpath('/html/body/div/div[last()-1]')  |  倒数第二个div节点 |
| xpath('/html/body/div/div[@class]') | 带有class属性的div节点  |
| xpath('/html/body/div/div[@class="main"]') | class属性为main的div节点  |
| xpath('/html/body/div[position()<3]')  | body下的前两个div节点  |
| xpath('//div[starts-with(@id,"ma")]')     |  选取id值以ma开头的div节点 |
| xpath('//div[contains(@id,"ma")]')  | 选取id值包含ma的div节点 |
| xpath('//div[contains(@id,"ma") and contains(@id,"in")]')   | 选取id值包含ma和in的div节点 |
| xpath('//div[contains(text(),"ma")]')   |  选取节点文本包含ma的div节点 |

### css选择器语法


| 实例| 说明 |
| :------: | :------: |
| *  | 选择所有节点  |
| #container  | 选择id为container的节点  |
| .container  |  选择所有class包含container的节点 |
| div,p  |  选择所有 div 元素和所有 p 元素 |
|  li a |  选取所有li 下所有a节点 |
|  ul + p | 选取ul后面的第一个p元素  |
| div#container > ul  | 选取id为container的div的第一个ul子元素  |
|  ul ~p |  选取与ul相邻的所有p元素 |
|  a[title] | 选取所有有title属性的a元素  |
|  a[href=”http://baidu.com”] | 选取所有href属性为http://baidu.com的a元素  |
| a[href\*=”baidu”]  |  选取所有href属性值中包含baidu的a元素 |
| a[href^=”http”]  | 选取所有href属性值中以http开头的a元素  |
| a[href$=”.jpg”]  | 选取所有href属性值中以.jpg结尾的a元素  |
|  input[type=radio]:checked | 选择选中的radio的元素  |
|  div:not(#container) | 选取所有id为非container 的div属性  |
| li:nth-child(3)  |  选取第三个li元素 |
| li:nth-child(2n)  |  选取第偶数个li元素 |
| a::attr(href)  | 选取a标签的href属性  |
| a::text  | 选取a标签下的文本  |


参考资料:
- [Xpath语法笔记](https://my.oschina.net/jhao104/blog/639448?fromerr=nlaEK3Ge)
- [xpath与css选择器详解](https://www.jianshu.com/p/489c5d21cdc7)
