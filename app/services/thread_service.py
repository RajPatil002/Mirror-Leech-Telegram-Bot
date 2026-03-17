from threading import Thread
from typing import Dict
import libtorrent as lt

from app.models.torrent_thread import TorrentThread

class ThreadService:

    def __init__(self):
        self.threads : Dict[str, TorrentThread] = {}


    def getTask(self, name)-> TorrentThread | None:
        tor_theads = self.threads.values()
        for tor in tor_theads:
            if tor.name() == name:
                return tor
        return None

    def newTask(self, id: str, target: callable, args):
        if id in self.threads:
            return None
        self.threads[id] = Thread(target=target, args=args)
        return id

    def stopTask(self, id: str):
        if id not in self.threads:
            return None
        pass