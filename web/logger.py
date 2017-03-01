#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os
from datetime import datetime


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
            'filename': os.path.abspath(os.path.join(THIS_DIR,'logs/sm.log')),
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

