import tkinter as tk
import json, threading, random, os
from tkinter import messagebox, Entry, Button, Label, ttk
from radio import Radio
from page import paging
from viewStationInfo import stationInfo
from stationSearcher import StationSearch
from saveFile import saveFile
from player import Player

class tkinterAppClass():
    def __init__(self, root):
        self.documents_path = os.path.join("C:\\Users", os.getlogin(), "Documents")
        self.station_array = self.saves = []
        self.playing = False
        self.current_station = ""
        self.api = Radio()
        self.root = root
        self.player = Player()
        
        # Main Frame
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Station Info Section
        station_info_frame = tk.LabelFrame(main_frame, text="Station Information", padx=10, pady=10)
        station_info_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)
        
        Label(station_info_frame, text="Station Count =").grid(row=0, column=0, sticky="w")
        self.station_count = Label(station_info_frame, text="NULL")
        self.station_count.grid(row=0, column=1, sticky="w")
        
        Label(station_info_frame, text='Station Name =').grid(row=1, column=0, sticky="w")
        self.display_station_name = Label(station_info_frame, text="NULL")
        self.display_station_name.grid(row=1, column=1, sticky="w")
        
        Label(station_info_frame, text="Station Country =").grid(row=2, column=0, sticky="w")
        self.display_station_country = Label(station_info_frame, text="NULL")
        self.display_station_country.grid(row=2, column=1, sticky="w")
        
        # Button Section
        button_frame = tk.Frame(main_frame, padx=10, pady=10)
        button_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
        
        self.get_station = Button(button_frame, text="Get All Stations", command=self.start_get_all_stations_thread)
        self.get_station.grid(row=0, column=0, padx=5, pady=5)
        
        self.random_station_button = Button(button_frame, text="Get a Random Station", command=self.get_random_station, state=tk.DISABLED)
        self.random_station_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.play_pause_button = Button(button_frame, text="▶ Play", command=self.play_pause, state=tk.DISABLED)
        self.play_pause_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.view_all_stations_button = Button(button_frame, text="View All Stations", command=self.view_all_stations, state=tk.DISABLED)
        self.view_all_stations_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.info_button = Button(button_frame, text="View More Information", command=lambda: stationInfo(self.root, self.current_station), state=tk.DISABLED)
        self.info_button.grid(row=1, column=1, padx=5, pady=5)
        
        self.search_button = Button(button_frame, text="Search", command=lambda: StationSearch(self.root, self.station_array, self), state=tk.DISABLED)
        self.search_button.grid(row=1, column=2, padx=5, pady=5)
        
        self.open_save_button = Button(button_frame, text="Open Save File", command=self.save_helper)
        self.open_save_button.grid(row=2, column=0, padx=5, pady=5)
        
        self.save_station_button = Button(button_frame, text="Save Station", command=self.save_station, state=tk.DISABLED)
        self.save_station_button.grid(row=2, column=1, padx=5, pady=5)
        
        # Set grid weights for proper resizing
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
    def save_helper(self):
        self.saves.append(saveFile(self.root, self))
    
    def save_station(self):
        self.folder_name = "Saved Stations"
        self.folder_path = os.path.join(self.documents_path, self.folder_name)
        self.json_file_name = "default_save.json"
        self.json_file_path = os.path.join(self.folder_path, self.json_file_name)
        
        try:
            os.makedirs(self.folder_path, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory: {e}")
            return
        
        stations = []
        if os.path.exists(self.json_file_path):
            try:
                with open(self.json_file_path, 'r') as json_file:
                    stations = json.load(json_file)
            except json.JSONDecodeError:
                pass
            
        if not any(s['stationuuid'] == self.current_station['stationuuid'] for s in stations):
            stations.append(self.current_station)
            
        try:
            with open(self.json_file_path, 'w') as json_file:
                json.dump(stations, json_file, indent=4)
            print(f"JSON file updated successfully at: {self.json_file_path}")
        except Exception as e:
            print(f"Error writing to file: {e}")
        
    def play_pause(self):
        if self.player.playing:
            print(f"Stopping Station : {self.current_station['name']}")
            # Stop playback in the main window
            self.player.stop()
            self.play_pause_button.config(text="▶ Play")
            
            # Ensure all saveFile buttons are set to "Play"
            for save in self.saves:
                if isinstance(save, saveFile):
                    if save.play_pause_button.cget('text') == "⏸ Pause":
                        save.play_pause_button.config(text="▶ Play")
        else:
            print(f"Playing Station : {self.current_station['name']}")
            # Check if any saveFile instance is playing
            if self.current_station:
                self.player.play(self.current_station['url'])
                self.play_pause_button.config(text="⏸ Pause")
                    
                # Set all saveFile buttons to "Play"
                for save in self.saves:
                    if isinstance(save, saveFile):
                        save.play_pause_button.config(text="▶ Play")

                
    def start_get_all_stations_thread(self):
        self.play_pause_button.config(text='▶ Play')
        self.root.after(0, lambda: self.change_buttons_state([
            self.get_station, self.random_station_button, self.play_pause_button,
            self.view_all_stations_button, self.info_button, self.search_button, self.save_station_button
        ], tk.DISABLED))
        threading.Thread(target=self.fetch_stations).start()

    def fetch_stations(self):
        print("Getting stations")
        self.root.after(0, self.create_progress_window)
        total_stations = self.api.downloadRadioBrowserStats()['stations']
        offset = 0
        limit = int(total_stations/3)
        while offset < total_stations:
            try:
                chunk = self.api.downloadRadioBrowserStations(offset, limit)
                if not chunk:
                    break# No more stations to fetch
                self.station_array.extend(chunk)
                # Update Tkinter progress bar and label
                self.root.after(0, self.update_progress, offset + len(chunk), total_stations)
                self.root.after(0, lambda: self.finalize_fetching(len(self.station_array)))
                offset += limit
                print(f"got {len(self.station_array)} stations out of a total of {total_stations} stations")
            except Exception as e:
                print(f"Failed to retrieve stations: {e}")
                break# Final updates
        self.root.after(0, lambda: getattr(self, 'progress_window', None) and self.progress_window.destroy())
        # Close progresswindow 

    def finalize_fetching(self, total_stations):
        self.station_count.config(text=f"Total Amount Of Stations: {total_stations}")
        self.change_buttons_state([
            self.get_station, self.random_station_button, self.view_all_stations_button, self.search_button
        ], tk.ACTIVE)

    def create_progress_window(self):
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.overrideredirect(1)
        self.progress_window.title("Progress Bar")
        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=20)
        self.progress_label = tk.Label(self.progress_window, text="Progress: 0%")
        self.progress_label.pack(pady=10)

    def update_progress(self, value, total_stations):
        self.progress_bar["value"] = value
        self.progress_bar["maximum"] = total_stations
        progress_percentage = (value / total_stations) * 100
        self.progress_label.config(text=f"Progress: {progress_percentage:.2f}%")
        self.progress_bar.update_idletasks()
        
    def change_buttons_state(self, buttons, state):
        for button in buttons:
            button.config(state=state)

    def get_random_station(self):
        self.current_station = random.choice(self.station_array)
        self.display_station_details(self.current_station)
        self.change_buttons_state([self.play_pause_button, self.info_button, self.save_station_button], tk.ACTIVE)
        if self.player.playing:
            self.player.stop()
            self.player.play(self.current_station['url'])

    def display_station_details(self, station):
        self.display_station_name.config(text=self.truncate_string(station['name']))
        self.display_station_country.config(text=self.truncate_string(station['country']))

    def truncate_string(self, string, length=22):
        return string[:length] + "..." if len(string) > length else string
    
    def view_all_stations(self):
        paging(self.root, self.station_array, self)

    def run(self):
        self.root.mainloop()