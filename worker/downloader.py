from PyQt5.QtCore import QThread, pyqtSignal
import yt_dlp
import os

class DownloadWorker(QThread):
    """
    Downloader Class for handling video downloads in a separate thread.
    """
    progress = pyqtSignal(int) # Signal for ProgressBar
    status = pyqtSignal(str)   # Signal for Status Updates

    def __init__(self, url, output_path):
        super().__init__()
        self.url = url
        self.output_path = output_path
    
    def run(self):
        """
        Start the download process.
        """
        def progress_hook(d):
            if d['status'] == "downloading":
                percent_str = d.get('_percent_str',"%0")
                percent_str = percent_str.strip().replace('%','')

                try:
                    percent = int(float(percent_str))
                    self.progress.emit(percent)
                except ValueError:
                    pass
            elif d['status'] == "finished":
                self.progress.emit(100)
                self.status.emit("Download finished, processing file...")

        ydl_opts = {
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,    
        }

        try:
            self.status.emit("Starting download...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

        except Exception as e:
            self.status.emit(f"Error: {str(e)}")
        
