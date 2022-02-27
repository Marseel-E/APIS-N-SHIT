from default import *
import requests, rich, json, webbrowser
from dotenv import load_dotenv

load_dotenv('.env')

headers = {
    'x-rapidapi-host': "google-search3.p.rapidapi.com",
    'x-rapidapi-key': os.environ.get("KEY")
}

def search(text : str, results : int):
    text = text.replace(' ', '+')
    
    url = f"https://google-search3.p.rapidapi.com/api/v1/search/q={text}&num={results}"
    response = requests.request("GET", url, headers=headers)
    res = json.loads(response.text)
    # rich.print(res)

    Magic.print(f"Found {res['total']} matches\n", Magic.color_green, True)
    [Magic.print(res['results'][i]['title'], Magic.color_green) for i in range(len(res['results']))]

    open = input("Open?\n")
    if open.lower() == "yes": [webbrowser.open(res['results'][i]['link']) for i in range(len(res['results']))]

def images(text : str, results : int):
    text = text.replace(' ', '+')

    url = f"https://google-search3.p.rapidapi.com/api/v1/images/q={text}&num={results}"
    response = requests.request("GET", url, headers=headers)
    res = json.loads(response.text)
    # rich.print(res)

    Magic.print(f"Found {res['total']} matches\n", Magic.color_green, True)
    [Magic.print(res['image_results'][i]['image'], Magic.color_green) for i in range(len(res['image_results']))]

    open = input("Open?\n")
    if open.lower() == "yes": [webbrowser.open(res['image_results'][i]['link']) for i in range(len(res['image_results']))]

def news(text : str, results : int):
    text = text.replace(' ', '+')

    url = f"https://google-search3.p.rapidapi.com/api/v1/news/q={text}&num={results}"
    response = requests.request("GET", url, headers=headers)
    res = json.loads(response.text)
    # rich.print(res)

    [Magic.print(res['entries'][i]['title'], Magic.color_green) for i in range(len(res['entries']))]

    Web.open('link', Magic.color_magenta, res['entries'])

    open = input("Open?\n")

if __name__ == ('__main__'):
    while True:
        Magic.print("#exit - To stop/end program.", Magic.color_magenta, True)
        
        text = input(f"{Magic.color_magenta}Search: {Magic.color_reset}")
        if text.lower() == "#exit": break
        
        s_images = input(f"{Magic.color_magenta}Images?\n{Magic.color_reset}")
        s_images = True if s_images.lower() == "yes" else False

        s_news = input(f"{Magic.color_magenta}News?\n{Magic.color_reset}")
        s_news = True if s_news.lower() == "yes" else False
        
        results = input(f"{Magic.color_magenta}Results (Recommended <= 100): {Magic.color_reset}")
        if not results.isnumeric(): continue
        
        if s_images: images(text, int(results))
        if s_news: news(text, int(results))
        else: search(text, int(results))