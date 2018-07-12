#!/usr/bin/env python3

import logging
import os

from telegram.ext import Updater, CommandHandler

from diana_conversation_handler import DianaConversationHandler
from diana_exceptions import BotTokenNotSetException
from diana_user_commands import DianaUserCommands


class Alfred:
    def __init__(self):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        token = os.getenv("DIANA_BOT_TOKEN")
        if token is None:
            raise BotTokenNotSetException("Set the bot token.")

        self.updater = Updater(token)

        dp = self.updater.dispatcher

        # User Commands
        dp.add_handler(CommandHandler("help", DianaUserCommands.help))

        # User Commands - Filter
        dp.add_handler(DianaConversationHandler.get_conversation_hander())

        # Log errors.
        dp.add_error_handler(self.error)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def launch(self):
        # Start the Bot.
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C.
        self.updater.idle()
