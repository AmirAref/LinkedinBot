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
        # get the video links
        json_data = soup.find('video')['data-sources']
        json_data = json.loads(json_data)[1:]
        links = [item['src'] for item in json_data]
        # out
        return links