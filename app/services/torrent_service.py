# import libtorrent
from typing import Generator
import libtorrent as lt
import time
from app.models.torrent_status import TorrentStatus
from app.exceptions.torrent_exception import NoSourceFound, NoMetadataFound

class TorrentService:

    def __init__(self, save_path: str):
        self.session = lt.session()
        self.session.listen_on(6881, 6891)
        self.params = {
            'save_path': save_path,
            'storage_mode': lt.storage_mode_t(2)
        }
        pass


    def download(self, link: str) -> lt.torrent_handle | None:
        try:
            handle = lt.add_magnet_uri(self.session, link, self.params)
        except Exception:
            raise NoSourceFound(message="No download sounce found")
        self.session.start_dht()

        for count in range(10):
            if(not handle.has_metadata()):
                time.sleep(1)
            else:
                break
        else:
            raise NoMetadataFound(message="Unable to fetch metadata")
        return handle
    
    def status_handler(self, handle: lt.torrent_handle, refresh: int | None = None) -> Generator[TorrentStatus, None, TorrentStatus]:
        status = handle.status()
        if not refresh:
            refresh = 10 if (status.total_wanted/1048576) > 500 else 5
        while (status.state != lt.torrent_status.seeding):
            status = handle.status()
            yield TorrentStatus(status)            
            time.sleep(refresh)

        return TorrentStatus(status)
