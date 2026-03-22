import os
from dotenv import load_dotenv

# 1. This line finds the .env file and loads the variables into your "Environment"
load_dotenv()

# 2. Use os.getenv to grab the specific variable by its name
api_key = os.getenv('YOUTUBE_API_KEY')

# 3. Safety Check: Always verify the key was actually found
if api_key is None:
    print("Error: YOUTUBE_API_KEY not found. Check your .env file!")
else:
    print("API Key loaded successfully!")
    # Now you can use it:
    # youtube = build('youtube', 'v3', developerKey=api_key)