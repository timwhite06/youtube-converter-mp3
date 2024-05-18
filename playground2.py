import os
import threading
from pytube import YouTube
from tkinter import filedialog
import tkinter as tk
from mutagen.mp4 import MP4, MP4Cover
import requests

print_lock = threading.Lock()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = (bytes_downloaded / total_size) * 100  # percentage of file that has been downloaded
    print(f"\033[33m Song download progress: {liveprogress:.1f}%\033[0m")  # print progress in orange text

def download_youtube_audio(url, download_path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)

        if yt.streams:
            any_stream = yt.streams.get_highest_resolution()
            any_stream.download(download_path)
            any_file = os.path.join(download_path, f"{yt.title}.mp4")
            print("Downloading highest quality stream: No specific audio file available.")
            set_mp4_metadata(any_file, yt.title, yt.author, yt.thumbnail_url)

            return True, any_file, yt.title
        else:
            print(" No streams available for this video.")
            return False, None, None

    except Exception as e:
        print(f"Error: {e}")
        return False, None, None

def set_mp4_metadata(file_path, title, artist, thumbnail_url=None):
    try:
        video = MP4(file_path)
    except Exception as e:
        print(f"\033[33mError opening file FOR META DATA: {e}\033[0m")
        return

    video["\xa9nam"] = title
    video["\xa9ART"] = artist

    if thumbnail_url:
        try:
            response = requests.get(thumbnail_url)
            cover = MP4Cover(response.content, imageformat=MP4Cover.FORMAT_JPEG)
            video["covr"] = [cover]
        except Exception as e:
            print(f"\033[33mError setting cover art FOR META DATA: {e}\033[0m")

    try:
        video.save()
    except Exception as e:
        print(f"\033[33mError saving file FOR META DATA: {e}\033[0m")

def prompt_for_download_path():
    root = tk.Tk()
    root.withdraw()
    download_path = filedialog.askdirectory(title="Select Download Location")
    return download_path

def process_download_queue(download_queue, download_path):
    while True:
        if download_queue:
            url = download_queue.pop(0)
            success, audio_file, title = download_youtube_audio(url, download_path)

            with print_lock:
                if success:
                    print(f"\n\033[92m{title}: downloaded successfully!\033[0m\n")
                else:
                    print("\033[91mFailed to download the audio.\033[0m\n")


if __name__ == "__main__":
    if not os.path.exists('saved_urls.txt'):
        open('saved_urls.txt', 'w').close()
    else:
        with open('saved_urls.txt', 'r') as file:
            urls = file.readlines()
            if urls:
                print(f"\n  Found \033[92m{len(urls)}\033[0m saved URLs.  ")

                download_saved = input(" Do you want to download these videos? (y/n): \n")
                if download_saved.lower() == 'y':
                    download_path = prompt_for_download_path()

                    if not download_path:
                        print(" Download location not selected. Exiting.")
                    else:
                        for i, url in enumerate(urls):
                            success, audio_file, title = download_youtube_audio(url.strip(), download_path)

                            if success:
                                print(f"\n \033[92m{title}: downloaded successfully! \033[0m\n")
                                print(f" Progress: \033[92m{((i + 1) / len(urls)) * 100:.2f}%\033[0m")
                            else:
                                print("\033[91m Failed to download the audio. \033[0m\n")

                else:
                    print(" Exiting. Moving onto main program. \n")                

    download_path = prompt_for_download_path()

    if not download_path:
        with print_lock:
            print("Download location not selected. Exiting.")
    else:
        download_queue = []
        download_thread = threading.Thread(target=process_download_queue, args=(download_queue, download_path))
        download_thread.start()

        while True:
            with print_lock:
                youtube_url = input("Enter the YouTube URL (or type 'exit' to stop): ")

            if youtube_url.lower() == 'exit':
                break
            else:
                download_queue.append(youtube_url)