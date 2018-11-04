#coding=utf-8
import os.path
import tornado.web
import tornado.httpserver
import tornado.ioloop
from datetime import datetime
import pickle
import re

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
        
        time_flag = 0
        time_delta = (datetime.strptime(date_time, "%Y-%m-%d") - datetime.now()).days + 1
        if time_delta > 0 and time_delta < 3:
            time_flag = 1
            
        department_flag = 0
        yuyue_info = pickle.load(open('data/data', 'r'))
        print yuyue_info
        if yuyue_info[department] == '':
            department_flag = 1
        
        self.render('yuyue02.html', time_flag=time_flag, department_flag=department_flag, department=department)

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
        
        if type == 'yuyue':
            geshi_flag = 1 if re.match(r'((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$', shouji) else 0
            yuyue_info = pickle.load(open('data/data', 'r'))
            shouji_flag = 1 if shouji not in yuyue_info.values() else 0
            
            if geshi_flag and shouji_flag:
                department = self.get_argument('department')
                yuyue_info[department] = shouji
                data = open('data/data', 'w')
                pickle.dump(yuyue_info, data)
                data.close()
        elif type == 'quxiaoyuyue':
            geshi_flag = 1 if re.match(r'((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$', shouji) else 0
            yuyue_info = pickle.load(open('data/data', 'r'))
            shouji_flag = 1 if shouji in yuyue_info.values() else 0
            
            if geshi_flag and shouji_flag:
                if yuyue_info['neike'] == shouji:
                    yuyue_info['neike'] = ''
                    print 'neike'
                elif yuyue_info['waike'] == shouji:
                    yuyue_info['waike'] = ''
                    print 'waike'
                print yuyue_info
                data = open('data/data', 'w')
                pickle.dump(yuyue_info, data)
                data.close()
            
        self.render('response.html', type=type, geshi_flag=geshi_flag, shouji_flag=shouji_flag)

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