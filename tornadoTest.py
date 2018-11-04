#coding=utf-8
import os.path
import tornado.web
import tornado.httpserver
import tornado.ioloop
from datetime import datetime
import pickle
import re

from suds.client import Client

host = '127.0.0.1'
port = 7789
client = Client('http://%s:%s/?wsdl' % (host, port))
print u'成功连上web service'

if not os.path.exists('data/data'):
    yuyue_info = {'neike': '', 'waike': ''}
    data = open('data/data', 'w')
    pickle.dump(yuyue_info, data)
    data.close()

#定义处理类型
class IndexHandler(tornado.web.RequestHandler):
    #添加一个处理get请求方式的方法
    def get(self):
        #向响应中，添加数据
        self.render('index.html')

class Yuyue01Handler(tornado.web.RequestHandler):
    #添加一个处理get请求方式的方法
    def get(self):
        #向响应中，添加数据
        self.render('yuyue01.html')

class Yuyue02Handler(tornado.web.RequestHandler):
    #添加一个处理get请求方式的方法
    def post(self):
        #得到数据
        try:
            date_time = self.get_argument('date')
        except:
            date_time = datetime.now().strftime("%Y-%m-%d")
        department = self.get_argument('department')
        print date_time, department
        
        flags = list(client.service.panDuanTimeAndDept(date_time, department))
        
        self.render('yuyue02.html', time_flag=flags[0][1][0], department_flag=flags[0][1][1], department=department)

class QuxiaoHandler(tornado.web.RequestHandler):
    #添加一个处理get请求方式的方法
    def get(self):
        #向响应中，添加数据
        self.render('quxiaoyuyue.html')

class ResponseHandler(tornado.web.RequestHandler):
    #添加一个处理post请求方式的方法
    def post(self):
        #得到数据
        shouji = self.get_argument('shouji')
        type = self.get_argument('type')
        department = self.get_argument('department', 'neike')
        
        flags = list(client.service.response(type, shouji, department))
            
        self.render('response.html', type=type, geshi_flag=flags[0][1][0], shouji_flag=flags[0][1][1])

if __name__ == '__main__':
    #创建一个应用对象
    app = tornado.web.Application(
        handlers = [(r'/',IndexHandler), (r'/yuyue01',Yuyue01Handler), (r'/yuyue02',Yuyue02Handler), (r'/quxiaoyuyue', QuxiaoHandler), (r'/response', ResponseHandler)],
        template_path = os.path.join(os.path.dirname(__file__), "html"))
    
    http_server = tornado.httpserver.HTTPServer(app)
    #绑定一个监听端口
    http_server.listen(8888)
    #启动web程序，开始监听端口的连接
    tornado.ioloop.IOLoop.current().start()