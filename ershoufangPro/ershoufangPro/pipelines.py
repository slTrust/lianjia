# -*- coding: utf-8 -*-
import pymysql

class ErshoufangproPipeline(object):
    def process_item(self, item, spider):
        return item

class AreaPipeline(object):
    conn = None

    # 在爬虫过程中，该方法只会在开始爬虫的时候调用一次
    def open_spider(self, spider):
        print('开始爬虫')
        # 连接数据库
        self.conn = pymysql.connect(host="localhost", user="root", password="831015", db="house", port=3306, charset="utf8")

    # 在爬虫过程中，该方法只会在爬虫结束的时候调用一次
    def close_spider(self, spider):
        print('结束爬虫')
        self.cursor.close()
        self.conn.close()

    # 该方法接收 爬虫文件中提交过来的item对象，并对item对象中存储的数据进行持久化存储
    '''
    :param
    # 参数item:表示接收到的item对象
    '''

    def process_item(self, item, spider):
        # 取出item对应的数据值
        infoParamList = item['infoParamList']

        # 连接数据库
        # 执行sql
        # sql语句
        sql = '''insert into app_house values(null,%s,%s,%s,%s,%s,
                                                     %s,%s,%s,%s,%s,
                                                     %s,%s,%s,%s,%s,
                                                     %s,%s,%s,%s,%s,
                                                     %s,%s,%s,%s,%s,
                                              %s,%s,%s);''';
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql,(*infoParamList,))
            self.conn.commit()
            # 提交事务
        except Exception as e:
            print(e)
            self.conn.rollback()

