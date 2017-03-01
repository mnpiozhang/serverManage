#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os
from datetime import datetime

'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def set_log():
    # return log object
    logfile = os.path.abspath(os.path.join(BASE_DIR,'logs/dj'))+datetime.now().strftime("%Y-%m-%d")+'.log'
    logger_local = logging.getLogger('sm')
    
    filehdlr = logging.FileHandler(logfile)
    console = logging.StreamHandler()
    
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    filehdlr.setFormatter(formatter)
    console.setFormatter(formatter)
    
    logger_local.addHandler(filehdlr)
    logger_local.addHandler(console)
    
    logger_local.setLevel(logging.DEBUG)
    
    return logger_local



log = set_log()
'''


THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.abspath(os.path.join(THIS_DIR,'logs/dj.log')),
            'when': 'midnight',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False,
        },
        'sm': {
            'handlers': ['console','file'],
            'propagate': False,
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file'],
        'propagate': True,
    }
}
def set_log():
    logging.config.dictConfig(LOGGING)
    logging.getLogger("sm")

