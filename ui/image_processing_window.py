from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QHBoxLayout, QSlider, QScrollArea, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtCore import Qt

from core.image_processor import *
from ui.utils.file_utils import saveImageFileDialog

class ImageProcessingWindow(QWidget):
    def __init__(self, parent=None, fileName=None):
        super().__init__()
        self.parent = parent
        self.setWindowIcon(QIcon("resources/icons/app_icon.png"))
        self.setWindowTitle("Image Processing - {}".format(fileName))
        self.setGeometry(100, 100, 540, 480)

        self.initUI()
        self.filePath = None
        self.zoomScale = 1.0
        self.image = None
        self.processedImage = None
        self.noiseGause = False
        self.blur = False
        
    def initUI(self):
        mainLayout = QVBoxLayout()
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setAlignment(Qt.AlignCenter)
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        scrollArea.setWidget(self.imageLabel)
        mainLayout.addWidget(scrollArea)

        secondLayout = QHBoxLayout()

        featuresLayout = QVBoxLayout()
        self.resizeWidthEdit = QLineEdit(self)
        self.resizeHeightEdit = QLineEdit(self)
        resizeButton = QPushButton("Resize Image", self)
        resizeButton.clicked.connect(self.resizeImageOnClick)
        resizeLayout = QHBoxLayout()
        resizeLayout.addWidget(QLabel("Width:"))
        resizeLayout.addWidget(self.resizeWidthEdit)
        resizeLayout.addWidget(QLabel("Height:"))
        resizeLayout.addWidget(self.resizeHeightEdit)
        resizeLayout.addWidget(resizeButton)
        featuresLayout.addLayout(resizeLayout)

        tempLayout = QHBoxLayout()
        rotateLeftButton = QPushButton("Rotate Left", self)
        rotateLeftButton.clicked.connect(lambda: self.rotateImageOnClick(90))
        rotateRightButton = QPushButton("Rotate Right", self)
        rotateRightButton.clicked.connect(lambda: self.rotateImageOnClick(-90))
        rotateLayout = QVBoxLayout()
        rotateLayout.addWidget(rotateLeftButton)
        rotateLayout.addWidget(rotateRightButton)
        tempLayout.addLayout(rotateLayout)
        
        flipHorizontalButton = QPushButton("Flip Horizontal", self)
        flipHorizontalButton.clicked.connect(lambda: self.flipImageOnClick('horizontal'))
        flipVerticalButton = QPushButton("Flip Vertical", self)
        flipVerticalButton.clicked.connect(lambda: self.flipImageOnClick('vertical'))
        flipLayout = QVBoxLayout()
        flipLayout.addWidget(flipHorizontalButton)
        flipLayout.addWidget(flipVerticalButton)
        tempLayout.addLayout(flipLayout)
        
        noiseCheckBox = QCheckBox("Apply Gaussian Noise", self)
        noiseCheckBox.stateChanged.connect(self.noiseToggle)
        blurCheckBox = QCheckBox("Apply Blur Effect", self)
        blurCheckBox.stateChanged.connect(self.blurToggle)
        filterLayout = QVBoxLayout()
        filterLayout.addWidget(noiseCheckBox)
        filterLayout.addWidget(blurCheckBox)
        tempLayout.addLayout(filterLayout)

        featuresLayout.addLayout(tempLayout)

        bcsLayout = QHBoxLayout()
        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setValue(0)
        self.contrastSlider = QSlider(Qt.Horizontal)
        self.contrastSlider.setMinimum(-100)
        self.contrastSlider.setMaximum(100)
        self.contrastSlider.setValue(0)
        self.saturationSlider = QSlider(Qt.Horizontal)
        self.saturationSlider.setMinimum(-100)
        self.saturationSlider.setMaximum(100)
        self.saturationSlider.setValue(0)
        self.brightnessSlider.valueChanged.connect(self.updateImage)
        self.contrastSlider.valueChanged.connect(self.updateImage)
        self.saturationSlider.valueChanged.connect(self.updateImage)
        bcsLayout.addWidget(QLabel("Brightness:"))
        bcsLayout.addWidget(self.brightnessSlider)
        bcsLayout.addWidget(QLabel("Contrast:"))
        bcsLayout.addWidget(self.contrastSlider)
        bcsLayout.addWidget(QLabel("Saturation:"))
        bcsLayout.addWidget(self.saturationSlider)
        featuresLayout.addLayout(bcsLayout)
        secondLayout.addLayout(featuresLayout)

        secondLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        commandLayout = QVBoxLayout()
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.onSaveButton)
        self.backButton = QPushButton("Cancel", self)
        self.backButton.clicked.connect(self.onBackButton)
        commandLayout.addWidget(self.saveButton)
        commandLayout.addWidget(self.backButton)
        secondLayout.addLayout(commandLayout)
        mainLayout.addLayout(secondLayout)

        self.setLayout(mainLayout)

    def loadImageOnStart(self, filePath):
        self.image = loadImage(filePath)
        self.filePath = filePath
        self.image = convertColor(self.image)
        if self.image is not None:
            height, width = self.image.shape[:2]
            self.resizeWidthEdit.setText(str(width))
            self.resizeHeightEdit.setText(str(height))
        self.displayImage(self.image)

    def updateImage(self):
        image = self.image.copy()
        if self.brightnessSlider.value():
            image = adjustBrightness(image, self.brightnessSlider.value())
        if self.contrastSlider.value():
            image = adjustContrast(image, self.contrastSlider.value())
        if self.saturationSlider.value():
            image = adjustSaturation(image, self.saturationSlider.value())
        if self.noiseGause:
            image = applyNoiseGause(image)
        if self.blur:
            image = applyBlur(image)

        self.processedImage = image
        self.displayImage(image)

    def displayImage(self, image):
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        scaledPixmap = pixmap.scaled(self.zoomScale * pixmap.size(), Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(scaledPixmap)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomScale *= 1.25
            else:
                self.zoomScale /= 1.25

            self.updateImage()
            event.accept()
        else:
            super().wheelEvent(event)

    def resizeImageOnClick(self):
        width = int(self.resizeWidthEdit.text())
        height = int(self.resizeHeightEdit.text())
        self.image = resizeImage(self.image, width, height)
        self.resizeWidthEdit.setText(str(self.image.shape[1]))
        self.resizeHeightEdit.setText(str(self.image.shape[0]))
        self.updateImage()

    def noiseToggle(self, state):
        self.noiseGause = state == Qt.Checked
        self.updateImage()

    def blurToggle(self, state):
        self.blur = state == Qt.Checked
        self.updateImage()

    def rotateImageOnClick(self, angle):
        self.image = rotateImage(self.image, angle)
        self.updateImage()

    def flipImageOnClick(self, direction):
        self.image = flipImage(self.image, direction)
        self.updateImage()

    def onSaveButton(self):
        newFilePath = saveImageFileDialog(self, self.filePath)
        
        if newFilePath:
            saveImage(newFilePath, self.processedImage)

    def onBackButton(self):
        self.hide()
        self.deleteLater()
        self.parent.show()