from bs4 import BeautifulSoup
import requests
import json
import re

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
        post_section = soup.find('section', attrs={'class':'section'})
        # check the post section is exists
        if not post_section:
            raise KeyError('post not exists !')
        # create post object
        post = Post()
        # post text
        post.text = post_section.find('p', attrs={'class':'share-update-card__update-text'}).text
        
        # get post details
        post_detail = post_section.find('div', attrs={'class':'social-action-counts'})
        if post_detail:
            # get count of likes
            _likes = post_detail.find(attrs={'data-tracking-control-name':'public_post_share-update_social-details_social-action-counts_likes-text'})
            post.likes = _likes.text.strip() if _likes else 0
            # get count of comments
            _comments = post_detail.find(attrs={'data-tracking-control-name':'public_post_share-update_social-details_social-action-counts_comments-text'})
            post.comments = re.search('\d+', _comments.text.strip()).group() if _comments else 0 # extract the number
            # convert to integer
            post.likes, post.comments = int(post.likes), int(post.comments)
        
        # extract the post images
        _image_list = post_section.find('ul', attrs={'class':'share-images'})
        if _image_list:
            post.images = [item.find('img')['data-delayed-url'] for item in _image_list.find_all('li')]
        
        # get the video links
        _json_data = post_section.find('video', attrs={'class':'video-js'})
        if _json_data:
            _json_data = json.loads(_json_data['data-sources'])[1:]
            post.videos = [item['src'] for item in _json_data]
        # out
        return post

class Post:
    def __init__(self) -> None:
        self.url : str = None
        self.text : str = None
        self.likes : int = ''
        self.comments : int = ''
        self.images : list[str]= []
        self.videos : list[str]= []