from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url = "https://www.billboard.com/charts/hot-100/" + date

response = requests.get(url=url,headers=header)
bilboard_web_page = response.text

soup = BeautifulSoup(bilboard_web_page,"html.parser")
spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in spans]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6e2a19dbea31438aa6797aebe5644888",
                                               client_secret="7104ea35d9864b62ab939963deeb068c",
                                               redirect_uri="http://127.0.0.1:8888/callback",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))
user_id = sp.current_user()["id"]


song_uris = []
year = date.split("-")[0]


for song in song_names:
     result = sp.search(q=f"track:{song} year:{year}", type="track")
     try:
         uri = result["tracks"]["items"][0]["uri"]
         song_uris.append(uri)
     except IndexError:
         print(f"'{song}' not found on Spotify.")

playlist = sp.user_playlist_create(
                        user=user_id,
                        name=f"{date} Bilboard 100",
                        public=False,
                        description="Top 100 songs from Billboard"
                        )

sp.playlist_add_items(
                    playlist_id = playlist["id"],
                    items = song_uris,
                    )
