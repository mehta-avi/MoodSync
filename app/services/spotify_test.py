from spotify_api import SpotifyAPI 
import secrets


spotify = SpotifyAPI(client_id, client_secret, redirect_uri)
# spotify.play_music(track_id)
# spotify.search_and_play("One Dance")
spotify.search_and_play_similar_song()