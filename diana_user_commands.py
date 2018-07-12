#!/usr/bin/env python3
import json

from diana_exceptions import DianaFileWrongFormatException


class DianaUserCommands:

    @staticmethod
    def get_text(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            if "text" not in data:
                raise DianaFileWrongFormatException("File does not contain 'text' key.")
            return data["text"]

    @staticmethod
    def start(bot, update):
        datenschutz = DianaUserCommands.get_text("datenschutz.json")
        update.message.reply_text(datenschutz)

    @staticmethod
    def help(bot, update):
        help = DianaUserCommands.get_text("help.json")
        update.message.reply_text(help)


"""

whatsnew - Erhalte News auf Anfrage.
mute - Schalte Push Notifications aus.


"""
