import os
import csv
from dotenv import load_dotenv
from googleapiclient.discovery import build

# 1. Load your API key from the .env file
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_youtube_comments(video_id, max_comments=500):
    # Initialize the YouTube API client
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    comments_data = []
    next_page_token = None
    
    print(f"Starting extraction for video ID: {video_id}...")

    while len(comments_data) < max_comments:
        # Request a page of comments
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # 100 is the max allowed per request
            pageToken=next_page_token,
            textFormat="plainText"
        )
        response = request.execute()

        # Extract data from the response
        for item in response['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            comments_data.append({
                'author': snippet['authorDisplayName'],
                'comment': snippet['textDisplay'],
                'published_at': snippet['publishedAt'],
                'likes': snippet['likeCount']
            })
            
            # Stop if we hit our limit mid-page
            if len(comments_data) >= max_comments:
                break

        # Check if there's another page
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
            
        print(f"Fetched {len(comments_data)} comments so far...")

    return comments_data

def save_to_csv(data, filename="youtube_comments_wrong_direction_passengers.csv"):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Successfully saved {len(data)} comments to {filename}!")

# --- EXECUTION ---
VIDEO_ID = "VvRVu78IHHo"  # From your URL: watch?v=VvRVu78IHHo
try:
    all_comments = get_youtube_comments(VIDEO_ID, max_comments=500)
    if all_comments:
        save_to_csv(all_comments)
except Exception as e:
    print(f"An error occurred: {e}")