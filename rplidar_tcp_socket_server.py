
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import socket
HOST_NAME = '0.0.0.0'  # 設定主機名
PORT = 9999  # 設定埠號 要確保這個埠號沒有被使用，可以在cmd裡面檢視


PORT_NAME = 'com3'
DMAX = 4000
IMIN = 0
IMAX = 50


def update_line(num, iterator, line, connect_socket):
    scan = connect_socket.recv(99999)
    scan = str(scan, encoding='gbk')
    scan = scan.strip('[(').strip(')]')
    scan = scan.split('), (')
    for i in range(len(scan)):
        scan[i] = scan[i].split(',')   
     
    print(scan[0])
    try:
        scan=[(float(x),float(y),float(z)) for (x,y,z) in scan]
        offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
        line.set_offsets(offsets)
        intens = np.array([meas[0] for meas in scan])
        line.set_array(intens)
    except ValueError:
        print('error!')
    except TypeError:
        print('error!')
    return line,


def run():
    addr = (HOST_NAME, PORT)
    srv = socket.socket()  # 建立一個socket
    srv.bind(addr)
    srv.listen(5)
    print("waitting connect")
    connect_socket, client_addr = srv.accept()
    print(client_addr)

    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                      cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)

    iterator = connect_socket.recv(4000)
    ani = animation.FuncAnimation(fig, update_line,
                                  fargs=(iterator, line, connect_socket), interval=50)
    plt.show()
    


if __name__ == '__main__':
    run()
