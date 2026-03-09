from telebot import TeleBot
from telebot.types import Message


class TelebotService:
    def __init__(self, api_key):
        self.bot = TeleBot(api_key, num_threads=10)
        self.start()

    def register(self, callback, commands):
        self.bot.register_message_handler(callback=callback, commands=commands)

    def start(self):
        self.bot.polling()

    def stop(self):
        self.bot.stop_bot()

    def send_message(self, message: Message, text: str):
        self.bot.send_message(chat_id=message.chat.id, text=text)

    def delete_message(self, message: Message, text: str):
        self.bot.delete_message(chat_id=message.chat.id, message_id=message.id)

    def reply_to(self, message: Message, reply: str):
        self.bot.reply_to(message=message, text=reply)