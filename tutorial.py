# -*- coding: utf-8 -*-
import threading
from mic_vad_streaming import VADAudio
from PyQt5 import QtCore, QtGui, QtWidgets
import argparse
class VADThread(threading.Thread):
    def __init__(self, args, callback):
        threading.Thread.__init__(self)
        self.args = args
        self.callback = callback

    def run(self):
        # Initialize VADAudio with callback
        vad_audio = VADAudio(aggressiveness=self.args.vad_aggressiveness,
                             device=self.args.device,
                             input_rate=self.args.rate,
                             file=self.args.file,
                             callback=self.callback)
        frames = vad_audio.vad_collector()

        for frame in frames:
            # Process the audio frame or trigger events as needed
            # You may want to use signals or other mechanisms to communicate with the main GUI thread
            pass

class ASLDisplay(object):
    def __init__(self, photo_label):
        self.photo_label = photo_label
        base_path = "Media/Alphabets/"
        # Set up a list of ASL files for each word in the sentence
        words = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
        self.asl_files = [base_path + word + '.jpg' for word in words.split()]
        self.current_word_index = 0

        # Set up timer to change images every second
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)

        # Initial display
        self.update_display()

    def update_display(self):
        if self.current_word_index < len(self.asl_files):
            # Load and display the current ASL image or video
            asl_file = self.asl_files[self.current_word_index]
            pixmap = QtGui.QPixmap(asl_file)
            self.photo_label.setPixmap(pixmap)

            # Move to the next word
            self.current_word_index += 1
        else:
            # Reset the display for the next sentence
            self.current_word_index = 0

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, args):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        
        
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(100, 10, 651, 481))
        self.photo.setText("")
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")

        # Create an instance of ASLDisplay and pass the QLabel
        self.asl_display = ASLDisplay(self.photo)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.vad_thread = VADThread(args=args, callback=self.handle_vad_event)
        self.vad_thread.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ASL Display App"))

    def handle_vad_event(self, speech_detected):
        # This function will be called when speech is detected or ends
        if speech_detected:
            print("Speech Detected")
            # Trigger actions in your PyQt application (e.g., change ASL images)
        else:
            print("Speech Ended")
            # Trigger actions for the end of speech (if needed)
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    parser = argparse.ArgumentParser(description="Your script description")
    parser.add_argument('-m', '--model', required=True, help="Path to the model (.pbmm)")
    parser.add_argument('-s', '--scorer', required=True, help="Path to the scorer file")
    # Add other arguments as needed
    args = parser.parse_args()
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, args)
    MainWindow.show()
    sys.exit(app.exec_())
