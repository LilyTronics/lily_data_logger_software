"""
Tester for serial port communications.
"""

import threading
import serial


class SerialCom(object):

    _TX_TIMEOUT = 2

    def __init__(self, port, baud, n_bits, parity, n_stop_bits, termination):
        self._termination = b"\n"
        if termination != "":
            self._termination = termination.encode()
        self._serial = serial.Serial(port=port, baudrate=int(baud), bytesize=int(n_bits), parity=parity,
                                     stopbits=float(n_stop_bits), write_timeout=self._TX_TIMEOUT)
        self._rx_thread = threading.Thread(target=self._receiver)
        self._rx_thread.daemon = True
        self._rx_thread.start()

    def _receiver(self):
        while True:
            if self._serial.in_waiting > 0:
                print("\nRX: {}".format(self._serial.read(self._serial.in_waiting)))

    def send(self, tx_data):
        output = tx_data.encode() + self._termination
        self._serial.write(output)
        print("TX: {}".format(output))


if __name__ == "__main__":

    _DEFAULTS = ["COM1", "9600", "8", "N", "1"]

    settings = input("Enter settings (defaults: {}): ".format(",".join(_DEFAULTS)))
    if settings == "":
        exit(1)

    parts = settings.split(",")
    if len(parts) < 1 or len(parts) > 5:
        print("Invalid input:", settings)
        exit(1)

    parts.extend(_DEFAULTS[len(parts):])

    parts.append(input("Enter termination (default: \\n): "))

    ser = SerialCom(*parts)
    while True:
        data = input("\nEnter data to send (q=quit): ")
        if data == "q":
            break
        ser.send(data)
