from flask_session import Session
from flask import Flask, session, redirect, render_template
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Global varaible for setup
CLIENT_ID = "cb9c0957660d4db4bec306b025a70d56"
CLIENT_SECRET = "61b4f8b477dc476a86400bb2b9a0d211"
REDIRECT_URL = 'http://localhost:5555/callback'
SCOPE = '''
user-read-currently-playing 
user-read-playback-state 
user-modify-playback-state 
user-follow-modify 
user-library-read'''

# App setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


@app.route("/")
def main_handler():
    global sp
    if sp:
        # Retrieve access token
        scc = SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        tokens = scc.get_access_token()

        # Get tracks - no longer used
        # covers = []
        # uris = []
        # track_ids = []
        # for track in sp.current_user_saved_tracks()['items']:
        #     covers.append(track['track']['album']['images'][0]['url'])
        #     uris.append(track['track']['uri'])
        #     track_ids.append(track['track']['id'])
        # tracks = zip(covers, uris)

        # Analyze tracks
        # data = sp.audio_analysis(track_ids[0])
        # loudest = data['sections'][0]['loudness']
        # start = data['sections'][0]['start']
        # for section in data['sections']:
        #     if section['loudness'] > loudest:
        #         loudest = section['loudness']
        #         start = section['start']

        # Get user playlists
        current_user_playlists = sp.current_user_playlists()
        names = []
        ids = []
        for playlist in current_user_playlists['items']:
            names.append(playlist['name'])
            ids.append(playlist['id'])
        playlists = zip(names, ids)

        # Render template
        rendered = render_template('home.html',
                                   accessToken=tokens['access_token'],
                                   seek=200000,
                                   playlists=playlists)

        return rendered
    else:
        return render_template('login.html')


@app.route("/login")
def login_handler():
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=SCOPE,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        show_dialog=True)
    global sp
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return redirect("/")


@app.route('/callback/')
def callback_handler():
    return render_template('home.html')


@app.route("/logout")
def logout():
    if "user_id" in session:
        session.pop("username")
    return redirect("/login")


if __name__ == "__main__":
    global sp
    sp = None
    app.run(host="localhost", port=1111, debug=True)
