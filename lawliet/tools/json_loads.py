import json
import re
def str_json(str):
    try:
        return json.loads(str)
    except:
        pass
    try:
        str = re.sub('\'', '\"', str)
        return json.loads(str)
    except:
        pass
    try:
        pass
    except:
        return {'errcode':'1005', 'errmsg':'json() error'}

