import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from subprocess import run
from pathlib import Path
import datetime
import json

home = os.getenv("HOME")
BASE_DIR = f"{home}/.music/"

def read_config(config_file=None):
    config_file = f"{home}/.config/weekly_dl/config.json" if config_file is None else config_file
    with open( config_file, 'r') as f:
        config_json = json.load(f)
    return config_json


def creds(config_file=None) -> dict:
    config_json = read_config()
    SPOTIFY_CLIENT_ID = config_json["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET = config_json["SPOTIFY_CLIENT_SECRET"]
    USERID = config_json["SPOTIFY_USER_ID"]

    creds = {"client_id": SPOTIFY_CLIENT_ID,
             "client_secret": SPOTIFY_CLIENT_SECRET}

    client_id = creds["client_id"]
    client_secret = creds["client_secret"]

    print("Authenticating with spotipy")

    # Create weekly_dl cache in .local/share if it does not exist
    config_dir = Path(f"{home}/.local/share/weekly_dl")
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri="http://localhost:3000",
                                                   scope="playlist-read-private",
                                                   cache_handler=CacheFileHandler(cache_path=f"{home}/.local/share/weekly_dl/auth_cache")
                                                   ))
    # My user id
    user = USERID
    results = sp.user_playlists(user)
    assert results is not None, "Authentification failed"
    return results

def get_weekly_url(results: dict) -> str:
    url = None
    for d in results["items"]:
        if d["name"] == "Discover Weekly":
            url = d["external_urls"]["spotify"]
    assert url is not None, "Could not get weekly url from results set"
    return url
        
def get_directory_name() -> str:
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    date = monday.strftime("%d_%m_%Y")
    new_dir = f"spotify_weekly-{date}"
    return BASE_DIR + new_dir

def main(config_file=None):
    results = creds(config_file)

    weekly_url = get_weekly_url(results)

    download_dir = Path(get_directory_name())

    download_dir.mkdir(parents=True, exist_ok=True)

    result = run(["spotdl", weekly_url], 
                 cwd=str(download_dir)
                 )
if __name__ == "__main__":
    main()
