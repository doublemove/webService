#coding=utf-8
import sys
sys.path.append('D:\soaplib-master\src')
import soaplib
from soaplib.core.model.primitive import String
from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase     #所有的服务类都继承DefinitionBase基类
from soaplib.core.service import soap      #soap标识方法的特性



class webserver(DefinitionBase):
    @soap(String, _returns=String)
    def panDuan(self, date_time, department):
        return date_time, department

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([webserver], 'tns', 'webservice')
        wsgi_application = wsgi.Application(soap_application)


        server = make_server('127.0.0.1', 7789, wsgi_application)
        server.serve_forever()

    except ImportError:
        print "Error: example server code requires Python >= 2.5"