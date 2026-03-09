# import libtorrent
from typing import Generator
import libtorrent as lt
import time
from app.models.torrent_status import TorrentStatus

class TorrentService:

    # PATH = '/content/drive/MyDrive/TGD'
    PATH = './content'

    def __init__(self):
        self.session = lt.session()
        self.session.listen_on(6881, 6891)
        self.params = {
            'save_path': self.PATH,
            'storage_mode': lt.storage_mode_t(2)
        }
        pass


    def download(self, link: str) -> lt.torrent_handle | None:
        try:
            handle = lt.add_magnet_uri(self.session, link, self.params)
        except Exception:
            return None
        self.session.start_dht()

        for count in range(10):
            if(not handle.has_metadata()):
                time.sleep(1)
            else:
                break
        else:
            return None
        return handle
    
    def status_handler(self, handle: lt.torrent_handle, refresh: int | None) -> Generator[TorrentStatus, None, TorrentStatus]:
        status = handle.status()
        if not refresh:
            refresh = 10 if (status.total_wanted/1048576) > 500 else 5
        while (status.state != lt.torrent_status.seeding):
            status = handle.status()
            yield TorrentStatus(status)            
            time.sleep(refresh)

        return TorrentStatus(status)
