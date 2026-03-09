from app.listener.message_listener import MessageListener
from app.settings.config import Config


def main() -> None:
    config = Config()
    listener = MessageListener(config=config)
    listener.start_polling()


if __name__ == "__main__":
    main()
