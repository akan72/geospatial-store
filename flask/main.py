from src.app import app

import os 
from dotenv import load_dotenv

load_dotenv('.env')

# Load pickled model here? 
if __name__ == "__main__":
    app.run()