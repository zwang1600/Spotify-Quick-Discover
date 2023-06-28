## What is in this repo?
In this repo, you can use the Spotify web player to navigate through your playlists and listen to tracks by hovering over them.

## Authentication
You do have to get an access token from [this website](https://developer.spotify.com/documentation/web-playback-sdk/tutorials/getting-started) in order to get the website to work. You can generate an access token under "Authenticating with Spotify." Keep in mind that the token expires in 1 hour, but you can generate a new one after that.

After acquiring a token, go to line 58 in
```bash
/templates/home.html
```
and replace 'token' with your own token.

## How to get it to work?
In your terminal, run:
```bash
python main.py
```
After that, open up "http://localhost:8888" in your browser. If your authentication is correct, you should be able to use Spotify Quick Discover!


## Acknowledgements
This is a project from the class [HCDE 310: Interactive Systems Design & Technology](https://www.smunson.com/teaching/hcde310/a21/) from the University of Washington.
