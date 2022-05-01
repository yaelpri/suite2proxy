from os import listdir
from os.path import dirname, isdir, join
from multiprocessing import Queue
from suite2p import default_ops

from engine.Worker import Worker


class Engine(object):
    """ Contains methods used by webpages.
    Send to Worker suite2p-run custom settings """

    # Experiment file extension
    FILE_FORMAT = 'raw'
    INPUT_FORMAT = 'haus'

    _SETTING_OVERRIDES = dict(
        fs=3.56,
        input_format=INPUT_FORMAT,
        delete_bin=False
    )

    USELESS_SETTINGS = (
        'fast_disk',
        'h5py',
        'save_path0',
        'save_folder',
        'subfolders',
        'nwb_driver',
        'nwb_file',
        'nwb_series'
    )

    DEFAULT_SETTINGS = default_ops()
    for useless_setting in USELESS_SETTINGS:
        del DEFAULT_SETTINGS[useless_setting]
    for key, value in _SETTING_OVERRIDES.items():
        DEFAULT_SETTINGS[key] = value

    # Use to test GUI and |sanity|
    _DIR_TEST_DATA = join(dirname(__file__), 'test')

    @classmethod
    def sanity(cls):
        """ Use this method to test basic application flow """

        dir_test_data = cls._DIR_TEST_DATA

        proxy = cls(data_root=dir_test_data,
                    data_extension=cls.FILE_FORMAT)

        proxy.activate_worker()

        for mouse in proxy.list_mouse_directories():
            for date in proxy.list_mouse_directories(mouse=mouse):
                dir_experiments = join(dir_test_data, mouse, date)
                for experiment in proxy.list_experiments(dir_experiments):
                    dir_experiment = join(dir_experiments, experiment)
                    proxy.schedule_job(cls.DEFAULT_SETTINGS, dir_experiment)

        proxy.terminate_worker()

    def __init__(self, data_root=None, data_extension=FILE_FORMAT):
        assert isdir(data_root)

        self._data_root = data_root
        self._data_ext = data_extension

        self._fifo = Queue()
        self._worker = Worker(self._fifo)
        self._active = False

    def activate_worker(self):
        assert not self._active, 'worker is already running'

        self._worker.start()
        self._active = True

    def wait_for_worker(self, timeout=None):
        assert self._active, 'worker is not running yet'

        self._worker.join(timeout=timeout)

    def terminate_worker(self):
        assert self._active, 'worker is not running yet'

        self._fifo.put_nowait(None)
        self.wait_for_worker()

    def list_mouse_directories(self, mouse=None):
        """ List all available data directories """

        root_path = self._data_root         \
            if mouse is None                \
            else join(self._data_root, mouse)

        assert isdir(root_path)

        return [
            name
            for name, path
            in (
                (p, join(root_path, p))
                for p
                in listdir(root_path)
            )
            if isdir(path)
            and listdir(path)
            and 'pycache' not in path
        ]

    def list_experiments(self, root_path):
        """ List all available experiments in given data directory """

        return [
            name
            for name, path
            in (
                (p, join(root_path, p))
                for p
                in listdir(root_path)
            )
            if isdir(path)
            and any(map(
                lambda fn: fn.endswith(self._data_ext),
                (
                    join(path, fn)
                    for fn
                    in listdir(path)
                )
            ))
        ]

    def schedule_job(self, settings, *experiment_dirs):
        """ Run list of experiments with custom settings """

        # Remark: Security flaw - data & exp names are controlled by user
        self._fifo.put_nowait((settings, experiment_dirs))
