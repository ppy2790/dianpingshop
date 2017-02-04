# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import json


class WebcrawlerScrapyPipeline(object):
    '''保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    def _conditional_insert(self, tx, item):
        # sql = "insert into jsit(author,title,url,pubday,comments,likes,rewards,views) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        # params = (item['author'], item['title'], item['url'], item['pubday'],item['comments'],item['likes'],item['rewards'],item['reads'])

        #sql = "insert into jobs(jobname,joburl,jobsalary,joblocation,jobnum,jobexpyear,jobpubday,companyname,jobdesc,companydesc) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #params = (item['jobtitle'], item['joburl'], item['jobsalary'], item['joblocation'],item['jobnum'],item['jobexpyear'],item['jobpubday'],item['companyname'],item['jobdesc'],item['companydesc'])
        #tx.execute(sql, params)

        # sql = "insert into lagou(jobname,joburl,jobsalary,jobexpyear,jobpubday,companyname,companytype,companylevel,jobdesc,edu) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # params = (item['jobtitle'], item['joburl'], item['jobsalary'], item['jobexpyear'],item['jobpubday'],item['companyname'],item['companytype'],item['companylevel'],item['jobdesc'],item['edu'])
        # tx.execute(sql, params)

        sql = "insert into foodshops(shopname,shoplevel,shopurl,commentnum,avgcost,taste,envi,service,foodtype,loc) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item['shopname'], item['shoplevel'], item['shopurl'], item['commentnum'],item['avgcost'],item['taste'],item['envi'],item['service'],item['foodtype'],item['loc'])
        tx.execute(sql, params)




    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue

