import json
import os

# Default values
DEFAULT_VERSION = "v5.4.0"
DEFAULT_AUTHOR = "Sukarna Jana"
DEFAULT_LICENSE = "GNU"
DEFAULT_TITLE = "THD Analysis Tool"
DEFAULT_THEME = "dark"
DEFAULT_COLOR = "green"
DEFAULT_BROADCAST_HOST = "localhost"
DEFAULT_BROADCAST_PORT = 12345
DEFAULT_UNITS = ['VOLTAGE', 'CURRENT', 'PF', 'kW', 'kVA', 'kVAR', 'FREQUENCY', 'kWh', 'kVAh']

# Global variables
version = DEFAULT_VERSION
author = DEFAULT_AUTHOR
title = DEFAULT_TITLE
color = DEFAULT_COLOR
theme = DEFAULT_THEME
license = DEFAULT_LICENSE
manifest = None
broadcast_host = DEFAULT_BROADCAST_HOST
broadcast_port = DEFAULT_BROADCAST_PORT
units = DEFAULT_UNITS

def load_manifest():
    global version, author, license, title, theme, color, manifest, broadcast_host, broadcast_port, units
    manifest_path = os.path.join(os.path.dirname(__file__), "assets", "manifest.json")

    try:
        with open(manifest_path, "r") as f:
            manifest_data = json.load(f)
            manifest = manifest_data
            print("Loaded Sucessfully")
            # Update global variables from manifest data
            version = manifest_data.get("version", DEFAULT_VERSION)
            author = manifest_data.get("author", DEFAULT_AUTHOR)
            license = manifest_data.get("license", DEFAULT_LICENSE)
            title = manifest_data.get("name", DEFAULT_TITLE)
            theme = manifest_data.get("theme", DEFAULT_THEME)
            color = manifest_data.get("color",DEFAULT_COLOR)
            broadcast_host = manifest_data.get("broadcast", {}).get("host", DEFAULT_BROADCAST_HOST)
            broadcast_port = manifest_data.get("broadcast", {}).get("port", DEFAULT_BROADCAST_PORT)
            units = manifest_data.get("units",DEFAULT_UNITS)

    except FileNotFoundError:
        print(f"File '{manifest_path}' not found. Using default values.")
        # Use default values if file not found
        version = DEFAULT_VERSION
        author = DEFAULT_AUTHOR
        title = DEFAULT_TITLE
        color = DEFAULT_COLOR
        theme = DEFAULT_THEME
        license = DEFAULT_LICENSE
        manifest = None
        broadcast_port = DEFAULT_BROADCAST_PORT
        broadcast_host = DEFAULT_BROADCAST_HOST
        units = DEFAULT_UNITS
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}. Using default values.")
        # Use default values if JSON decoding error
        version = DEFAULT_VERSION
        author = DEFAULT_AUTHOR
        title = DEFAULT_TITLE
        color = DEFAULT_COLOR
        theme = DEFAULT_THEME
        license = DEFAULT_LICENSE
        manifest = None
        broadcast_port = DEFAULT_BROADCAST_PORT
        broadcast_host = DEFAULT_BROADCAST_HOST
        units = DEFAULT_UNITS

def get_version():
    return version

def get_author():
    return author

def get_license():
    return license

def get_theme():
    return theme

def get_color():
    return color

def get_title():
    return title

def get_manifest():
    return manifest

def get_units():
    return units

def get_socket_config():
    return [broadcast_host, broadcast_port]
# Load manifest data on script start
load_manifest()