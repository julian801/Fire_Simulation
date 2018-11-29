#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 14:13:36 2018

@author: julianchan
"""

"""
the logging module
exercise: change the value of 'level' to
          DEBUG, ERROR, WARNING, INFO and CRITICAL
          find out what is their order of precedence
"""

import logging
import sys

logging.basicConfig(filename='debug.log', level=logging.CRITICAL)



def factorial(n=10):
    """Calculates factorials with log messages."""
    i = 1
    factorial = 1
    while i < n:
        logging.info('starting iteration {}'.format(i))
        factorial *= i
        logging.debug('new factorial: {}'.format(factorial))
        i += 1
        #logging.info('unhandled event: ' + str(event))
    logging.warning('Final result: {}'.format(factorial))
        

if __name__ == '__main__':
    logging.warning('this is a warning message')
    logging.info('this is a info message')
    factorial(10)
    logging.critical('Factorial calculation ended')


# more loggers to try: 

# log = logging.getLogger('example1')
# log.addHandler(logging.FileHandler('debug2.log', mode='w'))
# log.setLevel(logging.DEBUG)
# log.info('spam')

# log2 = logging.getLogger('example2')
# handler = logging.StreamHandler(sys.stderr)
# log2.addHandler(handler)
# fmt='%(asctime)s %(message)s'
# handler.setFormatter(logging.Formatter(fmt, datefmt='%m/%d/%Y %I:%M:%S %p'))
# log2.setLevel(logging.WARNING)
# log2.warning('spam spam spam')