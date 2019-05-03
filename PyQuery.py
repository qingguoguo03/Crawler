
# 初始化可以是url file str 更加灵活一点
html = '''
<div>
<ul>
<li class="item-0">first item<li class="item-0">first item11</li></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li> 
<li class ="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="links.html">fifth item</a></li> </ul>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html) # pq(url='') pq(filename='')
print(doc)

doc('li.item-0')
# 查找所有的子节点
doc.find('li.active')
doc.children('li') # 直接子节点
doc.children('ul')
for item in doc.find('li.active'):
    print(item)
    item.get('class') # attr没有这个函数
doc.find('li.active').text() # 所有的text的拼接
doc.find('li.active').html() # 只有第一个

# 比较特殊的: 直接对节点进行操作
li = doc.find('li.active.item-0')
#li = doc.find('li.item-0')
print(li)
li.removeClass('active') # 如果单独筛选[0]就没有办法操作了
print(li)
li.addClass('active')
print(li)
html = '''
<ul class="list">
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li></ul>
'''
doc = pq(html)
li = doc('li.item-0.active')
print(li)
li = li.attr('name', 'test')
print(li)
li = li.text('change items')
print(li)
li = li.html('<span>test</span>')
print(li)
# 有时候想要父节点的text但是会把子节点text选进去这个时候就可以用remove
li = li.html('change items<span>test</span>')
print(li)
print(li.text())
li = li.remove('span')
print(li.text())

# 伪类选择器 可以选择位置
html = '''
<div>
<ul>
<li class="item-0">first item<li class="item-0">first item11</li></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li> 
<li class ="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="links.html">fifth item</a></li> </ul>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html) # pq(url='') pq(filename='')
li = doc('li:first-child')
print(li, '\n\n')
li = doc('ul>li:last-child') # 强调必须是直接子节点
print(len(li),li, '\n\n')
li = doc('li:gt(2)')
print(li)
li = doc('li:contains(item)') # 强调是文本, 与xpath区别
print(li, '\n\n')
li = doc('li:nth-child(2n)')
print(li)

