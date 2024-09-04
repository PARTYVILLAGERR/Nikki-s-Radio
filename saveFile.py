import random, os, json, tkinter as tk
from tkinter import filedialog
from page import paging
from stationSearcher import StationSearch
from player import Player

class saveFile():
    def __init__(self, root, app_instance):
        self.player = Player()
        self.playing = False
        self.root = root
        self.app_instance = app_instance
        self.current_station = ""
        
        self.folder_name = "Saved Stations"
        self.folder_path = os.path.join(app_instance.documents_path, self.folder_name)
        self.file_path = filedialog.askopenfilename(
            title="Select a file",
            initialdir=self.folder_path,
            filetypes=[("JSON files", "*.json")]
        )
        
        if not self.file_path:
            return
        
        try:
            with open(self.file_path, 'r') as json_file:
                self.stations = json.load(json_file)
            print(f"Loaded Json File at Path: {self.file_path}")
        except json.JSONDecodeError:
            self.stations = []
        
        self.saveFileWindow = tk.Toplevel(self.root)
        self.saveFileWindow.title("Manage Saved Stations")
        self.saveFileWindow.geometry("400x200")
        
        # Station count display
        station_count_frame = tk.Frame(self.saveFileWindow)
        station_count_frame.pack(pady=10)
        tk.Label(station_count_frame, text="Station Count:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(station_count_frame, text=len(self.stations), font=("Arial", 10)).grid(row=0, column=1, padx=5)
        tk.Button(station_count_frame, text="Get A Random Station", command=self.get_random_station).grid(row=0, column=2, padx=5)
        
        # Station name display
        station_name_frame = tk.Frame(self.saveFileWindow)
        station_name_frame.pack(pady=10)
        tk.Label(station_name_frame, text="Station Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.display_station_name = tk.Label(station_name_frame, text="NULL", font=("Arial", 10))
        self.display_station_name.grid(row=0, column=1, padx=5)
        tk.Button(station_name_frame, text="Search", command=lambda: StationSearch(self.root, self.stations, self)).grid(row=0, column=2, padx=5)
        
        # Station country display
        station_country_frame = tk.Frame(self.saveFileWindow)
        station_country_frame.pack(pady=10)
        tk.Label(station_country_frame, text="Station Country:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.display_station_country = tk.Label(station_country_frame, text="NULL", font=("Arial", 10))
        self.display_station_country.grid(row=0, column=1, padx=5)
        self.play_pause_button = tk.Button(station_country_frame, text="▶ Play", command=self.playPause, state=tk.DISABLED)
        self.play_pause_button.grid(row=0, column=2, padx=5)
        
        # Bottom control buttons
        bottom_frame = tk.Frame(self.saveFileWindow)
        bottom_frame.pack(pady=10)
        tk.Button(bottom_frame, text="View All Stations", command=lambda: paging(self.root, self.stations, self)).grid(row=0, column=0, padx=10)
        self.load_station_button = tk.Button(bottom_frame, text="Load Station", command=self.load_station, state=tk.DISABLED)
        self.load_station_button.grid(row=0, column=1, padx=10)

    def get_random_station(self):
        self.current_station = random.choice(self.stations)
        self.display_station_name.config(text=self.current_station['name'])
        self.display_station_country.config(text=self.current_station['country'])
        self.load_station_button.config(state=tk.ACTIVE)
        self.play_pause_button.config(state=tk.ACTIVE)
        if self.player.playing:
            self.player.stop()
            self.player.play(self.current_station['url'])
        
    def update_play_pause_button(self, text):
        self.play_pause_button.config(text=text)
        
    def load_station(self):
        self.app_instance.display_station_name.config(text=self.app_instance.current_station['name'])
        self.app_instance.display_station_country.config(text=self.app_instance.current_station['country'])
        self.app_instance.playing = self.playing
        self.app_instance.play_pause_button.config(state=tk.ACTIVE)
        self.app_instance.save_station_button.config(state=tk.ACTIVE)
        self.playPause()
        
    def playPause(self):
        if self.player.playing:
            print(f"Stopping Station : {self.current_station['name']}")
            self.player.stop()
            self.play_pause_button.config(text="▶ Play")
            if self.app_instance.play_pause_button.cget('text') == "⏸ Pause":
                self.app_instance.play_pause_button.config(text="▶ Play")
        else:
            print(f"Playing Station : {self.current_station['name']}")
            if self.current_station:
                if self.play_pause_button.cget('text') == "▶ Play" or self.app_instance.play_pause_button.cget('text') == "▶ Play":
                    self.player.play(self.current_station['url'])
                    self.play_pause_button.config(text="⏸ Pause")
                    self.app_instance.play_pause_button.config(text="▶ Play")
            