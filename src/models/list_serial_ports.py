"""
Lists all the available serial ports on the system.
"""

import serial
import threading
import time


def get_available_serial_ports():
    ports = []
    threads = []
    lock = threading.RLock()

    for i in range(1, 256):
        t = threading.Thread(target=_check_serial_port, args=(lock, f'COM{i}', ports))
        t.daemon = True
        t.start()
        threads.append(t)

    while True in list(map(lambda x: x.is_alive(), threads)):
        time.sleep(0.01)

    if len(ports) == 0:
        ports.append('no ports')

    return sorted(ports)


def _check_serial_port(lock_object, port_name, port_list):
    try:
        p = serial.Serial(port_name)
        lock_object.acquire()
        try:
            port_list.append(port_name)
        finally:
            lock_object.release()
            p.close()
    except (Exception, ):
        pass


if __name__ == '__main__':

    start = time.perf_counter()
    print(get_available_serial_ports())
    stop = time.perf_counter()
    print('Ports detected in: {:.3f} seconds'.format(stop - start))
