from bs4 import BeautifulSoup
from pyrogram import Client, filters, types
import requests
import json
import re

# configuration

# get api id and api hash from https://my.telegram.org/auth
api_id = 12345
api_hash = "0123456789"
bot_token = "123456:ABC" # bot token from @BotFather
app = Client("linkedbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# functions
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
    json_data = json.loads(json_data)[1:]
    links = [item['src'] for item in json_data]
    # out
    return links

# check validition url
def validition_url(url):
    check = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    #out
    if check.match(url):
        return True
    else:
        return False


# message handler
# get only text messages from private chats
@app.on_message(filters.text & filters.private)
async def message_handler(client : Client, message : types.Message):
    # check the url pattern
    text = message.text
    if not validition_url(text):
        return await message.reply("Invalid Url !")
    
    # get the video links of video
    try:
        links = get_video_links(text)
    except Exception as e:
        print(e)
        return message.reply("an error occurred !")
    # output
    await message.reply("\n".join(links))


if __name__ == "__main__":
    # setup the bot
    app.run()