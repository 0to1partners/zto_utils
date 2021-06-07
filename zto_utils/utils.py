import logging
import os
import datetime


class SingletonMeta(type) :
    def __call__(cls, *args, **kwargs) :
        try :
            return cls.__instance 
        except AttributeError :
            cls.__instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            return cls.__instance



class CustomLogger(metaclass = SingletonMeta) :
    _logger = None

    def __init__(self) :
        self._logger = logging.getLogger('main')
        self._logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s] > %(message)s'
            )

        now = datetime.datetime.now()

        dirname = './log'
        if not os.path.exists(dirname) :
            os.mkdir(dirname)
        
        fileHandler = logging.FileHandler( 
            os.path.join(dirname , 'Log' +  now.strftime("%Y%m%d") + '.log'))
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(logging.DEBUG)

        streamHandler.setFormatter(formatter)
        streamHandler.setLevel(logging.INFO)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

    def info(self, *args, **kwargs) :
        self._logger.info(*args, *kwargs)
    
    def debug(self, *args, **kwargs) :
        self._logger.debug(*args, *kwargs)
    
    def warning(self, *args, **kwargs) :
        self._logger.warning(*args, *kwargs)
    
    def error(self, *args, **kwargs) :
        self._logger.error(*args, *kwargs)

    def critical(self, *args, **kwargs) :
        self._logger.critical(*args, *kwargs)
