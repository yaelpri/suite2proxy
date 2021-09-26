from os.path import isfile
from app.webpage import WebPage


class ViewLog(WebPage):

    _template = 'log.html'

    @staticmethod
    def modify(contents, **_):
        # TODO: Un-hardcode log name

        if isfile('.log'):
            with open('.log', 'r', encoding='utf-8') as log_file:
                return contents.format(LOG='<br>'.join(reversed(log_file.readlines())))
        else:
            return contents.format(LOG='Log not found at: ".log"')
