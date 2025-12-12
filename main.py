from ui.ui_main import Ui_MainWindow
import sys
from worker.downloader import DownloadWorker
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Select default save path
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # Start options
        self.ui.progressBar.setValue(0)
        self.ui.lbl_status.setText("Idle")

        # Button events
        self.ui.pushButton.clicked.connect(self.start_download)

        #Set worker to None
        self.worker = None

    def start_download(self):
        url = self.ui.url_lineedit.text().strip()

        if not url:
            self.ui.lbl_status.setText("Please enter a valid URL.")
            return
        
        self.ui.progressBar.setValue(0)
        self.ui.lbl_status.setText("Preparing to download...")
        
        #Worker options
        self.worker = DownloadWorker(url, self.download_path)
        self.worker.progress.connect(self.ui.progressBar.setValue)
        self.worker.status.connect(self.ui.lbl_status.setText)
        self.worker.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
