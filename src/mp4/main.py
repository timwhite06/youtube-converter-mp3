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

                download_saved = input("Do you want to download these videos? (y/n): \n")
                if download_saved.lower() == 'y':
                    download_path = prompt_for_download_path()

                    if not download_path:
                        print("Download location not selected. Exiting.")
                    else:
                        for i, url in enumerate(urls):
                            success, audio_file, title = download_youtube_audio(url.strip(), download_path)

                            if success:
                                print(f"\n \033[92m{title}: downloaded successfully! \033[0m\n")
                                print(f"Progress: \033[92m{((i + 1) / len(urls)) * 100:.2f}%\033[0m")
                            else:
                                print("\033[91m Failed to download the audio. \033[0m\n")

                else:
                    print("Exiting. Moving onto main program. \n")                

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
                # Open the file in append mode
                with open('../saved_urls.txt', 'a') as file:
                    # Write each line followed by a newline character
                    file.write(youtube_url + "\n")

                # Optionally, you can delete the downloaded video file
                # os.remove(video_file)
            else:
                print("\033[91m Failed to download the audio. \033[0m\n")