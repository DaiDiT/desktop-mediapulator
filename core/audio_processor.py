from pydub.utils import mediainfo
from ui.utils.file_utils import getFileNameAndExtension

import os

def getBitRate(filePath):
	audioInfo = mediainfo(filePath)
	bitrate = audioInfo['bit_rate']

	return str(int(bitrate)//1000) + 'k'

def changeVolume(audioSegment, val):
	audioSegment = audioSegment + val

	return audioSegment

def saveAudio(filePath, audioSegment, bitrate):
	fileType = getFileNameAndExtension(filePath)[1]

	audioSegment.export(filePath, format=fileType[1:], bitrate=bitrate)