import tkinter as tk
from tkinter import ttk
from page import paging
from radio import Radio

class StationSearch:
    def __init__(self, root, stations, app_instance):
        self.app_instance = app_instance
        self.root = root
        self.stations = stations
        self.searchTags = {}
        self.search_mapping = {
            "Change UUID": "changeuuid",
            "Station UUID": "stationuuid",
            "Server UUID": "serveruuid",
            "Name": "name",
            "URL": "url",
            "Resolved URL": "resolvedurl",
            "Homepage": "homepage",
            "Favicon": "favicon",
            "Tags": "tags",
            "Country": "country",
            "Country Code": "countrycode",
            "ISO 3166-2": "iso3166_2",
            "State": "state",
            "Language": "language",
            "Language Codes": "languagecodes",
            "Votes": "votes",
            "Last Change Time": "lastchangetime",
            "Last Change Time (ISO 8601)": "lastchangetime_iso8601",
            "Codec": "codec",
            "Bitrate": "bitrate",
            "HLS": "hls",
            "Last Check OK": "lastcheckok",
            "Last Check Time": "lastchecktime",
            "Last Check Time (ISO 8601)": "lastchecktime_iso8601",
            "Last Check OK Time": "lastcheckoktime",
            "Last Check OK Time (ISO 8601)": "lastcheckoktime_iso8601",
            "Last Local Check Time": "lastlocalchecktime",
            "Last Local Check Time (ISO 8601)": "lastlocalchecktime_iso8601",
            "Click Timestamp": "clicktimestamp",
            "Click Timestamp (ISO 8601)": "clicktimestamp_iso8601",
            "Click Count": "clickcount",
            "Click Trend": "clicktrend",
            "SSL Error": "ssl_error",
            "Geo Latitude": "geo_latitude",
            "Geo Longitude": "geo_longitude",
            "Has Extended Info": "has_extended_info"
        }

        # Toplevel window for the search interface
        self.searchTopLevel = tk.Toplevel(root)
        self.searchTopLevel.title("Search Window")
        self.searchTopLevel.geometry("600x400")
        
        # Create the main frame to hold all elements
        main_frame = tk.Frame(self.searchTopLevel, padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Search configuration section
        config_frame = tk.Frame(main_frame, padx=5, pady=5)
        config_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.tag_type_label = tk.Label(config_frame, text="Tag Type:")
        self.tag_type_label.grid(row=0, column=0, sticky="w", padx=5)
        
        self.searchStation = ttk.Combobox(config_frame, values=list(self.search_mapping.keys()), state="readonly")
        self.searchStation.set("Name")
        self.searchStation.grid(row=0, column=1, padx=5)

        self.tag_data_label = tk.Label(config_frame, text="Tag Data:")
        self.tag_data_label.grid(row=1, column=0, sticky="w", padx=5)
        
        self.searchEntry = tk.Entry(config_frame)
        self.searchEntry.grid(row=1, column=1, padx=5)

        self.addTagButton = tk.Button(config_frame, text="Add Tag", command=self.add_tag)
        self.addTagButton.grid(row=0, column=2, padx=5)
        
        self.removeTagButton = tk.Button(config_frame, text="Remove Tag(s)", command=self.remove_tag, state=tk.DISABLED)
        self.removeTagButton.grid(row=1, column=2, padx=5)

        self.clearTagButton = tk.Button(config_frame, text="Clear Tag(s)", command=self.clear_tags, state=tk.DISABLED)
        self.clearTagButton.grid(row=0, column=3, padx=5)
        
        self.searchButton = tk.Button(config_frame, text="Search", command=self.search, state=tk.DISABLED)
        self.searchButton.grid(row=1, column=3, padx=5)

        # Tag List Section
        self.tagFrame = tk.LabelFrame(main_frame, text="Selected Tags", padx=5, pady=5)
        self.tagFrame.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)

        self.tagListBox = tk.Listbox(self.tagFrame, height=10, width=60, selectmode=tk.EXTENDED)
        self.tagListBox.grid(row=0, column=0, sticky="nsew")

        self.tagScrollbar = tk.Scrollbar(self.tagFrame, orient=tk.VERTICAL, command=self.tagListBox.yview)
        self.tagScrollbar.grid(row=0, column=1, sticky="ns")
        self.tagListBox.config(yscrollcommand=self.tagScrollbar.set)

        # Configure grid weights for resizing
        self.searchTopLevel.grid_rowconfigure(0, weight=1)
        self.searchTopLevel.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.tagFrame.grid_rowconfigure(0, weight=1)
        self.tagFrame.grid_columnconfigure(0, weight=1)
        
    def add_tag(self):
        tag_data = self.searchEntry.get().strip()
        tag_type = self.searchStation.get().strip()
        tag_data_lower = tag_data.lower()

        if not tag_data:
            tk.messagebox.showinfo("Info", "Please enter tag data.")
            return

        if tag_type in self.searchTags:
            if any(tag_data_lower == tag.lower() for tag in self.searchTags[tag_type]):
                tk.messagebox.showinfo("Info", "This tag already exists.")
                return
            self.searchTags[tag_type].append(tag_data)
        else:
            self.searchTags[tag_type] = [tag_data]
    
        self.update_tag_listbox()

    def update_tag_listbox(self):
        self.tagListBox.delete(0, tk.END)
        for tag_type, tags in self.searchTags.items():
            for tag in tags:
                self.tagListBox.insert(tk.END, f"{tag_type}: {tag}")
        self.removeTagButton.config(state=tk.ACTIVE)
        self.clearTagButton.config(state=tk.ACTIVE)
        self.searchButton.config(state=tk.ACTIVE)

    def remove_tag(self):
        selected_indices = self.tagListBox.curselection()
        if not selected_indices:
            tk.messagebox.showerror("Error", "No tag selected to remove.")
            return
        
        for index in reversed(selected_indices):
            tag = self.tagListBox.get(index)
            self.tagListBox.delete(index)
            key, value = tag.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key in self.searchTags and value in self.searchTags[key]:
                self.searchTags[key].remove(value)
                if not self.searchTags[key]:
                    del self.searchTags[key]
                    
        if not self.searchTags:
            self.removeTagButton.config(state=tk.DISABLED)
            self.clearTagButton.config(state=tk.DISABLED)
            self.searchButton.config(state=tk.DISABLED)

    def clear_tags(self):
        self.searchTags.clear()
        self.tagListBox.delete(0, tk.END)
        self.removeTagButton.config(state=tk.DISABLED)
        self.clearTagButton.config(state=tk.DISABLED)
        self.searchButton.config(state=tk.DISABLED)
    
    def search(self):
        results = []
        for station in self.stations:
            match = True
            for tag_type, tags in self.searchTags.items():
                api_key = self.search_mapping.get(tag_type)
                station_value = station.get(api_key) if isinstance(station, dict) else getattr(station, api_key, None)
                if station_value:
                    station_tags = station_value.lower()
                    if not all(tag.lower() in station_tags for tag in tags):
                        match = False
                        break
                else:
                    match = False
                    break
            if match:
                results.append(station)
        paging(self.root, results, self.app_instance)