import json
import logging

import requests
from bs4 import BeautifulSoup

from LinkedinBot.errors import PageNotFound, PostNotFound
from LinkedinBot.linkedin.schemas import Document, Post, Video

logger = logging.getLogger("crawler")


# functions
def get_post_data(url: str):
    # send request
    logger.debug(f"send request to url {url}")
    response = requests.get(url)
    # check status
    if response.status_code in range(400, 500):
        logger.info("response is not valid, status code is between 400 and 500")
        raise PageNotFound("Page not found error !")
    # parse the response
    logger.debug("parsing page content")
    soup = BeautifulSoup(response.content, "html.parser")

    # check the post section is exists
    post_section = soup.find("article")
    if not post_section:
        logger.info('"article" tag not found!')
        raise PostNotFound("post not exists !")

    # post text
    post = Post(url=url)
    post_text = post_section.find("p", class_="attributed-text-segment-list__content")
    post.text = post_text.text if post_text else ""

    # get post details
    logger.debug("get post details, reactions and comments count")
    post_detail = post_section.find(
        "div", class_="main-feed-activity-card__social-actions"
    )
    if post_detail:
        # get count of reactions and comments
        _reactions = post_detail.find(attrs={"data-id": "social-actions__reactions"})
        post.reactions = int(_reactions["data-num-reactions"]) if _reactions else 0
        _reactions = post_detail.find(attrs={"data-id": "social-actions__comments"})
        post.comments = int(_reactions["data-num-comments"]) if _reactions else 0

    # extract the post images
    logger.debug("get post images")
    _image_list = post_section.find("ul", attrs={"class": "feed-images-content"})
    if _image_list:
        post.images = [item["data-delayed-url"] for item in _image_list.find_all("img")]

    # extract the document
    logger.debug("get post document")
    _document = post_section.find(
        "iframe", attrs={"data-id": "feed-paginated-document-content"}
    )
    # extarct the images from document
    if _document:
        _document = json.loads(_document["data-native-document-config"])
        # extract
        _doc_url = requests.get(_document["doc"]["url"]).json()[
            "transcribedDocumentUrl"
        ]
        _doc_title = _document["doc"]["title"]
        post.document = Document(url=_doc_url, title=_doc_title)

    # get the video links
    logger.debug("get post videos")
    _json_data = post_section.find("video")
    if _json_data:
        _json_data = json.loads(_json_data["data-sources"])
        post.videos = [
            Video(url=item["src"], bitrate=item["data-bitrate"]) for item in _json_data
        ]
        post.videos.sort(key=lambda x: x.bitrate, reverse=True)

    return post
