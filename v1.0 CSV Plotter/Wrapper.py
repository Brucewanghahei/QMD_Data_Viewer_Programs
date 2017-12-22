# Import numpy library
import numpy

import os

import sys

from Tkinter import *
from tkFileDialog import *
from tkMessageBox import showerror

# Import pylab library
# It contains some functions necessary to create some of the functions in the use of the plots
from pylab import *

# Adding navigation toolbar to the figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

# Import the PyQt4 modules for all the commands that control the GUI.
# Importing as from "Module" import 
from PyQt4.QtCore import *
from PyQt4.QtGui import *

linelist =[]

# This is very important because it imports the GUI created earlier using Qt Designer
# To import the GUI from another python file, it is very somple. Just following the following steps:
# 1. Creat an empty file called __init__.py in the same directory as the GUI file
# 2. If the GUI file and __init__.py file are in the same directory as this file, just type "from .GUIfilename import classname"
# 3. If the GUI file and __init__.py file are in the sub file of this file, then type "from subfilename.GUIfilename.GUIfilename import classname"
# classname is the name of the class in the GUI file, usually it should be 'Ui_MainWindow'

from Sub_Scripts.GUI import Ui_MainWindow

# This class controls all the operations of the GUI. This is the main class that contains all the functions that control the GUI.
class MyForm(QMainWindow):
    
    # The __init__ function is what everything the user wants to be initialized when the class is called.
    # Here we shall define the tring functions to corresponding variables.
    # The 'self' variable means that the function is part of the class and can be called inside and outside the class.
    def __init__(self, parent = None):
        
        # Standard GUI code
        QWidget.__init__(self, parent)
        
        # All the GUI data and widgets in the Ui_MainWindow() class is defined to "self.ui"
        # Thus to do anything on the GUI, the commands must go through this variable
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # For the canvas.
        self.canvas = FigureCanvas(self.ui.mplwidget.figure)
        self.canvas.setParent(self.ui.widget)
        # We need the toolbar widget for the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.ui.widget)
        
        # Create the QVBoxLayout object and add the widget into the layout
        vbox = QVBoxLayout()
        # The matplotlib canvas
        vbox.addWidget(self.canvas)
        # The matplotlib toolbar
        vbox.addWidget(self.mpl_toolbar)
        self.ui.widget.setLayout(vbox)
        
        # Connect the mplwidget with canvas
        self.ui.mplwidget = self.canvas
        
        self.connect(self.ui.pushButton_browse, SIGNAL('clicked()'), self.Browse)
        self.connect(self.ui.pushButton_plot, SIGNAL('clicked()'), self.Plot)
        self.connect(self.ui.pushButton_show, SIGNAL('clicked()'), self.Show)
        
    def Browse(self):
        self.prev_dir = 'C:\Users\QMDlab\Desktop'
        self.fileDir = QFileDialog.getOpenFileName(self, 'Select File to Open:', 'C:\Users\QMDlab\Desktop')
        
        if self.fileDir != '':
            self.fileDir.replace('/', '\\')
            self.ui.lineEdit_address.setText(self.fileDir)
            self.ui.lineEdit_condition1.setText('Open Source File')
        else:
            self.ui.lineEdit_address.setText('None')
            self.ui.lineEdit_condition1.setText('Failed to Read File')
        
        self.ui.groupBox_labels.setEnabled(True)
        
    def Show(self):
        labels = ''
        row = 1
        raw_parameters = []
        parameters = []
        fp = open(self.fileDir)
        while True:
            line = fp.readline()
            #print 1, line
            linelist = line.split(',')
            if linelist[0] == 'Collected Data\n':
                break
            labels += linelist[0]
            row += 1
        self.ui.textEdit_labels.setText(labels)
        #fp.close()
        
        #fp = open(self.fileDir)
        

        """
        raw_parameters = lines[row].split(',')
        for i in range(0, len(raw_parameters) - 1):
            parameters.append(raw_parameters[i])
        parameters.append(raw_parameters[len(raw_parameters) - 1].strip())
        for i in range(0, len(parameters)):
            self.ui.comboBox_x.addItem(parameters[i])
            self.ui.comboBox_y.addItem(parameters[i])
        #fp.close()
        list_bundle = [[] for i in range(0, len(parameters))]
        """

        #Read Parameters
        parameters = fp.readline().replace("\n", '')
        #print 'parameters', parameters
        parameters = parameters.split(',')

        for i in range(0, len(parameters)):
            self.ui.comboBox_x.addItem(parameters[i])
            self.ui.comboBox_y.addItem(parameters[i])

        #Read Units
        units = fp.readline().replace("\n", '')
        #print 'units', units
        units = units.split(",")

        
        self.data = []

        for i in range(0, len(parameters)):
            new_data = [parameters[i], units[i], []]
            self.data.append(new_data)

        
        #fp = open(self.fileDir)
        while True:
            #parameters = []
            #fp = open(self.fileDir)
            lines = fp.readline().replace("\n","")
            #print "lines", lines
            if lines == '':
                break
            
            values = lines.split(',')

            for i in range(0, len(values)):
                self.data[i][2].append(values[i])
            #row += 1
            
        #print data


            ###
            #for i in range(0, len(raw_parameters) - 1):
            #    parameters.append(raw_parameters[i])
            #parameters.append(raw_parameters[len(raw_parameters) - 1].strip())
            #for i in range(0, len(parameters)):
            #    list_bundle[i].append(parameters[i])
            ###
            
            #fp.close()
        self.ui.groupBox_plot.setEnabled(True)
        self.ui.lineEdit_condition2.setText('Ready to Plot.')
        
    def Plot(self):
        x_value = self.ui.comboBox_x.currentIndex()
        y_value = self.ui.comboBox_y.currentIndex()
        self.reset_plot()
        self.axes.plot(self.data[x_value][2], self.data[y_value][2], marker = '.', linestyle = ':')
        self.axes.set_title(self.data[x_value][0] + ' vs. ' + self.data[y_value][0])
        self.axes.set_xlabel(self.data[x_value][0] + ' (' + self.data[x_value][1] + ')')
        self.axes.set_ylabel(self.data[y_value][0] + ' (' + self.data[y_value][1] + ')')
        self.ui.mplwidget.draw()
        
        self.ui.lineEdit_condition2.setText('Plot successfully.')
    
    def reset_plot(self):
        self.ui.mplwidget.figure.clear()        
        self.axes = self.ui.mplwidget.figure.add_subplot(111)
        
    def closeEvent(self, question):
        quit_msg = "Do you want to quit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        # If your answer is "yes", then quit
        if reply == QMessageBox.Yes:
            question.accept()
        # If your answer is "no", then get back
        else:
            question.ignore()

if __name__ == "__main__":
    # To open the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()
    
    # It shows the GUI
    myapp.show()
    
    # Exit the GUI when "x" button is clicked
    sys.exit(app.exec_())  
        
