import os
from tkinter import Tk, filedialog
from moviepy.editor import VideoFileClip
from colorama import init, Fore

def select_directory(prompt):
    """Open a dialog to select a directory and return the selected path."""
    root = Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title=prompt)
    root.destroy()
    return folder_selected

def convert_mp4_to_mp3(input_dir, output_dir):
    """Convert all MP4 files in the input directory to MP3 and save them in the output directory."""
    for filename in os.listdir(input_dir):
        if filename.endswith('.mp4'):
            mp4_path = os.path.join(input_dir, filename)
            mp3_filename = os.path.splitext(filename)[0] + '.mp3'
            mp3_path = os.path.join(output_dir, mp3_filename)

            try:
                # Load the video file
                video = VideoFileClip(mp4_path)
                # Extract the audio
                audio = video.audio
                # Write the audio file with the same metadata
                audio.write_audiofile(mp3_path, codec='mp3')

                print(f"Converted: {mp4_path} -> {mp3_path}")

            except Exception as e:
                print(Fore.RED + f"Failed to convert: {mp4_path}. Error: {e}" + Fore.RESET)

if __name__ == '__main__':
    # Initialize colorama
    init(autoreset=True)

    # Select the input directory
    input_directory = select_directory("Select the directory containing MP4 files")
    if not input_directory:
        print("No input directory selected. Exiting...")
        exit()

    # Select the output directory
    output_directory = select_directory("Select the output directory for MP3 files")
    if not output_directory:
        print("No output directory selected. Exiting...")
        exit()

    # Convert MP4 files to MP3
    convert_mp4_to_mp3(input_directory, output_directory)
    print("Conversion process completed.")
