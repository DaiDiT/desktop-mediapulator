from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ui.image_processing_window import ImageProcessingWindow
from ui.audio_processing_window import AudioProcessingWindow
from ui.utils.file_utils import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("resources/icons/app_icon.png"))
        self.setWindowTitle("Mediapulator")
        self.setGeometry(100, 100, 240, 320)
        self.imageProcessingWindow = None
        self.audioProcessingWindow = None
        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout()
        centralWidget.setLayout(layout)

        self.label = QLabel("Simple Tools for Image and Audio Processing", self)
        self.label.setObjectName(u"appDescription")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.imgButton = QPushButton("Process Image", self)
        self.imgButton.setObjectName(u"imgButton")
        layout.addWidget(self.imgButton)

        self.audioButton = QPushButton("Process Audio", self)
        self.audioButton.setObjectName(u"audioButton")
        layout.addWidget(self.audioButton)

        self.imgButton.clicked.connect(self.processImage)
        self.audioButton.clicked.connect(self.processAudio)

    def show(self):
        super().show()
        if self.imageProcessingWindow is not None:
            self.imageProcessingWindow.deleteLater()
            self.imageProcessingWindow = None

        if self.audioProcessingWindow is not None:
            self.audioProcessingWindow.deleteLater()
            self.audioProcessingWindow = None
                
    def processImage(self):
        filePath = openImageFileDialog(self)
        print(filePath)
        
        if filePath:
            if self.imageProcessingWindow is not None:
                self.imageProcessingWindow.deleteLater()
            
            fileName = getFileNameAndExtension(filePath)[0]
            self.imageProcessingWindow = ImageProcessingWindow(self, fileName)
            self.imageProcessingWindow.loadImageOnStart(filePath)
            self.imageProcessingWindow.show()
            self.hide()
        else:
            print("No file selected")


    def processAudio(self):
        filePath = openAudioFileDialog(self)
        print(filePath)
        
        if filePath:
            if self.audioProcessingWindow is not None:
                self.audioProcessingWindow.deleteLater()
            
            fileName = getFileNameAndExtension(filePath)[0]
            self.audioProcessingWindow = AudioProcessingWindow(self, fileName)
            self.audioProcessingWindow.loadAudioOnStart(filePath)
            self.audioProcessingWindow.show()
            self.hide()
        else:
            print("No file selected")