# coding=utf-8
import logging
import os


class context(object):
    cwd = "/home/explorer/mycontainer/"
    runc = "/home/explorer/project/blackzone/runc"
    log_level = 'INFO'

    def __init__(self):
        # init log
        log_path = os.path.join(self.cwd, "blackzone.log")
        self.dict_log_level = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARN': logging.WARN,
                               'ERROR': logging.ERROR,
                               'FATAL': logging.FATAL}
        # log_fmt = '[%(asctime)s] %(name)-8s: %(levelname)-8s %(message)s'
        log_fmt = '[%(asctime)s] : %(levelname)-7s >>>  %(message)s'

        logging.basicConfig(level=self.dict_log_level['DEBUG'],
                            format=log_fmt,
                            datefmt='%m-%d %H:%M',
                            filename=log_path,
                            filemode='a+')
        self.console = logging.StreamHandler()
        self.console.setLevel(self.dict_log_level[self.log_level])  # 输出到屏幕的log的level，默认INFO
        formatter = logging.Formatter(log_fmt)
        self.console.setFormatter(formatter)
        logging.getLogger('black_zone').addHandler(self.console)

    def get_logger(self):
        return logging.getLogger("black_zone")

    def __setattr__(self, key, value):
        if key == 'log_level':
            self.console.setLevel(self.dict_log_level[value])
        else:
            return object.__setattr__(self, key, value)

context = context()
