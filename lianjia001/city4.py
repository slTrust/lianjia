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

    # 获取所有info
    obj = {};
    # 房屋基本信息
    data = tree.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/text()');
    obj['houseType'] = data[0]; # 房屋户型
    obj['floor'] = data[1]; # 所在楼层
    obj['coverArea'] = data[2]; # 建筑面积
    obj['houseStruct'] = data[3]; # 户型结构
    obj['insideArea'] = data[4]; # 套内面积
    obj['buildType'] = data[5]; # 建筑类型
    obj['orientation'] = data[6]; # 房屋朝向
    obj['buildStruct'] = data[7]; # 建筑结构
    obj['redecorated'] = data[8]; # 装修情况
    obj['ladderHouseholdRatio'] = data[9]; # 梯户比例
    obj['heatingMode'] = data[10]; # 供暖方式
    obj['isElevator.'] = data[11]; # 配备电梯
    obj['property'] = data[12]; # 产权

    # 交易属性
    data2 = tree.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[2]/text()');
    obj['listingDate'] = data2[0] ; # 挂牌时间
    obj['tradeRight'] = data2[1];  # 交易权属
    obj['lastTransaction'] = data2[2];  # 上次交易
    obj['houseUse'] = data2[3];  # 房屋用途
    obj['houseYears'] = data2[4];  # 房屋年限
    obj['propertyOwner'] = data2[5];  # 产权所属
    obj['mortgageInfo'] = data2[6];  # 抵押信息
    obj['spareParts'] = data2[7];  # 房本备件

    # 关注信息
    obj['totalPrice'] = tree.xpath('/html/body/div[5]/div[2]/div[2]/span[1]/text()')[0] # 总价格
    obj['squareMetrePrice'] = tree.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span/text()')[0] # 元/平
    print('----------')
    print(obj);
    print('----------')
    return obj; # 房屋详情列表

with open('detail.txt','r',encoding='utf-8') as f , open('a','w',encoding='utf-8') as f2:
    count = 0;
    for line in f:
        s = f.readline().replace('\n','');
        info = level(s)
        print(info);
        print(count);
        count+=1;

