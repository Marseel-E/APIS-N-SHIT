from default import *
import requests, json
from dotenv import load_dotenv

load_dotenv('.env')

headers = {
    'content-type': "application/x-www-form-urlencoded",
    'accept-encoding': "application/gzip",
    'x-rapidapi-host': "google-translate1.p.rapidapi.com",
    'x-rapidapi-key': os.environ.get("KEY")
}
url = "https://google-translate1.p.rapidapi.com/language/translate/v2"


def choose(text : str, language : str):
    text = text.replace(' ', '%20')
    
    payload = f"q={text}&format=text&target={language}"
    response = requests.request("POST", url, data=payload, headers=headers)
    res = json.loads(response.text)

    text = text.replace('%20', ' ')
    Magic.print(f"{res['data']['translations'][0]['detectedSourceLanguage']}: {text}", Magic.color_green, True)
    Magic.print(f"{language}: {', '.join([res['data']['translations'][i]['translatedText'] for i in range(len(res['data']['translations']))])}", Magic.color_green)

if __name__ == ('__main__'):
    while True:
        Magic.print("#exit - To end/stop the program.", Magic.color_cyan, True)
        
        text = input(f"{Magic.color_cyan}Text: {Magic.color_reset}")
        if text.lower() == "#exit": break
        lang = input(f"{Magic.color_cyan}Language: {Magic.color_reset}")
        
        choose(text, lang)
