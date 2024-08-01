from dotenv import load_dotenv
import os


class EnvironmentSetup:
    @staticmethod
    def load_env():
        load_dotenv()

    @staticmethod
    def get_env(key):
        return os.getenv(key)