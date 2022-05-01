import ast
import numpy as np
from json import loads
from suite2p import default_ops
from argparse import ArgumentParser
from os.path import join, isdir, dirname, basename, abspath
from flask import Flask, request, send_from_directory

from engine import Engine

from app import Pages, DIR_CSS, DIR_IMG, DIR_JS

from app.webpage.Welcome import Welcome
from app.webpage.ViewLog import ViewLog
from app.webpage.SelectMouse import SelectMouse
from app.webpage.SelectDate import SelectDate
from app.webpage.ScheduleJob import ScheduleJob
from app.webpage.ScheduleJobComplex import ScheduleJobComplex


class Suite2Proxy(Flask):
    COMMAND_LINE_ARGUMENTS = {
        ('-p', '--port'): dict(
            type=int,
            default=80,
            help='Server http port'
        ),
        ('-4', '--ip'): dict(
            default='0.0.0.0',
            help='Provide ip for preferred network interface'
        ),
        ('-dr', '--data-root'): dict(
            help='Root experiment data directory'
        ),
        ('-dx', '--data-extension'): dict(
            default=Engine.FILE_FORMAT,
            help='experiment data extension (raw/???)'
        ),
        ('-op', '--ops'): dict(
            default=None,
            help='suite2p ops-file location'
        )
    }

    _pages = Pages()

    @classmethod
    def from_argv(cls):
        """ Deploy a new Server instance using configuration from command line arguments """

        parser = ArgumentParser()

        for argument_names, custom_parameter_settings in cls.COMMAND_LINE_ARGUMENTS.items():
            parser.add_argument(*argument_names, **custom_parameter_settings)

        arguments = parser.parse_args()

        if arguments.data_root is None:
            parser.print_help()
        else:
            srv = cls(
                data_extension=arguments.data_extension,
                data_root=arguments.data_root,
                ip=arguments.ip,
                port=arguments.port,
                ops=arguments.ops
            )

            return srv.serve_forever()

    def __init__(
        self,
        ip='0.0.0.0',
        port=80,
        data_root=None,
        data_extension=Engine.FILE_FORMAT,
        ops=None
    ):
        assert data_root

        self.ip = ip
        self.port = port
        self.data_root = data_root
        self.ops = ops

        self.engine = Engine(data_root=data_root,
                             data_extension=data_extension)

        Flask.__init__(self, type(self).__name__)

        for route, callback_name, methods in self._pages.get():
            self.route(
                route,
                methods=methods
            )(
                getattr(self, callback_name)
            )

    def serve_forever(self):
        self.engine.activate_worker()
        self.run(port=self.port, host=self.ip)

    @staticmethod
    def retype_settings(settings):
        typed_settings = {}
        for k, v in settings.items():
            try:
                typed_settings[k] = float(v) if '.' in v else int(v)
            except ValueError:
                if 'True' == v:
                    typed_settings[k] = True
                elif 'False' == v:
                    typed_settings[k] = False
                elif '[' == v[0]:
                    typed_settings[k] = ast.literal_eval(v)
                else:
                    typed_settings[k] = v
        return typed_settings

    @_pages.add('/js/<path:path>')
    def _js(self, path):
        """ Any file under app/js may be served """

        return send_from_directory(DIR_JS, path)

    @_pages.add('/css/<path:path>')
    def _css(self, path):
        """ Any file under app/css may be served """

        return send_from_directory(DIR_CSS, path)

    @_pages.add('/img/<path:path>')
    def _img(self, path):
        """ Any file under app/img may be served """

        return send_from_directory(DIR_IMG, path)

    @_pages.add('/favicon.ico')
    def _favicon(self):
        """ Serve tab icon """

        return send_from_directory(DIR_IMG, 'favicon.ico')

    @_pages.add('/')
    def _welcome(self):
        """ Main (landing) page """

        return Welcome()

    @_pages.add('/log')
    def _log_view(self):
        """ Realtime log-inspection page """

        return ViewLog()

    @_pages.add('/mouse')
    def _mouse_selection(self):
        """ Select individual mouse """

        return SelectMouse(self.engine.list_mouse_directories())

    @_pages.add('/date')
    def _date_selection(self):
        """ Select specific date for mouse-specific experiments """

        mouse = request.args.get('mouse')
        return SelectDate(mouse, self.engine.list_mouse_directories(mouse))

    @_pages.add('/schedule-job')
    def _schedule_job(self):
        """ Schedule suite2p computation job on a single experiment's data.
        Job is performed immediately when Engine's worker is free, otherwise queued with other jobs """

        dir_mouse = request.args.get('mouse')
        dir_date = request.args.get('date')

        if self.ops:
            settings_dict = np.load(self.ops, allow_pickle=True).item()
            settings = {key: value for (key, value) in settings_dict.items() if key in default_ops()}
            for useless_setting in self.engine.USELESS_SETTINGS:
                del settings[useless_setting]

        else:
            settings = self.engine.DEFAULT_SETTINGS

        path = join(self.data_root, dir_mouse, dir_date)

        assert isdir(path)
        return ScheduleJob(path, self.engine.list_experiments(path), settings)

    @_pages.add('/schedule-job-complex')
    def _schedule_job_complex(self):
        dir_date = request.args.get('dir_date')
        experiment = request.args.get('experiment')
        path = join(dir_date, experiment)
        assert isdir(path)

        mouse = basename(dirname(dir_date))

        dates2experiments = {
            (date, dir_date): self.engine.list_experiments(dir_date)
            for date, dir_date
            in [
                (date, join(self.data_root, mouse, date))
                for date
                in self.engine.list_mouse_directories(mouse)
            ]
        }

        return ScheduleJobComplex(path, experiment, dates2experiments, self.engine.DEFAULT_SETTINGS)

    @_pages.add('/register-job', methods=['POST'])
    def _register_job(self):
        data = loads(request.data)
        for date_path, experiments in data.items():
            for exp, settings in experiments.items():
                self.engine.schedule_job(self.retype_settings(settings), abspath(join(date_path, exp)))
        return 'SUCCESS'

    @_pages.add('/register-job-complex', methods=['POST'])
    def _register_job_complex(self):
        data = loads(request.data)
        settings = data['settings']
        experiments = [
            abspath(join(dir_date, exp_name))
            for dir_date, exp_name
            in data['experiments']
        ]
        self.engine.schedule_job(self.retype_settings(settings), *experiments)
        return 'SUCCESS'


'__main__' == __name__ and Suite2Proxy.from_argv()
