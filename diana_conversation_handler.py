#!/usr/bin/env python3
import os
import re

import numpy as np
from telegram import ReplyKeyboardMarkup
from telegram.ext import (CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from nn import NN


class DianaConversationHandler:
    CHOOSING, TYPING_REPLY, TYPING_CHOICE, PHOTO_REPLY = range(4)
    photo_dir = "photos"
    if not os.path.exists(photo_dir):
        os.mkdir(photo_dir)

    option1 = 'Bildsuche'
    option2 = 'Option1'
    option3 = 'Option2'
    option4 = 'Beenden'

    nn = NN("xception")

    reply_keyboard = [[option1, option2], [option3, option4]]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    @staticmethod
    def get_conversation_hander():
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', DianaConversationHandler.start)],

            states={
                DianaConversationHandler.CHOOSING: [RegexHandler('^(' + DianaConversationHandler.option1 +
                                                                  '|' + DianaConversationHandler.option2 +
                                                                  '|' + DianaConversationHandler.option3 +
                                                                  ')$',
                                                                 DianaConversationHandler.regular_choice,
                                                                 pass_user_data=True),
                                                    RegexHandler('^Something else...$',
                                                                 DianaConversationHandler.custom_choice)],

                DianaConversationHandler.TYPING_CHOICE: [MessageHandler(Filters.text,
                                                                        DianaConversationHandler.regular_choice,
                                                                        pass_user_data=True)],

                DianaConversationHandler.TYPING_REPLY: [MessageHandler(Filters.text,
                                                                       DianaConversationHandler.received_text_information,
                                                                       pass_user_data=True)],
                DianaConversationHandler.PHOTO_REPLY: [MessageHandler(Filters.photo,
                                                                      DianaConversationHandler.received_photo_information,
                                                                      pass_user_data=True)],
            },

            fallbacks=[RegexHandler('^' + DianaConversationHandler.option4 + '$', DianaConversationHandler.done,
                                    pass_user_data=True)]
        )

        return conv_handler

    @staticmethod
    def start(bot, update):
        update.message.reply_text("Hallo, was moechten Sie tun? Bitte waehlen Sie eine Option aus.",
                                  reply_markup=DianaConversationHandler.markup)

        return DianaConversationHandler.CHOOSING

    @staticmethod
    def regular_choice(bot, update, user_data):
        text = update.message.text
        user_data['choice'] = text.lower()

        if text.lower() == DianaConversationHandler.option1.lower():
            answer = "Bitte senden Sie ein Bild von dem zu suchenden Produkt."
            update.message.reply_markdown(answer)
            return DianaConversationHandler.PHOTO_REPLY
        else:
            answer = "Diese Funktionalitaet steht noch nicht zur Verfuegung."
            update.message.reply_text(answer, reply_markup=DianaConversationHandler.markup)
            return DianaConversationHandler.CHOOSING

    @staticmethod
    def received_photo_information(bot, update, user_data):
        category = user_data['choice']
        user = update.message.from_user
        if category == DianaConversationHandler.option1.lower():
            update.message.reply_text("Bild wird verarbeitet ...")

            photo_file = bot.get_file(update.message.photo[-1].file_id)

            filename = os.path.join(DianaConversationHandler.photo_dir, str(user["id"])) + ".jpg"

            photo = photo_file.download(custom_path=filename)
            user_data[category] = photo

            prediction = DianaConversationHandler.nn.predict(img_path=photo)
            label = prediction["label"]
            prob = str(np.around(prediction["prob"] * 100, decimals=1))
            amazon = "\nhttps://www.amazon.com/s?url=search-alias&field-keywords={}"
            answer = "*Klasse* : {} \n*Wahrscheinlichkeit*: {}".format(re.sub("_", "\_", label),
                                                                       prob)
            update.message.reply_markdown(answer)
            update.message.reply_text(amazon.format(label), reply_markup=DianaConversationHandler.markup)

            del user_data['choice']

        else:
            update.message.reply_text("Ungueltige Eingabe.",
                                      reply_markup=DianaConversationHandler.markup)

        return DianaConversationHandler.CHOOSING

    @staticmethod
    def custom_choice(bot, update):
        update.message.reply_text('Not implemented.')

        return DianaConversationHandler.TYPING_CHOICE

    @staticmethod
    def received_text_information(bot, update, user_data):
        text = update.message.text
        category = user_data['choice']

        user_data[category] = text.lower()
        del user_data['choice']

        update.message.reply_text("{} gespeichert.".format(
            DianaConversationHandler.facts_to_str(user_data)), reply_markup=DianaConversationHandler.markup)

        return DianaConversationHandler.CHOOSING

    @staticmethod
    def done(bot, update, user_data):
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_text("Auf Wiedersehen!".format(DianaConversationHandler.facts_to_str(user_data)))

        return ConversationHandler.END

    @staticmethod
    def facts_to_str(user_data):
        facts = list()

        for key, value in user_data.items():
            facts.append('{} - {}'.format(key, value))

        return "\n".join(facts).join(['\n', '\n'])
