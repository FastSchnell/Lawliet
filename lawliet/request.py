import json
def get_input(**kwargs):
    try:
        len_input = int(kwargs['CONTENT_LENGTH'])
        input_str = kwargs['wsgi.input'].read(len_input)
        if kwargs['CONTENT_TYPE'] == 'application/json':
            return json.loads(input_str)
        return input_str
    except:
        return None
