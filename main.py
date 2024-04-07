import os
from pytube import YouTube
from tkinter import filedialog
import tkinter as tk

# Function to download YouTube audio in the best quality
def download_youtube_audio(url, download_path):
    try:
        global progress_bar
        yt = YouTube(url)

        if yt.streams:
            # If there are no audio streams but other streams are available
            any_stream = yt.streams.get_highest_resolution()

            any_stream.download(download_path)
            any_file = os.path.join(download_path, f"{yt.title}.mp4")  # Use any file extension
            print("Downloading ANY stream: No audio available.")

            return True, any_file, yt.title
        else:
            print("No streams available for this video.")
            return False, None, None

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
                print("\n \033[92m" + title + ": downloaded successfully! \033[0m\n")

                # Optionally, you can delete the downloaded video file
                # os.remove(video_file)
            else:
                print("\033[91m Failed to download the audio. \033[0m\n")
