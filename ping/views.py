from lawliet import response

xml_str = """
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
    return '1111111'

def res_json():
    return {'a': '11', 'b':999}

def test_response():
    return response(xml_str, 'application/xml')
