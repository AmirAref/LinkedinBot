from bs4 import BeautifulSoup
import requests
import json

class Linkedin():
    def __init__(self, url : str) -> None:
        self.url = url
    
    # functions
    def get_post_data(self):
        #send request
        response = requests.get(self.url)
        # check status
        if response.status_code in range(400, 500):
            raise ValueError("Page not found error !")
        # parse the response
        soup = BeautifulSoup(response.content, "html.parser")
        # create post object
        post = Post()
        # post text
        post.text = soup.find('p', attrs={'class':'share-update-card__update-text'}).text
        # get the video links
        _json_data = soup.find('video', attrs={'class':'video-js'})
        _json_data = json.loads(_json_data['data-sources'])[1:]
        post.videos = [item['src'] for item in _json_data]
        # out
        return post

class Post:
    def __init__(self) -> None:
        self.url : str = None
        self.text : str = None
        self.videos : list[str]= None