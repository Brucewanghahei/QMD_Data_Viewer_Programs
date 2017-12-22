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

        # For the canvas.
        self.canvas_first_step = FigureCanvas(self.ui.mplwidget_first_step.figure)
        self.canvas_first_step.setParent(self.ui.widget_first_step)
        # We need the toolbar widget for the canvas
        self.mpl_toolbar_first_step = NavigationToolbar(self.canvas_first_step, self.ui.widget_first_step)
        
        # For the canvas.
        self.canvas_second_step = FigureCanvas(self.ui.mplwidget_second_step.figure)
        self.canvas_second_step.setParent(self.ui.widget_second_step)
        # We need the toolbar widget for the canvas
        self.mpl_toolbar_second_step = NavigationToolbar(self.canvas_second_step, self.ui.widget_second_step)
        
        
        # Create the QVBoxLayout object and add the widget into the layout
        vbox = QVBoxLayout()
        # The matplotlib canvas
        vbox.addWidget(self.canvas)
        # The matplotlib toolbar
        vbox.addWidget(self.mpl_toolbar)
        self.ui.widget.setLayout(vbox)
        
        # Create the QVBoxLayout object and add the widget into the layout
        vbox_first_step = QVBoxLayout()
        # The matplotlib canvas
        vbox_first_step.addWidget(self.canvas_first_step)
        # The matplotlib toolbar
        vbox_first_step.addWidget(self.mpl_toolbar_first_step)
        self.ui.widget_first_step.setLayout(vbox_first_step)
        
        # Create the QVBoxLayout object and add the widget into the layout
        vbox_second_step = QVBoxLayout()
        # The matplotlib canvas
        vbox_second_step.addWidget(self.canvas_second_step)
        # The matplotlib toolbar
        vbox_second_step.addWidget(self.mpl_toolbar_second_step)
        self.ui.widget_second_step.setLayout(vbox_second_step)
        
        
        # Connect the mplwidget with canvas
        self.ui.mplwidget = self.canvas
        
        # Connect the mplwidget with canvas
        self.ui.mplwidget_first_step = self.canvas_first_step
        
        # Connect the mplwidget with canvas
        self.ui.mplwidget_second_step = self.canvas_second_step
        
        self.connect(self.ui.pushButton_browse, SIGNAL('clicked()'), self.Browse)
        self.connect(self.ui.pushButton_change_name, SIGNAL('clicked()'), self.Plot)
        self.connect(self.ui.pushButton_openfile, SIGNAL('clicked()'), self.OpenFile)
        self.connect(self.ui.radioButton_qmd, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.radioButton_ppms, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.radioButton_other, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.pushButton_Plot, SIGNAL('clicked()'), self.Plot_ready)
        self.connect(self.ui.pushButton_recent, SIGNAL('clicked()'), self.Open_Recent)
        self.connect(self.ui.pushButton_plot_first_step, SIGNAL('clicked()'), self.plot1)
        self.connect(self.ui.pushButton_plot_second_step, SIGNAL('clicked()'), self.plot2)
        
        self.first_round = True
        self.open_dir = ''
        self.open_files_number = 0
        self.all_info = []
        
    def Choose_type(self):
        if self.ui.radioButton_qmd.isChecked():
            self.divider = 'Collected Data'
            self.ui.lineEdit_divider.setText(self.divider)
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition1.setText('Please choose your file.')
        elif self.ui.radioButton_ppms.isChecked():
            self.divider = '[Data]'
            self.ui.lineEdit_divider.setText(self.divider)
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition1.setText('Please choose your file.')
        elif self.ui.radioButton_other.isChecked():
            self.ui.lineEdit_divider.setText('')
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition1.setText('Please enter data divider.')
            
    def Browse(self):
        self.open_recent = False
        
        if self.ui.radioButton_other.isChecked():
            if self.ui.lineEdit_divider.text() == '':
                self.ui.lineEdit_condition1.setText('Data divider cannot be empty.')
            else:
                self.divider = self.ui.lineEdit_divider.text()
                self.file_list = []
                if self.first_round == True:
                    self.prev_dir = 'C:\Google Drive'
                else:
                    self.prev_dir = self.open_dir
                    
                self.fileDir = QFileDialog.getOpenFileName(self, 'Select File to Open:', self.prev_dir)
                
                self.open_dir = ''
                
                if self.fileDir != '':
                    self.file_list = str(self.fileDir).split('/')
                    for i in range(0, len(self.file_list) - 1):
                        if i < len(self.file_list) - 1:
                            self.open_dir += self.file_list[i] + '\\'
                        elif i == len(self.file_list) - 1:
                            self.open_dir += self.file_list[i]
                    self.fileDir.replace('/', '\\')
                    self.ui.lineEdit_address.setText(self.fileDir)
                    self.ui.lineEdit_condition1.setText('Open Source File')
                else:
                    self.ui.lineEdit_address.setText('None')
                    self.ui.lineEdit_condition1.setText('Failed to Read File')
                
                self.ui.pushButton_show.setEnabled(True)
                self.ui.groupBox_labels.setEnabled(True)
                self.first_round = False
                self.file_name = self.file_list[len(self.file_list) - 1]
        else:
            self.file_list = []
            
            if self.first_round == True:
                self.prev_dir = 'C:\Google Drive'
            else:
                self.prev_dir = self.open_dir
                
            self.fileDir = QFileDialog.getOpenFileName(self, 'Select File to Open:', self.prev_dir)
            
            self.open_dir = ''
            
            if self.fileDir != '':
                self.file_list = str(self.fileDir).split('/')
                for i in range(0, len(self.file_list) - 1):
                    if i < len(self.file_list) - 1:
                        self.open_dir += self.file_list[i] + '\\'
                    elif i == len(self.file_list) - 1:
                        self.open_dir += self.file_list[i]
                self.fileDir.replace('/', '\\')
                self.ui.lineEdit_address.setText(self.fileDir)
                self.ui.lineEdit_condition1.setText('Open Source File')
            else:
                self.ui.lineEdit_address.setText('None')
                self.ui.lineEdit_condition1.setText('Failed to Read File')
            
            self.ui.pushButton_openfile.setEnabled(True)
            self.ui.groupBox_labels.setEnabled(True)
            self.first_round = False
            self.file_name = self.file_list[len(self.file_list) - 1]
        
    def OpenFile(self):
        
        # Every you click the "Open File" button, the content in the plot combox is refreshed
        self.reset_plot()
        self.reset_first_step_plot()
        self.reset_second_step_plot()
        self.ui.comboBox_x.clear()
        self.ui.comboBox_y.clear()
        self.ui.comboBox_x_2.clear()
        self.ui.comboBox_y_2.clear()
        self.ui.comboBox_y_first_step.clear()
        self.ui.comboBox_y_second_step.clear()
        self.ui.comboBox_first.clear()
        self.ui.comboBox_second.clear()
        self.ui.lineEdit_x.setText('')
        self.ui.lineEdit_y.setText('')
        self.ui.lineEdit_name.setText('')
        self.ui.lineEdit_condition2.setText('')
        
        labels = ''
        
        raw_parameters = []
        units = []
        parameters = []
        new_parameters = []
        self.data = []
        new_data = []
        first_data = []
        
        item = 0
        length = 0
        # This count is the number of the reading loops for labels. If count is over 1000, that means there's something wrong with the divider line and it helps to stop the program
        count = 0
        
        # It is false when program cannot find the line divider and runs the while loop 1000 times
        self.divider_found = True
        
        self.fileDir = self.ui.lineEdit_address.text()
        self.divider = str(self.ui.lineEdit_divider.text())
        fp = open(self.fileDir)
        while True:
            if count > 1000:
                self.ui.lineEdit_condition1.setText('Line divider is not found.')
                self.divider_found = False
                break
            line = fp.readline()
            #print 1, line
            linelist = line.split(',')
            if linelist[0].upper() == self.divider.upper() + '\n':
                break
            for i in range(0, len(linelist)):
                labels += linelist[i]
            count += 1
            
        if self.divider_found == True:
            self.ui.textEdit_labels.setText(labels)
            parameters = fp.readline().replace("\n", '')
            parameters = parameters.split(',')
            
            if self.ui.radioButton_ppms.isChecked():
                lines = fp.readline().replace("\n","")
                first_data = lines.split(",")
                for i in range(0, len(first_data)):
                    par = []
                    if first_data[i] != '':
                        par = parameters[i].split(' (')
                        if len(par) == 2:
                            units.append(par[1].replace(')', ''))
                        elif len(par) == 1:
                            units.append('1')
                        new_parameters.append(par[0])
                parameters = new_parameters
            elif self.ui.radioButton_qmd.isChecked():
                units = fp.readline().replace("\n", '')
                units = units.split(",")
            
            self.ui.comboBox_x_2.addItem('None')
            self.ui.comboBox_y_2.addItem('None')
            self.ui.comboBox_first.addItem('None')
            self.ui.comboBox_second.addItem('None')
            for i in range(0, len(parameters)):
                self.ui.comboBox_x.addItem(parameters[i])
                self.ui.comboBox_y.addItem(parameters[i])
                self.ui.comboBox_y_first_step.addItem(parameters[i])
                self.ui.comboBox_y_second_step.addItem(parameters[i])               
                self.ui.comboBox_x_2.addItem(parameters[i])
                self.ui.comboBox_y_2.addItem(parameters[i])
                self.ui.comboBox_first.addItem(parameters[i])
                self.ui.comboBox_second.addItem(parameters[i])
    
            for i in range(0, len(parameters)):
                new_data = [parameters[i], units[i], []]
                self.data.append(new_data)
    
            if self.ui.radioButton_ppms.isChecked():
                for i in range(0, len(first_data)):
                    if first_data[i] != '':
                        self.data[item][2].append(first_data[i])
                        item += 1
                
                length = item
                
            while True:
                val = []
                lines = fp.readline().replace("\n","")
                if lines == '':
                    break
                values = lines.split(',')
                for i in range(0, len(values)):
                    if values[0] != 'Measurement was Aborted':
                        if values[i] != '':
                            val.append(values[i])
                if self.ui.radioButton_ppms.isChecked():
                    if len(val) < length:
                        break
                    
                for i in range(0, len(val)):
                    self.data[i][2].append(val[i])
            
            if self.open_recent == False:   
                self.item_info = []
                self.item_info.append(self.divider)
                self.item_info.append(self.file_name)
                self.item_info.append(str(self.ui.lineEdit_address.text()))
                self.all_info.append(self.item_info)
                print self.all_info
                self.ui.comboBox_recent.addItem(self.all_info[len(self.all_info) - 1][1])
            
            self.ui.groupBox_plot.setEnabled(True)
            self.ui.groupBox_first.setEnabled(True)
            self.ui.groupBox_second.setEnabled(True)
            self.ui.lineEdit_condition2.setText('Ready to Plot.')
            self.ui.label_11.setEnabled(True)
            self.ui.comboBox_recent.setEnabled(True)
            self.ui.pushButton_recent.setEnabled(True)
            self.ui.comboBox_y_first_step.setEnabled(True)
            self.ui.pushButton_plot_first_step.setEnabled(True)
            self.ui.pushButton_plot_second_step.setEnabled(True)
            self.ui.comboBox_y_second_step.setEnabled(True)
            self.ui.label_14.setEnabled(True)
            self.ui.label_15.setEnabled(True)
    
    def Open_Recent(self):
        file_number = self.ui.comboBox_recent.currentIndex();
        
        if self.all_info[file_number][0].upper() == '[Data]'.upper():
            self.ui.radioButton_ppms.setChecked(True)
            self.ui.lineEdit_divider.setText('[Data]')
            self.divider = '[Data]' + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
        elif self.all_info[file_number][0].upper() == 'Collected Data'.upper():
            self.ui.radioButton_qmd.setChecked(True)
            self.ui.lineEdit_divider.setText('Collected Data')
            self.divider = 'Collected Data' + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
        else:
            self.ui.radioButton_other.setChecked(True)
            self.ui.lineEdit_divider.setText(self.all_info[file_number][1])
            self.divider = self.all_info[file_number][1] + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
        
        self.open_recent = True
    
    def Plot_ready(self):
        self.x_value = 0
        self.y_value = 0
        self.x_value = self.ui.comboBox_x.currentIndex()
        self.y_value = self.ui.comboBox_y.currentIndex()
        xaxis = self.data[self.x_value][0]
        xunit = self.data[self.x_value][1]
        yaxis = self.data[self.y_value][0]
        yunit = self.data[self.y_value][1]
        
        self.x2_value = 0
        self.y2_value = 0
        self.x2_value = self.ui.comboBox_x_2.currentIndex() - 1
        self.y2_value = self.ui.comboBox_y_2.currentIndex() - 1
        x2axis = self.data[self.x2_value][0]
        x2unit = self.data[self.x2_value][1]
        y2axis = self.data[self.y2_value][0]
        y2unit = self.data[self.y2_value][1]
        
        if self.x2_value == -1:
            self.ui.lineEdit_x.setText(xaxis + ' (' + xunit + ')')
            self.x_value = self.data[self.x_value][2]
        elif self.x2_value >= 0:
            self.ui.lineEdit_x.setText(xaxis + '/' + x2axis + ' (' + xunit + '/' + x2unit + ')')
            if self.ui.radioButton_x_divide.isChecked():
                self.x_value = numpy.array(self.data[self.x_value][2], dtype = 'float') / numpy.array(self.data[self.x2_value][2], dtype = 'float')
            elif self.ui.radioButton_x_multiply.isChecked():
                self.x_value = numpy.array(self.data[self.x_value][2], dtype = 'float') * numpy.array(self.data[self.x2_value][2], dtype = 'float')
            elif self.ui.radioButton_x_plus.isChecked():
                self.x_value = numpy.array(self.data[self.x_value][2], dtype = 'float') + numpy.array(self.data[self.x2_value][2], dtype = 'float')
            elif self.ui.radioButton_x_minus.isChecked():
                self.x_value = numpy.array(self.data[self.x_value][2], dtype = 'float') - numpy.array(self.data[self.x2_value][2], dtype = 'float')
        if self.ui.checkBox_x_value.isChecked():
            self.x_value = numpy.absolute(self.x_value)
            
        if self.y2_value == -1:
            self.ui.lineEdit_y.setText(yaxis + ' (' + yunit + ')')
            self.y_value = self.data[self.y_value][2]
        elif self.y2_value >= 0:
            self.ui.lineEdit_y.setText(yaxis + '/' + y2axis + ' (' + yunit + '/' + y2unit + ')')
            if self.ui.radioButton_y_divide.isChecked():
                self.y_value = numpy.array(self.data[self.y_value][2], dtype = 'float') / numpy.array(self.data[self.y2_value][2], dtype = 'float')
            elif self.ui.radioButton_x_multiply.isChecked():
                self.y_value = numpy.array(self.data[self.y_value][2], dtype = 'float') * numpy.array(self.data[self.y2_value][2], dtype = 'float')
            elif self.ui.radioButton_x_plus.isChecked():
                self.y_value = numpy.array(self.data[self.y_value][2], dtype = 'float') + numpy.array(self.data[self.y2_value][2], dtype = 'float')
            elif self.ui.radioButton_x_minus.isChecked():
                self.y_value = numpy.array(self.data[self.y_value][2], dtype = 'float') - numpy.array(self.data[self.y2_value][2], dtype = 'float')
        if self.ui.checkBox_y_value.isChecked():
            self.y_value = numpy.absolute(self.y_value)
            
        if self.x2_value == -1 and self.y2_value == -1:
            self.ui.lineEdit_name.setText(yaxis + ' vs. ' + xaxis)
        elif self.x2_value >= 0 and self.y2_value == -1:
            self.ui.lineEdit_name.setText(yaxis + ' vs. ' + xaxis + '/' + x2axis)
        elif self.x2_value == -1 and self.y2_value >= 0:
            self.ui.lineEdit_name.setText(yaxis + '/' + y2axis + ' vs. ' + xaxis)
        else:
            self.ui.lineEdit_name.setText(yaxis + '/' + y2axis + ' vs. ' + xaxis + '/' + x2axis)
        
        self.ui.pushButton_change_name.setEnabled(True)
        self.Plot()
        
    def Plot(self):
        self.reset_plot()
        self.axes.plot(self.x_value, self.y_value, marker = '.', linestyle = ':')
        self.axes.grid()
        self.axes.set_title(self.ui.lineEdit_name.text())
        self.axes.set_xlabel(self.ui.lineEdit_x.text())
        self.axes.set_ylabel(self.ui.lineEdit_y.text())
        self.ui.mplwidget.draw()
        
        self.ui.lineEdit_condition2.setText('Plot successfully.')
        
    
    def plot1(self):
        y_value1 = self.ui.comboBox_y_first_step.currentIndex()
        y_value2 = self.ui.comboBox_first.currentIndex() - 1
        y_axis1 = self.data[y_value1][0]
        y_axis2 = self.data[y_value2][0]
        y_unit1 = self.data[y_value1][1]
        y_unit2 = self.data[y_value2][1]
        yv1 = self.data[y_value1][2]
        yv2 = self.data[y_value2][2]
        xv = []
        
        item = 0
        for i in range(0, len(yv1)):
            xv.append(item)
            item += 1
        
        if y_value2 == -1:
            y_value = yv1
            y_name = y_axis1 + ' (' + y_unit1 + ')'
            name = y_axis1 + ' Steps'
        elif y_value2 >= 0:
            if self.ui.radioButton_first_divide.isChecked():
                y_value = numpy.array(self.data[y_value1][2], dtype = 'float') / numpy.array(self.data[y_value2][2], dtype = 'float')
                y_name = y_axis1 + ' / ' + y_axis2 + ' (' + y_unit1 + ' / ' + y_unit2 + ')'
                name = y_axis1 + ' / ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_first_multiply.isChecked():
                y_value = numpy.array(self.data[y_value1][2], dtype = 'float') * numpy.array(self.data[y_value2][2], dtype = 'float')
                y_name = y_axis1 + ' * ' + y_axis2 + ' (' + y_unit1 + ' * ' + y_unit2 + ')'
                name = y_axis1 + ' * ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_first_plus.isChecked():
                y_value = numpy.array(self.data[y_value1][2], dtype = 'float') + numpy.array(self.data[y_value2][2], dtype = 'float')
                y_name = y_axis1 + ' + ' + y_axis2 + ' (' + y_unit1 + ' + ' + y_unit2 + ')'
                name = y_axis1 + ' + ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_first_minus.isChecked():
                y_value = numpy.array(self.data[y_value1][2], dtype = 'float') - numpy.array(self.data[y_value2][2], dtype = 'float')
                y_name = y_axis1 + ' - ' + y_axis2 + ' (' + y_unit1 + ' - ' + y_unit2 + ')'
                name = y_axis1 + ' - ' + y_axis2 + ' Steps'
        if self.ui.checkBox_first.isChecked():
            y_value = numpy.absolute(y_value)      
                
        self.reset_first_step_plot()
        self.axes_first_step.plot(xv, y_value, marker = '.', linestyle = ':')
        self.axes_first_step.grid()
        self.axes_first_step.set_title(name)
        self.axes_first_step.set_xlabel('Unit Step (1)')
        self.axes_first_step.set_ylabel(y_name)
        self.ui.mplwidget_first_step.draw()
 
    def plot2(self):
        y_value1 = self.ui.comboBox_y_second_step.currentIndex()
        y_value2 = self.ui.comboBox_second.currentIndex() - 1
        y_axis1 = self.data[y_value1][0]
        y_axis2 = self.data[y_value2][0]
        y_unit1 = self.data[y_value1][1]
        y_unit2 = self.data[y_value2][1]
        yv1 = self.data[y_value1][2]
        yv2 = self.data[y_value2][2]
        xv = []
        item = 0
        for i in range(0, len(yv1)):
            xv.append(item)
            item += 1
        
        if y_value2 == -1:
            y_value = yv1
            y_name = y_axis1 + ' (' + y_unit1 + ')'
            name = y_axis1 + ' Steps'
        elif y_value2 >= 0:
            if self.ui.radioButton_second_divide.isChecked():
                y_value = numpy.array(self.data[y_value1][2], dtype = 'float') / numpy.array(self.data[y_value2][2], dtype = 'float')
                y_name = y_axis1 + ' / ' + y_axis2 + ' (' + y_unit1 + ' / ' + y_unit2 + ')'
                name = y_axis1 + ' / ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_second_multiply.isChecked():
                y_value = numpy.array(self.data[y_value1][2], dtype = 'float') * numpy.array(self.data[y_value2][2], dtype = 'float')
                y_name = y_axis1 + ' * ' + y_axis2 + ' (' + y_unit1 + ' * ' + y_unit2 + ')'
                name = y_axis1 + ' * ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_second_plus.isChecked():
                y_value = numpy.array(self.data[y_value1][2], dtype = 'float') + numpy.array(self.data[y_value2][2], dtype = 'float')
                y_name = y_axis1 + ' + ' + y_axis2 + ' (' + y_unit1 + ' + ' + y_unit2 + ')'
                name = y_axis1 + ' + ' + y_axis2 + ' Steps'
            elif self.ui.radioButton_second_minus.isChecked():
                y_value = numpy.array(self.data[y_value1][2], dtype = 'float') - numpy.array(self.data[y_value2][2], dtype = 'float')
                y_name = y_axis1 + ' - ' + y_axis2 + ' (' + y_unit1 + ' - ' + y_unit2 + ')'
                name = y_axis1 + ' - ' + y_axis2 + ' Steps'
        if self.ui.checkBox_second.isChecked():
            y_value = numpy.absolute(y_value)    
        
        self.reset_second_step_plot()
        self.axes_second_step.plot(xv, y_value, marker = '.', linestyle = ':')
        self.axes_second_step.grid()
        self.axes_second_step.set_title(name)
        self.axes_second_step.set_xlabel('Unit Step (1)')
        self.axes_second_step.set_ylabel(y_name)
        self.ui.mplwidget_second_step.draw()   
    
    def reset_plot(self):
        self.ui.mplwidget.figure.clear()        
        self.axes = self.ui.mplwidget.figure.add_subplot(111)

    def reset_first_step_plot(self):
        self.ui.mplwidget_first_step.figure.clear()        
        self.axes_first_step = self.ui.mplwidget_first_step.figure.add_subplot(111)
        
    def reset_second_step_plot(self):
        self.ui.mplwidget_second_step.figure.clear()        
        self.axes_second_step = self.ui.mplwidget_second_step.figure.add_subplot(111)
        
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
        
