#from lawliet.response import response
from lawliet import Response, redirect, abort, json

xml_str = u"""
 <xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>
"""
def ping():
    a = {'aaa':22}
    return a

def res_json(request):
    return request.get('qqq')

def test_response():
    return Response(xml_str, headers={'Content-type': 'application/xml'})
