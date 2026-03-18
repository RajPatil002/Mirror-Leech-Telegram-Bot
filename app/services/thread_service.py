from telebot.types import Message
from threading import Thread
from typing import Dict
import libtorrent as lt

from app.exceptions.thread_exception import DuplicateThread
from app.models.torrent_thread import TorrentThread

class ThreadService:

    def __init__(self):
        self.threads : Dict[str, TorrentThread] = {}


    def getTask(self, name=None, id=None)-> TorrentThread | None:
        tor_theads = self.threads.values()
        for tor in tor_theads:
            if id and id == tor.id:
                return tor
            if name and tor.name() == name:
                return tor
        return None

    def newTask(self, id: str, target: callable, handle: lt.torrent_handle, reply: Message):
        if id in self.threads:
            print("Has already", self.threads.keys())
            raise DuplicateThread("Thread with same ID already exist")
        t = Thread(target=target, args=(handle,reply))
        self.threads[id] = TorrentThread(thread=t,handle=handle,id=reply.id)
        t.start()
        return id

    def stopTask(self, id: str):
        if id not in self.threads:
            return None
        pass