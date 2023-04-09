import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import secrets


class SpotifyAPI:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-library-read,user-read-playback-state,user-modify-playback-state')
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)

    def search_and_play(self, track_name):
        results = self.sp.search(q=track_name, type='track', limit=1)
            
        if len(results['tracks']['items']) > 0:
            track_id = results['tracks']['items'][0]['id']
            print(f"Playing track '{track_name}' with ID: {track_id}")
                
            # Get the list of available devices
            devices = self.sp.devices()
            if devices['devices']:
                # Extract the id of the first available device
                device_id = devices['devices'][0]['id']
                
                # Reactivate the player on the target device
                self.sp.transfer_playback(device_id)
                
                # Call the "/me/player/play" endpoint to play the track on the target device
                self.sp.start_playback(uris=['spotify:track:' + track_id])
            else:
                print("No active devices found.")
        else:
            print("No track found with the given name.")


    def play_music(self, track_id):
        self.sp.start_playback()

    def pause_music(self):
        self.sp.pause_playback()

    def skip_to_next_song(self):
        # Skip to the next song in the current playback
        self.sp.next_track()

    def skip_to_previous_song(self):
        # Skip to the previous song in the current playback
        self.sp.previous_track()

    def refresh_token(self):
        # Refresh the access token
        if self.sp_oauth.client_credentials_manager:
            self.sp_oauth.client_credentials_manager.get_access_token()
        else:
            token_info = self.sp_oauth.get_cached_token()
            if token_info and self.sp_oauth.is_token_expired(token_info):
                try:
                    token_info = self.sp_oauth.refresh_access_token(token_info['refresh_token'])
                    self.sp_oauth.token_info = token_info
                    self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)
                except spotipy.oauth2.SpotifyOauthError as e:
                    print(f"Error occurred while refreshing access token: {e}")
                    print("Make sure you have provided correct client ID, client secret, redirect URI, and refresh token.")
