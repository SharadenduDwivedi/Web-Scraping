import os
import csv
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_youtube_comments(video_id, max_comments):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    comments_data = []
    next_page_token = None
    
    print(f"Starting extraction for video ID: {video_id}...")

    while len(comments_data) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100, 
            pageToken=next_page_token,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            comments_data.append({
                'author': snippet['authorDisplayName'],
                'comment': snippet['textDisplay'],
                'published_at': snippet['publishedAt'],
                'likes': snippet['likeCount']
            })
            
            if len(comments_data) >= max_comments:
                break

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
            
        print(f"Fetched {len(comments_data)} comments so far...")

    return comments_data

# FIX: Remove the f-string from the function header
def save_to_csv(data, filename):
    if not data:
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Successfully saved {len(data)} comments to {filename}!")

# --- EXECUTION ---
VIDEO_ID = input("Enter the Youtube Video ID: ")
user_filename = input("Enter filename for CSV (without .csv): ")
full_filename = f"{user_filename}.csv"
comments_count = int(input("Enter how many comments you want to extract: "))

try:
    all_comments = get_youtube_comments(VIDEO_ID, max_comments=comments_count)
    if all_comments:
        # Pass the filename here!
        save_to_csv(all_comments, full_filename)
    else:
        print("No comments found or video ID is incorrect.")
except Exception as e:
    print(f"An error occurred: {e}")