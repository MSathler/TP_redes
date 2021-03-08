import socket
import random
import time
from lib.server import server

__author__ = 'Maurício Souza Sathler'
__license__ = 'MIT'

if __name__ == '__main__':
    s = server()

    while True:
        s.routine()

    s.close()
