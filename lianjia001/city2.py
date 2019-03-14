#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def level1():
    linkArr = [];
    a = 1;
    with open('./link_s.txt', 'r', encoding='utf-8') as f:
        for line in f:
            s = line.replace('\n','');
            linkArr.append(s);
    return linkArr;

def level2(url):
    # 2 发请求
    data = requests.get(url, headers=getAgent()).text
    # 3 获取页面内容
    page_text = data
    # 4 解析
    tree = etree.HTML(page_text)

    # 获取所有li
    data = tree.xpath('//*[@class="contentBottom clear"]/div[2]/div[1]/@page-data')
    if len(data)==0:
        return {"url":url, "totalPage": 1}
    else:
        print('-d s------------------')
        print(data);
        print('-d e------------------')
        res = json.loads(data[0]);
        curPage = res['curPage'];
        totalPage = res['totalPage'];
        aa = {"url":url, "totalPage": totalPage}
        print('-------------------')
        print(aa);
        print('-------------------')

    return aa;


'''
userInfo = {'url': 'https://tj.lianjia.com/ershoufang/chentangzhuang/', 'totalPage': 19}
'''
def convertUrlList(userInfo):
    count = 1;
    res = []
    while count<=userInfo['totalPage']:
        page = '' if count==1 else ('pg'+str(count)+'/');
        url = userInfo['url'] + page
        res.append(url);
        count+=1;
    return res;

def level3():
    pass


res = level1();

allUrl = [];
count = 0
with open('res.txt', 'w', encoding='utf-8') as f:
    while count < len(res):
        aa = level2(res[count]);
        list = convertUrlList(aa);
        for item in list:
            f.write(item+'\n');
        count+=1;





