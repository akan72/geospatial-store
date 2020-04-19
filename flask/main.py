import os 
from src.app import app
from dotenv import load_dotenv

load_dotenv('.env')

# Load pickled model here? 
if __name__ == "__main__":
    app.run()