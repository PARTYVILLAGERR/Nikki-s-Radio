import tkinter as tk

class stationInfo:
    def __init__(self, root, station):
        self.root = root
        self.station = station

        # Mapping descriptive labels to station data keys
        self.data_dict = {
            "Change UUID": "changeuuid",
            "Station UUID": "stationuuid",
            "Server UUID": "serveruuid",
            "Name": "name",
            "URL": "url",
            "Resolved URL": "url_resolved",
            "Homepage": "homepage",
            "Favicon": "favicon",
            "Tags": "tags",
            "Country": "country",
            "Country Code": "countrycode",
            "ISO 3166-2": "iso_3166_2",
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
            "Geo Latitude": "geo_lat",
            "Geo Longitude": "geo_long",
            "Has Extended Info": "has_extended_info"
        }

        # Create the Toplevel window
        self.stationWindow = tk.Toplevel(root)
        self.stationWindow.title(f"Information for {self.station.get('name', 'N/A')}")

        # Set up the scrollable content area
        self._setup_scrollable_area()

        # Populate the window with station information
        self._populate_station_info()

        # Update window size to fit the content
        self._update_window_size()

    def _setup_scrollable_area(self):
        """Sets up the scrollable area in the Toplevel window."""
        self.canvas = tk.Canvas(self.stationWindow)
        self.scrollbar = tk.Scrollbar(self.stationWindow, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _populate_station_info(self):
        """Populates the station information in the scrollable area."""
        for key, api_key in self.data_dict.items():
            self._create_info_row(key, self.station.get(api_key, 'N/A'))

    def _create_info_row(self, label, value):
        """Creates a row of information in the scrollable area."""
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(fill=tk.X, pady=5)

        tk.Label(frame, text=f"{label}:", width=20, anchor="w").pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text=value, wraplength=400, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(frame, text="Copy", command=lambda: self.copy(value)).pack(side=tk.RIGHT, padx=5)

    def _update_window_size(self):
        """Adjusts the Toplevel window size to match the content width."""
        self.stationWindow.update_idletasks()  # Ensure the content is fully rendered
        frame_width = self.scrollable_frame.winfo_width()
        self.stationWindow.geometry(f"{frame_width + 20}x400")  # Adjust window width and height as needed

    def copy(self, data):
        """Copies the given data to the clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(data)
        self.root.update()

    def _on_mouse_wheel(self, event):
        """Handles mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")