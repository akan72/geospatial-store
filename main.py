from app import app

import os 
from dotenv import load_dotenv

load_dotenv()

# Load pickled model here? 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
