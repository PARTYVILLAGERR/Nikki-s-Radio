import tkinter as tk
import random
from tkinter import ttk
from viewStationInfo import stationInfo

RESULTS_PER_PAGE = 10

class paging():
    def __init__(self, root, data_array, app_instance):
        self.app_instance = app_instance
        self.root = root
        self.data_array = data_array
        self.current_page = 0
        self.total_pages = (len(data_array) + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
        
        self.stationWindow = tk.Toplevel(root)
        self.stationWindow.title("Search Window")
        self.stationWindow.geometry("600x450")  # Initial size, can be adjusted dynamically

        # Create a main frame with padding
        self.searchFrame = ttk.Frame(self.stationWindow, padding="10 10 10 10")
        self.searchFrame.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the results
        self.results_frame = ttk.Frame(self.searchFrame)
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame for navigation buttons
        self.nav_frame = ttk.Frame(self.searchFrame, padding="5 5 5 5")
        self.nav_frame.pack(fill=tk.X, pady=10, side=tk.BOTTOM)

        # Initialize navigation buttons
        self.prev_button = ttk.Button(self.nav_frame, text="◀ Previous", command=self.prev_page, style='TButton')
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.page_label = ttk.Label(self.nav_frame, text=f"Page {self.current_page + 1} of {self.total_pages}", font=("Arial", 10, "bold"))
        self.page_label.pack(side=tk.LEFT, padx=10)

        self.next_button = ttk.Button(self.nav_frame, text="Next ▶", command=self.next_page, style='TButton')
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        self.random_station_button = ttk.Button(self.nav_frame, text="Get Random Station", command=lambda: self.load_station(random.choice(self.data_array)), style='TButton')
        self.random_station_button.pack(side=tk.LEFT, padx=5)
        
        # Station Counter Label
        self.station_counter = ttk.Label(self.nav_frame, text=f"Total Stations Found: {len(self.data_array)}", font=("Arial", 10, "bold"))
        self.station_counter.pack(side=tk.RIGHT, padx=5)

        self.update_display()

    def update_display(self):
        # Clear existing content
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Calculate indices for the current page
        start_index = self.current_page * RESULTS_PER_PAGE
        end_index = start_index + RESULTS_PER_PAGE
        subset = self.data_array[start_index:end_index]

        # Display new results
        for station in subset:
            item_frame = ttk.Frame(self.results_frame, padding="5 5 5 5", relief="solid")
            item_frame.pack(fill=tk.X, pady=5)

            stationName = station.get('name', 'Not Provided')

            ttk.Label(item_frame, text=f"Station Name: {stationName}", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
            
            ttk.Button(item_frame, text="View Information", command=lambda s=station: stationInfo(self.root, s), style='TButton').pack(side=tk.RIGHT, padx=10)
            ttk.Button(item_frame, text="Load Station", command=lambda s=station: self.load_station(s), style='TButton').pack(side=tk.RIGHT, padx=10)
        
        # Update labels and button states
        self.page_label.config(text=f"Page {self.current_page + 1} of {self.total_pages}")
        self.station_counter.config(text=f"Total Stations Found: {len(self.data_array)}")
        self.update_button_states()

        # Adjust the height dynamically based on content
        self.stationWindow.update_idletasks()  # Ensure the window and its content are fully rendered
        self.adjust_window_size()

    def adjust_window_size(self):
        """Adjust the window height based on its content."""
        content_height = self.results_frame.winfo_reqheight() + self.nav_frame.winfo_reqheight() + 50  # Add some padding
        content_width = self.nav_frame.winfo_reqwidth() + 25
        self.stationWindow.geometry(f"{content_width}x{content_height}")
        

    def update_button_states(self):
        """Enable or disable navigation buttons based on the current page."""
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page < self.total_pages - 1 else tk.DISABLED)

    def load_station(self, station):
        """Load the selected station into the main application."""
        self.app_instance.current_station = station
        self.app_instance.display_station_name.config(text=station['name'])
        self.app_instance.display_station_country.config(text=station['country'])
        self.app_instance.play_pause_button.config(state=tk.ACTIVE)
        if self.app_instance.player.playing:
            self.app_instance.player.stop()
            self.app_instance.player.play(station['url'])
        try:
            self.app_instance.save_station_button.config(state=tk.ACTIVE)
        except AttributeError as e:
            print("Could not find button, this is fine if it is a save file")
        
    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_display()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()