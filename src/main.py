from tkinter import *
import customtkinter
import os
from PIL import Image, ImageTk
import time
import subprocess

# Custom Lib
import config

# Set appearance mode and default color theme
customtkinter.set_appearance_mode(config.theme)
customtkinter.set_default_color_theme(config.color)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title(config.title)
        self.geometry("1300x700+0+0")

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.script_dir, "assets", "logo.png")
        self.iconpath = ImageTk.PhotoImage(file=self.image_path)
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        self.minsize(1300, 700)
        self.maxsize(1500, 780)

        # Configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

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
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="THD\nAnalysis\nTool", font=customtkinter.CTkFont(size=20, weight="bold"), justify='left')
        self.logo_label.grid(row=1, column=0, padx=5, pady=(2, 20), sticky="")

        # Connection init
        self.label_radio_group = customtkinter.CTkLabel(master=self.sidebar_frame, text="Connect Sat :",font=customtkinter.CTkFont(size=20, weight="bold"), justify='left')
        self.label_radio_group.grid(row=2, column=0, padx=5, pady=(2, 2), sticky="")
        self.COMentry = customtkinter.CTkEntry(master=self.sidebar_frame, placeholder_text="COM4")#, textvariable=comNEnter)
        self.COMentry.grid(row=3, column=0, pady=(2, 2), padx=5, sticky="n")
        self.Boudentry = customtkinter.CTkEntry(master=self.sidebar_frame, placeholder_text="9600")#, textvariable=boudRateEnter)
        self.Boudentry.grid(row=4, column=0, pady=(2, 2), padx=5, sticky="n")
        self.sidebar_button_3 = customtkinter.CTkButton(master=self.sidebar_frame, text="Connect")#command=self.connectD
        self.sidebar_button_3.grid(row=5, column=0, pady=(2, 2), padx=5, sticky="n")
        
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
        self.appearance_mode_label.grid(row=9, column=0, padx=5, pady=(20, 2))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=5, pady=(2, 2))

        # UI Scaling option menu
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=5, pady=(2, 2))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=12, column=0, padx=5, pady=(2, 2))

        # Download button
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.download_in_CSV, text="Download as CSV")
        self.sidebar_button_3.grid(row=13, column=0, padx=20, pady=10)

        # Create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.tabview.add("Serial Monitor")
        self.tabview.add("Digital Serial Plotter")
        self.tabview.add("Graphical Serial Plotter")
        self.tabview.tab("Serial Monitor").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Graphical Serial Plotter").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Digital Serial Plotter").grid_columnconfigure(0, weight=1)

        # Example widgets in tab "Serial Monitor"

        # Example widgets in tab "Graphical Serial Plotter"

        # Start time
        self.start_time = time.time()

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

    def download_in_CSV(self):
        # Replace with your download logic
        print("Downloading CSV...")

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
    app.mainloop()
