#! -*-coding: utf-8 -*-
from lxml import etree
import requests
import random
import json

def getAgent():
    agentList = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'}
    ];
    return random.choice(agentList);


def level(url):
    # 2 发请求
    data = requests.get(url, headers=getAgent()).text
    # 3 获取页面内容
    page_text = data
    # 4 解析
    tree = etree.HTML(page_text)

    # 获取所有li
    data = tree.xpath('//div[@class="leftContent"]/ul/li/a[@data-el="ershoufang"]/@href')
    return data; # 房屋详情列表

res = [];
with open('res.txt','r',encoding='utf-8') as f , open('a','w',encoding='utf-8') as f2:
    count = 0;
    for line in f:
        s = f.readline().replace('\n','');
        list = level(s)
        res.append(list);
        print(count);
        count+=1;

with open('detail.txt','w',encoding='utf-8') as f:
    count2 = 0;
    for list in res:
        for item in list:
            f.write(item+'\n');
            print(count2);
            count2+=1;