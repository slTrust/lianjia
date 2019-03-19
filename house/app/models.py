from django.db import models

# Create your models here.

class House(models.Model):
    id = models.AutoField(primary_key=True)

    house_type = models.CharField(max_length=32)
    floor = models.CharField(max_length=32)
    coverArea = models.DecimalField(max_digits=12, decimal_places=2)
    house_struct = models.CharField(max_length=32)
    inside_area = models.CharField(max_length=32)

    build_type = models.CharField(max_length=32)
    orientation = models.CharField(max_length=32)
    build_struct = models.CharField(max_length=32)
    redecorated = models.CharField(max_length=32)
    ladder_household_ratio = models.CharField(max_length=32)

    heating_mode = models.CharField(max_length=32)
    is_elevator = models.CharField(max_length=32)
    property = models.CharField(max_length=32)
    use_water_type = models.CharField(max_length=32)
    electricity_type = models.CharField(max_length=32)

    listing_date = models.DateField()
    trade_right = models.CharField(max_length=32)
    last_transaction = models.DateField()
    house_use = models.CharField(max_length=32)
    house_years = models.CharField(max_length=32)
    property_owner = models.CharField(max_length=32)
    mortgage_info = models.CharField(max_length=32)
    spare_parts = models.CharField(max_length=32)

    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    square_metre_price = models.DecimalField(max_digits=12, decimal_places=2)
    district = models.CharField(max_length=32)
    address = models.CharField(max_length=32)


    city = models.CharField(max_length=32)
    area = models.CharField(max_length=32)
    street = models.CharField(max_length=32)



'''
obj['houseType'] = replaceLine(data[0]); # 房屋户型
obj['floor'] = replaceLine(data[1]); # 所在楼层
obj['coverArea'] = float(replaceLine(data[2])); # 建筑面积
obj['houseStruct'] = replaceLine(data[3]); # 户型结构
obj['insideArea'] = replaceLine(data[4]); # 套内面积
obj['buildType'] = replaceLine(data[5]); # 建筑类型
obj['orientation'] = replaceLine(data[6]); # 房屋朝向
obj['buildStruct'] = replaceLine(data[7]); # 建筑结构
obj['redecorated'] = replaceLine(data[8]); # 装修情况
obj['ladderHouseholdRatio'] = replaceLine(data[9]); # 梯户比例
obj['heatingMode'] = replaceLine(data[10]); # 供暖方式
obj['isElevator.'] = replaceLine(data[11]); # 配备电梯
obj['property'] = int(replaceLine(data[12])); # 产权

useWaterType 用水类型
electricityType 用电类型


# 交易属性
obj['listingDate'] = replaceLine(data2[0]) ; # 挂牌时间
obj['tradeRight'] = replaceLine(data2[1]);  # 交易权属
obj['lastTransaction'] = replaceLine(data2[2]);  # 上次交易
obj['houseUse'] = replaceLine(data2[3]);  # 房屋用途
obj['houseYears'] = replaceLine(data2[4]);  # 房屋年限
obj['propertyOwner'] = replaceLine(data2[5]);  # 产权所属
obj['mortgageInfo'] = replaceLine(data2[6]);  # 抵押信息
obj['spareParts'] = replaceLine(data2[7]);  # 房本备件

# 关注信息
obj['totalPrice'] = tree.xpath('/html/body/div[5]/div[2]/div[2]/span[1]/text()')[0] # 总价格
obj['squareMetrePrice']
obj['district']
obj['address']

info['city'] = tempObj['city']
info['area'] = tempObj['area']
info['street'] = tempObj['street']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'house',# 要连接的数据库，连接前需要创建好
        'USER':'root',# 连接数据库的用户名
        'PASSWORD':'831015',# 连接数据库的密码
        'HOST':'127.0.0.1',       # 连接主机，默认本级
        'PORT':3306 #  端口 默认3306
    }
}
'''
