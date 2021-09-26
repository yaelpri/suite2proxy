from app.webpage import WebPage


class ScheduleJob(WebPage):

    _template = 'schedule-job.html'

    @staticmethod
    def modify(contents, dir_exp=None, data_files=None, default_settings=None):
        assert dir_exp
        assert data_files
        assert default_settings

        return contents.format(
            EXP=dir_exp,
            DATA_FILES=''.join([
                '\n'.join([
                    f'<form class="df-view" data-file="{df}" dir-exp="{dir_exp}">',
                    f'  <input type="checkbox" value="{df}">{df}</input>',
                    f'  <div class="inputs">',
                    *[
                        '\n'.join((
                            f'  <label class="settings-key">{key}</label>',
                            f'  <input type="text" name="{key}" class="settings-val" value="{value}"></input>'
                        ))
                        for key, value in default_settings.items()
                    ],
                    f'  </div>',
                    f'  <a class="btnplus" href="/schedule-job-complex?dir_date={dir_exp}&experiment={df}">🔗</a>',
                    '</form>'
                ])
                for df in data_files
            ])
        )

