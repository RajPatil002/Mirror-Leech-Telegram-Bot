import libtorrent as lt
class TorrentStatus:
    
    STATE_STR = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']

    def __init__(self, status: lt.torrent_status):
        self.progress = status.progress
        self.size = status.total_wanted
        self.peers = status.num_peers
        self.seeds = status.num_seeds
        self.down_speed = status.download_rate
        self.up_speed = status.upload_rate
        self.state = self.STATE_STR[status.state]

    def time_left(self):
        return (self.total_wanted * (1 - self.progress)) / self.download_rate