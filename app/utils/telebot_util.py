from telebot.types import Message
class TelebotUtil:

    @staticmethod
    def getMessageText(message: Message) -> str:
        if(message.reply_to_message):
            return message.reply_to_message.text
        return message.text
    
    def extractLink(text):
        link = None
        if "/tm" in text :
            text = text.replace("/tm","").strip()
        elif "/tormirror" in text:
            text = text.replace("/tormirror","").strip()

        if "magnet:?xt=urn:btih:" in text:
            link = text[text.index("magnet"):]

        return link