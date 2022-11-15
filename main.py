##########
# IMPORT #
##########
import base64
import requests
import webbrowser

def get_access_token():
    client_id = "7efceb8a917642719a27f76a8a458978"
    client_secret = "ccda20d8959e46efb384184cabf3e260"

    # auth_url = "https://accounts.spotify.com/authorize"
    # auth_data = {
    #     "client_id": client_id,
    #     "response_type": "code",
    #     "redirect_uri": "https://github.com/WilliamDevv/playlist-sorter",
    #     "scope": "playlist-modify-public+playlist-modify-private"
    # }

    # auth_url_v2 = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2FWilliamDevv%2Fplaylist-sorter&scope=playlist-modify-public%20playlist-modify-private"
    # webbrowser.open(auth_url_v2)

    # code = requests.get(auth_url, auth_data)
    # print(code)

    client_creds_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode())

    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "client_credentials",
        "code": "AQDZ0zinIy3dgMWs7IZVwJSOIoR1GAUULkgz9Qtl6_9ajMHkhzOpA5RF9534HDr4dHVfsn675DmIM9V-PDlD5plMqQLsQhblBSYU4fFfeUg74Hc9NmJF0YpGGh9YjwrZ3n1NcNPCbGL4LrFcFoWVaweWyhYnFibrZVtwDjp5QTS3MT9geYx226S0blwaMK_xbArJV9GL1BMBYo9zJ8ZT_qfxuYpYfG9JKE6qXSZXrHwz3bAaStjSNVtnijQMiTCMox7X",
        #"code": f"{code}",
        "redirect_uri": "https://github.com/WilliamDevv/playlist-sorter"
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
    # ACCESS_TOKEN = get_access_token()
    ACCESS_TOKEN = "BQAEd-ztYs2Eljh1OYZWurjWc6KQ04VoCFNv3kP21ALWir8_7HQ57Bgo2D8w2qkgxUsDe7BW28iNaxJG3tzFmNOVRpX8bTWuKEHZc_EHOY-PjVx2Co8Ki-Qpu8G5GRzGO_8O1Rgg-4EOSEImcwbASNOnHSyFGzldyRBxWVwzHoiGaZqMJq1BOJ6EAiR2m8gV8fAVL4zNU8JJKMG4zsgUvgzK8iHfs2b3xXaAA_a2PBigmDIqYYf_fKv3CGlCbHU8"
    print(f"Access token : {ACCESS_TOKEN}")

    mix_detente_items = get_playlist_items('37i9dQZF1EVHGWrwldPRtj')
    bing_chilling_items = get_playlist_items('6baTLBdDiym4LEiLr7a6Ij')

    new_tracks = check_items()
    
    if len(new_tracks) > 0:
        add_tracks('6baTLBdDiym4LEiLr7a6Ij')
    else:
        print('\n0 sons à ajouter')