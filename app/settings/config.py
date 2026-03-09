from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.tele_api_key = os.getenv("API_KEY")
        self.save_path = os.getenv("PATH")
        self.saved_path_link = os.getenv("PATH_LINK")