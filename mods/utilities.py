from mods.setupflask import printerr
from random import choice

def errorHandle(e):
    line = e.__traceback__.tb_lineno-1
    printerr('File "{}", line {}, in {}'.format(e.__traceback__.tb_frame.f_code.co_filename,
                                               line,
                                               e.__traceback__.tb_frame.f_code.co_name))
    with open(e.__traceback__.tb_frame.f_code.co_filename) as f:
        lines = f.readlines()
        printerr('    {}\t{}'.format(line-1, lines[line-1][:-1]))
        printerr('>>> {}\t{}'.format(line,   lines[line][:-1]))
        printerr('    {}\t{}'.format(line+1, lines[line+1][:-1]))
        printerr('{}: {}'.format(str(type(e))[8:-2], str(e)))
        f.close()

def randChar(index=None) -> str:
    return choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-')

def randString(length: int) -> str:
    return ''.join(map(randChar, range(length)))

def addto(ns, name):
    def internal(func):
        setattr(ns, name, func)
        return None
    return internal

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)