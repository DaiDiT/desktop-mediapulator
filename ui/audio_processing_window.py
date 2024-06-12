from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio

from core.audio_processor import *
from ui.utils.file_utils import saveAudioFileDialog

class AudioProcessingWindow(QWidget):
	def __init__(self, parent=None, fileName=None):
		super().__init__()
		self.parent = parent
		self.setWindowIcon(QIcon("resources/icons/app_icon.png"))
		self.setWindowTitle("Audio Processing - {}".format(fileName))
		self.setGeometry(300, 300, 350, 170)

		self.initUI()
		self.filePath = None
		self.audioSegment = None
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateTime)
		self.startTime = 0
		self.playing = False
		self.audio = None

	def initUI(self):
		mainLayout = QVBoxLayout()
		controlLayout = QHBoxLayout()

		controlButtonLayout = QVBoxLayout()
		self.playButton = QPushButton("Play")
		self.playButton.clicked.connect(self.playButtonOnClick)
		self.pauseButton = QPushButton("Pause")
		self.pauseButton.clicked.connect(self.pauseButtonOnClick)
		self.resumeButton = QPushButton("Resume")
		self.resumeButton.clicked.connect(self.resumeButtonOnClick)
		self.stopButton = QPushButton("Stop")
		self.stopButton.clicked.connect(self.stopButtonOnClick)
		controlButtonLayout.addWidget(self.playButton)
		controlButtonLayout.addWidget(self.pauseButton)
		controlButtonLayout.addWidget(self.resumeButton)
		controlButtonLayout.addWidget(self.stopButton)
		controlLayout.addLayout(controlButtonLayout)

		audioProgressLayout = QVBoxLayout()
		self.timeLabel = QLabel("00:00 / 00:00")
		audioProgressLayout.addWidget(self.timeLabel)

		self.timeSlider = QSlider(Qt.Horizontal)
		self.timeSlider.setMinimum(0)
		self.timeSlider.setMaximum(100)
		self.timeSlider.setValue(0)
		self.timeSlider.sliderPressed.connect(self.stopAudio)
		self.timeSlider.sliderMoved.connect(self.changeStartTime)
		self.timeSlider.valueChanged.connect(self.updateTimeLabel)
		self.timeSlider.sliderReleased.connect(self.timeSliderValueOnChanged)
		audioProgressLayout.addWidget(self.timeSlider)
		controlLayout.addLayout(audioProgressLayout)

		commandLayout = QVBoxLayout()
		self.saveButton = QPushButton("Save", self)
		self.saveButton.clicked.connect(self.onSaveButton)
		self.backButton = QPushButton("Cancel", self)
		self.backButton.clicked.connect(self.onBackButton)
		commandLayout.addWidget(self.saveButton)
		commandLayout.addWidget(self.backButton)
		controlLayout.addLayout(commandLayout)
		mainLayout.addLayout(controlLayout)

		featuresLayout = QHBoxLayout()
		self.volumeSlider = QSlider(Qt.Horizontal)
		self.volumeSlider.setMinimum(-10)
		self.volumeSlider.setMaximum(10)
		self.volumeSlider.setValue(0)
		self.volumeSlider.sliderPressed.connect(self.stopAudio)
		self.volumeSlider.sliderReleased.connect(self.volumeSliderValueOnChanged)
		featuresLayout.addWidget(QLabel("Volume:"))
		featuresLayout.addWidget(self.volumeSlider)

		self.bitrateComboBox = QComboBox(self)
		self.bitrateComboBox.addItems(["64k", "128k", "192k", "256k", "320k"])
		featuresLayout.addWidget(QLabel("Bitrate:"))
		featuresLayout.addWidget(self.bitrateComboBox)
        
		mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
		mainLayout.addLayout(featuresLayout)

		self.setLayout(mainLayout)

	def loadAudioOnStart(self, filePath):
		self.audioSegment = AudioSegment.from_file(filePath)
		self.bitrateComboBox.setCurrentText(getBitRate(filePath))
		self.filePath = filePath
		self.timeLabel.setText("00:00 / " + "{:02}:{:02}".format(*divmod(len(self.audioSegment) // 1000, 60)))
		self.pauseButton.hide()
		self.resumeButton.hide()
		self.stopButton.hide()
		self.timeSlider.setMaximum((len(self.audioSegment)))

		

	def playAudio(self, audio):
		self.audio = _play_with_simpleaudio(audio[self.startTime:])
		self.timer.start(10)

	def stopAudio(self):
		if self.audio:
			self.audio.stop()
			self.timer.stop()

	def playButtonOnClick(self):
		self.playing = True
		self.playAudio(self.audioSegment)
		self.startTime = 0 if self.startTime == None else self.startTime
		self.timeLabel.setText("00:00 / " + "{:02}:{:02}".format(*divmod(len(self.audioSegment) // 1000, 60)))
		
		self.playButton.hide()
		self.pauseButton.show()
		self.stopButton.show()

	def pauseButtonOnClick(self):
		self.audio.stop()
		self.timer.stop()
		self.pauseButton.hide()
		self.resumeButton.show()

	def resumeButtonOnClick(self):
		self.playAudio(self.audioSegment[self.startTime:])
		self.timer.start(10)
		self.resumeButton.hide()
		self.pauseButton.show()

	def stopButtonOnClick(self):
		self.stopAudio()
		self.audio = None
		self.startTime = 0
		self.playButton.show()
		self.pauseButton.hide()
		self.resumeButton.hide()
		self.stopButton.hide()

	def updateTimeLabel(self):
		self.timeLabel.setText('{:02}:{:02} / '.format(*divmod(self.startTime//1000, 60)) + "{:02}:{:02}".format(*divmod(len(self.audioSegment) // 1000, 60)))

	def updateTime(self):
		self.startTime += 10
		self.timeSlider.setValue(self.startTime)

		if not self.playing:
			self.timer.stop()

		if self.startTime >= len(self.audioSegment):
			self.playing = False
			self.timer.stop()
			self.startTime = None
			self.playButton.show()
			self.pauseButton.hide()
			self.resumeButton.hide()
			self.stopButton.hide()

	def changeStartTime(self):
		self.startTime = self.timeSlider.value()

	def timeSliderValueOnChanged(self):
		self.stopAudio()
		self.changeStartTime()
		if self.audio:
			self.playAudio(self.audioSegment)

	def volumeSliderValueOnChanged(self):
		self.audioSegment = changeVolume(self.audioSegment, self.volumeSlider.value())
		if self.audio:
			self.playAudio(self.audioSegment)

	def onSaveButton(self):
		newFilePath = saveAudioFileDialog(self, self.filePath)
        
		if newFilePath:
			saveAudio(newFilePath, self.audioSegment, self.bitrateComboBox.currentText())

	def onBackButton(self):
		self.stopAudio()
		self.hide()
		self.deleteLater()
		self.parent.show()