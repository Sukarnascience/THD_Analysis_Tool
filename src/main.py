from tkinter import *
import customtkinter
import os
from PIL import Image, ImageTk
import time
import subprocess
import socket #add
import csv #add
import ast #add

# Custom Lib
import config
import device_handler as controller

# Set appearance mode and default color theme
customtkinter.set_appearance_mode(config.theme)
customtkinter.set_default_color_theme(config.color)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.logData = ""

        # Configure window
        self.title(config.title)
        self.geometry("1300x700+0+0")

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.script_dir, "assets", "logo.png")
        self.iconpath = ImageTk.PhotoImage(file=self.image_path)
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        self.status = controller.ConnectDevice()

        self.minsize(1300, 700)
        self.maxsize(1500, 780)

        # Configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #Broadcast Graph
        getSocketData = config.get_socket_config()
        self.broadcast_host = getSocketData[0]  # Set the broadcast host
        self.broadcast_port = getSocketData[1]  # Set the broadcast port
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create UDP socket
        self.collectData = []
        self.units = config.get_units()

        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")#rowspan=4,
        self.sidebar_frame.grid_rowconfigure(14, weight=1)

        # Set icon
        image_path = os.path.join(os.path.dirname(__file__), "assets")
        self.Logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(150, 150))
        self.home_logo = customtkinter.CTkLabel(master=self.sidebar_frame, text="", image=self.Logo)
        self.home_logo.grid(row=0, column=0, padx=5, pady=2, sticky="")

        # Logo and header
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="THD Analysis\nTool", font=customtkinter.CTkFont(size=20, weight="bold"), justify='center')
        self.logo_label.grid(row=1, column=0, padx=5, pady=(2, 20), sticky="")

        # Connection init
        self.label_conf_txt = customtkinter.CTkLabel(master=self.sidebar_frame, text="Configuration :",font=customtkinter.CTkFont(size=20, weight="bold"), justify='left')
        self.label_conf_txt.grid(row=2, column=0, padx=5, pady=(2, 2), sticky="")
        self.COMentry = customtkinter.CTkEntry(master=self.sidebar_frame, placeholder_text="COM4")#, textvariable=comNEnter)
        self.COMentry.grid(row=3, column=0, pady=(2, 2), padx=5, sticky="n")
        self.Boudentry = customtkinter.CTkEntry(master=self.sidebar_frame, placeholder_text="9600")#, textvariable=boudRateEnter)
        self.Boudentry.grid(row=4, column=0, pady=(2, 2), padx=5, sticky="n")
        self.connect_btn = customtkinter.CTkButton(master=self.sidebar_frame, text="Connect", command=self.connectD)#command=self.connectD
        self.connect_btn.grid(row=5, column=0, pady=(2, 2), padx=5, sticky="n")
        
        # Create buttons dynamically from outsource_data
        outsource_data = config.get_manifest().get("outsource", [])

        if outsource_data:
            for index, entry in enumerate(outsource_data):
                button_text = entry["name"]
                command_to_run = entry["exe"]

                # Create button with command execution
                button = customtkinter.CTkButton(
                    master=self.sidebar_frame,
                    command=lambda cmd=command_to_run: self.run_command(cmd),
                    text=button_text
                )
                button.grid(row=6 + index, column=0, pady=(2, 2), padx=5, sticky="n")

        # Additional label or UI element
        self.connectStatusText = customtkinter.CTkLabel(
            master=self.sidebar_frame,
            text="Not Connected",
            font=customtkinter.CTkFont(size=13, weight="bold"),
            justify='left'
        )
        self.connectStatusText.grid(row=6 + len(outsource_data), column=0, padx=5, pady=(2, 20), sticky="n")



        # Appearance Mode option menu
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=10, column=0, padx=5, pady=(20, 2))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=11, column=0, padx=5, pady=(2, 2))

        # UI Scaling option menu
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=12, column=0, padx=5, pady=(2, 2))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=13, column=0, padx=5, pady=(2, 2))

        # Graph button
        #self.down_csv = customtkinter.CTkButton(self.sidebar_frame, command=self.download_csv, text="Deploy Graph")
        #self.down_csv.grid(row=14, column=0, padx=20, pady=10)

        # Download button
        self.down_csv = customtkinter.CTkButton(self.sidebar_frame, command=self.download_csv, text="Download as CSV")
        self.down_csv.grid(row=14, column=0, padx=20, pady=10)

        # Create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.tabview.add("Serial Monitor")
        self.tabview.add("Digital Serial Plotter")
        #self.tabview.add("Graphical Serial Plotter")
        self.tabview.tab("Serial Monitor").grid_columnconfigure(0, weight=1) 
        self.tabview.tab("Serial Monitor").grid_rowconfigure(0, weight=0)
        self.tabview.tab("Serial Monitor").grid_columnconfigure(1, weight=0) 
        self.tabview.tab("Serial Monitor").grid_rowconfigure(1, weight=1)
        # self.tabview.tab("Graphical Serial Plotter").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Digital Serial Plotter").grid_columnconfigure((0, 1, 2), weight=1)
        self.tabview.tab("Digital Serial Plotter").grid_rowconfigure((0, 1, 2), weight=1)

        # Example widgets in tab "Serial Monitor"
        # create serialIn
        self.entry = customtkinter.CTkEntry(self.tabview.tab("Serial Monitor"), placeholder_text="Enter Serial Command")
        self.entry.grid(row=0, column=0, padx=5, pady=(20,2), sticky="nsew")
        self.serialSend = customtkinter.CTkButton(self.tabview.tab("Serial Monitor"), command=self.send_serial_data, text="Send", width=100)
        self.serialSend.grid(row=0, column=1, padx=5, pady=(20,2))
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab("Serial Monitor"))
        self.textbox.grid(row=1, column=0, columnspan=2, padx=5, pady=(2, 0), sticky="nsew")
        self.printInSerialMonitor()

        # Example widgets in tab "Graphical Serial Plotter"
        # Widgets in "Digital Serial Plotter" tab
        self.digital_values = []
        for i in range(3):
            for j in range(3):
                value_label = customtkinter.CTkLabel(self.tabview.tab("Digital Serial Plotter"), text=f"Value {i * 3 + j + 1}", font=("Helvetica", 40, "bold"))
                unit_label = customtkinter.CTkLabel(self.tabview.tab("Digital Serial Plotter"), text="Unit", font=("Helvetica", 12))
                value_label.grid(row=i, column=j, pady=(10, 10), padx=10, sticky="n")
                unit_label.grid(row=i, column=j, pady=(80, 10), padx=10, sticky="n")
                self.digital_values.append((value_label, unit_label))

        # Set default values
        self.appearance_mode_optionemenu.set(config.theme)
        self.scaling_optionemenu.set("100%")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_digital_plotter(self, numbers_list):
        for i, (value_label, unit_label) in enumerate(self.digital_values):
            if i < len(numbers_list):
                value_label.configure(text=f"{numbers_list[i]}")
                unit_label.configure(text=self.units[i])
            else:
                value_label.configure(text="N/A")
                unit_label.configure(text="N/A")

    def on_closing(self, event=0):
        self.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def run_command(self, command):
        try:
            # Use subprocess to run the command in a new terminal window
            subprocess.Popen(f'start cmd /c {command}', shell=True)
        except Exception as e:
            print(f"Error: {str(e)}")

    def download_csv(self):
        filename = "full_backup.csv"
        if self.collectData:
            try:
                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    # Process all entries
                    processed_data = [self.process_entry(entry) for entry in self.collectData]
                    writer.writerows(processed_data)
                print(f"Data backed up to {filename}")
            except Exception as e:
                print(f"Failed to backup data: {e}")
        else:
            print("No data to backup")

    def createLiveData(self, fname, data):
        try:
            with open(('live_{}.csv'.format(fname)), 'a', newline='') as file:
                writer = csv.writer(file)
                # Split the datetime string into date and time
                datetime_str = data[0]
                date_str, time_str = datetime_str.split()

                # Convert the string representation of the list to an actual list of numbers
                numbers_list = ast.literal_eval(data[1])

                # Combine everything into the desired format
                final_list = [date_str, time_str] + numbers_list
                writer.writerow(final_list)
                self.collectData.append(data)
                try:
                    file.close()
                except:
                    print("Failed to close the file")
            print("Backup Successfully")
        except:
            print("Backup Failed")
    # Function to process a single entry
    def process_entry(self,entry):
        datetime_str = entry[0]
        date_str, time_str = datetime_str.split()
        numbers_list = ast.literal_eval(entry[1])
        return [date_str, time_str] + numbers_list

    def connectD(self):
        port_value = self.COMentry.get()
        baud_rate_value = self.Boudentry.get()

        if port_value and baud_rate_value:
            try:
                port_number = port_value
                baud_rate = int(baud_rate_value)
                self.logData = "Data Collected are: {},{}\n".format(port_value, baud_rate_value)
                self.textbox.insert("0.0", self.logData)
                print("Data Collected are: {},{}".format(port_value, baud_rate_value))
                self.status.connect(portN=port_number, baudRateN=baud_rate)
            except ValueError:
                print("Invalid input: Port number and baud rate must be integers")
        else:
            print("Port number and baud rate cannot be empty")

    def updateConn_stats(self):
        if(self.status.is_connected()):
            self.connectStatusText.configure(text="Connected")
        else:
            self.connectStatusText.configure(text="Not Connected")
        self.connectStatusText.after(200, self.updateConn_stats)
    
    def printInSerialMonitor(self):
        if self.status.is_connected():
            logData = self.status.get_data()
            if logData:
                self.textbox.insert("end", logData + "\n")
                self.textbox.see("end")
                self.createLiveData("live_data", [time.strftime("%Y-%m-%d %H:%M:%S"), logData])
                numbers_list = ast.literal_eval(logData)
                self.update_digital_plotter(numbers_list)
        self.after(200, self.printInSerialMonitor)
    def send_serial_data(self):
        if self.status.is_connected():
            command = self.entry.get()
            self.status.send_data(command)
            self.entry.delete(0, 'end')



if __name__ == "__main__":
    # Header information
    '''
    header_info = f"""
========================================
    Version: {config.version}
    Author: {config.author}
    License: {config.license}
========================================
    """
    print(header_info.strip())
    '''
    # Run the application
    app = App()
    app.updateConn_stats()
    app.printInSerialMonitor()
    app.mainloop()