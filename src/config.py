import json
import os

# Default values
DEFAULT_VERSION = "v1.0.0"
DEFAULT_AUTHOR = "Sukarna Jana"
DEFAULT_LICENSE = "GNU"
DEFAULT_TITLE = "THD Analysis Tool - Alpha Edition"
DEFAULT_THEME = "dark"
DEFAULT_COLOR = "green"

# Global variables
version = DEFAULT_VERSION
author = DEFAULT_AUTHOR
title = DEFAULT_TITLE
color = DEFAULT_COLOR
theme = DEFAULT_THEME
license = DEFAULT_LICENSE
manifest = None

def load_manifest():
    global version, author, license, title, theme, color, manifest
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

# Load manifest data on script start
load_manifest()