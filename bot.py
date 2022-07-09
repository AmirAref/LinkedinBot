from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, Message
from config import *
from Linkedin import Linkedin
from Linkedin.errors import *
import re

# configuration
app = Client("linkedbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, proxy=proxy)


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


# command handler
@app.on_message(filters.text & filters.private & filters.command('start'))
async def command_handler(client : Client, message : Message):
    await message.reply('Hello my friend, Welcome to the bot.\n\njust send me the post link from Linkedin.com ! ')


# message handler
# get only text messages from private chats
@app.on_message(filters.text & filters.private)
async def message_handler(client : Client, message : Message):
    # progrss message
    msg = await message.reply("Processing ...", reply_to_message_id=message.id) 
    # check the url pattern
    text = message.text
    if not validition_url(text):
        return await msg.edit("Invalid Url !")
    
    # get the video links of video
    try:
        linkedin = Linkedin(text)
        post = linkedin.get_post_data()
    except PageNotFound:
        return await msg.edit("🌐 Page not found !")
    except PostNotFOund:
        return await msg.edit("❌ Post not found !")
    except Exception as e:
        print(e)
        return await msg.edit("❗️ an error occurred !")
    # create inline keyboard
    _post_details = [
        [InlineKeyboardButton(text=f"👍 {post.likes:,}", callback_data='.'), InlineKeyboardButton(text=f"💬 {post.comments:,}", callback_data='.'), ],
        ]
    keyboard = InlineKeyboardMarkup(_post_details)
    # output
    output = await msg.edit(post.text, reply_markup=keyboard)
    
    # upload images
    if post.images:
        await client.send_media_group(message.chat.id, [InputMediaPhoto(image) for image in post.images], reply_to_message_id=output.id)

    # upload videos
    if post.videos:
        # send only last one
        await client.send_video(message.chat.id, post.videos[-1], reply_to_message_id=output.id)


if __name__ == "__main__":
    # setup the bot
    print("App Started !")
    app.run()