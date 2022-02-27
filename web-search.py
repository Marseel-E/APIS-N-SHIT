from typing import Optional
from pprint import pprint
import requests, json

from utils import *


with open("./config.json", 'r') as f:
	SECRET_KEY = json.loads(f.read())['web-search']


class API:
	def __init__(self):
		self.headers = {
			'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
			'x-rapidapi-key': SECRET_KEY
		}
		self.url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/"
		self.query = {}


	def news(self, page_number: Optional[int] = 1, results: Optional[int] = 5, images: Optional[bool] = False, location: Optional[str] = None):
		"""
			Get the latest news.

			Takes:
				'page_number' (int) - The page to fetch results from.
				'results' (int) - The amount of results to fetch.
				'images' (bool) - Whether to include images in the results or not.
				'location' (str) - Search based on a specific location.

			Raises:
				NotFound - Didn't find any results.
		"""
		new_query = {
			"pageNumber": page_number,
			"pageSize": results,
			"withThumbnails": images
		}

		if (location): new_query['location'] = location
		
		self.query = new_query
		self.url += "TrendingNewsAPI"
		
		response = requests.request("GET", self.url, headers=self.headers, params=self.query)
		data = json.loads(response.text)

		for i in range(len(data['value'])):
			Magic.print(data['value'][i]['url'], Magic.color_highlight_yellow, True)
			Magic.print(data['value'][i]['image']['url'], Magic.color_highlight_yellow)
			Magic.print(f"[Title] [Language: {data['value'][i]['language']}]:\n{data['value'][i]['title']}", Magic.color_yellow, True)
			Magic.print(f"[Description]:\n{data['value'][i]['description']}", Magic.color_yellow, True)
			Magic.print(f"[Release date]: {data['value'][i]['datePublished']}", Magic.color_yellow, True)
			Magic.print(f"[Provider]: {data['value'][i]['provider']['name']}", Magic.color_yellow)

		Web.open('url', Magic.color_blue, data['value'])


	def search(self, text: str, page_number: int, results: int, auto_correct: Optional[bool] = False, safe_search: Optional[bool] = False):
		"""
			Searchs the internet for the specified query.

			Takes:
				'text' (str) - What to search for. (Required)

				'page_number' (int) - The page to fetch results from.
				'results' (int) - The amount of results to fetch.
				'auto_correct' (bool) - Whether to auto_correct the search text or not.
				'safe_search' (bool) - Include NSFW & other unsafe data in the results or not.

			Raises:
				NotFound - Didn't find any results
		"""
		self.query = {
			"q": text,
			"pageNumber": page_number,
			"pageSize": results,
			"autoCorrect": auto_correct,
			"safeSearch": safe_search
		}
		self.url += "WebSearchAPI"

		response = requests.request("GET", self.url, headers=self.headers, params=self.query)
		data = json.loads(response.text)

		if (data['didUMean']):
			if (input(Magic.colorize(f"Did u mean '{data['didUMean']}' ? [y/n]: ", Magic.color_blue)).lower() == "y"):
				self.search(data['didUMean'], page_number, results, auto_correct, safe_search)
				return

		for i in range(len(data['value'])):
			Magic.print(data['value'][i]['url'], Magic.color_highlight_yellow, True)

			safe = Magic.colorize("(secure)", Magic.color_green) if (data['value'][i]['isSafe']) else Magic.colorize("(not secure)", Magic.color_red)

			Magic.print(f"[{data['value'][i]['provider']['name']}] {safe}: {data['value'][i]['title']}", Magic.color_yellow, True)

		if (data['relatedSearch']):
			related_searches = '\n> '.join(data['relatedSearch'])

			related_searches = related_searches.replace('<b>', ' ')
			related_searches = related_searches.replace('</b>', ' ')

			Magic.print(f"Related searches:\n> {related_searches}", Magic.color_yellow, True)

		Web.open('url', Magic.color_blue, data['value'])


	def news_search(self, text: str, page_number: Optional[int] = 1, results: Optional[int] = 50, auto_correct: Optional[bool] = False, safe_search: Optional[bool] = False, images: Optional[bool] = False, start: Optional[str] = "null", end: Optional[str] = "null"):
		"""
			Searchs the internet for news.

			Takes:
				'text' (str) - What to search for. (Required)

				'page_number' (int) - The page to fetch results from.
				'results' (int) - The amount of results to fetch.
				'auto_correct' (bool) - Whether to auto_correct the search text or not.
				'safe_search' (bool) - Include NSFW & other unsafe data in the results or not.
				'images': (bool) - Whether to include images in the results or no.
				'start': (str) - The minimum date to fetch from.
				'end': (str) - The maximum date to fetch from.

			Raises:
				NotFound - Didn't find any results
		"""
		self.query = {
			"q": text,
			"pageNumber": page_number,
			"pageSize": results,
			"autoCorrect": auto_correct,
			"safeSearch": safe_search,
			"withThumbnails": images,
			"fromPublishedDate": start,
			"toPublishedDate": end
		}
		self.url += "NewsSearchAPI"

		response = requests.request("GET", self.url, headers=self.headers, params=self.query)
		data = json.loads(response.text)

		if (data['didUMean']):
			Magic.print(f"Did u mean '{data['didUMean']}' ? [y/n]", Magic.color_blue, True)
			
			if (input("\n").lower() == "y"):
				self.news_search(data['didUMean'], page_number, results, auto_correct, safe_search, images, start, end)
				return

		for i in range(len(data['value'])):
			Magic.print(data['value'][i]['url'], Magic.color_highlight_yellow, True)
			
			safe = Magic.colorize("(secure)", Magic.color_green) if (data['value'][i]['isSafe']) else Magic.colorize("(not secure)", Magic.color_red)
			
			Magic.print(f"[{data['value'][i]['provider']['name']}] {safe}: {data['value'][i]['title']}", Magic.color_yellow, True)
			Magic.print(f"[Date published]: {data['value'][i]['datePublished']}", Magic.color_yellow)

		if (data['relatedSearch']):
			related_searches = '\n> '.join(data['relatedSearch'])

			related_searches = related_searches.replace('<b>', ' ')
			related_searches = related_searches.replace('</b>', ' ')

			Magic.print(f"Related searches:\n> {related_searches}", Magic.color_yellow, True)

		Web.open('url', Magic.color_blue, data['value'])


	def image_search(self, text: str, page_number: Optional[int] = 1, results: Optional[int] = 50, auto_correct: Optional[bool] = False, safe_search: Optional[bool] = False):
		"""
			Searchs the internet for images.

			Takes:
				'text' (str) - What to search for. (Required)

				'page_number' (int) - The page to fetch results from.
				'results' (int) - The amount of results to fetch.
				'auto_correct' (bool) - Whether to auto_correct the search text or not.
				'safe_search' (bool) - Include NSFW & other unsafe data in the results or not.

			Raises:
				NotFound - Didn't find any results
		"""
		self.url += "ImageSearchAPI"
		self.query = {
			"q": text,
			"pageNumber": page_number,
			"pageSize": results,
			"autoCorrect": auto_correct,
			"safeSearch": safe_search
		}

		response = requests.request("GET", self.url, headers=self.headers, params=self.query)
		data = json.loads(response.text)

		Web.open('url', Magic.color_blue, data['value'])


	def auto_complete(self, text: str):
		"""
			Auto completes the query.

			Takes:
				'text' (str) - What to search for. (Required)

			Raises:
				NotFound - Didn't find any results
		"""
		self.url += "AutoComplete"

		response = requests.request("GET", self.url, headers=self.headers, params={"text": text})
		data = json.loads(response.text)

		Magic.print('\n'.join(data), Magic.color_yellow, True)


if __name__ == ('__main__'):
	while True:
		Magic.print("#exit - To stop/end program.", Magic.color_blue, True)
		
		query = input(Magic.colorize("How can I help you? (search, news, news search, image search, auto complete): ", Magic.color_blue)).lower()

		if (query == "#exit"): break
		

		if (query == "news"):
			location = input(Magic.colorize("Location (Global, us, es, fr, etc...): ", Magic.color_blue)).lower()
			if (location == "global"): location = None

			results = input(Magic.colorize("Results (Recommended <= 100): ", Magic.color_blue))
			if not (results.isnumeric()): continue

			images = True if (input(Magic.colorize("Images? [y/n]: ", Magic.color_blue)).lower() == "y") else False
			
			page = input(Magic.colorize("Page number: ", Magic.color_blue))
			if not (page.isnumeric()): continue
			
			API().news(int(page), int(results), bool(images), location)


		if (query == "search"):
			text = input(Magic.colorize("Text: ", Magic.color_blue))

			page_number = input(Magic.colorize("Page: ", Magic.color_blue))
			if not (page_number.isnumeric()): continue
			
			results = input(Magic.colorize("Results: ", Magic.color_blue))
			if not (results.isnumeric()): continue
			
			auto_correct = True if (input(Magic.colorize("Auto correct? [y/n]: ", Magic.color_blue)).lower() == "y") else False
			safe_search = True if (input(Magic.colorize("Safe search? [y/n]: ", Magic.color_blue)).lower() == "y") else False

			API().search(text, int(page_number), int(results), auto_correct, safe_search)


		if (query == "news search"):
			text = input(Magic.colorize("Text: ", Magic.color_blue))

			page_number = input(Magic.colorize("Page: ", Magic.color_blue))
			if not (page_number.isnumeric()): continue
			
			results = input(Magic.colorize("Results: ", Magic.color_blue))
			if not (results.isnumeric()): continue
			
			auto_correct = True if (input(Magic.colorize("Auto correct? [y/n]: ", Magic.color_blue)).lower() == "y") else False
			safe_search = True if (input(Magic.colorize("Safe search? [y/n]: ", Magic.color_blue)).lower() == "y") else False
			images = True if (input(Magic.colorize("Images? [y/n]: ", Magic.color_blue)).lower() == "y") else False

			API().news_search(text, int(page_number), int(results), auto_correct, safe_search, images, input(Magic.colorize("From: ", Magic.color_blue)), input(Magic.colorize("To: ", Magic.color_blue)))
		

		if (query == "image search"):
			text = input(Magic.colorize("Text: ", Magic.color_blue))

			page_number = input(Magic.colorize("Page: ", Magic.color_blue))
			if not (page_number.isnumeric()): continue
			
			results = input(Magic.colorize("Results: ", Magic.color_blue))
			if not (results.isnumeric()): continue
			
			auto_correct = True if (input(Magic.colorize("Auto correct? [y/n]: ", Magic.color_blue)).lower() == "y") else False
			safe_search = True if (input(Magic.colorize("Safe search? [y/n]: ", Magic.color_blue)).lower() == "y") else False

			API().image_search(text, int(page_number), int(results), auto_correct, safe_search)


		if (query == "auto complete"): API().auto_complete(input(Magic.colorize("Text: ", Magic.color_blue)))