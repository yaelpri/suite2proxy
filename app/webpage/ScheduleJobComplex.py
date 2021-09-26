from os.path import dirname
from app.webpage import WebPage


class ScheduleJobComplex(WebPage):

    _template = 'schedule-job-complex.html'

    @staticmethod
    def modify(contents, path=None, experiment=None, dates2experiments=None, default_settings=None):
        assert path
        assert experiment
        assert dates2experiments
        assert default_settings

        return contents.format(
            PATH=dirname(path),
            BASE_EXP=experiment,
            SETTINGS='\n'.join([
                '\n'.join((
                    f'  <label class="settings-key">{key}</label>',
                    f'  <input type="text" name="{key}" class="settings-val" value="{value}"></input>'
                ))
                for key, value in default_settings.items()
            ]),
            TREE='\n'.join([
                '\n'.join([
                    f'<ul dir-date="{date_path}" list-title="{date}">',
                    *[
                      f'<li  dir-date="{date_path}" experiment="{exp}">{exp}</li>'
                        for exp
                        in experiments
                    ],
                    '</ul>'
                ])
                for (date, date_path), experiments
                in dates2experiments.items()
            ])
        )

