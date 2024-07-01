import os
from pytube import YouTube
from tkinter import filedialog
import tkinter as tk
from mutagen.mp4 import MP4, MP4Cover
import requests


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = (bytes_downloaded / total_size) * 100  # percentage of file that has been downloaded
    print(f"\033[33m Song download progress: {liveprogress:.1f}%\033[0m")  # print progress in orange text


# Function to download YouTube audio in the best quality
def download_youtube_audio(url, download_path):
    try:
        # Create a YouTube object
        yt = YouTube(url, on_progress_callback=on_progress)

        if yt.streams:
            # If there are no audio streams but other streams are available
            any_stream = yt.streams.get_highest_resolution()

            # Download the highest resolution stream
            any_stream.download(download_path)
            any_file = os.path.join(download_path, f"{yt.title}.mp4")  # Use any file extension
            print("Downloading highest quality stream: No specific audio file available.")
            
            # Set metadata for the downloaded file
            set_mp4_metadata(any_file, yt.title, yt.author, yt.thumbnail_url)

            return True, any_file, yt.title
        else:
            print(" No streams available for this video.")
            return False, None, None

    except Exception as e:
        print(f"Error: {e}")
        return False, None, None

# Function to set MP4 metadata
def set_mp4_metadata(file_path, title, artist, thumbnail_url=None):
    try:
        # Open the MP4 file for editing
        video = MP4(file_path)
    except Exception as e:
        print(f"\033[33mError opening file FOR META DATA: {e}\033[0m")
        return

    # Set the title metadata
    video["\xa9nam"] = title  # '\xa9nam' is the key for the title metadata

    # Set the artist metadata
    video["\xa9ART"] = artist  # '\xa9ART' is the key for the artist metadata

    # If a thumbnail URL is provided, fetch and set the cover art
    if thumbnail_url:
        try:
            response = requests.get(thumbnail_url)  # Fetch the thumbnail image
            cover = MP4Cover(response.content, imageformat=MP4Cover.FORMAT_JPEG)  # Convert image to MP4Cover format
            video["covr"] = [cover]  # 'covr' is the key for cover art metadata
        except Exception as e:
            print(f"\033[33mError setting cover art FOR META DATA: {e}\033[0m")

    try:
        # Save the changes to the MP4 file
        video.save()
    except Exception as e:
        print(f"\033[33mError saving file FOR META DATA: {e}\033[0m")

# Function to prompt user for download location using tkinter
def prompt_for_download_path():
    # Create a root window and hide it
    root = tk.Tk()
    root.withdraw()
    # Open a directory selection dialog and return the selected path
    download_path = filedialog.askdirectory(title="Select Download Location")
    return download_path

if __name__ == "__main__":
    # Check if saved_urls.txt exists
    if not os.path.exists('../saved_urls.txt'):
        # Create the file if it doesn't exist
        open('../saved_urls.txt', 'w').close()

    else:
        # Ask the user if they want to download the videos in saved_urls.txt
        with open('../saved_urls.txt', 'r') as file:
            urls = file.readlines()
            if urls:
                # print a count of the urls
                print(f"\n  Found \033[92m{len(urls)}\033[0m saved URLs.  ")

                download_saved = input(" Do you want to download these videos? (y/n): \n")
                if download_saved.lower() == 'y':
                    download_path = prompt_for_download_path()

                    if not download_path:
                        print(" Download location not selected. Exiting.")
                    else:
                        # Download each URL in the saved_urls.txt file
                        for i, url in enumerate(urls):
                            success, audio_file, title = download_youtube_audio(url.strip(), download_path)

                            if success:
                                print(f"\n \033[92m{title}: downloaded successfully! \033[0m\n")
                                print(f" Progress: \033[92m{((i + 1) / len(urls)) * 100:.2f}%\033[0m")
                            else:
                                print("\033[91m Failed to download the audio. \033[0m\n")

                else:
                    print(" Exiting. Moving onto main program. \n")                

    # Prompt the user for a download location
    download_path = prompt_for_download_path()

    if not download_path:
        print("Download location not selected. Exiting.")
    else:
        # Continuously prompt the user for YouTube URLs to download
        while True:
            youtube_url = input(" Enter the YouTube URL (or type 'exit' to stop): ")

            if youtube_url.lower() == 'exit':
                break

            # Download the YouTube video and save the URL to saved_urls.txt
            success, audio_file, title = download_youtube_audio(youtube_url, download_path)

            if success:
                print("\n \033[92m" + title + ": downloaded successfully! \033[0m\n")
                # Open the file in append mode
                with open('../saved_urls.txt', 'a') as file:
                    # Write each line followed by a newline character
                    file.write(youtube_url + "\n")

                # Optionally, you can delete the downloaded video file
                # os.remove(audio_file)
            else:
                print("\033[91m Failed to download the audio. \033[0m\n")
