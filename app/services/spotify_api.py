import spotipy
from spotipy.oauth2 import SpotifyOAuth
import secrets


class SpotifyAPI:
    def __init__(self, client_id, client_secret, redirect_uri):
        # Initialize SpotifyOAuth with client ID, client secret, and redirect URI
        self.sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-library-read,user-read-playback-state,user-modify-playback-state')
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)

    def search_and_play(self, track_name):
        # Search for a song by name
        results = self.sp.search(q=track_name, type='track', limit=1)
        
        # Extract the track ID from the search results
        if len(results['tracks']['items']) > 0:
            track_id = results['tracks']['items'][0]['id']
            print(f"Playing track '{track_name}' with ID: {track_id}")
            
            # Play the track
            self.play_music(track_id)
        else:
            print("No track found with the given name.")
    
    def get_currently_playing_track(self):
        # Get the currently playing track's information
        currently_playing = self.sp.current_playback()
        return currently_playing

    def search_and_play_similar_song(self):
        # Get the currently playing track's information
        currently_playing = self.get_currently_playing_track()
                
        # Extract the track ID from the currently playing track's information
        if currently_playing is not None:
            track_id = currently_playing['item']['id']
            print(currently_playing['item']['genres'])

            # Get the track's properties (e.g., artist, album, genre)
            artist = currently_playing['item']['artists'][0]['name']
            album = currently_playing['item']['album']['name']
            genre = currently_playing['item']['genres'][0] if 'genres' in currently_playing['item'] else None
            
            # Search for similar songs based on the track's properties
            results = self.sp.search(q=f'genre:"{genre}"', type='track', limit=10)

            # print(results)
            # Extract the track ID from the search results
            if len(results['tracks']['items']) > 0:
                track_id = results['tracks']['items'][0]['id']
                print(f"Playing similar track with ID: {track_id}")
                
                # Play the similar track
                self.play_music(track_id)
            else:
                print("No similar track found.")
        else:
            print("No track is currently playing.")

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