from default import *
import requests, rich, json
from dotenv import load_dotenv

load_dotenv('.env')

headers = {
    'x-rapidapi-host': "instagram47.p.rapidapi.com",
    'x-rapidapi-key': os.environ.get("KEY")
}


class Get:
    def user_id(username : str):
        querystring = {"username": username}

        url = "https://instagram47.p.rapidapi.com/get_user_id"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['user_id']
        except: rich.print(res); Error.not_found()

    def user_following(user_id : int):
        querystring = {"userid": user_id}

        url = "https://instagram47.p.rapidapi.com/user_following"

        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['body']['users']
        except: rich.print(res); Error.not_found()

        #- is private ['is_private']
        #- full name ['full_name']
        #- user id ['pk']
        #- username ['username']
        #- has anonymous profile picture ['has_anonymous_profile_picture']
        #- is favourite ['is_favorite']
        #- profile picture url ['profile_pic_url']
        #- is verified ['is_verified']

    def user_followers(user_id : int):
        querystring = {"userid": user_id}

        url = "https://instagram47.p.rapidapi.com/user_followers"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['body']['count']
        except: rich.print(res); Error.not_found()

    def user_posts(user_id : int):
        querystring = {"userid": user_id}

        url = "https://instagram47.p.rapidapi.com/public_user_posts"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['body']['edges']
        except: rich.print(res); Error.not_found()

        #- can be shared? [0]['viewer_can_reshare']
        #- tagged users [0]['edge_media_to_tagged_user']['edges'][0]['node']['user']
        #- likes [0]['edge_media_preview_like']['count']
        #- video url [0]['video_url']
        #- are comments disabled? [0]['comments_disabled']
        #- short code [0]['shortcode']
        #- comments count [0]['edge_media_to_comment']['count']
        #- comment text [0]['edge_media_to_comment']['edges'][0]['node']['text']
        #- comment user [0]['edge_media_to_comment']['edges'][0]['node']['owner']
        #- video views [0]['video_view_count']
        #- video caption [0]['edge_media_to_caption']['edges'][0]['node']['text']
        #- is video [0]['is_video']
        #- id [0]['id']

    def get_comments(short_code : str):
        querystring = {"shortcode": short_code}

        url = "https://instagram47.p.rapidapi.com/public_post_comments"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['body']
        except: rich.print(res); Error.not_found()

        #- Comments ['count']
        #- Comment text ['edges'][0]['node']['text']
        #- Comment owner (user) ['edges'][0]['node']['owner']
        #- Comment likes (user) ['edges'][0]['node']['edge_liked_by']['count']

    def post(short_code : str):
        querystring = {"shortcode": short_code}

        url = "https://instagram47.p.rapidapi.com/post_details"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['body']
        except: rich.print(res); Error.not_found()

        #- is ad ['is_ad']
        #- owner ['owner']
        #- is edited ['caption_is_edited']
        #- are comments disabled? ['comments_disabled']
        #- id ['id']
        #- comments ['edge_media_preview_comment']['count']
        #- accessibility caption ['accessibility_caption']
        #- can be shared? ['viewer_can_reshare']
        #- tagged users ['edge_media_to_tagged_user']['edges'][0]['node']['user']
        #- likes ['edge_media_preview_like']['count']
        #- Caption ['edge_media_to_caption']['edges'][0]['node']['text']


class Search:
    def search(text : str):
        querystring = {"search": text}

        url = "https://instagram47.p.rapidapi.com/search"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['body']
        except: rich.print(res); Error.not_found()

        #- user ['users'][0]['user']
        #- hashtag name ['hashtags'][0]['name']
        #- hashtag useage ['hashtags'][0]['search_result_subtitle']


class Location:
    def search(location : str):
        querystring = {"search": location}

        url = "https://instagram47.p.rapidapi.com/location_search"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['body']
        except: rich.print(res); Error.not_found()

        #- title [0]['title']
        #- longitude [0]['location']['lng']
        #- latitude [0]['location']['lat']
        #- id [0]['location']['pk']

    def post(location_id : int):
        querystring = {"locationid": location_id}

        url = "https://instagram47.p.rapidapi.com/location_posts"
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        try: return res['body']
        except: rich.print(res); Error.not_found()

        #- name ['name']
        #- posts ['edge_location_to_top_posts']['count']
        #- post likes ['edge_location_to_top_posts']['edges'][0]['node']['edge_liked_by']['count']
        #- post short code ['edge_location_to_top_posts']['edges'][0]['node']['shortcode']
        #- post owner ['edge_location_to_top_posts']['edges'][0]['node']['owner']
        #- post comments ['edge_location_to_top_posts']['edges'][0]['node']['edge_media_to_comment']['count']
        #- post caption ['edge_location_to_top_posts']['edges'][0]['node']['edge_media_to_caption']['edges'][0]['node']['text']
        #- post id ['edge_location_to_top_posts']['edges'][0]['node']['edge_media_to_caption']['edges'][0]['node']['id']


if __name__ == ('__main__'):
    while True:
        Magic.print("#exit - To stop/end program.", Magic.color_magenta, True)

        what = input(Magic.colored("user, search, location, post: ", Magic.color_magenta))
        if what.lower() == "#exit": break

        if what.lower() == "user":
            username = input(Magic.colored("Username: ", Magic.color_magenta))
            user_id = Get.user_id(username)

            what = input(Magic.colored("posts, followers, following: ", Magic.color_magenta))
            if what.lower() == "posts":
                data = Get.user_posts(user_id)

                # rich.print(data)

                for i in range(len(data)):
                    post = Get.post(data[i]['node']['shortcode'])

                    # rich.print(post)

                    Magic.print(post['edge_media_to_caption']['edges'][i]['node']['text'], Magic.color_cyan, True)

                    is_ad = Magic.colored(" (AD)", Magic.color_yellow) if post['is_ad'] else ""
                    is_edited = Magic.colored(" (Edited)", Magic.color_magenta) if post['caption_is_edited'] else ""
                    if is_ad or is_edited != "":
                        Magic.print(f"[Tags]: " + is_ad + is_edited, Magic.color_cyan)

                    if data[i]['node']['is_video']:
                        Magic.print(f"[Video]: {data[i]['edge_media_to_caption']['edges'][0]['node']['text']}", Magic.color_cyan, True)
                        Magic.print(data[i]['video_url'], Magic.color_highlight_cyan)
                        Magic.print(f"[Views]: {data[i]['video_view_count']}", Magic.color_cyan)
                    
                    if post['edge_media_to_tagged_user']['edges']:
                        tagged_users = [Magic.colored(f"@{user['node']['user']['username']}", Magic.color_blue) for user in post['edge_media_to_tagged_user']['edges']]
                        Magic.print(f"[Tagged users]: {', '.join(tagged_users)}", Magic.color_cyan)

                    Magic.print(f"[Likes]: {post['edge_media_preview_like']['count']}", Magic.color_cyan)

                    if not post['comments_disabled']:
                        Magic.print(f"[Comments] ({data[i]['edge_media_to_comment']['count']}):\n", Magic.color_cyan, True)

                        for comment in data[i]['edge_media_to_comment']['edges']:
                            Magic.print(f"@{comment['node']['owner']['username']}", Magic.color_blue, True)
                            Magic.print({comment['node']['text']}, Magic.color_blue)
            
            if what.lower() == "followers": #- Done
                data = Get.user_followers(user_id)
                Magic.print(f"[Followers]: {data}", Magic.color_cyan, True)
            
            if what.lower() == "following": #- Done
                data = Get.user_following(user_id)
                for i in range(len(data)):
                    is_verified = Magic.colored(" (Verified)", Magic.color_blue) if data[i]['is_verified'] else ""
                    is_private = Magic.colored(" (Private)", Magic.color_red) if data[i]['is_private'] else ""
                    is_favourite = Magic.colored(" (Favourite)", Magic.color_yellow) if data[i]['is_favorite'] else ""

                    Magic.print(data[i]['profile_pic_url'], Magic.color_highlight_cyan, True)
                    Magic.print(data[i]['full_name'], Magic.color_cyan)
                    if is_verified or is_favourite or is_private != "": Magic.print("[Tags]: " + is_verified + is_favourite + is_private, Magic.color_cyan)
                    Magic.print("[Username]: " + data[i]['username'], Magic.color_cyan)

        if what.lower() == "search": pass
        if what.lower() == "location": pass
        if what.lower() == "post": pass