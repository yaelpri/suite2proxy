from os.path import abspath, dirname, join


_HERE = abspath(dirname(__file__))

DIR_JS = join(_HERE, 'js')
DIR_IMG = join(_HERE, 'img')
DIR_CSS = join(_HERE, 'css')
DIR_HTML = join(_HERE, 'html')


class Pages(object):
    """ Suite2Proxy routing utility object
    Allows for easy-to-use url-route definitions at method declaration point prior to instantiation
    create once inside your class """

    def __init__(self):
        self._pages = {}

    def add(self, route, methods=('GET', )):
        """ use |add| to decorate your class' methods with specific (route, methods) pairs """
        def _f(f):
            self._pages[route] = (f.__name__, list(methods))
            return f
        return _f

    def get(self):
        """ use |get| to fetch collected routes """
        for route, (callback_name, methods) in self._pages.items():
            yield route, callback_name, methods
