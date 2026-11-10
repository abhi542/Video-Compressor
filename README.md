# Video Compressor

A fast, lightweight video compression tool built with **Python** and **FFmpeg**. It delivers **90%+ file size reduction** while preserving high visual quality and ensuring **100% universal playback compatibility** (Apple QuickTime, iPhone, Windows, Android, Chrome, Safari).

Developed by **[Abhinav Bhatt](https://abhinav-portfolio-website-murex.vercel.app/#)**.

Repository: **[github.com/abhi542/Video-Compressor](https://github.com/abhi542/Video-Compressor)**

---

## Features

- **Universal Playback Compatibility**: Encodes in standard H.264 High Profile (`yuv420p`, AAC audio, `+faststart` metadata) so compressed videos play seamlessly on all devices and browsers without codec errors.
- **High Compression Efficiency**: Reduces video file sizes by ~85%–95% (e.g. 288 MB down to 19 MB).
- **Modern Drag & Drop Web Interface**: Run `python3 web_app.py` for a sleek studio UI with real-time progress tracking and automatic downloads.
- **Batch / CLI Processing**: Drop files in `input/` and run `python3 app.py`.
- **GitHub Actions Ready**: Includes an automated CI/CD pipeline (`.github/workflows/compress.yml`) supporting direct uploads, YouTube links, and cloud URLs.
- **Zero External PIP Overhead**: Built purely on Python's standard library and FFmpeg.

---

## Prerequisites & Installation

### 1. Python 3
macOS and modern Linux distributions come with Python 3:
```bash
python3 --version
```

### 2. FFmpeg
Make sure FFmpeg is installed on your system PATH:
- **macOS (via Homebrew)**:
  ```bash
  brew install ffmpeg
  ```
- **Ubuntu / Debian**:
  ```bash
  sudo apt-get update && sudo apt-get install -y ffmpeg
  ```
- **Windows**:
  ```bash
  winget install Gyan.FFmpeg
  ```

### 3. Dependencies
The project uses standard library Python. You can inspect `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## Usage

### Method 1: Web Interface (Recommended)

Start the local server:
```bash
python3 web_app.py
```

Open your browser to:
**[http://localhost:8080](http://localhost:8080)**

- **Drag & drop** any video (`.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`).
- Choose your compression profile (Balanced recommended).
- Click **Compress Video** and watch the real-time upload and compression status.
- The compressed video **downloads automatically** when completed.

---

### Method 2: Command Line / Batch Folder

1. Place your video(s) into the `input/` folder:
   ```
   video-compressor/
   ├── input/
   │   └── my_video.mp4
   ├── output/
   └── app.py
   ```

2. Run:
   ```bash
   python3 app.py
   ```

3. The compressed video is saved to `output/` (e.g., `output/my_video_compressed.mp4`).

You can also compress any file directly from any path:
```bash
python3 app.py "/path/to/my_video.mov"
```

---

### Method 3: GitHub Actions Pipeline

A GitHub Actions workflow is included at [`.github/workflows/compress.yml`](.github/workflows/compress.yml).

- **Git Push**: Push video files into `input/` to trigger automatic cloud compression and download the artifact.
- **Workflow Dispatch (URL Mode)**:
  1. Go to your GitHub repository ➔ **Actions** ➔ **Video Compressor** ➔ **Run workflow**.
  2. Paste a video URL (YouTube, Vimeo, Twitter/X, direct link).
  3. GitHub Actions downloads it via `yt-dlp`, compresses it with universal H.264, and publishes the compressed file in the **Artifacts** tab.

---

## Project Structure

```
video-compressor/
├── .github/
│   └── workflows/
│       └── compress.yml      # Automated GitHub Actions workflow
├── input/                    # Put source videos here
├── output/                   # Compressed videos are saved here
├── app.py                    # Core CLI & batch compression script
├── web_app.py                # Drag & drop Web Studio interface
├── requirements.txt          # Requirements & system prerequisites
├── .gitignore                # Prevents large video binaries in Git
└── README.md                 # Documentation
```

---

## NOTE : Known Limitations & URL Handling

1. **YouTube & Social Media URLs**:
   - In GitHub Actions, YouTube, Vimeo, TikTok, Twitter/X, and Reddit links are downloaded automatically using `yt-dlp`.
   - For local CLI usage on your computer, YouTube downloading requires `yt-dlp` (`brew install yt-dlp`).
2. **Dropbox URLs**:
   - Standard Dropbox sharing links end in `?dl=0`, which serves a web preview page rather than the raw file. You must change the link suffix from `?dl=0` to `?dl=1` to allow direct video download.
3. **Google Drive URLs**:
   - Google Drive files larger than 100 MB show a "Virus scan warning" confirmation interstitial page. Direct CLI downloading (`curl`) will usually fail without browser session cookies or Google API tokens.
4. **GitHub 100 MB File Limit**:
   - GitHub imposes a strict 100 MB file size limit for regular Git commits. If you are uploading videos larger than 100 MB, do not commit them via `git push`. Instead, use the local Web App (`python3 web_app.py`) or the `workflow_dispatch` URL trigger in GitHub Actions.

---

## Author

Created by **Abhinav Bhatt**  
Portfolio: [abhinav-portfolio-website-murex.vercel.app](https://abhinav-portfolio-website-murex.vercel.app/#)  
GitHub: [github.com/abhi542](https://github.com/abhi542)
