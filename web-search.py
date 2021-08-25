from default import *
import requests, json, rich
from dotenv import load_dotenv

load_dotenv('.env')

headers = {
    'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
    'x-rapidapi-key': os.environ.get("KEY")
}

def news(page_number : int = 1, results : int = 5, images : bool = False, location : str = None):
    querystring = {
        "pageNumber": page_number,
        "pageSize": results,
        "withThumbnails": images
    }
    if location != None: querystring.update({'location': location})
    
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/TrendingNewsAPI"
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)
    
    # rich.print(res)

    for i in range(len(res['value'])):
        Magic.print(res['value'][i]['url'], Magic.color_highlight_yellow, True)
        Magic.print(res['value'][i]['image']['url'], Magic.color_highlight_yellow)
        Magic.print(f"[Title] [Language: {res['value'][i]['language']}]:\n{res['value'][i]['title']}", Magic.color_yellow, True)
        Magic.print(f"[Description]:\n{res['value'][i]['description']}", Magic.color_yellow, True)
        Magic.print(f"[Release date]: {res['value'][i]['datePublished']}", Magic.color_yellow, True)
        Magic.print(f"[Provider]: {res['value'][i]['provider']['name']}", Magic.color_yellow)

    Web.open('url', Magic.color_blue, res['value'])

def search(text : str, page_number : int, results : int, auto_correct : bool = False, safe_search : bool = False):  
    querystring = {
        "q": text,
        "pageNumber": page_number,
        "pageSize": results,
        "autoCorrect": auto_correct,
        "safeSearch": safe_search
    }
    
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)

    # rich.print(res)

    if res['didUMean']:
        Magic.print(f"Did u mean '{res['didUMean']}' ?", Magic.color_blue, True)
        answer = input("\n")
        if answer.lower() == "yes":
            search(res['didUMean'], page_number, results, auto_correct, safe_search)
            return

    for i in range(len(res['value'])):
        Magic.print(res['value'][i]['url'], Magic.color_highlight_yellow, True)
        
        safe = f"{Magic.color_green}(Secure){Magic.color_reset}" if res['value'][i]['isSafe'] else f"{Magic.color_red}(Not secure){Magic.color_reset}"
        Magic.print(f"[{res['value'][i]['provider']['name']}] {safe}: {res['value'][i]['title']}", Magic.color_yellow, True)

    if res['relatedSearch']:
        related_searches = '\n> '.join(res['relatedSearch'])

        related_searches = related_searches.replace('<b>', ' ')
        related_searches = related_searches.replace('</b>', ' ')

        Magic.print(f"Related searches:\n> {related_searches}", Magic.color_yellow, True)

    Web.open('url', Magic.color_blue, res['value'])

def news_search(text : str, page_number : int = 1, results : int = 50, auto_correct : bool = False, safe_search : bool = False, images : bool = False, start : str = "null", end : str = "null"):
    querystring = {
        "q": text,
        "pageNumber": page_number,
        "pageSize": results,
        "autoCorrect": auto_correct,
        "safeSearch": safe_search,
        "withThumbnails": images,
        "fromPublishedDate": start,
        "toPublishedDate": end
    }

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)

    # rich.print(res)

    if res['didUMean']:
        Magic.print(f"Did u mean '{res['didUMean']}' ?", Magic.color_blue, True)
        answer = input("\n")
        if answer.lower() == "yes":
            search(res['didUMean'], page_number, results, auto_correct, safe_search)
            return

    for i in range(len(res['value'])):
        Magic.print(res['value'][i]['url'], Magic.color_highlight_yellow, True)
        
        safe = f"{Magic.color_green}(Secure){Magic.color_reset}" if res['value'][i]['isSafe'] else f"{Magic.color_red}(Not secure){Magic.color_reset}"
        Magic.print(f"[{res['value'][i]['provider']['name']}] {safe}: {res['value'][i]['title']}", Magic.color_yellow, True)
        Magic.print(f"[Date published]: {res['value'][i]['datePublished']}", Magic.color_yellow)

    if res['relatedSearch']:
        related_searches = '\n> '.join(res['relatedSearch'])

        related_searches = related_searches.replace('<b>', ' ')
        related_searches = related_searches.replace('</b>', ' ')

        Magic.print(f"Related searches:\n> {related_searches}", Magic.color_yellow, True)

    Web.open('url', Magic.color_blue, res['value'])

def image_search(text : str, page_number : int = 1, results : int = 50, auto_correct : bool = False, safe_search : bool = False):
    querystring = {
        "q": text,
        "pageNumber": page_number,
        "pageSize": results,
        "autoCorrect": auto_correct,
        "safeSearch": safe_search
    }

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)

    Web.open('url', Magic.color_blue, res['value'])

def auto_complete(text : str):
    querystring = {
        "text": text
    }

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/spelling/AutoComplete"
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)

    Magic.print('\n'.join(res), Magic.color_yellow, True)

if __name__ == ('__main__'):
    while True:
        Magic.print("#exit - To stop/end program.", Magic.color_blue, True)
        
        what = input(f"{Magic.color_blue}How can I help you? (search, news, news search, image search, auto complete): {Magic.color_reset}")
        if what.lower() == "#exit": break
        
        if what.lower() == "news":
            location = input(f"{Magic.color_blue}Location (Global, us, es, fr, etc...): {Magic.color_reset}")
            location = None if location.lower() == "global" else location

            results = input(f"{Magic.color_blue}Results (Recommended <= 100): {Magic.color_reset}")
            if not results.isnumeric(): continue

            images = input(f"{Magic.color_blue}Images?\n{Magic.color_reset}")
            images = True if images.lower() == "yes" else False
            
            page = input(f"{Magic.color_blue}Page number: {Magic.color_reset}")
            if not page.isnumeric(): continue
            
            news(int(page), int(results), bool(images), location)

        if what.lower() == "search":
            text = input(f"{Magic.color_blue}Text: {Magic.color_reset}")

            page_number = input(f"{Magic.color_blue}Page: {Magic.color_reset}")
            if not page_number.isnumeric(): continue
            
            results = input(f"{Magic.color_blue}Results: {Magic.color_reset}")
            if not results.isnumeric(): continue
            
            auto_correct = input(f"{Magic.color_blue}Auto correct?\n{Magic.color_reset}")
            auto_correct = True if auto_correct.lower() == "yes" else False
            
            safe_search = input(f"{Magic.color_blue}Safe search?\n{Magic.color_reset}")
            safe_search = True if safe_search.lower() == "yes" else False

            search(text, page_number, results, auto_correct, safe_search)

        if what.lower() == "news search":
            text = input(f"{Magic.color_blue}Text: {Magic.color_reset}")

            page_number = input(f"{Magic.color_blue}Page: {Magic.color_reset}")
            if not page_number.isnumeric(): continue
            
            results = input(f"{Magic.color_blue}Results: {Magic.color_reset}")
            if not results.isnumeric(): continue
            
            auto_correct = input(f"{Magic.color_blue}Auto correct?\n{Magic.color_reset}")
            auto_correct = True if auto_correct.lower() == "yes" else False
            
            safe_search = input(f"{Magic.color_blue}Safe search?\n{Magic.color_reset}")
            safe_search = True if safe_search.lower() == "yes" else False

            images = input(f"{Magic.color_blue}Images?\n{Magic.color_reset}")
            images = True if images.lower() == "yes" else False

            start = input(f"{Magic.color_blue}From: {Magic.color_reset}")
            end = input(f"{Magic.color_blue}To: {Magic.color_reset}")

            news_search(text, page_number, results, auto_correct, safe_search, images, start, end)
        
        if what.lower() == "image search":
            text = input(f"{Magic.color_blue}Text: {Magic.color_reset}")

            page_number = input(f"{Magic.color_blue}Page: {Magic.color_reset}")
            if not page_number.isnumeric(): continue
            
            results = input(f"{Magic.color_blue}Results: {Magic.color_reset}")
            if not results.isnumeric(): continue
            
            auto_correct = input(f"{Magic.color_blue}Auto correct?\n{Magic.color_reset}")
            auto_correct = True if auto_correct.lower() == "yes" else False
            
            safe_search = input(f"{Magic.color_blue}Safe search?\n{Magic.color_reset}")
            safe_search = True if safe_search.lower() == "yes" else False

            image_search(text, page_number, results, auto_correct, safe_search)

        if what.lower() == "auto complete":
            text = input(f"{Magic.color_blue}Text: {Magic.color_reset}")
            auto_complete(text)