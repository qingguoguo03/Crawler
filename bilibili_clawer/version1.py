

# 目标： 爬去关键词视频第一下所有用户评论，提取用户评论中的链接（资源链接）
# 后期需要的迭代
# 1. 海量url的去重问题
# 2. 多线程并行处理
# 3. 代理问题


# 目前：爬去离公司附近30min路程的小区，从各个租房源筛选查找符合的信息
import requests
from urllib import parse
import json
from pyquery import PyQuery as pq
from collections import defaultdict
import re, math
# import validators
# validators.url("http://google.com")


# 爬去哔哩哔哩上某视频下面用户讨论的链接，云盘以及密码

def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    }
    html = None
    max_cnt = 1
    while max_cnt<4:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                html = response.text
            else:
                print(response.status_code, response.reason)
            break
        except requests.exceptions.HTTPError as e:
            print(e)
            max_cnt += 1
        except requests.exceptions.RequestException as e:
            print(e)
            break
    return response, html


def get_video_list_from_one_page(search_url):
    _, html = get_page(search_url)
    urls = [] # 不会有重复 一般
    if html:
        doc = pq(html)
        items = list(doc.find("#server-search-app > div.contain > div.body-contain ul.video-contain.clearfix  > li").items()) 
        for item in items:
            href = 'https:'+item("a").attr('href') # 视频的链接
            tags = item("div.info")
            watch = tags("[title='观看']").text()
            barrage = tags("[title='弹幕']").text()
            up_time = tags("[title='上传时间']").text()
            urls.append([href, watch, barrage, up_time])
    return urls


import time
def get_reply_message_url(reply):
    message = reply['content']['message'].strip()
    source_url = url_pattern.match(message)
    if source_url:
        return (source_url.group(1).strip(), message)
    return None

def find_source_url_in_replies(oid):
    pn = 1
    reply_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=%d&type=1&oid=%d&sort=2" % (pn, oid)
    _, html = get_page(reply_url)
    data = json.loads(html)
    if data['code'] != 0:
        return None
    data = data['data']
    pn_end = math.ceil(data['page']['count']/data['page']['size']) 
    items = []
    for pn in range(1, pn_end+1):
        reply_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=%d&type=1&oid=%d" % (pn, oid)
        time.sleep(1)
        _, html = get_page(reply_url)
        data = json.loads(html)['data']
        for reply in data['replies']:
            flag = get_reply_message_url(reply) #  如果匹配出url把链接以及文本都匹配出来
            if flag:
                items.append(flag)
            if reply['replies']: # 回复的人
                for reply_ in reply['replies']:
                    flag = get_reply_message_url(reply_)
                    if flag:
                        items.append(flag)
    return set(items)



# 需要得到多少页
params = {
        "keyword": keyword,
        "order": "stow", # 最多收藏的
        "duration": 0, # 没有限制时长
    }
params = parse.urlencode(params)
urls = []
search_url = "https://search.bilibili.com/all?page=1&" + params
html = get_page(search_url)
doc = pq(html)
page_num = int(doc("#server-search-app > div.contain > div.body-contain > div > div.page-wrap > div > ul > li.page-item.last > button").text())
for page in range(1, page_num):   
    search_url = "https://search.bilibili.com/all?page=%d&" % page + params
    time.sleep(2)
    new_urls = get_video_list_from_one_page(search_url)
    urls.extend(new_urls)



url_pattern = re.compile('.*?(http[s]?://(.*?/)+[^\u4e00-\u9fa5\s]*)', re.S)
oid_pattern = re.compile("av(\d*)?")
keyword = "机器学习"
page = 1

#urls = get_video_list_from_one_page(page, keyword)


video_data = defaultdict(dict)
down_list = set()
cnt = 0
for url_info in urls:
    if cnt>50:
        break
    url = url_info[0]
    watch, barrage, up_time = url_info[1:]
    if url in down_list:
        continue
    print('正在处理页面： %s'% url)
    _, html = get_page(url)
    doc = pq(html)
    video_data[url]['watch'] = watch
    video_data[url]['barrage'] = barrage
    video_data[url]['up_time'] = up_time
    info = doc("#v_desc > div.info.open").text().strip()
    video_data[url]['info'] = info
    tags = doc("#v_tag > ul").find('li').text().split(' ')
    video_data[url]['tags'] = tags
    title = doc("#viewbox_report > h1 > span").text().strip()
    video_data[url]['title'] = title
    print('页面的标题： %s' % title)
    video_data[url]['source_url'] = set()
    oid = int(oid_pattern.search(url).group(1))
    items = find_source_url_in_replies(oid)
    if items:
        video_data[url]['source_url'].update(items)
    down_list.add(url)
    cnt += 1



import pandas as pd
data = pd.DataFrame(video_data).T
data['url'] = data.index
data.index = range(len(data))
tmp = data['source_url'].apply(lambda x: pd.Series(list(x))).stack().reset_index(level=1,drop=True).rename('source')
data = data.join(tmp)
data = data.dropna(subset=['source'])
del data['source_url']
data['source_url'] = data['source'].apply(lambda x: x[0])
data['remark'] = data['source'].apply(lambda x: x[1])
del data['source']
data.to_excel('test.xlsx')

