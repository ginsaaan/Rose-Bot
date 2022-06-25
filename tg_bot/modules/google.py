from requests import post
import json

import logging

from telegram import Update, File
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Defaults

BOT_TOKEN = "TOKEN" # Replace TOKEN with your Telegram bot token

# Upload a photo on Telegraph, returns the URL
def telegraphUploadPhoto(byteArray):
    telegraphURL = 'https://telegra.ph/upload'
    result = post(telegraphURL, files={'file': byteArray}).content

    return 'https://telegra.ph' + json.loads(result)[0]['src']


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define handlers
def help(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        # If you manage to add a newline without of using a multiline string, please open a pull request
        fr"""Hi {user.mention_markdown_v2()}\!
By sending an image to this bot\, it\'ll give you a link to Google it\!
The bot was made by \@Knocks"""
    )


def photo_handler(update: Update, _: CallbackContext) -> None:
    # Get the image
    imageFile = update.message.photo[1].get_file()
    update.message.reply_text('Here\'s your link!\nhttps://www.google.com/searchbyimage?image_url=' +
                              telegraphUploadPhoto(imageFile.download_as_bytearray()))


def text_handler(update: Update, _: CallbackContext) -> None:
    # Text handler
    update.message.reply_text('You have to send an image!')


def main() -> None:
    # Set the default parameters for the bot
    defaults = Defaults(run_async=True, quote=True)

    # Create the Updater and pass it your bot's token.
    updater = Updater(
        token=BOT_TOKEN, defaults=defaults)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Set command handlers
    dispatcher.add_handler(CommandHandler("start", help))
    dispatcher.add_handler(CommandHandler("help", help))

    # Add handlers for non-commands
    dispatcher.add_handler(MessageHandler(
        Filters.photo & ~Filters.command, photo_handler))
    dispatcher.add_handler(MessageHandler(
        ~Filters.photo & ~Filters.command, text_handler))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
