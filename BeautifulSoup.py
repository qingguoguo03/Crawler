
# 节点筛选器
# 有问题，只选择第一个节点，后面都会忽略掉的
soup.title.string
soup.p.attrs
soup.p.name # 节点名称
soup.p['name'] # 属性名称
soup.p.attrs['class'] 


# 获取子节点:直接子节点
soup.p.contents
[item for item in soup.p.children]
# 所有子节点b
[item for item in soup.p.descendants]

# 反过来就是直接父节点与所有父节点
soup.b.parent
list(soup.b.parents) # parents出现了两个一样的父节点，最后一个就是整个网页


# 方法选择器
for p in soup.findAll(name='p'):
    print(p)
for p in soup.findAll(class_='title'):
    print(p)
for p in soup.findAll(attrs={'class':'title'}):
    print(p)
print('测试text')
# text 匹配文本或者是正则
import re
for p in soup.findAll(text='The Dormouse’s story'):
    print(p)
print('相似匹配')
for p in soup.findAll(text=re.compile('The Dormouse’s story')):  # 推荐这种方法
    print(p)

# CSS选择器
soup.select('#link2')
soup.select('p b')[0].text
soup.select('p a.sister')[0].attrs['id']
