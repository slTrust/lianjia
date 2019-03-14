#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import requests
import random
import json
import re

def replaceString(string):
    return string.replace('/ershoufang/','').replace('/','')

def replaceLine(string):
    return string.replace('\n','').replace('\t','').replace(' ','');

def replaceNotNum(string):
    return re.search(r'[0-9\.]+',string).group() 


def covertFloat(value):
    if value :
        return float(replaceNotNum(value))
    else:
        return value


def getAgent():
    agentList = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'}
    ]
    return random.choice(agentList);

# 返回 天津所有 区的链接
def getCityAreaUrl():
    url = "https://tj.lianjia.com/ershoufang/"
    # 2 发请求
    data = requests.get(url, headers=getAgent()).text
    # 3 获取页面内容
    page_text = data
    # 4 解析
    tree = etree.HTML(page_text)

    # 获取所有li
    li_list = tree.xpath('//div[@data-role="ershoufang"]/div/a/@href')
    res = [];
    for li in li_list:
        res.append(li);
    return res;

# 返回天津所有区的url
def converAreaInfo2Obj(arr):
    linkArr = [];
    for item in arr:
        s = item;
        linkArr.append({"url":'https://tj.lianjia.com' + s,"city":"tj","area":replaceString(s)});
    return linkArr;


# 返回一个区对应的所有街道url地址
def getAreaStreetUrl(url):
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
        arr.append(li);
    return arr;


def execStep1():
    a1List = getCityAreaUrl();
    areaObjList = converAreaInfo2Obj(a1List);
    # 区列表
    # 街道列表
    res = [];
    for i in areaObjList:
        curArr = getAreaStreetUrl(i['url']);
        for deepItem in curArr:
            res.append({
                "url":'https://tj.lianjia.com'+deepItem,
                'city':i['city'],
                'area':i['area'],
                'street':replaceString(deepItem)
            })
    return res;

# ----------------------------
def getPageInfo(url):
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
        print(data,url);
        print('-d e------------------')
        res = json.loads(data[0]);
        curPage = res['curPage'];
        totalPage = res['totalPage'];
        aa = {"url":url, "totalPage": totalPage}
    return aa;

'''
userInfo = {'url': 'https://tj.lianjia.com/ershoufang/chentangzhuang/', 'totalPage': 19}
'''
def convertUrlList(userInfo):
    count = 1;
    res = []
    baseUrl = userInfo['url'];
    while count<=userInfo['totalPage']:
        page = '' if count==1 else ('pg'+str(count)+'/');
        url = baseUrl + page
        # 深拷贝
        tmpUserInfo = json.loads(json.dumps(userInfo));
        tmpUserInfo['url'] = url;
        res.append(tmpUserInfo);
        count+=1;
    return res;

def execStep2(streetUrlLists):
    allUrl = [];
    with open('link2.txt','w',encoding="utf-8") as f:
        for i in streetUrlLists:
            obj = getPageInfo(i['url']);
            i['totalPage'] = obj['totalPage']
            urlLists = convertUrlList(i);
            for item in urlLists:
                f.write(json.dumps(item)+'\n');

print('开始分析省市区街道的url....');
# streetUrlLists = execStep1();
print('所有街道url获取完毕...');
print('开始分析街道的url  的页码数据....');
# execStep2(streetUrlLists)
print('所有街道url获取完毕...');

print('开始分析街道每页对应房屋的详情url  的页码数据....');
def execStep3():
    def getDetailUrl(url):
        data = requests.get(url, headers=getAgent()).text
        page_text = data
        tree = etree.HTML(page_text)
        data = tree.xpath('//div[@class="leftContent"]/ul/li/a[@data-el="ershoufang"]/@href')
        return data; # 房屋详情列表

    with open('link2.txt','r',encoding='utf-8') as f , open('detail.txt','w+',encoding='utf-8') as f2:
        count = 0;
        
        # 序列化的 url信息 
        '''
        {
            "url": "https://tj.lianjia.com/ershoufang/nanyingmenjie/", 
            "city": "tj", 
            "area": 
            "heping", 
            "street": "nanyingmenjie", 
            "totalPage": 21
        }
        '''
        while 1:
            line = f.readline()
            if not line:
                break
            s = line.replace('\n','');
            print('---------------')
            print(s)
            tmpObj = json.loads(s);
            detailList = getDetailUrl(tmpObj['url'])
            res = detailList
            for deepItem in detailList:
                o2 = json.loads(s);
                o2['detailUrl'] = deepItem;
                s2 = json.dumps(o2);
                f2.write(s2+'\n');
            print(count);
            print(s2);
            count+=1;

            
       

# execStep3();
print('开始分析街道每页对应房屋的详情url获取完毕...');


print('the last 获取房屋所有信息')
import pymysql

def execSql(*args):
    try:
        # 连接数据库
        db = pymysql.connect(host="localhost",user="root",password="831015",db="house",port=3306,charset="utf8")
        #创建游标对象
        cursor = db.cursor() 
        # sql语句
        sql = '''insert into app_house values(null,%s,%s,%s,%s,%s,
                                                 %s,%s,%s,%s,%s,
                                                 %s,%s,%s,%s,%s,
                                                 %s,%s,%s,%s,%s,
                                                 %s,%s,%s,%s,%s,
                                                 %s,%s,%s)
            ''';
        #执行SQL语句
        cursor.execute(sql,(*args,)) 
        #提交
        db.commit()
    except Exception as e:
            db.rollback() 
            print(e)
    finally:
            db.close()


def convertInfoAndNoValueSetDef(k,v):
    obj = {};
    count = 0
    while count < len(k):
        obj[k[count]] = replaceLine(v[count]);
        count+=1
    return obj;

def mergeMap(mapArr):
    res = {};
    for oMap in mapArr:
        for k in oMap:
            res[k] = oMap[k]
    return res;

def convertKeyName2English(baseMap):
    keyMap = {
        "房屋户型":{"key":"houseType","defVal":""},
        "所在楼层":{"key":"floor","defVal":""},
        "建筑面积":{"key":"coverArea","defVal":0},
        "户型结构":{"key":"houseStruct","defVal":""},
        "套内面积":{"key":"insideArea","defVal":""},
        "建筑类型":{"key":"buildType","defVal":""},
        "房屋朝向":{"key":"orientation","defVal":""},
        "建筑结构":{"key":"buildStruct","defVal":""},
        "装修情况":{"key":"redecorated","defVal":""},
        "梯户比例":{"key":"ladderHouseholdRatio","defVal":""},
        "供暖方式":{"key":"heatingMode","defVal":""},
        "配备电梯":{"key":"isElevator","defVal":""},
        "产权年限":{"key":"property","defVal":""},
        "用水类型":{"key":"useWaterType","defVal":""},
        "用电类型":{"key":"electricityType","defVal":""},

        "挂牌时间":{"key":"listingDate","defVal":"1970-01-01"},
        "交易权属":{"key":"tradeRight","defVal":""},
        "上次交易":{"key":"lastTransaction","defVal":"1970-01-01"},
        "房屋用途":{"key":"houseUse","defVal":""},
        "房屋年限":{"key":"houseYears","defVal":""},
        "产权所属":{"key":"propertyOwner","defVal":""},
        "抵押信息":{"key":"mortgageInfo","defVal":""},
        "房本备件":{"key":"spareParts","defVal":""},
    }
    res = {};
    for key in keyMap:
        deepItem = keyMap[key];
        deepItemKey = deepItem['key'];
        deepItemDefVal = deepItem['defVal'];
        res[deepItemKey] = baseMap.get(key,deepItemDefVal);

    res['coverArea'] = covertFloat(res['coverArea']);
    return res;

def mapInfo2Arr(oMap):
    res = [];
    baseKeyArr = [
        "houseType",
        "floor",
        "coverArea",
        "houseStruct",
        "insideArea",

        "buildType",
        "orientation",
        "buildStruct",
        "redecorated",
        "ladderHouseholdRatio",

        "heatingMode",
        "isElevator",
        "property",
        "useWaterType",
        "electricityType",

        "listingDate",
        "tradeRight",
        "lastTransaction",
        "houseUse",
        "houseYears",
        "propertyOwner",
        "mortgageInfo",
        "spareParts",

        "totalPrice",
        "squareMetrePrice",
        
        "city",
        "area",
        "street"
        ]
    for key in baseKeyArr:
        res.append(oMap[key])
    return res;
    

def getHouseInfo(url):
    data = requests.get(url, headers=getAgent()).text
    page_text = data
    tree = etree.HTML(page_text)
    # 获取所有info
    obj = {};
    # 房屋基本信息
    dataKey = tree.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span/text()');
    data = tree.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/text()');
    # 交易属性
    dataKey2 = tree.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[1]/text()');
    data2 = tree.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[2]/text()');

    res = convertInfoAndNoValueSetDef(dataKey,data);
    res2 = convertInfoAndNoValueSetDef(dataKey2,data2);
    res3 = mergeMap([res,res2]);
    res4 = convertKeyName2English(res3);
    # 关注信息
    totalPrice = tree.xpath('/html/body/div[5]/div[2]/div[2]/span[1]/text()')[0] # 总价格
    squareMetrePrice = tree.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span/text()')[0] # 元/平

    res4['totalPrice'] = covertFloat(totalPrice)
    res4['squareMetrePrice'] = covertFloat(squareMetrePrice)
    return res4; # 房屋详情列表

def execStep4():

    

    with open('detail.txt','r',encoding='utf-8') as f :
        count = 0
        while 1:
            line = f.readline()
            if not line:
                break
            s = line.replace('\n','');
            tempObj = json.loads(s);
            
            info = getHouseInfo(tempObj['detailUrl']);
            info['city'] = tempObj['city']
            info['area'] = tempObj['area']
            info['street'] = tempObj['street']
            print('----------1访问的url为：'+ tempObj['detailUrl'])
            print('----------2info数据信息为：')
            
            print(info);
            paramList = mapInfo2Arr(info)
            print('----------3info数据信息结束')
            print(paramList)
            print('数据长度为：'+str(len(paramList)))
            execSql(*paramList);
            print('----------4插入操作结束')
            print(count);
            count+=1;

execStep4();
print('end')

print('test')
# print(getHouseInfo('https://tj.lianjia.com/ershoufang/101103011672.html'));







