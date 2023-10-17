import os
import subprocess
from pytube import YouTube

# Function to download YouTube video in highest quality
def download_youtube_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download()
        # return True, yt.title + ".mp4"
        return True, yt.title + ".mp3"
    except Exception as e:
        print(f"Error: {e}")
        return False, None

# Function to convert downloaded video to MP3 using ffmpeg
def convert_to_mp3(video_file):
    try:
        base_name, _ = os.path.splitext(video_file)
        mp3_file = os.path.join("music", f"{base_name}.mp3")
        subprocess.run(["ffmpeg", "-i", video_file, "-q:a", "0", "-map", "a", mp3_file])
        return mp3_file
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")
    
    success, video_file = download_youtube_video(youtube_url)
    
    if success:
        print("Video downloaded successfully!")
        
        mp3_file = convert_to_mp3(video_file)
        
        if mp3_file:
            print(f"MP3 file '{mp3_file}' created successfully!")
            
            # Optionally, you can delete the downloaded video file
            os.remove(video_file)
        else:
            print("Failed to convert to MP3.")
    else:
        print("Failed to download the video.")
