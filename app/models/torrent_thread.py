from threading import Thread
import libtorrent as lt


class TorrentThread:
    def __init__(self, id, handle : lt.torrent_handle, thread: Thread):
        self.id = id
        self.handle = handle
        self.thread = thread

    def name(self) -> str:
        return self.handle.name()
    
    def hash(self):
        return self.handle.info_hash()