import socket
import random
import time
from lib.server import server

__author__ = 'Maurício Souza Sathler'
__license__ = 'MIT'


if __name__ == '__main__':
    s = server()        # Initialize a server object with a default host and port

    while True:
        s.routine()     # Routine to colect new clients and create their threads

    s.close()           # close server
