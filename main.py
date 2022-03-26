import os
import configparser

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


_config_file_name = "config.ini"
_bot_token = ""


class TelgramCommandHandler:
    '''
    All telegram command handlers
    '''

    @classmethod
    def hello(cls, update: Update, context: CallbackContext):
        '''
        Hello message
        '''
        update.message.reply_text(f"Hello, my name is Printi ;)\nSend me any file and i try to print it.")

    @classmethod
    def document(cls, update: Update, context: CallbackContext): #TODO test send print request method
        '''
        message with document
        '''
        message = update.message
        file_name = message.document.file_name
        message.document.get_file().download(file_name)
        send_print_request(file_name)


def parse_config():
    '''
    Parse config file.
    '''
    global _bot_token

    parser = configparser.ConfigParser()
    parser.read(_config_file_name)

    _bot_token = parser.get("DEFAULT", "bot-token")


def send_print_request(file):
    '''
    Send a request to the printer to start the print.
    '''
    os.startfile(file, "print")


def main():
    '''
    Main.
    '''
    parse_config()

    updater = Updater(_bot_token)

    updater.dispatcher.add_handler(CommandHandler('start', TelgramCommandHandler.hello, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('hello', TelgramCommandHandler.hello, run_async=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, TelgramCommandHandler.document, run_async=True))

    updater.start_polling()
    print(f"Start polling...")

    updater.idle()


if __name__ == "__main__":
    main()