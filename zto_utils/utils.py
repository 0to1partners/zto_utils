#%%
import logging
import os
from datetime import datetime
from time import time
from functools import wraps


class SingletonMeta(type) :
    def __call__(cls, *args, **kwargs) :
        try :
            return cls.__instance 
        except AttributeError :
            cls.__instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            return cls.__instance



# def time_elapsed(func, *args, **kwargs) :
#     @wraps(func)
#     def wrapper(func, *args, **kwargs) :

#         time_start = datetime.now()
#         ret = func(*args, **kwargs)
#         time_elapsed = datetime.now() - time_start

#         CustomLogger().info(f'{func} : time elpased ')
#         return ret
    
#     return wrapper


class TimeDecorator() :
    def __init__(self, f) :
        self.func = f

    def __call__(self, *args, **kwargs) :
        time_start = time.time()
        ret = self.func(*args, **kwargs)
        time_elapsed = round(time.time() - time_start, 3)

        msg = f'{self.func.__name__}'
        if len(args) > 0 :
            msg = msg + f'{args}'
        if len(kwargs) > 0 :
            msg = msg + f'{kwargs}'
        msg = f'Function {msg} : {time_elapsed}s elapsed '
        CustomLogger().info(msg)
        return ret
        



class CustomLogger(metaclass = SingletonMeta) :
    _logger = None

    def __init__(self) :
        self._logger = logging.getLogger('main')
        self._logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)s] > %(message)s'
            )

        now = datetime.now()

        dirname = './log'
        if not os.path.exists(dirname) :
            os.mkdir(dirname)
        
        fileHandler = logging.FileHandler( 
            os.path.join(dirname , 'log_' +  now.strftime("%Y%m%d") + '.log'))
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

