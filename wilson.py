# -*- coding: utf-8 -*-

from .base import *

IS_TEST_ENV = True
enableCmdQR = False

HEAD_IMG_DIR = "{}/head_img".format(BASE_DIR)

DEBUG = True

ADMIN_DABASE = {

    'ENGINE': 'mysql',
    'NAME': 'mq_admin',
    'USER': 'test',
    'PASSWORD': 'test',
    'HOST': '192.168.89.38',  # Or an IP Address that your DB is hosted on
    'PORT': '3306',
    'charset': 'utf8mb4'

}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(filename)s:%(name)s:%(lineno)s %(message)s'
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {
            'handlers': ['logfile'],
            'level': 'DEBUG'
        }
    }
}
