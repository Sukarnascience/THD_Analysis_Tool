# Digital Serial Plotter

## Project Structure

```
C:.
├───src
│   ├───assets
│   │   └───manifest.json
│   └───__pycache__
└───test
    └───dummyTHD
```

## Description

This project is a digital serial plotter designed to read and display sensor data in real-time. The configuration details, including device connections and value units, are defined in the `manifest.json` file located in the `assets` folder.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. The recommended Python version is defined in the `manifest.json` file. If your Python version does not match, use the `quick_setup.bat` file to download the required libraries.

### Installation

1. **Install Dependencies:**
   Run the `install.bat` file to install all required dependencies.
   ```bash
   install.bat
   ```

2. **Quick Setup:**
   If you encounter issues with the installation, use the `quick_setup.bat` file to download and install the necessary libraries.
   ```bash
   quick_setup.bat
   ```

### Running the Application

1. **Start the Application:**
   Use the `start.bat` file to launch the application.
   ```bash
   start.bat
   ```

### Configuration

Before starting the application, you need to configure the `manifest.json` file located in the `assets` folder.

```json
{
  "name": "THD Analysis Tool",
  "version": "5.4.0",
  "license": "GNU",
  "theme": "dark",
  "color": "green",
  "outsource": {
    "NWT 4": "C:/path/to/nwt4",
    "NWT 5": "C:/path/to/nwt5",
    "Deploy Graph": "C:/path/to/display_graph.py"
  },
  "units": [
    "VOLTAGE",
    "CURRENT",
    "PF",
    "kW",
    "kVA",
    "kVAR",
    "FREQUENCY",
    "kWh",
    "kVAh"
  ]
}
```

### Edit Configuration

1. **Outsource Paths:**
   Update the paths in the `outsource` key based on your system's directory structure.

2. **Units:**
   Ensure the units listed in the `units` key match the units your device will output.

## Testing Without a Device

If you do not have access to the actual device, you can test the software using the dummy Arduino code provided.

1. **Dummy Device Setup:**
   Upload the Arduino code located in `test/dummyTHD` to any Arduino board to simulate the device.

## Source Files

### `config.py`
Handles the configuration settings and reads the `manifest.json` file to apply the configurations.

### `device_handler.py`
Manages the connection and communication with the device, including reading sensor data.

### `display_graph.py`
Handles the plotting and graphical display of the sensor data in real-time.

### `main.py`
The main script that initializes the application and manages the overall workflow.

## Contact

For any issues or further assistance, please contact Sukarna Jana at sukarnascience@gmail.com .

```
This README file provides comprehensive instructions for installing, configuring, and running your software, as well as testing it with a dummy device if the actual device is not available.
```
