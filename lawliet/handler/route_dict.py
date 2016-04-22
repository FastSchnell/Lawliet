

def tuple_dict(args):
    route_dict = dict()
    for i in args:
        key = i[0]
        i.pop(0)
        route_dict[key] = i
    return route_dict
