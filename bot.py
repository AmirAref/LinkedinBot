from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, Message
from config import *
from Linkedin import LinkedinPost
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
        post = LinkedinPost(text)
        post.get_post_data()
    except PageNotFound:
        return await msg.edit("🌐 The Page not found !")
    except PostNotFound:
        return await msg.edit("❌ The Post not found !\n🛡 maybe The Post is private for a specific community ( for a group or the user's connections )")
    except Exception as e:
        print(e)
        return await msg.edit("❗️ an error occurred !")
    # create inline keyboard
    _post_details = [
        [InlineKeyboardButton(text=f"👍 {post.likes:,}", callback_data='.'), InlineKeyboardButton(text=f"💬 {post.comments:,}", callback_data='.'), ],
        [InlineKeyboardButton(text='🌐 View on Linkedin', url=text)],
        ]
    keyboard = InlineKeyboardMarkup(_post_details)
    # output
    caption = post.text
    
    # check limit characters
    if len(caption) > 1024:
        # send media and post text separately
        output = await msg.edit(post.text, reply_markup=keyboard)
        caption = None
    else :
        # send the text as caption under the media
        output = message
        caption = post.text
        # delete process msg
        if (post.images or post.videos):
            await msg.delete()
        else:
            # send only text
            await msg.edit(post.text, reply_markup=keyboard)
    
    # upload images
    if post.images:
        # first image with caption and keyboard
        output = await client.send_photo(
            chat_id=message.chat.id,
            photo=post.images.pop(0),
            caption=caption,
            reply_markup=keyboard,
            reply_to_message_id=output.id,
        )
        # other images as a group
        try:
            images = [InputMediaPhoto(image) for image in post.images[:-1]] + [InputMediaPhoto(post.images[-1], caption=caption)]
        except IndexError:
            # there is not any other image
            images = []
        await client.send_media_group(message.chat.id, images, reply_to_message_id=output.id)

    # upload videos
    elif post.videos:
        # send only last one
        await client.send_video(
            chat_id=message.chat.id,
            video=post.videos[-1],
            caption=caption,
            reply_to_message_id=output.id,
            reply_markup=keyboard,
            )
        

if __name__ == "__main__":
    # setup the bot
    print("App Started !")
    app.run()