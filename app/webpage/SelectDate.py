from app.webpage import WebPage


class SelectDate(WebPage):

    _template = 'select-date.html'

    @staticmethod
    def modify(contents, mouse=None, date_folders=None):
        assert mouse
        assert date_folders
        return contents.format(
            MOUSE=mouse,
            FOLDERS='<br>'.join([
                f'<a class="btn long" href="/schedule-job?mouse={mouse}&date={date}">{date}</a>'
                for date in date_folders
            ])
        )

