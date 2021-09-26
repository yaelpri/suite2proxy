from os.path import join
from app import DIR_HTML


class WebPage(object):
    """ Template for creating webpage.
    Returns html string.

    Containing fixed header and footer, the middle content created in | modify | by a specific inheritor.
    It is never called, but is inherited from multiple times, by each specific page.
    Overwriting of __new__ by WebPage preventing the inheritors from creating instances.
    """

    HEADER = '_header.html'
    FOOTER = '_footer.html'

    # webpage name
    _template = None

    @classmethod
    def html(cls, name):
        with open(join(DIR_HTML, name), 'r', encoding='utf-8') as html_file:
            return html_file.read()

    def __new__(cls, *expand_args, **expand_kwargs):

        assert cls._template is not None

        return ''.join((
            cls.html(cls.HEADER),
            cls.modify(
                cls.html(cls._template),
                *expand_args,
                **expand_kwargs
            ),
            cls.html(cls.FOOTER)
        ))

    @staticmethod
    def modify(contents, *expand_args, **expand_kwargs):
        """ override this for custom _pages """

        return contents
