import os
import shutil
from time import sleep, localtime
from json import dumps
from suite2p import run_s2p, default_ops
from os.path import join, exists
from multiprocessing import Process


class Worker(Process):
    """ Gets from engine setting to run in suite2p.
     Run the analysis by scheduled order. """

    INTERVAL = 1
    LOG_NAME = '.log'
    ENABLE_LOGGING = True
    WORKING_DIRECTORY = r'.\in_process'

    def __init__(self, incoming):
        self._incoming = incoming

        Process.__init__(self)

    def run(self):
        """ Main entry point for Worker process """

        while True:
            try:
                while not self._incoming.empty():
                    data = self._incoming.get_nowait()
                    if data is None:
                        raise InterruptedError('Stopped by parent (gracefully)')
                    self.process(*data)
            except InterruptedError:
                break
            sleep(self.INTERVAL)

    @classmethod
    def log(cls, *args, **kwargs):
        print(*args, **kwargs)
        if cls.ENABLE_LOGGING:
            with open(cls.LOG_NAME, 'a+', encoding='utf-8') as log_file:
                print(*args, file=log_file, **kwargs)

    @staticmethod
    def make_output_directory(exp_path):
        dir_out = join(exp_path, f'_results_{"".join(map(str, localtime()[:6]))}')
        while exists(dir_out):
            dir_out += '.'
        return dir_out

    @staticmethod
    def copy_function(root, processing_results_path):
        shutil.copytree(src=root, dst=join(processing_results_path, os.path.basename(root)))

    @classmethod
    def process(cls, settings, exp_paths):
        """ Copy data file from data dir to "in_process" dir.
        Run suite2p with the settings scheduled in the GUI.
        Move suite2p results to original data dir. """

        assert exp_paths

        if not os.path.isdir(cls.WORKING_DIRECTORY):
            os.mkdir(cls.WORKING_DIRECTORY)
        processing_results_path = cls.make_output_directory(cls.WORKING_DIRECTORY)

        cls.log(f'')
        for exp_path in exp_paths:
            cls.log(f'experiment={exp_path}')
        cls.log(f'settings={dumps(settings)}')

        cls.log(f'copying files... ({":".join(map(str, localtime()[:6]))})')
        suite2p_process_path = []
        for exp in exp_paths:
            shutil.copytree(src=exp, dst=join(processing_results_path, os.path.basename(exp)))
            suite2p_process_path.append(join(processing_results_path, os.path.basename(exp)))

        ops = default_ops()
        for key, value in settings.items():
            ops[key] = value

        cls.log(f'processing... ({":".join(map(str, localtime()[:6]))})')

        run_s2p(ops=ops, db=dict(data_path=suite2p_process_path, save_path0=processing_results_path))

        shutil.move(processing_results_path + '\suite2p', join(exp_paths[0], os.path.basename(processing_results_path)))
        shutil.rmtree(processing_results_path, ignore_errors=True)

        cls.log(f'processing is complete.')

        cls.log(f'results @ "{join(exp_paths[0], os.path.basename(processing_results_path))}"')
