from default import *
import requests, rich, json, os
from dotenv import load_dotenv

load_dotenv('.env')

headers = {
    'x-rapidapi-host': "shazam.p.rapidapi.com",
    'x-rapidapi-key': os.environ.get("KEY")
}


class Get:
    def search(text : str, results : int = 5):
        querystring = {
            "term": text,
            "offset":"0",
            "limit": results
        }
        
        url = "https://shazam.p.rapidapi.com/search"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: res['tracks'] and res['artists']
        except: rich.print(res); Error.not_found()

        return res

    def artist_top_songs(artist_id : int):
        url = "https://shazam.p.rapidapi.com/songs/list-artist-top-tracks"
        response = requests.request("GET", url, headers=headers, params={"id": artist_id})
        res = json.loads(response.text)

        try: return res['tracks']
        except: rich.print(res); Error.not_found()

    def recommendations(song_key : str):
        url = "https://shazam.p.rapidapi.com/songs/list-recommendations"
        response = requests.request("GET", url, headers=headers, params={"key": song_key})
        res = json.loads(response.text)

        try: return res['tracks']
        except: rich.print(res); Error.not_found()

    def top_x(results : int = 10, start_from : int = 0):
        querystring = {
            "pageSize": results,
            "startFrom": start_from
        }

        url = "https://shazam.p.rapidapi.com/charts/track"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['tracks']
        except: rich.print(res); Error.not_found()


if __name__ == ('__main__'):
    while True:
        Magic.print("#exit - To stop/end program.", Magic.color_blue, True)

        what = input(Magic.colored("Search (s), Artist top songs (a, ats), Recommendations (r), Top (t): ", Magic.color_blue))
        if what.lower() == "#exit": break

        if what.lower() in ['search', 's']: #- Done
            text = input(Magic.colored("Search: ", Magic.color_blue))

            results = input(Magic.colored("Results (min = 5): ", Magic.color_blue))
            if not results.isnumeric(): continue
            if int(results) < 5: continue

            data = Get.search(text, int(results))

            for song in data['tracks']['hits']:
                Magic.print(song['track']['url'], Magic.color_highlight_yellow, True)
                Magic.print(f"{song['track']['subtitle']} - {song['track']['title']}", Magic.color_yellow)

        if what.lower() in ['ats', 'artist top songs', 'a']: #- Done
            artist = input(Magic.colored("Artist name: ", Magic.color_blue))
            data = Get.search(artist, 5)
            artist_id = data['artists']['hits'][0]['artist']['id']

            data = Get.artist_top_songs(artist_id)
            for song in data:
                Magic.print(song['url'], Magic.color_highlight_yellow, True)
                Magic.print(f"{song['subtitle']} - {song['title']}", Magic.color_yellow)
        
        if what.lower() in ['r', 'recommendations']: #- Done
            track = input(Magic.colored("Track name: ", Magic.color_blue))
            data = Get.search(track, 5)
            track_key = data['tracks']['hits'][0]['track']['key']

            data = Get.recommendations(track_key)
            for song in data:
                Magic.print(song['url'], Magic.color_highlight_yellow, True)
                Magic.print(f"{song['subtitle']} - {song['title']}", Magic.color_yellow)
        
        if what.lower() in ['t', 'top']: #- Done
            results = input(Magic.colored("Results (Max 20): ", Magic.color_blue))
            if not results.isnumeric(): continue
            if int(results) > 20: continue

            start_from = input(Magic.colored("Start: ", Magic.color_blue))
            if not results.isnumeric(): continue

            start_from = int(start_from)

            data = Get.top_x(int(results), start_from)
            for song in data:
                Magic.print(song['url'], Magic.color_highlight_yellow, True)
                Magic.print(f"#{start_from} | {song['subtitle']} - {song['title']}", Magic.color_yellow)
                start_from += 1