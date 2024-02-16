import os
from pytube import YouTube
from tkinter import filedialog
import tkinter as tk

# Function to download YouTube audio in the best quality
def download_youtube_audio(url, download_path):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        audio.download(download_path)
        audio_file = os.path.join(download_path, f"{yt.title}.mp3")
        return True, audio_file, yt.title
    except Exception as e:
        print(f"Error: {e}")
        return False, None, None

# Function to prompt user for download location using tkinter
def prompt_for_download_path():
    root = tk.Tk()
    root.withdraw()
    download_path = filedialog.askdirectory(title="Select Download Location")
    return download_path

if __name__ == "__main__":
    download_path = prompt_for_download_path()

    if not download_path:
        print("Download location not selected. Exiting.")
    else:
        while True:
            youtube_url = input("Enter the YouTube URL (or type 'exit' to stop): ")

            if youtube_url.lower() == 'exit':
                break

            success, audio_file, title = download_youtube_audio(youtube_url, download_path)

            if success:
                print("\n" + title + ": Audio downloaded successfully!\n")

                # Optionally, you can delete the downloaded video file
                # os.remove(video_file)
            else:
                print("Failed to download the audio.")
