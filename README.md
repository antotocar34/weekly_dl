A simple script to download your spotify weekly playlist with the help of `spotipy` and `spotdl`.

# How to install

1. `git clone https://github.com/antotocar34/weekly_dl && cd weekly_dl`
2. Make a `config.json` file at `$HOME/.config/weekly_dl` with the following structure
```{json}
{
  "SPOTIFY_USER_ID" : "01234567890",
  "SPOTIFY_CLIENT_ID" : "a2a2a2a2a2a2a2a2a2a2a2a2a2a2a2a2",
  "SPOTIFY_CLIENT_SECRET" : "b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3b3"
}
```
where `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` are spotify api credentials.

3. `poetry install && poetry run python ./weekly_dl/main.py`
