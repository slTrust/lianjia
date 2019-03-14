# -*- coding: utf-8 -*-
import scrapy
from ershoufangPro.items import AreaItem
import re
import json



class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    # allowed_domains = ['tj.lianjia.com/ershoufang']
    # start_urls = ['https://tj.lianjia.com/ershoufang/']

    def start_requests(self):  # 由此方法通过下面链接爬取页面

        # 定义爬取的链接
        urls = [
            'https://tj.lianjia.com/ershoufang',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse1)

    # 解析区的url
    def parse1(self, response):
        areaLinks = response.xpath('//div[@data-role="ershoufang"]/div/a/@href');
        baseUrl = 'https://tj.lianjia.com/ershoufang/'
        for i in areaLinks:
            area = replaceStringErshoufang(i.extract())
            curUrl = baseUrl +area;
            #  所有区的url
            # print('小区的url'+curUrl);
            item = AreaItem();
            item['city'] = 'tj';
            item['area'] = area;
            yield scrapy.Request(url=curUrl, callback=self.parse2,meta={'item':item})

    #  解析街道的url
    def parse2(self, response):
        # 获取参数
        item = response.meta['item']
        streetLinks = response.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href');
        baseUrl = 'https://tj.lianjia.com/ershoufang/'


        for i in streetLinks:
            street = replaceStringErshoufang(i.extract())
            curUrl = baseUrl + street;
            #  所有街道的url
            # print('街道的'+curUrl);
            item['street'] = street;
            item['baseStreetUrl'] = curUrl
            yield scrapy.Request(url=curUrl, callback=self.parse3,meta={'item':item})
        pass

    #  解析街道的url 对应的totalPage
    def parse3(self, response):
        item = response.meta['item']
        # print('parse3-------------解析 item参数-')
        streetsTotalPage = response.xpath('//*[@class="contentBottom clear"]/div[2]/div[1]/@page-data');
        res = json.loads(streetsTotalPage[0].extract()); # 总页数
        curPage = res['curPage'];
        totalPage = res['totalPage'];
        # print(res);
        # 生成 该街道所有页码的url
        url = item['baseStreetUrl']
        streetUrlList = convertUrlList(url,totalPage)
        # print('获取所有街道的url pg数组')
        # print(streetUrlList)
        for i in streetUrlList:
            #  街道的url 第 xx页的url
            item['streetPgUrl'] = i;
            yield scrapy.Request(url=i, callback=self.parse4,meta={'item':item})
        pass

 #  解析街道的url 对应的每页 30条数据的详情url
    def parse4(self, response):
        item = response.meta['item']
        # print('第四步解析开始----------'+item['streetPgUrl'])
        detailUrls = response.xpath('//div[@class="leftContent"]/ul/li/a[@data-el="ershoufang"]/@href');
        for i in detailUrls:
            detailUrl = i.extract()
            #  所有区的url
            item['detailUrl'] = detailUrl;
            # print('每页房屋的url===》 ' + detailUrl);
            yield scrapy.Request(url=detailUrl, callback=self.parse5,meta={'item':item})

    #  解析房屋的url 对应的 房屋信息
    def parse5(self, response):
        item = response.meta['item']
        print('第5步解析 房屋信息开始----------'+item['detailUrl'])
        print(item);
        # 获取所有info
        obj = {};
        # 房屋基本信息
        dataKey = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span/text()');
        tempKey = []
        for i in dataKey:
            tempKey.append(i.extract());

        data = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/text()');
        tempData = []
        for i in data:
            tempData.append(i.extract());
        # 交易属性
        dataKey2 = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[1]/text()');
        tempKey2 = []
        for i in dataKey2:
            tempKey2.append(i.extract());
        data2 = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li/span[2]/text()');
        tempData2 = []
        for i in data2:
            tempData2.append(i.extract());
        res = convertInfoAndNoValueSetDef(tempKey, tempData);
        res2 = convertInfoAndNoValueSetDef(tempKey2, tempData2);
        res3 = mergeMap([res, res2]);
        res4 = convertKeyName2English(res3);

        # 关注信息
        totalPrice = response.xpath('/html/body/div[5]/div[2]/div[2]/span[1]/text()')[0].extract()  # 总价格
        squareMetrePrice = response.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span/text()')[0].extract()  # 元/平

        res4['totalPrice'] = covertFloat(totalPrice)
        res4['squareMetrePrice'] = covertFloat(squareMetrePrice)
        print('叶子节点的所有信息对象')
        res4['city'] = item['city']
        res4['area'] = item['area']
        res4['street'] = item['street']
        paramList = mapInfo2Arr(res4);
        print('数据长度为：' + str(len(paramList)))
        # print(paramList);

        item['infoParamList'] = paramList;

        return item

def replaceStringErshoufang(string):
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

def convertUrlList(baseUrl,totalPage):
    count = 1;
    res = []
    while count<=totalPage:
        page = '' if count==1 else ('/pg'+str(count)+'/');
        url = baseUrl + page
        res.append(url);
        count+=1;
    return res;

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