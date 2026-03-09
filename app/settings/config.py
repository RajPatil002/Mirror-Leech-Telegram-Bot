from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.tele_api_key = os.getenv("API_KEY")