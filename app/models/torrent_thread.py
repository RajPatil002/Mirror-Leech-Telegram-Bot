from threading import Thread
import libtorrent as lt


class TorrentThread:
    def __init__(self, handle : lt.torrent_handle, thread: Thread):
        self.handler = handle
        self.thread = thread

    def name(self) -> str:
        return self.handler.name()
    
    def hash(self):
        return self.handler.info_hash()