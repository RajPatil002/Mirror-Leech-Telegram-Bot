from telebot.types import Message
from app.models.torrent_status import TorrentStatus

class TelebotUtil:

    @staticmethod
    def getMessageText(message: Message) -> str:
        if(message.reply_to_message):
            return message.reply_to_message.text
        return message.text
    
    @staticmethod
    def extractLink(text):
        link = None
        if "/tm" in text :
            text = text.replace("/tm","").strip()
        elif "/tormirror" in text:
            text = text.replace("/tormirror","").strip()

        if "magnet:?xt=urn:btih:" in text:
            link = text[text.index("magnet"):]

        return link
    
    @staticmethod
    def size_in_mb(bytes: int):
        return bytes / 1048576
    
    @staticmethod
    def format_sec(sec):
        if sec < 60:
            return '%02ds' % sec
        else:
            m = sec / 60
            s = sec % 60
            return '%dm : %02ds' % (m,s)

    @staticmethod
    def format_torrent_status(status: TorrentStatus, name: str):
        return (
            f"Name : {name}\n\n"
            f"☁️ {status.progress_perc():.2f}% of {TelebotUtil.size_in_mb(status.size):.3f} MB\n"
            f"⏰ : {TelebotUtil.format_sec(status.time_left_sec())}\n"
            f"🔽 : {TelebotUtil.size_in_mb(status.down_speed):.3f} MB/s "
            f"🔼 : {TelebotUtil.size_in_mb(status.up_speed):.3f} MB/s\n"
            f"👥 peers : {status.peers}  🌱 seeds : {status.seeds}\n\n"
            f"{status.state}"
        )