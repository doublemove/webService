#coding=utf-8
import sys
sys.path.append('D:\soaplib-master\src')
from datetime import datetime
import pickle, re
import soaplib
from soaplib.core.model.primitive import String,Integer
from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase     #所有的服务类都继承DefinitionBase基类
from soaplib.core.service import soap      #soap标识方法的特性
from soaplib.core.model.clazz import Array



class webserver(DefinitionBase):
    @soap(String, String, _returns=Array(Integer))
    def panDuanTimeAndDept(self, date_time, department):
        time_flag = 0
        time_delta = (datetime.strptime(date_time, "%Y-%m-%d") - datetime.now()).days + 1
        if time_delta > 0 and time_delta < 3:
            time_flag = 1
            
        department_flag = 0
        yuyue_info = pickle.load(open('data/data', 'r'))
        print yuyue_info
        if yuyue_info[department] == '':
            department_flag = 1
        
        return [time_flag, department_flag]
        
    @soap(String, String, String, _returns=Array(Integer))
    def response(self, type, shouji, department):
        if type == 'yuyue':
            geshi_flag = 1 if re.match(r'((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$', shouji) else 0
            yuyue_info = pickle.load(open('data/data', 'r'))
            shouji_flag = 1 if shouji not in yuyue_info.values() else 0
            
            if geshi_flag and shouji_flag:
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
        
        return [geshi_flag, shouji_flag]

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([webserver], 'tns', 'webservice')
        wsgi_application = wsgi.Application(soap_application)


        server = make_server('127.0.0.1', 7789, wsgi_application)
        server.serve_forever()

    except ImportError:
        print "Error: example server code requires Python >= 2.5"