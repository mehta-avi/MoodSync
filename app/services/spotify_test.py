from spotify_api import SpotifyAPI
from my_secrets import client_id, client_secret, redirect_uri 


spotify = SpotifyAPI(client_id, client_secret, redirect_uri)
spotify.search_and_play('One Dance')

