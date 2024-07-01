import os
from pytube import YouTube
from tkinter import filedialog
import tkinter as tk
from mutagen.mp3 import MP3, EasyMP3
from mutagen.id3 import ID3, APIC, error
import requests

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    liveprogress = (bytes_downloaded / total_size) * 100  # percentage of file that has been downloaded
    print(f"\033[33m Song download progress: {liveprogress:.1f}%\033[0m")  # print progress in orange text

def download_youtube_audio(url, download_path):
    try:
        # Create a YouTube object
        yt = YouTube(url, on_progress_callback=on_progress)
        
        if yt.streams.filter(only_audio=True):
            # Download the highest quality audio stream
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_file_path = audio_stream.download(download_path)
            base, ext = os.path.splitext(audio_file_path)
            new_file_path = base + '.mp3'
            os.rename(audio_file_path, new_file_path)
            
            # Set metadata for the downloaded file
            set_mp3_metadata(new_file_path, yt.title, yt.author, yt.thumbnail_url)
            
            return True, new_file_path, yt.title
        else:
            print("No audio streams available for this video.")
            return False, None, None
    except Exception as e:
        print(f"Error: {e}")
        return False, None, None

def set_mp3_metadata(file_path, title, artist, thumbnail_url=None):
    try:
        audio = EasyMP3(file_path)
        audio['title'] = title
        audio['artist'] = artist
        audio.save()
        
        if thumbnail_url:
            audio = MP3(file_path, ID3=ID3)
            try:
                audio.add_tags()
            except error:
                pass
            
            response = requests.get(thumbnail_url)
            audio.tags.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime='image/jpeg',  # image/jpeg or image/png
                    type=3,  # 3 is for the cover image
                    desc=u'Cover',
                    data=response.content
                )
            )
            audio.save()
    except Exception as e:
        print(f"\033[33mError setting metadata: {e}\033[0m")

def prompt_for_download_path():
    root = tk.Tk()
    root.withdraw()
    download_path = filedialog.askdirectory(title="Select Download Location")
    return download_path

if __name__ == "__main__":
    if not os.path.exists('../saved_urls.txt'):
        open('../saved_urls.txt', 'w').close()
    else:
        with open('../saved_urls.txt', 'r') as file:
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
        print("Download location not selected. Exiting.")
    else:
        while True:
            youtube_url = input(" Enter the YouTube URL (or type 'exit' to stop): ")
            if youtube_url.lower() == 'exit':
                break
            success, audio_file, title = download_youtube_audio(youtube_url, download_path)
            if success:
                print("\n \033[92m" + title + ": downloaded successfully! \033[0m\n")
                with open('../saved_urls.txt', 'a') as file:
                    file.write(youtube_url + "\n")
            else:
                print("\033[91m Failed to download the audio. \033[0m\n")
