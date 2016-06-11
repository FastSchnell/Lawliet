from lawliet import Response, redirect, abort, Cache

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
    Cache.set('ok', 'test')
    Cache.expire('ok', 5)


def res_json(request):
    return {1: 2222}


def test_response():
    return Response(xml_str, headers={'Content-type': 'application/xml'})
