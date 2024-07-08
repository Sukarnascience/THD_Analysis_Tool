import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import socket
from collections import deque
import threading

#my custom lib
import config

max_len = 20

class DataPlotter:
    def __init__(self, broadcast_host, broadcast_port):
        getSocketData = config.get_socket_config()
        print(getSocketData)
        self.broadcast_host = getSocketData[0]  # Set the broadcast host
        self.broadcast_port = getSocketData[1]  # Set the broadcast port

        # Initialize deque objects for each value
        self.voltage_data = deque(maxlen=max_len)
        self.frequency_data = deque(maxlen=max_len)
        self.charge_data = deque(maxlen=max_len)
        self.pressure_data = deque(maxlen=max_len)
        self.moisture_data = deque(maxlen=max_len)
        self.temperature_data = deque(maxlen=max_len)
        self.air_quality_data = deque(maxlen=max_len)
        self.partial_discharge_data = deque(maxlen=max_len)
        self.oil_level_data = deque(maxlen=max_len)

        # Set up UDP socket for receiving broadcasted data
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind((self.broadcast_host, self.broadcast_port))

    def receive_data(self):
        while True:
            try:
                data, _ = self.receive_socket.recvfrom(1024)
                data = data.decode('utf-8').split(',')
                print(data)
                if len(data) == 9:
                    values = data
                    values = list(map(float, values))
                    voltage, frequency, charge, pressure, moisture, temperature, air_quality, partial_discharge, oil_level = values
                    self.voltage_data.append(voltage)
                    self.frequency_data.append(frequency)
                    self.charge_data.append(charge)
                    self.pressure_data.append(pressure)
                    self.moisture_data.append(moisture)
                    self.temperature_data.append(temperature)
                    self.air_quality_data.append(air_quality)
                    self.partial_discharge_data.append(partial_discharge)
                    self.oil_level_data.append(oil_level)
            except Exception as e:
                print(f"Failed to fetch broadcast data: {e}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Data Plotter")

        self.data_plotter = DataPlotter(broadcast_host='localhost', broadcast_port=12345)

        self.create_widgets()

        # Start a separate thread to continuously receive data
        self.receive_thread = threading.Thread(target=self.data_plotter.receive_data)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.plot_data()

    def create_widgets(self):
        self.fig = Figure(figsize=(15, 10), dpi=100)

        # Create subplots for each value
        self.voltage_plot_area = self.fig.add_subplot(331)
        self.frequency_plot_area = self.fig.add_subplot(332)
        self.charge_plot_area = self.fig.add_subplot(333)
        self.pressure_plot_area = self.fig.add_subplot(334)
        self.moisture_plot_area = self.fig.add_subplot(335)
        self.temperature_plot_area = self.fig.add_subplot(336)
        self.air_quality_plot_area = self.fig.add_subplot(337)
        self.partial_discharge_plot_area = self.fig.add_subplot(338)
        self.oil_level_plot_area = self.fig.add_subplot(339)

        # Set titles and labels for each subplot
        self.voltage_plot_area.set_title('Voltage (V)')
        self.voltage_plot_area.set_xlabel('Time')
        self.voltage_plot_area.set_ylabel('Voltage (V)')

        self.frequency_plot_area.set_title('Frequency (Hz)')
        self.frequency_plot_area.set_xlabel('Time')
        self.frequency_plot_area.set_ylabel('Frequency (Hz)')

        self.charge_plot_area.set_title('Charge (uC)')
        self.charge_plot_area.set_xlabel('Time')
        self.charge_plot_area.set_ylabel('Charge (uC)')

        self.pressure_plot_area.set_title('Pressure (bar)')
        self.pressure_plot_area.set_xlabel('Time')
        self.pressure_plot_area.set_ylabel('Pressure (bar)')

        self.moisture_plot_area.set_title('Moisture (ppm)')
        self.moisture_plot_area.set_xlabel('Time')
        self.moisture_plot_area.set_ylabel('Moisture (ppm)')

        self.temperature_plot_area.set_title('Temperature (°C)')
        self.temperature_plot_area.set_xlabel('Time')
        self.temperature_plot_area.set_ylabel('Temperature (°C)')

        self.air_quality_plot_area.set_title('Air Quality (ppm)')
        self.air_quality_plot_area.set_xlabel('Time')
        self.air_quality_plot_area.set_ylabel('Air Quality (ppm)')

        self.partial_discharge_plot_area.set_title('Partial Discharge')
        self.partial_discharge_plot_area.set_xlabel('Time')
        self.partial_discharge_plot_area.set_ylabel('Partial Discharge')

        self.oil_level_plot_area.set_title('Oil Level (%)')
        self.oil_level_plot_area.set_xlabel('Time')
        self.oil_level_plot_area.set_ylabel('Oil Level (%)')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_data(self):
        self.voltage_plot_area.clear()
        self.frequency_plot_area.clear()
        self.charge_plot_area.clear()
        self.pressure_plot_area.clear()
        self.moisture_plot_area.clear()
        self.temperature_plot_area.clear()
        self.air_quality_plot_area.clear()
        self.partial_discharge_plot_area.clear()
        self.oil_level_plot_area.clear()

        if self.data_plotter.voltage_data:
            self.voltage_plot_area.plot(self.data_plotter.voltage_data, 'r-', label='Voltage')
            self.voltage_plot_area.legend()

        if self.data_plotter.frequency_data:
            self.frequency_plot_area.plot(self.data_plotter.frequency_data, 'g-', label='Frequency')
            self.frequency_plot_area.legend()

        if self.data_plotter.charge_data:
            self.charge_plot_area.plot(self.data_plotter.charge_data, 'b-', label='Charge')
            self.charge_plot_area.legend()

        if self.data_plotter.pressure_data:
            self.pressure_plot_area.plot(self.data_plotter.pressure_data, 'm-', label='Pressure')
            self.pressure_plot_area.legend()

        if self.data_plotter.moisture_data:
            self.moisture_plot_area.plot(self.data_plotter.moisture_data, 'c-', label='Moisture')
            self.moisture_plot_area.legend()

        if self.data_plotter.temperature_data:
            self.temperature_plot_area.plot(self.data_plotter.temperature_data, 'y-', label='Temperature')
            self.temperature_plot_area.legend()

        if self.data_plotter.air_quality_data:
            self.air_quality_plot_area.plot(self.data_plotter.air_quality_data, 'k-', label='Air Quality')
            self.air_quality_plot_area.legend()

        if self.data_plotter.partial_discharge_data:
            self.partial_discharge_plot_area.plot(self.data_plotter.partial_discharge_data, 'r-', label='Partial Discharge')
            self.partial_discharge_plot_area.legend()

        if self.data_plotter.oil_level_data:
            self.oil_level_plot_area.plot(self.data_plotter.oil_level_data, 'g-', label='Oil Level')
            self.oil_level_plot_area.legend()

        self.canvas.draw()

        self.root.after(1000, self.plot_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
