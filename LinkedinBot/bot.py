from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from LinkedinBot.config import bot_token
from LinkedinBot.errors import PageNotFound, PostNotFound
from LinkedinBot.linkedin.crawler import get_post_data
from LinkedinBot.utils import validition_url

# command handlers


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # progrss message
    if update.message is None:
        return
    # welcome and help message
    await update.message.reply_text(
        text="Hello my friend, Welcome to the bot.\n\njust send me the post link from Linkedin.com ! "
    )


async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # progrss message
    if update.message is None or update.message.text is None:
        return

    msg = await update.message.reply_text(
        "Processing ...", reply_to_message_id=update.message.id
    )
    # check the url pattern
    url = update.message.text
    if not validition_url(url):
        return await msg.edit_text(text="Invalid Url !")

    # get the video links of video
    try:
        post = get_post_data(url=url)
    except PageNotFound:
        return await msg.edit_text(text="🌐 The Page not found !")
    except PostNotFound:
        return await msg.edit_text(
            text="❌ The Post not found !\n🛡 maybe The Post is private for a specific community ( for a group or the user's connections )",
        )
    except Exception as e:
        print(e)
        return await msg.edit_text(text="❗️ an error occurred !")
    # create inline keyboard
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=f"👍 {post.reactions:,}", callback_data="."),
                InlineKeyboardButton(text=f"💬 {post.comments:,}", callback_data="."),
            ],
            [InlineKeyboardButton(text="🌐 View on Linkedin", url=url)],
        ]
    )

    # output
    caption = post.text if post.text else ""
    # check limit charactersd
    if len(caption) > 1024:
        # send media and post text separately
        output = msg = await msg.edit_text(text=caption, reply_markup=keyboard)
        caption = ""
    else:
        # send the text as caption under the media
        output = update.message
        # delete process msg
        if post.images or post.videos or post.document:
            await msg.delete()
        else:
            # send only text
            await msg.edit_text(text=caption, reply_markup=keyboard)

    if not isinstance(output, Message):
        return

    # upload images
    if post.images:
        # first image with caption and keyboard
        if output is not msg:
            output = await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=post.images.pop(0),
                caption=caption,
                reply_markup=keyboard,
                reply_to_message_id=output.id,
            )
        # other images as a group
        try:
            images = [InputMediaPhoto(image) for image in post.images[:-1]] + [
                InputMediaPhoto(post.images[-1], caption=caption)
            ]
        except IndexError:
            # there is not any other image
            images = []
        await context.bot.send_media_group(
            chat_id=update.message.chat_id, media=images, reply_to_message_id=output.id
        )

    # upload videos
    elif post.videos:
        # send only first one (best quality)
        await context.bot.send_video(
            chat_id=update.message.chat_id,
            video=str(post.videos[0].url),
            caption=caption,
            reply_to_message_id=output.id,
            reply_markup=keyboard,
        )
    elif post.document:
        # send only last one
        await context.bot.send_document(
            chat_id=update.message.chat_id,
            document=str(post.document.url),
            caption=caption,
            reply_to_message_id=output.id,
            reply_markup=keyboard,
        )


if __name__ == "__main__":
    # setup the bot
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler(command="start", callback=start_handler))
    app.add_handler(
        MessageHandler(filters=filters.ChatType.PRIVATE, callback=download_handler)
    )
    app.run_polling()
