#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import socket

hostname = '192.168.137.1'
port = 9999

PORT_NAME = '/dev/ttyUSB0'


def run():
    lidar = RPLidar(PORT_NAME)
    iterator = lidar.iter_scans()
    addr = (hostname, port)
    clientsock = socket.socket()  # 建立一個socket
    clientsock.connect(addr)  # 建立連線
    clientsock.send(bytes(str(iterator), encoding='gbk'))  # 傳送訊息
    try:
        print('Recording measurments... Press Crl+C to stop.')
        while True:
            scan = next(iterator)
#            print(scan)
            clientsock.send(bytes(str(scan), encoding='gbk'))  # 傳送訊息
    except KeyboardInterrupt:
        print('Stoping.')
    clientsock.close()
    lidar.stop()
    lidar.disconnect()


if __name__ == '__main__':
    run()

