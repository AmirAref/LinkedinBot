from bs4 import BeautifulSoup
import requests
import json

def get_video_links(url : str):
    #send request
    response = requests.get(url)
    # check status
    if response.status_code in range(400, 500):
        raise ValueError("Page not found error !")
    # parse the response
    soup = BeautifulSoup(response.content, "html.parser")
    # get the video links
    json_data = soup.find('video')['data-sources']
    json_data = json.loads(json_data)
    links = [item['src'] for item in json_data]
    # out
    return links
