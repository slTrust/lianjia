#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import requests
import random

def getAgent():
    agentList = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'}
    ];
    return random.choice(agentList);

# 返回 天津所有 区的链接
def level1():

    url = "https://tj.lianjia.com/ershoufang/"

    # 2 发请求
    data = requests.get(url, headers=getAgent()).text
    # 3 获取页面内容
    page_text = data
    # 4 解析
    tree = etree.HTML(page_text)

    # 获取所有li
    li_list = tree.xpath('//div[@data-role="ershoufang"]/div/a/@href')

    fp = open('./link.txt', 'w', encoding='utf-8')
    print(li_list)
    for li in li_list:
        # 5 持久化
        fp.write(li + '\n');
        print('写入成功')


# 返回天津所有
def level2():
    linkArr = [];
    a = 1;
    with open('./link.txt', 'r', encoding='utf-8') as f:
        for line in f:
            s = line.replace('\n','');
            print(s)
            linkArr.append('https://tj.lianjia.com'+s);
    return linkArr;


# 返回一个区对应的所有街道url地址
def level3(url):
    # '//div[@data-role="ershoufang"]/div[2]/a/@href'

    # 2 发请求
    data = requests.get(url, headers=getAgent()).text
    # 3 获取页面内容
    page_text = data
    # 4 解析
    tree = etree.HTML(page_text)


    # 获取所有li
    li_list = tree.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href')

    arr = []
    for li in li_list:
        arr.append('https://tj.lianjia.com'+li);

    return arr;


level1();
# 区列表
cityList = level2();

# 街道列表
res = [];
for i in cityList:
    curArr = level3(i);
    res += curArr;

print(res);

with open('./link_s.txt.txt','w',encoding='utf-8') as f:
    for i in res:
        f.write(i+'\n');







