from app.webpage import WebPage


class SelectMouse(WebPage):

    _template = 'select-mouse.html'

    @staticmethod
    def modify(contents, data_folders=None, **_):
        assert data_folders

        return contents.format(FOLDERS='<br>'.join([
            f'<a class="btn long" href="/date?mouse={folder}">{folder}</a>'
            for folder in data_folders
        ]))
