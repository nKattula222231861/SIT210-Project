#python Project.py
#Imports, GPIO is for the raspberry Pi Pins and the QT imports are for the GUI
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

#Sets up GUI window Class
class Window(QMainWindow):
    
    #Initialises Window Object
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(610, 340, 600, 400)
        self.setWindowTitle("Control Hub")
        self.initUi()
    
    #Initialises GUI
    def initUi(self): 
        #Top text box (Tells user to insert battery and press button)
        self.instructText = QtWidgets.QLabel(self)
        self.instructText.setText("Please insert battery and select size to test.")
        self.instructText.adjustSize()
        self.instructText.move(125, 50)
    
        #AA Button
        self.bAA = QtWidgets.QPushButton(self)
        self.bAA.setText("AA")
        self.bAA.move(100, 100)
        self.bAA.clicked.connect(self.pressAA)
            
        #AAA Button
        self.bAAA = QtWidgets.QPushButton(self)
        self.bAAA.setText("AAA")
        self.bAAA.move(400, 100)
        self.bAAA.clicked.connect(self.pressAAA)
    
        #Main info text. Writes out variables to user. Consists of 3 label "pairs", one stating what the variable is and the other representing the actual data
        #Type Text
        self.typeText = QtWidgets.QLabel(self)
        self.typeText.setText("Type: ")
        self.typeText.move(200, 150)
        self.typeActual = QtWidgets.QLabel(self)
        self.typeActual.setText("N/A")
        self.typeActual.move(325, 150)
        
        #Voltage Text
        self.voltageText = QtWidgets.QLabel(self)
        self.voltageText.setText("Voltage: ")
        self.voltageText.move(200, 200)
        self.voltageActual = QtWidgets.QLabel(self)
        self.voltageActual.setText("N/A")
        self.voltageActual.move(325, 200)
        
        #Status Text
        self.statusText = QtWidgets.QLabel(self)
        self.statusText.setText("Status: ")
        self.statusText.move(200, 250)
        self.statusActual = QtWidgets.QLabel(self)
        self.statusActual.setText("N/A")
        self.statusActual.move(325, 250)
        
        #Exit Button
        self.bExit = QtWidgets.QPushButton(self)
        self.bExit.setText("Push To Exit")
        self.bExit.move(250, 300)
        self.bExit.clicked.connect(self.pressExit)
        
    #Reacts when the AA button is pressed
    def pressAA(self):
        #Sends a 1 bit to the arduino
        self.typeActual.setText("AA")

    #Reacts when the AAA button is pressed
    def pressAAA(self):
        #Sends a 2 Bit to the arduino
        self.typeActual.setText("AAA")
        
    #Reacts when the exit button is pressed
    def pressExit(self):
        GPIO.cleanup()
        self.close()

#Method to construct a window object
def CreateWindow():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

#Sets up the GPIO I2C pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


#Calls Window Creation Method
CreateWindow()

