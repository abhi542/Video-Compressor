import os
import sys
import shutil
import urllib.parse
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from app import compress_video, BASE_DIR, INPUT_DIR, OUTPUT_DIR

PORT = 8080

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Video Compressor Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #090d16;
      --card-bg: rgba(17, 24, 39, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-border-hover: rgba(56, 189, 248, 0.35);
      --primary: #38bdf8;
      --primary-hover: #0ea5e9;
      --primary-glow: rgba(56, 189, 248, 0.25);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --surface: #0f172a;
      --surface-border: #1e293b;
      --success: #10b981;
      --success-glow: rgba(16, 185, 129, 0.2);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-base);
      background-image: 
        radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(14, 165, 233, 0.08) 0px, transparent 50%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
      -webkit-font-smoothing: antialiased;
    }

    .wrapper {
      width: 100%;
      max-width: 600px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    /* Brand Header Badge */
    .brand-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(8px);
      margin-bottom: 20px;
      text-decoration: none;
      transition: all 0.25s ease;
    }

    .brand-badge:hover {
      border-color: var(--primary);
      background: rgba(56, 189, 248, 0.08);
      transform: translateY(-1px);
    }

    .brand-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--primary);
      box-shadow: 0 0 10px var(--primary);
    }

    .brand-badge-text {
      font-size: 12px;
      font-weight: 500;
      color: var(--text-muted);
      letter-spacing: 0.02em;
    }

    .brand-badge-name {
      color: var(--text-main);
      font-weight: 600;
    }

    /* Main Container Card */
    .card {
      width: 100%;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 36px 32px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(16px);
    }

    .header {
      margin-bottom: 24px;
    }

    .title-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 6px;
    }

    .icon-box {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--primary);
    }

    h1 {
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text-main);
    }

    p.subtitle {
      color: var(--text-muted);
      font-size: 13.5px;
      line-height: 1.5;
    }

    /* Dropzone */
    .dropzone {
      position: relative;
      border: 1.5px dashed var(--surface-border);
      border-radius: 14px;
      padding: 38px 24px;
      text-align: center;
      cursor: pointer;
      transition: all 0.25s ease;
      background: rgba(15, 23, 42, 0.5);
    }

    .dropzone:hover, .dropzone.dragover {
      border-color: var(--primary);
      background: rgba(56, 189, 248, 0.04);
      box-shadow: 0 0 24px rgba(56, 189, 248, 0.08);
    }

    .upload-icon-circle {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      margin: 0 auto 14px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--primary);
      transition: transform 0.2s ease;
    }

    .dropzone:hover .upload-icon-circle {
      transform: translateY(-2px);
    }

    .dropzone-label {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 4px;
    }

    .dropzone-hint {
      font-size: 12px;
      color: var(--text-dim);
    }

    .file-badge {
      display: none;
      margin-top: 14px;
      padding: 8px 14px;
      border-radius: 8px;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.25);
      font-size: 13px;
      font-weight: 600;
      color: var(--primary);
      word-break: break-all;
    }

    /* Controls */
    .controls {
      margin-top: 22px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .setting-group {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 14px;
      border-radius: 10px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--surface-border);
    }

    .setting-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text-muted);
    }

    select {
      background: var(--surface);
      color: var(--text-main);
      border: 1px solid var(--surface-border);
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 13px;
      font-family: inherit;
      outline: none;
      cursor: pointer;
      transition: border-color 0.2s;
    }

    select:focus {
      border-color: var(--primary);
    }

    /* Action Button */
    .submit-btn {
      width: 100%;
      background: var(--primary);
      color: #090d16;
      border: none;
      padding: 14px 20px;
      font-size: 14.5px;
      font-weight: 700;
      letter-spacing: 0.01em;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 14px var(--primary-glow);
    }

    .submit-btn:hover:not(:disabled) {
      background: var(--primary-hover);
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(14, 165, 233, 0.35);
    }

    .submit-btn:disabled {
      opacity: 0.45;
      cursor: not-allowed;
      box-shadow: none;
    }

    /* Status & Progress */
    .status-panel {
      display: none;
      margin-top: 22px;
      padding: 20px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--surface-border);
      border-radius: 12px;
      text-align: center;
    }

    .spinner-ring {
      display: inline-block;
      width: 26px;
      height: 26px;
      border: 2.5px solid rgba(255, 255, 255, 0.1);
      border-top-color: var(--primary);
      border-radius: 50%;
      animation: spin 0.8s infinite linear;
      margin-bottom: 12px;
    }

    @keyframes spin {
      100% { transform: rotate(360deg); }
    }

    .status-title {
      font-weight: 600;
      font-size: 14px;
      color: var(--text-main);
    }

    .status-detail {
      font-size: 12.5px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .progress-track {
      width: 100%;
      height: 6px;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 9999px;
      overflow: hidden;
      margin-top: 14px;
    }

    .progress-fill {
      width: 0%;
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #0ea5e9);
      border-radius: 9999px;
      transition: width 0.2s ease;
    }

    /* Result Card */
    .result-box {
      display: none;
      margin-top: 22px;
      padding: 20px;
      background: rgba(16, 185, 129, 0.06);
      border: 1px solid rgba(16, 185, 129, 0.25);
      border-radius: 14px;
      text-align: center;
    }

    .result-header {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-weight: 600;
      font-size: 14.5px;
      color: var(--success);
      margin-bottom: 14px;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-bottom: 18px;
    }

    .stat-card {
      background: rgba(0, 0, 0, 0.25);
      padding: 10px 8px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.04);
    }

    .stat-label {
      font-size: 11px;
      color: var(--text-dim);
      margin-bottom: 2px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .stat-val {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
    }

    .stat-val.highlight {
      color: var(--success);
    }

    .download-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 12px 18px;
      background: var(--success);
      color: #090d16;
      font-weight: 700;
      font-size: 14px;
      text-decoration: none;
      border-radius: 8px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 12px var(--success-glow);
    }

    .download-btn:hover {
      background: #059669;
      transform: translateY(-1px);
    }

    /* Footer */
    footer {
      margin-top: 24px;
      text-align: center;
    }

    .footer-link {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--text-dim);
      font-size: 12.5px;
      text-decoration: none;
      transition: color 0.2s ease;
    }

    .footer-link:hover {
      color: var(--primary);
    }

    .footer-link span.name {
      color: var(--text-muted);
      font-weight: 600;
    }

    .footer-link:hover span.name {
      color: var(--primary);
    }
  </style>
</head>
<body>
  <div class="wrapper">
    <!-- Abhinav Bhatt Branding Header -->
    <a href="https://abhinav-portfolio-website-murex.vercel.app/#" target="_blank" rel="noopener noreferrer" class="brand-badge">
      <div class="brand-dot"></div>
      <span class="brand-badge-text">Built by <span class="brand-badge-name">Abhinav Bhatt</span></span>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--text-dim);"><path d="M7 17l9.2-9.2M17 17V7H7"/></svg>
    </a>

    <!-- Main Card -->
    <div class="card">
      <div class="header">
        <div class="title-row">
          <div class="icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="23 7 16 12 23 17 23 7"/>
              <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
            </svg>
          </div>
          <h1>Video Compressor</h1>
        </div>
        <p class="subtitle">Compress high-bitrate videos into compact, universally compatible MP4 files.</p>
      </div>

      <input type="file" id="fileInput" accept="video/*" style="display: none;" />
      
      <!-- Drag & Drop Zone -->
      <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
        <div class="upload-icon-circle">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <div class="dropzone-label">Click or drag & drop video file here</div>
        <div class="dropzone-hint">Supports MP4, MOV, MKV, WebM, AVI</div>
        <div class="file-badge" id="fileBadge"></div>
      </div>

      <!-- Controls -->
      <div class="controls">
        <div class="setting-group">
          <label class="setting-label" for="crf">Compression Profile</label>
          <select id="crf">
            <option value="20">High Quality (Subtle reduction)</option>
            <option value="22" selected>Balanced</option>
            <option value="26">Maximum Compression (Smallest file)</option>
          </select>
        </div>

        <button type="button" class="submit-btn" id="submitBtn" disabled onclick="startUpload()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>Compress Video</span>
        </button>
      </div>

      <!-- Live Status Panel -->
      <div class="status-panel" id="statusPanel">
        <div class="spinner-ring" id="spinner"></div>
        <div class="status-title" id="statusTitle">Uploading video...</div>
        <div class="status-detail" id="statusDetail">0%</div>
        <div class="progress-track" id="progressTrack">
          <div class="progress-fill" id="progressFill"></div>
        </div>
      </div>

      <!-- Result Card -->
      <div class="result-box" id="resultBox">
        <div class="result-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          <span>Video Compressed Successfully</span>
        </div>

        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">Original</div>
            <div class="stat-val" id="statOriginal">0 MB</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Compressed</div>
            <div class="stat-val" id="statCompressed">0 MB</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Saved</div>
            <div class="stat-val highlight" id="statSaved">0%</div>
          </div>
        </div>

        <a id="downloadLink" class="download-btn" href="#" download>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          <span>Download Compressed Video</span>
        </a>
      </div>
    </div>

    <!-- Footer Branding -->
    <footer>
      <a href="https://abhinav-portfolio-website-murex.vercel.app/#" target="_blank" rel="noopener noreferrer" class="footer-link">
        <span>Designed & Developed by <span class="name">Abhinav Bhatt</span></span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
      </a>
    </footer>
  </div>

  <script>
    const fileInput = document.getElementById('fileInput');
    const dropzone = document.getElementById('dropzone');
    const fileBadge = document.getElementById('fileBadge');
    const submitBtn = document.getElementById('submitBtn');
    const statusPanel = document.getElementById('statusPanel');
    const statusTitle = document.getElementById('statusTitle');
    const statusDetail = document.getElementById('statusDetail');
    const progressFill = document.getElementById('progressFill');
    const resultBox = document.getElementById('resultBox');
    const statOriginal = document.getElementById('statOriginal');
    const statCompressed = document.getElementById('statCompressed');
    const statSaved = document.getElementById('statSaved');
    const downloadLink = document.getElementById('downloadLink');

    let selectedFile = null;

    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        setFile(fileInput.files[0]);
      }
    });

    ['dragover', 'dragenter'].forEach(e => {
      dropzone.addEventListener(e, (evt) => {
        evt.preventDefault();
        dropzone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(e => {
      dropzone.addEventListener(e, (evt) => {
        evt.preventDefault();
        dropzone.classList.remove('dragover');
      });
    });

    dropzone.addEventListener('drop', (evt) => {
      if (evt.dataTransfer.files.length > 0) {
        setFile(evt.dataTransfer.files[0]);
      }
    });

    function setFile(file) {
      selectedFile = file;
      const sizeMb = (file.size / (1024 * 1024)).toFixed(1);
      fileBadge.textContent = `${file.name} (${sizeMb} MB)`;
      fileBadge.style.display = 'inline-block';
      submitBtn.disabled = false;
      resultBox.style.display = 'none';
      statusPanel.style.display = 'none';
    }

    function startUpload() {
      if (!selectedFile) return;

      submitBtn.disabled = true;
      resultBox.style.display = 'none';
      statusPanel.style.display = 'block';
      statusTitle.textContent = "Uploading video...";
      statusDetail.textContent = "0%";
      progressFill.style.width = "0%";

      const crf = document.getElementById('crf').value;
      const url = `/api/upload?filename=${encodeURIComponent(selectedFile.name)}&crf=${encodeURIComponent(crf)}`;

      const xhr = new XMLHttpRequest();
      xhr.open("POST", url, true);
      xhr.responseType = "json";

      xhr.upload.onprogress = (evt) => {
        if (evt.lengthComputable) {
          const percent = Math.round((evt.loaded / evt.total) * 100);
          progressFill.style.width = percent + "%";
          const uploadedMb = (evt.loaded / (1024 * 1024)).toFixed(1);
          const totalMb = (evt.total / (1024 * 1024)).toFixed(1);
          statusDetail.textContent = `Uploaded ${percent}% (${uploadedMb} MB / ${totalMb} MB)`;
          if (percent >= 100) {
            statusTitle.textContent = "Compressing video with FFmpeg...";
            statusDetail.textContent = "Encoding frames (Universal H.264 profile)... please wait...";
          }
        }
      };

      xhr.onload = () => {
        submitBtn.disabled = false;
        if (xhr.status === 200 && xhr.response && xhr.response.download_url) {
          statusPanel.style.display = 'none';
          resultBox.style.display = 'block';
          statOriginal.textContent = `${xhr.response.original_size} MB`;
          statCompressed.textContent = `${xhr.response.compressed_size} MB`;
          statSaved.textContent = `-${xhr.response.space_saved}%`;
          downloadLink.href = xhr.response.download_url;
          downloadLink.setAttribute('download', xhr.response.filename);
          // Auto trigger download
          downloadLink.click();
        } else {
          statusTitle.textContent = "Compression Error";
          statusDetail.textContent = (xhr.response && xhr.response.error) || "Failed to process video.";
        }
      };

      xhr.onerror = () => {
        submitBtn.disabled = false;
        statusTitle.textContent = "Upload Error";
        statusDetail.textContent = "Connection interrupted or file transfer failed.";
      };

      xhr.send(selectedFile);
    }
  </script>
</body>
</html>
"""


class VideoServerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Keep server log clean
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
            return

        # Download endpoint: /download/<filename>
        if path.startswith("/download/"):
            filename = urllib.parse.unquote(path[len("/download/"):])
            file_path = OUTPUT_DIR / filename
            if file_path.is_file():
                self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                self.send_header("Content-Length", str(file_path.stat().st_size))
                self.end_headers()
                with open(file_path, "rb") as f:
                    shutil.copyfileobj(f, self.wfile)
                return
            else:
                self.send_error(404, "File not found")
                return

        self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/upload":
            query_params = urllib.parse.parse_qs(parsed.query)
            raw_filename = query_params.get("filename", ["video.mp4"])[0]
            crf_val = query_params.get("crf", ["22"])[0]

            try:
                crf = int(crf_val)
            except ValueError:
                crf = 22

            filename = Path(raw_filename).name
            if not filename:
                filename = "uploaded_video.mp4"

            INPUT_DIR.mkdir(parents=True, exist_ok=True)
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            upload_path = INPUT_DIR / filename

            try:
                content_length = int(self.headers.get("Content-Length", 0))
            except (ValueError, TypeError):
                content_length = 0

            # Stream directly to disk in 64KB chunks to conserve memory
            remaining = content_length
            with open(upload_path, "wb") as f:
                while remaining > 0:
                    chunk_size = min(remaining, 65536)
                    chunk = self.rfile.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)

            # Compress video
            output_file = compress_video(upload_path, crf=crf, codec="h264")

            if not output_file or not output_file.exists():
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Video compression failed."}')
                return

            original_size = upload_path.stat().st_size
            compressed_size = output_file.stat().st_size
            saved = original_size - compressed_size
            percentage = (saved / original_size) * 100 if original_size > 0 else 0

            resp_data = (
                f'{{"download_url": "/download/{urllib.parse.quote(output_file.name)}", '
                f'"filename": "{output_file.name}", '
                f'"original_size": "{original_size / (1024**2):.2f}", '
                f'"compressed_size": "{compressed_size / (1024**2):.2f}", '
                f'"space_saved": "{percentage:.2f}"}}'
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(resp_data.encode("utf-8"))
            return

        self.send_error(404, "Endpoint Not Found")


def run(port=PORT):
    server = HTTPServer(("0.0.0.0", port), VideoServerHandler)
    print("=" * 60)
    print("Video Compressor Web App is ready!")
    print(f"Local:   http://localhost:{port}")
    print(f"Network: http://0.0.0.0:{port}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.server_close()


if __name__ == "__main__":
    run()
