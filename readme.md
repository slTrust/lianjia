### house 为django

- model里对应数据库的表（这里是单表 29个字段，所有房屋信息）
    ```
    # 务必执行 
    # 初始化orm
    python manage.py makemigrations
    # 创建具体的表
    python manage.py migrate
    ```

### ershoufangPro 未 scrapy

爬取天津的所有二手房 省市区街道房屋详情信息

```
scrapy crawl lianjia
```