# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
import requests
import pygame

class Spotify:
    ID_CLIENTE = '4a1d64facea94a94b12ecdc5989248b7'
    CHAVE_CLIENTE = '67b6b5ef75684d27b4b2350f286e1f8b'

    def __init__(self):
        self.token = self.get_token()
        self.header = {"Authorization": f"Bearer {self.token}"}
        self.base_url = "https://api.spotify.com/v1/"
        self.audio_file = "/temp/audio.mp3"


    def get_token(self):
        url = "https://accounts.spotify.com/api/token"

        header = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": Spotify.ID_CLIENTE,
            "client_secret": Spotify.CHAVE_CLIENTE
        }

        response = requests.post(url, headers=header ,data=data)
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()['access_token']
        else:
            print(f"Erro ao conectar ao spotify {response.text}")
            return None


    def search_track(self, nome_musica):
        url = f'{self.base_url}search'
        params = {
            "q": nome_musica,
            "type": "track",
            "limit": 1
        }

        response = requests.get(url, headers=self.header, params=params)

        if response.status_code >= 200 and response.status_code < 300:
            data = response.json()
            if data['tracks']['items']:
                track_info = data['tracks']['items'][0]
                return {
                    'name': track_info['name'],
                    'artist': track_info['artists'][0]['name'],
                    'album': track_info['album']['name'],
                    'preview_url': track_info['preview_url']
                }
            else:
                print("Nenhuma música encontrada.")
                return None
        else:
            print(f"Erro ao pesquisar música: {response.text}")
            return None


    def play_track(self, nome_musica):
        track_info = self.search_track(nome_musica=nome_musica)
        if track_info:
            preview_url = track_info['preview_url']
            if preview_url:
                audio_data = requests.get(preview_url).content
                with open(self.audio_file, 'wb') as f:
                    f.write(audio_data)

                try:
                    pygame.init()
                    pygame.mixer.music.load(self.audio_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                except Exception as e:
                    print(f"Erro ao reproduzir áudio: {e}")
            else:
                print("URL de pré-visualização inválida.")
        else:
            print("Nenhuma informação disponível.")