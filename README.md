# youtube-converter-mp3

This is a simple Python script to download audio from YouTube videos.

# Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
   - [Clone the Repository](#clone-the-repository)
   - [Install Dependencies](#virutal-environment--install-dependencies)
3. [Usage](#usage)
   - [Run the Script](#run-the-script)
   - [Expectations](#expectations)
4. [Contributing](#contributing)
5. [License](#license)

## Installation
Clone the Repository:

```bash
git clone https://github.com/timwhite06/youtube-converter-mp3.git
```

### Virutal Environment & Install Dependencies:

Before running the script, make sure you have Python installed on your system. Then, install the required Python packages using pip:

Navigate to the Project Directory:
```bash
cd <youtube-converter-mp3>
```

Create virtual environment
```bash
python -m venv .venv
```

On windows:
```bash
.venv\Scripts\activate
```

On Linux/macOS:
```bash
source .venv/bin/activate
```

Install the dependencies
``` bash
pip install -r requirements.txt
```

## Usage
####Run the Script:

Execute the script by running the following command:

```bash
python main.py
```
## Expectations

1) Select Download Location:

    - Choose the location on your computer where you want to save the downloaded audio file.

2) Enter YouTube URL:

    - You will be prompted to enter the URL of the YouTube video from which you want to download the audio.

3) Download Audio:

    - The script will download the audio in the best available quality and save it to the specified location.

# Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

# License
This project is licensed under the MIT License.
