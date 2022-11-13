##########
# IMPORT #
##########
import base64
import requests

def get_access_token():
    client_creds = f"7efceb8a917642719a27f76a8a458978:ccda20d8959e46efb384184cabf3e260".encode()
    client_creds_b64 = base64.b64encode(client_creds)

    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "client_credentials",
        "scope": "playlist-read-public  playlist-modify-public playlist-read-private  playlist-modify-private"
    }
    token_header = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }

    response = requests.post(token_url, data=token_data, headers=token_header)
    return response.json()["access_token"]

# Récupérer les sons dans la playlist
def get_playlist_items(playlist_id):
    tracks_id = []
    offset = 0
    total_tracks = 0
    count = 0

    response_total = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", 
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        })

    if response_total.status_code == 200:
        total_tracks = response_total.json()["tracks"]["total"]
    else:
        print(f"ERROR: {response_total.status_code} - {response_total.reason}")
        return

    print(f"\nPlaylist : " + response_total.json()["name"])

    while count < total_tracks:
        response_tracks = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100&offset={offset}", 
            headers={
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            })

        if response_total.status_code != 200:
            print(f"ERROR: {response_total.status_code} - {response_total.reason}")
            return

        json_resp_tracks = response_tracks.json()

        for track in json_resp_tracks["items"]:
            tracks_id.append({"id": track["track"]["id"], "artist": track["track"]["artists"][0]["name"], "name": track["track"]["name"]})
            count += 1

        offset += 100
        
    print(f"Total de {count} sons enregistrés")

    return tracks_id

# Récupérer les sons non présent dans BING CHILLING
def check_items():
    final_tracks = []

    if len(mix_detente_items) <= 0 or len(bing_chilling_items) <= 0:
        print("Playlist vide")
        return 0

    for current_track in mix_detente_items:
        if not current_track in bing_chilling_items:
            final_tracks.append(current_track)

    return final_tracks

# Ajouter les sons dans BING CHILLING
def add_tracks(playlist_id):
    count = 0

    print("\n-----Ajout des sons-----")

    for track in new_tracks:
        response_add = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris=spotify:track:" + track["id"], 
            headers={
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            })

        if response_add.status_code != 201:
            print(f"ERROR: {response_add.status_code} - {response_add.reason}")
            return

        count += 1
        print(f"[" + track["id"] + "]" + track["name"] + " - " + track["artist"])

    print(f"{count} sons ajoutés")

############################
#   PROGRAMME PRINCIPALE   #
############################
if __name__ == '__main__':
    ACCESS_TOKEN = get_access_token()

    mix_detente_items = get_playlist_items('37i9dQZF1EVHGWrwldPRtj')
    bing_chilling_items = get_playlist_items('6baTLBdDiym4LEiLr7a6Ij')

    new_tracks = check_items()
    
    if len(new_tracks) > 0:
        add_tracks('6baTLBdDiym4LEiLr7a6Ij')
    else:
        print('0 sons à ajouter')