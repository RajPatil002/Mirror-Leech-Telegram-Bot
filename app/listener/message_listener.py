import time

from app.exceptions.thread_exception import DuplicateThread
from app.services.thread_service import ThreadService
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
        self.thread_service = ThreadService()
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
        # self.telebot_service.send_message(chat=message.chat, text="Shutting Down")
        
        parts = message.text.split()
        id = parts[1] if len(parts) > 1 else None
        tor_thread = self.thread_service.getTask(id=id) if id else None

        if not tor_thread:
            self.telebot_service.reply_to(message=message, reply=f"Download not found {id}")
            return
        

        print('Stopping ',tor_thread.name())
        self.telebot_service.reply_to(message=message, reply=f"Download stopped {id}")
        self.torrent_service.stop_download(handle=tor_thread.handle)
        # self.bot.stop_polling()
        # self.telebot_service.stop()
        # exit(0)

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

            self.telebot_service.reply_to(message,"Sleeping... 😴")
            if(handle):
                name = handle.name()
                hash = str(handle.info_hash())
                
                print(f"{hash}\n{name}")
                try:
                    self.telebot_service.edit_message(message=reply,edit_text=f"Got Metadata, Starting Torrent Download...\n\nUploading: {name}\n`/stop {hash}`")
                    exist = self.thread_service.searchTask(name=name)
                    if exist: 
                        raise DuplicateThread("Already downloading")
                    self.thread_service.newTask(id=hash, handle=handle, reply=reply, target=self.dummy)
                except DuplicateThread as e:
                    self.telebot_service.reply_to(message,"Woke up... 🥱")

                return # todo remove
                for status in self.torrent_service.status_handler(handle=handle):
                    msg = TelebotUtil.format_torrent_status(status=status,name=name)
                    self.telebot_service.edit_message(message=reply,edit_text=msg)
                else:
                    self.telebot_service.delete_message(reply)
                    msg = f"✅ Upload COMPLETED\n\n{name}\n{f'\nCheck Here : {self.path_link}' if(self.path_link) else ''}\n\nReady To Go Again"
                    self.telebot_service.send_message(message=message,text=msg)
        else:
            self.telebot_service.edit_message(message=reply,edit_text="No download link found")

    def stream_status(self, handle, reply: Message):
        name = handle.name()

        for status in self.torrent_service.status_handler(handle=handle):
            msg = TelebotUtil.format_torrent_status(status=status,name=name)
            self.telebot_service.edit_message(message=reply,edit_text=msg)
        else:
            self.telebot_service.delete_message(reply)
            msg = f"✅ Upload COMPLETED\n\n{name}\n{f'\nCheck Here : {self.path_link}' if(self.path_link) else ''}\n\nReady To Go Again"
            self.telebot_service.send_message(message=reply.chat, text=msg)

    def dummy(self, handle, reply):
        print('Dummy')
        for i in range(10):
            print(f"{i} Threading")
            time.sleep(10)
        print('Dummy Done')
        self.telebot_service.reply_to(reply,"Woke up... 🥱")