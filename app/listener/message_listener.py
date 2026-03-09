
from app.services.torrent_service import TorrentService
from app.utils.telebot_util import TelebotUtil
from app.services.telebot_service import TelebotService
from telebot.types import Message
from app.settings.config import Config
from libtorrent import torrent_handle
from app.models.torrent_status import TorrentStatus

class MessageListener:
    def __init__(self, config: Config):
        self.torrent_service = TorrentService()
        self.telebot_service = TelebotService(api_key=config.tele_api_key)
        self.telebot_service.register(callback= self._handle_start,commands=["hi","start"])
        self.telebot_service.register(callback= self._handle_stop,commands=["stop","exit"])
        self.telebot_service.register(callback= self._handle_torrent_download,commands=["tm","tormirror"])

    def start_polling(self):
        print("Starting polling")
        self.telebot_service.start()

    def _handle_start(self, message: Message):
        if message.reply_to_message:
            self.telebot_service.reply_to(message.reply_to_message,"This is telegram bot for torrent to gdrive")
        else:
            self.telebot_service.reply_to(message,"This is telegram bot for torrent to gdrive")

    def _handle_stop(self, message: Message):
        self.telebot_service.send_message(message.chat.id,"Shutting Down")
        # self.bot.stop_polling()
        self.telebot_service.stop_bot()

    def _handle_torrent_download(self, message: Message):
        text = TelebotUtil.getMessageText(message=message)
        link = TelebotUtil.extractLink(text=text)
        if(link):
            handle = self.torrent_service.download(link=link)
            if(handle):
                for status in self.torrent_service.status_handler(handle=handle):
                    status: TorrentStatus
                    self.telebot_service.reply_to(message=message,reply="Downloading %s}" % status.progress)
        pass
        # self.telebot_service.send_message(message.chat.id,"Shutting Down")