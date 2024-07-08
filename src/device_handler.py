import serial
import csv
import time
import os
import socket
import config
import ast #add

class ConnectDevice:
    def __init__(self):
        super().__init__()

        # Set some default parameters
        self.port = "COM4"
        self.baudRate = 9600
        self.timeOut = 0.1
        self.statusD = False
        self.device = None
        self.collectData = []

        getSocketData = config.get_socket_config()
        #print(getSocketData)
        self.broadcast_host = getSocketData[0]  # Set the broadcast host
        self.broadcast_port = getSocketData[1]  # Set the broadcast port
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self, portN="", baudRateN=9600, timeOutN=0.1):
        self.port = portN or self.port
        self.baudRate = baudRateN or self.baudRate
        self.timeOut = timeOutN

        try:
            self.device = serial.Serial(port=self.port, baudrate=self.baudRate, timeout=self.timeOut)
            self.statusD = True
            print("Connection established successfully")
        except Exception as e:
            self.statusD = False
            print(f"Connection failed: {e}")

    def is_connected(self):
        return self.statusD

    def send_data(self, data):
        try:
            if self.is_connected():
                self.device.write(data.encode())
                print("Data sent successfully")
            else:
                print("Device is not connected")
        except Exception as e:
            print(f"Failed to send data: {e}")

    def get_data(self):
        try:
            if self.is_connected():
                ser_bytes = self.device.readline()
                data = ser_bytes.decode("utf-8").strip()
                if(data!=""):
                    print(data)
                if data.startswith("[") and data.endswith("]"):
                    self.broadcast_data(data)
                    return data
                else:
                    #print("Data is corrupted")
                    return None
            else:
                print("Device is not connected")
                return None
        except Exception as e:
            print(f"Failed to get data: {e}")
            return None
        
    def broadcast_data(self, data):
        numbers_list = ast.literal_eval(data)
        numbers_str = ','.join(map(str, numbers_list))
        try:
            self.broadcast_socket.sendto(numbers_str.encode(), (self.broadcast_host, self.broadcast_port))
            print(f"Data broadcasted: {numbers_str}")
        except Exception as e:
            print(f"Failed to broadcast data: {e}")
