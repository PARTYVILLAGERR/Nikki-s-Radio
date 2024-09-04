import vlc

class Player:
    active_player = None  # Class variable to track the currently playing instance

    def __init__(self):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.playing = False
        
    def play(self, media):
        # Stop the currently active player if there is one
        if Player.active_player is not None and Player.active_player != self:
            Player.active_player.stop()

        # Set this player as the active one and play the media
        Player.active_player = self
        if not self.playing:
            self.playing = True
            audio = self.instance.media_new(media)
            self.media_player.set_media(audio)
            self.media_player.play()
            
    def stop(self):
        if self.playing:
            self.playing = False
            self.media_player.stop()

            # Clear the active player if this instance is stopping
            if Player.active_player == self:
                Player.active_player = None