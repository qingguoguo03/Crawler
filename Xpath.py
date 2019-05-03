
from lxml import etree
text = '''
    <div>
    <ul><li class='item-0'><a href='link1.html'>first item</a></li>
    <li class='item-1'><a href='link2.html'>second item</a></li>
    <li class='item-inactive'><a href='link3.html'>third item</a></li>
    <li class='item-1 item-11' name='item11'><a href='link4.html'>fourth item</a></li>
    <li class='item-0'><a href='link5.html'>fifth item</a>
    </ul>
    </div>
'''
html = etree.HTML(text)
print(etree.tostring(html).decode('utf-8')) #自动补充代码
with open('xpath.html', 'w') as f:
    f.write(text)
html = etree.parse('xpath.html', etree.HTMLParser()) #直接读取文件
print(etree.tostring(html).decode('utf-8')) #自动补充代码,并且多了头部文件



html.xpath('//*') # 选取所有节点
html.xpath('//li[1]') # 下标从1开始
html.xpath('//li/a[@href="link4.html"]/../@class') #父节点的class值
html.xpath('//li/a[@href="link4.html"]/parent::*/@class') # parent::后面要带有*号
html.xpath('//li/a/text()') # 注意这两种写法的区别
html.xpath('//li//text()') # 多了li后面的回车符号
# 属性多值匹配
html.xpath('//li[@class="item-11"]') # 筛选不出来
html.xpath('//li[@class="item-1"]') # 只筛选出第一个单值
html.xpath('//li[contains(@class,"item-1")]') # 多值匹配用contains筛选出两个
html.xpath('//li[contains(@class,"item-11")]') # 多值匹配用contains筛选出想要的那个， contains只强调包含关键词即可
html.xpath('//li[contains(@class,"item-11") and contains(@class,"item-1")]')

text = '''
    <div class="test demo"></div>
    <div class="demo test"></div>
    <div class="test demo2"></div>
'''
html = etree.HTML(text)
html.xpath('//div[contains(@class, "demo") and contains(@class, "test")]')
for item in html.xpath('//div[contains(concat(" ",@class," "), " demo ")]'): # 加了空格就把最后一种排除掉了
    print(item.get('class'))

# 多属性匹配
html.xpath('//li[contains(@class,"item-11") and @name="item11"]//text()')

# 按序筛选
html.xpath('//li[position()<3]//text()') # 注意筛选器后面有括号
html.xpath('//li[last()-2]//text()')

# 替代：操作节点轴进行筛选
html.xpath('//li[1]/ancestor::*')
html.xpath('//li[1]/ancestor::div')
html.xpath('//li[1]/ancestor::div/attribute::*')
html.xpath('//li[1]/attribute::*')
html.xpath('//li[1]/child::*[@href="link1.html"]/@href') #筛选属性值要加括号
html.xpath('//li[1]/following::*') # 所有在后面的节点
html.xpath('//li[1]/following-sibling::*') # 兄弟节点
html.xpath('//li[1]/self::*/@class')
