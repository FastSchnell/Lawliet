import json


def str_json(str):
    try:
        return json.loads(str)
    except:
        pass
    try:
        return eval(str)
    except:
        return {'errcode': '1005', 'errmsg': 'json() error'}


