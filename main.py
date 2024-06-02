import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.utils.audio_utils import configure_pydub

def loadStylesheet(path):
    with open(path, "r") as f:
        return f.read()

def main():
	configure_pydub()
	app = QApplication(sys.argv)
	app.setStyleSheet(loadStylesheet("resources/styles/style.qss"))

	mainWindow = MainWindow()
	mainWindow.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()