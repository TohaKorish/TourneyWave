import os


class Settings:
    def __init__(self):
        self.BACKEND_URL = os.getenv('BACKEND_URL')


settings = Settings()