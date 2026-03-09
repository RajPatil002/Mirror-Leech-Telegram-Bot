
from app.services.torrent_service import TorrentService
from app.utils.telebot_util import TelebotUtil
from app.services.telebot_service import TelebotService
from telebot.types import Message
from app.settings.config import Config
from app.exceptions.torrent_exception import NoSourceFound, NoMetadataFound

class MessageListener:
    def __init__(self, config: Config):
        self.torrent_service = TorrentService(save_path=config.save_path)
        self.telebot_service = TelebotService(api_key=config.tele_api_key)
        self.path_link = config.saved_path_link

        # Register listeners
        self.telebot_service.register(callback= self._handle_start,commands=["hi","start"])
        self.telebot_service.register(callback= self._handle_stop,commands=["stop","exit"])
        self.telebot_service.register(callback= self._handle_torrent_download,commands=["tm","tormirror"])
        print("Registered listeners")

    def start_polling(self):
        print("Starting polling...")
        self.telebot_service.start()

    def _handle_start(self, message: Message):
        if message.reply_to_message:
            self.telebot_service.reply_to(message.reply_to_message,"This is telegram bot for torrent to gdrive")
        else:
            self.telebot_service.reply_to(message,"This is telegram bot for torrent to gdrive")

    def _handle_stop(self, message: Message):
        self.telebot_service.send_message(message,"Shutting Down")
        # self.bot.stop_polling()
        self.telebot_service.stop()

    def _handle_torrent_download(self, message: Message):
        reply = self.telebot_service.reply_to(message=message,reply="Starting")
        text = TelebotUtil.getMessageText(message=message)
        link = TelebotUtil.extractLink(text=text)
        if(link):
            self.telebot_service.edit_message(message=reply,edit_text="Downloading Metadata...")
            try:
                handle = self.torrent_service.download(link=link)
            except NoSourceFound as e:
                self.telebot_service.edit_message(message=reply,edit_text="No download source found")
            except NoMetadataFound as e:
                self.telebot_service.edit_message(message=reply,edit_text="Unable to fetch metadata")

            if(handle):
                name = handle.name()
                self.telebot_service.edit_message(message=reply,edit_text=f"Got Metadata, Starting Torrent Download...\n\nUploading: {name}")
                for status in self.torrent_service.status_handler(handle=handle):
                    msg = TelebotUtil.format_torrent_status(status=status,name=name)
                    self.telebot_service.edit_message(message=reply,edit_text=msg)
                else:
                    self.telebot_service.delete_message(reply)
                    msg = f"✅ Upload COMPLETED\n\n{name}{f"\nCheck Here :{self.path_link}" if(self.path_link) else ''}\n\nReady To Go Again"
                    self.telebot_service.send_message(message=message,text=msg)
        else:
            self.telebot_service.edit_message(message=reply,edit_text="No download link found")