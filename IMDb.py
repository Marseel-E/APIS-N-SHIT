from default import *
import requests, os, json, webbrowser
from dotenv import load_dotenv

load_dotenv('.env')

headers = {
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': os.environ.get("KEY")
}
url = "https://imdb8.p.rapidapi.com/auto-complete"
default_types = [str, int, float, bool]


class Error:
    def not_found():
        return f"{Magic.color_red}404 | Title not found{Magic.color_reset}"


def check_and_print(text, color, new_line : bool = False):
    try: Magic.print(text, color, new_line)
    except: pass

def choose(title : str):
    try: response = requests.request("GET", url, headers=headers, params={"q": title})
    except: raise Error.not_found
    else:
        res = json.loads(response.text)

        # Image [d][0][i][imageUrl]
        try: webbrowser.open(res['d'][0]['i']['imageUrl'], new=1)
        except: pass
                
        # Name [d][0][l] & Type (movie, tv series, actor) [d][0][q]
        try: Magic.print(f"{res['d'][0]['l']} {({res['d'][0]['q']})}", Magic.color_white, True)
        except: Magic.print(res['d'][0]['l'], Magic.color_white, True)
        else:
            # Stars [d][0][s]
            Magic.print(f"Stars: {res['d'][0]['s']}", Magic.color_yellow)

        # Rank [d][0][rank]
        try: Magic.print(f"Rank: {res['d'][0]['rank']}", Magic.color_cyan)
        except: pass
                
        # life time (start year and end year) [d][0][yr]
        try: Magic.print(f"Life time: {res['d'][0]['yr']}", Magic.color_red)
        except:
            # First apperance [d][0][y]
            try: Magic.print(f"First apperance: {res['d'][0]['y']}", Magic.color_green)
            except: pass

if __name__ == ('__main__'):
    while True:
        os.system('')
        title = input(f"{Magic.color_green}\nAnything that you are familiar with, such as:\n> Name/title\m> Album\n> Song\n> etc…{Magic.color_reset}\n")
        if title.lower() in ['cancel', 'exit']: break
        choose(title)