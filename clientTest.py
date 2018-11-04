#coding=utf-8

from suds.client import Client

host = '127.0.0.1'
port = 7789
client = Client('http://%s:%s/?wsdl' % (host, port))

print client.service.GetModel('1212')