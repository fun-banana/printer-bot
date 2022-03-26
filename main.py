import os
import configparser

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


_supported_file_extensions = ['.pdf', '.txt']
_config_file_name = "config.ini"
_bot_token = ""
_admin_id = 0


class Log:
    '''
    Logs.
    '''

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    def __init__(self, data: str, level = DEBUG):
        '''
        Base log method.
        '''
        print(f"[{level}]: {data}\n")
        if (level in {self.ERROR, self.CRITICAL}):
            self.send_log_to_admin(data, level)

    def send_log_to_admin(self, data, level = INFO):
        '''
        Send log data to admin.
        '''
        bot = telegram.Bot(token=_bot_token)
        bot.send_message(_admin_id, f"LOG\n[{level}]: {data}")


class TelgramCommandHandler:
    '''
    All telegram command handlers.
    '''

    @classmethod
    def hello(cls, update: Update, context: CallbackContext):
        '''
        Hello message.
        '''
        print(f"{'='*80}")
        update.message.reply_text(f"Hello, my name is Printi ;)\nSend me any file and i try to print it.")
        Log(f"Hello message was sended to [{update.message.chat.full_name}]", level=Log.INFO)

    @classmethod
    def document(cls, update: Update, context: CallbackContext):
        '''
        Message with document.
        '''
        print(f"{'='*80}")
        message = update.message
        file_name = message.document.file_name

        if (not get_file_extension(file_name) in _supported_file_extensions):
            update.message.reply_text(f"Sorry, I don't know how to work with this file (\nBut you can send these extensions of files:\n{_supported_file_extensions}")
            Log("The file extension does not support it.", level=Log.WARNING)
            return

        message.document.get_file().download(file_name)
        if (not send_print_request(file_name)):
            update.message.reply_text(f"Something went wrong (((\nPlease cath admin or check the log information.")
            return
        update.message.reply_text(f"Printing was started successfully :)")
        
        Log("Printing was started successfully", level=Log.INFO)


def get_file_extension(file: str):
    '''
    Get file extension.
    '''
    return os.path.splitext(file)[1]


def parse_config():
    '''
    Parse config file.
    '''
    global _bot_token
    global _admin_id

    if (not os.path.isfile(_config_file_name)):
        Log(f"Config file was not found", level=Log.CRITICAL)
        raise FileNotFoundError

    parser = configparser.ConfigParser()
    parser.read(_config_file_name)

    _bot_token = parser.get("DEFAULT", "bot-token")
    _admin_id = parser.get("DEFAULT", "admin-id")

    Log("Config parsed successfully", level=Log.INFO)


def send_print_request(file: str):
    '''
    Send a request to the printer to start the print.
    '''
    if (not os.path.isfile(file)):
        Log(f"File not found [{file}]", level=Log.ERROR)
        return False
    try:
        os.startfile(file, "print")
        return True
    except:
        return False


def main():
    '''
    Main.
    '''
    print(f"{'='*80}")
    parse_config()

    updater = Updater(_bot_token)

    updater.dispatcher.add_handler(CommandHandler('start', TelgramCommandHandler.hello, run_async=True))
    updater.dispatcher.add_handler(CommandHandler('hello', TelgramCommandHandler.hello, run_async=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, TelgramCommandHandler.document, run_async=True))

    updater.start_polling()
    Log(f"Start polling...", level=Log.INFO)

    updater.idle()


if __name__ == "__main__":
    main()