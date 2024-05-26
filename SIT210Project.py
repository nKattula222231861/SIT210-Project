#python Project.py
#Imports, GPIO is for the raspberry Pi Pins and the QT imports are for the GUI. Smbus is for I2C. Finally time is so the program can wait for i2c messages
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from smbus2 import SMBus
import sys
import time

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
        #Changes text to show the input
        self.typeActual.setText("AA")
        self.statusActual.setText("Measuring...")
        self.voltageActual.setText("...")
        
        #Sends an 1 byte over i2c to the arduno
        with SMBus(1) as bus:
                bus.write_byte_data(9, 0, 1)
                
                #Then waits to read 4 bytes of data, which is the float representing the voltage measured by the arduino. Converts the sent list to a string and then to a float
                time.sleep(0.1)
                listAA = bus.read_i2c_block_data(9, 0, 4)
                stringAA = ''.join(chr(x) for x in listAA)
                floatAA = float(stringAA.strip('\x00'))
                                                
                #Sets voltage to it's calculated value using string
                self.voltageActual.setText(str(floatAA))
                
                #Sets status based off voltage float
                if floatAA < 1.8 and floatAA > 1.65:
                        self.statusActual.setText("Near Fully Charged")
                        self.statusActual.adjustSize()
                        
                elif floatAA < 1.65 and floatAA > 1.5:
                        self.statusActual.setText("Halfway Charged")
                        self.statusActual.adjustSize()
                        
                elif floatAA < 1.5 and floatAA > 1.3:
                        self.statusActual.setText("Battery Low")
                        self.statusActual.adjustSize()
                else:
                        self.statusActual.setText("Battery Invalid/Dead")
                        self.statusActual.adjustSize()
                
    #Reacts when the AAA button is pressed
    def pressAAA(self):
        #Changes UI to represent input
        self.typeActual.setText("AAA")
        self.statusActual.setText("Measuring...")
        self.voltageActual.setText("...")
        
        #Sends an 2 byte over i2c to the arduno
        with SMBus(1) as bus:
                bus.write_byte_data(9, 0, 2)
                
                #Then waits to read 4 bytes of data, which is the float representing the voltage measured by the arduino. Converts the sent list to a string and then to a float
                time.sleep(0.1)
                listAAA = bus.read_i2c_block_data(9, 0, 4)
                stringAAA = ''.join(chr(x) for x in listAAA)
                floatAAA = float(stringAAA.strip('\x00'))
                                                
                #Sets voltage to it's calculated value using string
                self.voltageActual.setText(str(floatAAA))
                
                #Sets status based off voltage float
                if floatAAA < 1.8 and floatAAA > 1.65:
                        self.statusActual.setText("Near Fully Charged")
                        self.statusActual.adjustSize()
                        
                elif floatAAA < 1.65 and floatAAA > 1.5:
                        self.statusActual.setText("Halfway Charged")
                        self.statusActual.adjustSize()
                        
                elif floatAAA < 1.5 and floatAAA > 1.3:
                        self.statusActual.setText("Battery Low")
                        self.statusActual.adjustSize()
                else:
                        self.statusActual.setText("Battery Invalid/Dead")
                        self.statusActual.adjustSize()
                        
                        
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

#Sets up the GPIO pins
GPIO.setwarnings(False)

#Calls Window Creation Method
CreateWindow()

