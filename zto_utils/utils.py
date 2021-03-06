#%%
import logging
from logging import getLogger, handlers
import os
from datetime import datetime
from time import time
from functools import wraps
from multiprocessing import Queue

class SingletonMeta(type) :
    def __call__(cls, *args, **kwargs) :
        try :
            return cls.__instance 
        except AttributeError :
            cls.__instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            return cls.__instance



def time_elapsed(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :

        time_start = time()
        ret = func(*args, **kwargs)
        time_elapsed = round( time() - time_start, 3 )

        msg = f'{func.__name__}'
        if len(args) > 0 :
            msg = msg + f'{args}'
        if len(kwargs) > 0 :
            msg = msg + f'{kwargs}'
        msg = f'Function {msg} : {time_elapsed}s elapsed '
        CustomLogger().info(msg)

        return ret
    
    return wrapper


# class TimeDecorator() :
#     def __init__(self, f) :
#         self.func = []#f
#         self.func.append(f)

#     def __call__(self, *args) :
#         print(args)
#         # print(args, kwargs)
#         time_start = time()
#         ret = self.func[0](*args)
#         time_elapsed = round( time() - time_start, 3 )

#         msg = f'{self.func.__name__}'
#         if len(args) > 0 :
#             msg = msg + f'{args}'
#         # if len(kwargs) > 0 :
#             # msg = msg + f'{kwargs}'
#         msg = f'Function {msg} : {time_elapsed}s elapsed '
#         CustomLogger().info(msg)
#         return ret

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


class CustomLoggerMulti(metaclass = SingletonMeta) :
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

        # ??? ????????? ??????
        self.file_queue = Queue()
        file_queue_handler = handlers.QueueHandler(self.file_queue)
        self._logger.addHandler(file_queue_handler)

        self.stream_queue = Queue()
        stream_queue_handler = handlers.QueueHandler(self.stream_queue)
        self._logger.addHandler(stream_queue_handler)

        self.file_listner = handlers.QueueListener(self.file_queue, fileHandler)
        self.stream_listner = handlers.QueueListener(self.stream_queue, streamHandler)
        self.file_listner.start()
        self.stream_listner.start()

    def get_logger(self) :
        return self._logger


logger = CustomLoggerMulti().get_logger()



# %%
if __name__ == '__main__' :
    a = CustomLoggerMulti()
    b = CustomLoggerMulti()
    print( a is b, a == b)

# %%

CustomLoggerMulti().get_logger().info('aa')

# %%
