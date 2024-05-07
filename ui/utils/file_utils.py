from pathlib import Path
from PyQt5.QtWidgets import QFileDialog

def openImageFileDialog(parent):
	options = QFileDialog.Options()
	fileName, _ = QFileDialog.getOpenFileName(parent, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
	
	return fileName

def saveImageFileDialog(parent, filePath):
	options = QFileDialog.Options()
	fileName, _ = QFileDialog.getSaveFileName(parent, "Save As", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
	if fileName:
		if not fileName.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
			fileName += getFileNameAndExtension(filePath)[1]
	
	return fileName

def openAudioFileDialog(parent):
	options = QFileDialog.Options()
	fileName, _ = QFileDialog.getOpenFileName(parent, "Select Audio", "", "Audio Files (*.mp3 *.wav *.ogg)", options=options)
	
	return fileName

def saveAudioFileDialog(parent, filePath):
	options = QFileDialog.Options()
	fileName, _ = QFileDialog.getSaveFileName(parent, "Save As", "", "Audios (*.mp3 *.wav *.ogg);;All Files (*)", options=options)
	if fileName:
		if not fileName.endswith(('.mp3', '.wav', '.ogg')):
			fileName += getFileNameAndExtension(filePath)[1]
	
	return fileName

def getFileNameAndExtension(filePath):
    path = Path(filePath)
    return [path.name, path.suffix]