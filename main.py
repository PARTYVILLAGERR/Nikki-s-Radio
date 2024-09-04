import os
import sys
import tkinter as tk
from tkinter import PhotoImage
from appRun import tkinterAppClass

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Nikki's Radio v1.0")

    # Use forward slashes or raw strings for paths
    icon_image_path = resource_path("RadioBrowserV2/images.png")
    icon_path = resource_path("RadioBrowserV2/images.ico")

    # Set taskbar icon using the PNG file
    try:
        icon = PhotoImage(file=icon_image_path)
        root.iconphoto(True, icon)
    except tk.TclError as e:
        print(f"Error loading taskbar icon: {e}")

    # Set window icon using the ICO file
    try:
        root.iconbitmap(icon_path)
    except tk.TclError as e:
        print(f"Error loading window icon: {e}")

    app = tkinterAppClass(root)
    app.run()