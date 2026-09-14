import os

from dotenv import load_dotenv

load_dotenv()

JSON_PATH = os.getenv("JSON_PATH", "tasks.json")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False") == "True"
DB_PATH = os.getenv("DB_PATH", "data/tasks.db")