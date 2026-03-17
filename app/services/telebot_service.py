from telebot import TeleBot
from telebot.types import Message


class TelebotService:
    def __init__(self, api_key):
        self.bot = TeleBot(api_key, threaded=False)

    def register(self, callback, commands):
        self.bot.register_message_handler(callback=callback, commands=commands)

    def start(self):
        self.bot.polling()

    def stop(self):
        self.bot.stop_bot()

    def send_message(self, message: Message, text: str):
        return self.bot.send_message(chat_id=message.chat.id, text=text)

    def delete_message(self, message: Message):
        return self.bot.delete_message(chat_id=message.chat.id, message_id=message.id)

    def reply_to(self, message: Message, reply: str):
        return self.bot.reply_to(message=message, text=reply)
    
    def edit_message(self, message: Message, edit_text: str):
        return self.bot.edit_message_text(text=edit_text, chat_id=message.chat.id, message_id=message.message_id)