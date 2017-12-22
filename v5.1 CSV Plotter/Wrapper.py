# Import numpy library
import numpy

import datetime, time

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
        self.connect(self.ui.radioButton_frontpanel, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.radioButton_zbridge, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.radioButton_compressor, SIGNAL('clicked()'), self.Choose_type)
        self.connect(self.ui.pushButton_Plot, SIGNAL('clicked()'), self.Plot_ready)
        self.connect(self.ui.pushButton_recent, SIGNAL('clicked()'), self.Open_Recent)
        self.connect(self.ui.pushButton_plot_first_step, SIGNAL('clicked()'), self.plot1)
        self.connect(self.ui.pushButton_plot_second_step, SIGNAL('clicked()'), self.plot2)
        self.connect(self.ui.pushButton_find, SIGNAL('clicked()'), self.Find)
        self.connect(self.ui.pushButton_modify, SIGNAL('clicked()'), self.Modify)
        self.connect(self.ui.pushButton_return, SIGNAL('clicked()'), self.Return)

        
        self.first_round = True
        self.open_dir = ''
        self.open_files_number = 0
        self.all_info = []
        
    def Choose_type(self):
        if self.ui.radioButton_qmd.isChecked():
            self.divider = 'Collected Data'
            self.ui.lineEdit_divider.setText(self.divider)
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
        elif self.ui.radioButton_ppms.isChecked():
            self.divider = '[Data]'
            self.ui.lineEdit_divider.setText(self.divider)
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
        elif self.ui.radioButton_frontpanel.isChecked():
            self.divider = 'frontpanel'
            self.ui.lineEdit_divider.setText('None')
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
        elif self.ui.radioButton_zbridge.isChecked():
            self.divider = '#'
            self.ui.lineEdit_divider.setText(self.divider)
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
        elif self.ui.radioButton_compressor.isChecked():
            self.divider = 'compressor'
            self.ui.lineEdit_divider.setText('None')
            self.ui.pushButton_browse.setEnabled(True)
            self.ui.lineEdit_condition.setText('Please choose your file.')
            
    def Browse(self):
        self.open_recent = False
        
        prev_dir = os.getcwd()
        if self.ui.lineEdit_address.text() == '' or self.ui.lineEdit_address.text() == 'None':
            fileDir = QFileDialog.getOpenFileName(self, 'Select Folder to Save', prev_dir)
        else:
            fileDir = QFileDialog.getOpenFileName(self, 'Select Folder to Save', self.ui.lineEdit_address.text())
        if fileDir != '':
            open_dir = ''
            file_list = str(fileDir).split('/')
            for i in range(0, len(file_list) - 1):
                if i < len(file_list) - 1:
                    open_dir += file_list[i] + '\\'
                elif i == len(file_list) - 1:
                    open_dir += file_list[i]
            fileDir.replace('/', '\\')
            self.ui.lineEdit_address.setText(fileDir)
            
            self.ui.pushButton_openfile.setEnabled(True)
            self.ui.groupBox_labels.setEnabled(True)
            self.first_round = False
            filedir = str(fileDir).split('\\')
            self.file_name = filedir[len(filedir) - 1]
        else:
            self.ui.lineEdit_address.setText('None')
            self.ui.lineEdit_condition.setText('Failed to Read File')
        
    def OpenFile(self):
        
        # Every you click the "Open File" button, the content in the plot combox is refreshed
        self.reset_plot()
        self.ui.mplwidget.draw()
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
        self.ui.lineEdit_condition.setText('')
        self.ui.lineEdit_minute.setText('')
        self.ui.lineEdit_date.setText('')
        
        labels = ''
        
        raw_parameters = []
        units = []
        parameters = []
        new_parameters = []
        self.data = []
        new_data = []
        first_data = []
        self.date_time = []
        temp_parameters = []
        
        item = 0
        z_item = 0
        length = 0
        # This count is the number of the reading loops for labels. If count is over 1000, that means there's something wrong with the divider line and it helps to stop the program
        count = 0
        
        # It is false when program cannot find the line divider and runs the while loop 1000 times
        self.divider_found = True
        
        self.fileDir = self.ui.lineEdit_address.text()
        self.divider = str(self.ui.lineEdit_divider.text())
        fp = open(self.fileDir)
        if self.ui.radioButton_frontpanel.isChecked():
            labels = 'None'
        elif self.ui.radioButton_compressor.isChecked():
            labels = fp.readline()
        elif self.ui.radioButton_zbridge.isChecked():
            line = fp.readline()
            labels += line
            line = fp.readline()
            labels += line
            line = fp.readline()
            linelist = line.split(':')
            namelist = linelist[1].split('\t')
            labels += '        ' + linelist[0] + ':\n'
            for i in range(0, len(namelist) - 1):
                labels += '\t' + str(i) + '. ' + namelist[i] + '\n'
            labels += '\t' + str(len(namelist) - 1) + '. ' + namelist[len(namelist) - 1] + '\n'
            line = fp.readline()
            linelist = line.split(':')
            namelist = linelist[1].split('\t')
            labels += '        ' + linelist[0] + ':\n'
            for i in range(0, len(namelist) - 1):
                labels += '\t' + str(i) + '. ' + namelist[i] + '\n'
            labels += '\t' + str(len(namelist) - 1) + '. ' + namelist[len(namelist) - 1] + '\n'
            line = fp.readline()
            linelist = line.split(':')
            namelist = linelist[1].split('\t')
            labels += linelist[0] + ':\n'
            for i in range(0, len(namelist)):
                labels += '\t' + str(i) + '. ' + namelist[i] + '\n'
            line = fp.readline()
        else:
            while True:
                if count > 1000:
                    self.ui.lineEdit_condition.setText('Line divider is not found.')
                    self.divider_found = False
                    break
                line = fp.readline()
                linelist = line.split(',')
                if linelist[0].upper() == self.divider.upper() + '\n':
                    break
                for i in range(0, len(linelist)):
                    labels += linelist[i]
                count += 1
            
        if self.divider_found == True:
            self.ui.textEdit_labels.setText(labels)
            parameters = fp.readline().replace("\n", '')
            if self.ui.radioButton_frontpanel.isChecked():
                parameters = parameters.split('\t')
                for i in range(0, len(parameters)):
                    if parameters[i] == 'P1':
                        parameters[i] = 'Probe Line (P1)'
                    elif parameters[i] == 'P2':
                        parameters[i] = ' OVC Line (P2)'
                    elif parameters[i] == 'P3':
                        parameters[i] = 'IVC/Aux Port Line (P3)'
                    elif parameters[i] == 'P4':
                        parameters[i] = 'Turbo-to-S3 (P4)'
                    elif parameters[i] == 'P5':
                        parameters[i] = 'S3-to-traps (P5)'
                    elif parameters[i] == 'P6':
                        parameters[i] = '4He Dump (P6)'
                    elif parameters[i] == 'P7':
                        parameters[i] = '3He Dump (P7)'
                    elif parameters[i] == 'MG2':
                        parameters[i] = 'OVC Maxigauge (MG2)'
                    elif parameters[i] == 'MG3':
                        parameters[i] = 'Still Maxiguage (MG3)'
                    elif parameters[i] == 'MG4':
                        parameters[i] = 'IVC Maxiguage (MG4)'
                    elif parameters[i] == 'MG5':
                        parameters[i] = 'Probe Maxiguage (MG5)'
                    elif parameters[i] == 'P_low':
                        parameters[i] = 'P_high'
                    elif parameters[i] == 'P_high':
                        parameters[i] = 'P_low'
            elif self.ui.radioButton_zbridge.isChecked():
                parameters = parameters.split('\t')
                new_p = []
                new_p.append('Time')
                new_p.extend(parameters[12:22])
                parameters = new_p
            elif self.ui.radioButton_compressor.isChecked():
                parameters = parameters.split('\t')
            else:
                temp_parameters = parameters.split(',')
                if temp_parameters[0] == 'Date':
                    parameters = temp_parameters[1:]
                else:
                    parameters = temp_parameters
            
            # The following is for the units
            if self.ui.radioButton_ppms.isChecked():
                lines = fp.readline().replace("\n", "")
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
                if temp_parameters[0] == 'Date':
                    units = units[1:]
            elif self.ui.radioButton_frontpanel.isChecked():
                for i in range(0, len(parameters)):
                    units.append('')
            elif self.ui.radioButton_zbridge.isChecked():
                units.append('hour')
                for i in range(1, len(parameters)):
                    units.append('K')
            elif self.ui.radioButton_compressor.isChecked():
                units.append('')
                new_parameters.append(parameters[0])
                for i in range(1, len(parameters)):
                    par = []
                    if parameters[i] != "Errors":
                        par = parameters[i].split('(')
                        if par[1].replace(')', '') == 's':
                            units.append('h')
                        else:
                            units.append(par[1].replace(')', ''))
                        new_parameters.append(par[0])
                    else:
                        units.append("")
                        new_parameters.append(parameters[i])
                parameters = new_parameters
            
            self.ui.comboBox_x_2.addItem('None')
            self.ui.comboBox_y_2.addItem('None')
            self.ui.comboBox_first.addItem('None')
            self.ui.comboBox_second.addItem('None')
            if self.ui.radioButton_compressor.isChecked():
                for i in range(1, len(parameters)):
                    self.ui.comboBox_x.addItem(parameters[i])
                    self.ui.comboBox_y.addItem(parameters[i])
                    self.ui.comboBox_y_first_step.addItem(parameters[i])
                    self.ui.comboBox_y_second_step.addItem(parameters[i])               
                    self.ui.comboBox_x_2.addItem(parameters[i])
                    self.ui.comboBox_y_2.addItem(parameters[i])
                    self.ui.comboBox_first.addItem(parameters[i])
                    self.ui.comboBox_second.addItem(parameters[i])
            elif self.ui.radioButton_zbridge.isChecked():
                self.ui.comboBox_x.addItem(parameters[0])
                for i in range(0, len(parameters)):
                    self.ui.comboBox_y_first_step.addItem(parameters[i])
                    self.ui.comboBox_y_second_step.addItem(parameters[i])               
                    self.ui.comboBox_first.addItem(parameters[i])
                    self.ui.comboBox_second.addItem(parameters[i])
            else:
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
                new_data = [parameters[i], units[i], [], []]
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
                if self.ui.radioButton_frontpanel.isChecked() or self.ui.radioButton_compressor.isChecked() or self.ui.radioButton_zbridge.isChecked():
                    values = lines.split('\t')
                else:
                    values = lines.split(',')
                for i in range(0, len(values)):
                    if values[0] != 'Measurement was Aborted':
                        if values[i] != '':
                            val.append(values[i])
                if self.ui.radioButton_ppms.isChecked():
                    if len(val) < length:
                        break
                elif self.ui.radioButton_frontpanel.isChecked():
                    date_info = val[0].split(' ')
                    weekday = datetime.datetime.strptime(date_info[0], '%Y-%m-%d').strftime('%a')
                    date = date_info[0] + ' ' + weekday + ' ' + date_info[1]
                    self.data[0][3].append(date)
                    self.data[0][3].append(self.convert_time(val[0]))
                    for i in range(0, len(val) - 1):
                        self.data[i][2].append(val[i]) #+ 1])
                
                elif self.ui.radioButton_zbridge.isChecked():
                    date_info = val[0].split(' ')
                    weekday = datetime.datetime.strptime(date_info[0], '%Y-%m-%d').strftime('%a')
                    date = date_info[0] + ' ' + weekday + ' ' + date_info[1]
                    self.date_time.append(date)
                    self.data[0][2].append(val[1])
                    for i in range(1, len(parameters)):
                        if val[i + 11] == '-Inf':
                            self.data[i][3].append(z_item)
                        else:
                            self.data[i][2].append(val[i + 11])
                    
                elif self.ui.radioButton_qmd.isChecked():
                    if temp_parameters[0] == 'Date':
                        date_info = val[0].split(' ')
                        weekday = datetime.datetime.strptime(date_info[0], '%Y-%m-%d').strftime('%a')
                        date = date_info[0] + ' ' + weekday + ' ' + date_info[1]
                        self.date_time.append(date)
                        start = 1
                    else:
                        start = 0
                    for i in range(start, len(val)):
                        self.data[i - start][2].append(val[i])
                        
                else:
                    for i in range(0, len(val)):
                        self.data[i][2].append(val[i])
                z_item += 1
            
            
            if self.ui.radioButton_zbridge.isChecked():
                set_zero = float(self.data[0][2][0])
                for i in range(0, len(self.data[0][2])):
                    self.data[0][2][i] = ((float(self.data[0][2][i]) - set_zero) / 3600)
                new_data = []
                new_par = []
                for i in range(0, len(self.data)):
                    if len(self.data[i][3]) != len(self.data[0][2]):
                        new_data.append(self.data[i])
                        new_par.append(parameters[i])
                self.data = new_data
                parameters = new_par
                for i in range(0, len(parameters)):
                    self.ui.comboBox_y.addItem(parameters[i])

            if self.ui.radioButton_frontpanel.isChecked():
                set_zero = self.data[0][3][1]
                for i in range(0, len(self.data[0][2])):
                    self.data[0][2][i] = ((float(self.data[0][3][2 * i + 1]) - set_zero) / 3600)
                self.data[0][1] = 'hour'

            if self.open_recent == False:   
                self.item_info = []
                if self.ui.radioButton_frontpanel.isChecked():
                    self.item_info.append('frontpanel')
                elif self.ui.radioButton_compressor.isChecked():
                    self.item_info.append('compressor')
                else:
                    self.item_info.append(self.divider)
                self.item_info.append(self.file_name)
                self.item_info.append(str(self.ui.lineEdit_address.text()))
                self.all_info.append(self.item_info)
                self.ui.comboBox_recent.addItem(self.all_info[len(self.all_info) - 1][1])
            
            if self.ui.radioButton_compressor.isChecked():
                self.date_transfer = []
                date_tran = []
                date_tran = self.data[0][2]
                for i in range(0, len(date_tran)):
                    date_info = []
                    date_info = date_tran[i].split(' ')
                    weekday = date_info[0]
                    day = date_info[2]
                    year = date_info[4]
                    mon = date_info[1]
                    if mon == 'Jan':
                        mon = '01'
                    elif mon == 'Feb':
                        mon = '02'
                    elif mon == 'Mar':
                        mon = '03'
                    elif mon == 'Apr':
                        mon = '04'
                    elif mon == 'May':
                        mon = '05'
                    elif mon == 'Jun':
                        mon = '06'
                    elif mon == 'Jul':
                        mon = '07'
                    elif mon == 'Aug':
                        mon = '08'
                    elif mon == 'Sep':
                        mon = '09'
                    elif mon == 'Oct':
                        mon = '10'
                    elif mon == 'Nov':
                        mon = '11'
                    elif mon == 'Dec':
                        mon = '12'
                    date = year + '-' + mon + '-' + day + ' ' + weekday + ' ' + date_info[3]
                    self.date_transfer.append(date)
                #self.date_transfer.append(self.data[1][2])
                self.data = self.data[1:]
                for i in range(0, len(self.data[0][2])):
                    self.data[0][2][i] = float(self.data[0][2][i]) / 3600
                
            self.ui.groupBox_plot.setEnabled(True)
            self.ui.groupBox_first.setEnabled(True)
            self.ui.groupBox_second.setEnabled(True)
            self.ui.lineEdit_condition.setText('Ready to Plot.')
            self.ui.label_11.setEnabled(True)
            self.ui.comboBox_recent.setEnabled(True)
            self.ui.pushButton_recent.setEnabled(True)
            self.ui.comboBox_y_first_step.setEnabled(True)
            self.ui.pushButton_plot_first_step.setEnabled(True)
            self.ui.pushButton_plot_second_step.setEnabled(True)
            self.ui.comboBox_y_second_step.setEnabled(True)
            self.ui.label_14.setEnabled(True)
            self.ui.label_15.setEnabled(True)
            if self.ui.radioButton_frontpanel.isChecked() or self.ui.radioButton_compressor.isChecked():
                self.ui.groupBox_date.setEnabled(True)
            elif self.ui.radioButton_zbridge.isChecked():
                self.ui.groupBox_date.setEnabled(True)
                self.ui.groupBox_x.setEnabled(False)
                self.ui.groupBox_y.setEnabled(False)
                self.ui.tabWidget_xy.setCurrentIndex(1)
            elif self.ui.radioButton_qmd.isChecked() and temp_parameters[0] == 'Date':
                self.ui.groupBox_date.setEnabled(True)
            self.ui.groupBox_modify.setEnabled(False)
            
    def Open_Recent(self):
        file_number = self.ui.comboBox_recent.currentIndex()
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
        elif self.all_info[file_number][0].upper() == 'frontpanel'.upper():
            self.ui.radioButton_frontpanel.setChecked(True)
            self.ui.lineEdit_divider.setText('')
            self.divider = self.all_info[file_number][1] + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
            self.ui.lineEdit_divider.setText('None')
            self.ui.lineEdit_condition.setText(self.ui.comboBox_recent.currentText() + ' has been opened.')
        elif self.all_info[file_number][0].upper() == 'compressor'.upper():
            self.ui.radioButton_compressor.setChecked(True)
            self.ui.lineEdit_divider.setText('')
            self.divider = self.all_info[file_number][1] + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
            self.ui.lineEdit_divider.setText('None')
            self.ui.lineEdit_condition.setText(self.ui.comboBox_recent.currentText() + ' has been opened.')
        elif self.all_info[file_number][0].upper() == '#'.upper():
            self.ui.radioButton_zbridge.setChecked(True)
            self.ui.lineEdit_divider.setText('#')
            self.divider = '#' + '\n'
            self.ui.lineEdit_address.setText(self.all_info[file_number][2])
        
        self.reset_plot()
        self.ui.mplwidget.draw()
        self.open_recent = True
        self.OpenFile()
        
    def Find(self):
        try:
            time = float(self.ui.lineEdit_minute.text())
            if time <= float(self.data[0][2][0]):
                if self.ui.radioButton_frontpanel.isChecked():
                    self.ui.lineEdit_date.setText(self.data[0][3][0])
                elif self.ui.radioButton_compressor.isChecked():
                    self.ui.lineEdit_date.setText(self.date_transfer[0])
                else:
                    self.ui.lineEdit_date.setText(self.date_time[0])
            elif time >= float(self.data[0][2][len(self.data[0][2]) - 1]):
                if self.ui.radioButton_frontpanel.isChecked():
                    self.ui.lineEdit_date.setText(self.data[0][3][2 * (len(self.data[0][2]) - 1)])
                elif self.ui.radioButton_compressor.isChecked():
                    self.ui.lineEdit_date.setText(self.date_transfer[len(self.date_transfer) - 1])
                else:
                    self.ui.lineEdit_date.setText(self.date_time[len(self.date_time) - 1])
            else:
                item = 0
                while float(self.data[0][2][item]) - time < 0:
                    item += 1
                if abs(float(self.data[0][2][item - 1]) - time) <= abs(float(self.data[0][2][item]) - time):
                    if self.ui.radioButton_frontpanel.isChecked():
                        self.ui.lineEdit_date.setText(self.data[0][3][2 * (item - 1)])
                    elif self.ui.radioButton_compressor.isChecked():
                        self.ui.lineEdit_date.setText(self.date_transfer[item - 1])
                    else:
                        self.ui.lineEdit_date.setText(self.date_time[item - 1])
                else:
                    if self.ui.radioButton_frontpanel.isChecked():
                        self.ui.lineEdit_date.setText(self.data[0][3][2 * item])
                    elif self.ui.radioButton_compressor.isChecked():
                        self.ui.lineEdit_date.setText(self.date_transfer[item])
                    else:
                        self.ui.lineEdit_date.setText(self.date_time[item])
                        
        except ValueError:
            self.ui.lineEdit_date.setText('')
            self.ui.lineEdit_condition.setText('Please enter valid time.')
        
    def Plot_ready(self):
        self.x_value = []
        self.y_value = []
        self.x_num = 0
        self.y_num = 0
        self.x_num = self.ui.comboBox_x.currentIndex()
        self.y_num = self.ui.comboBox_y.currentIndex()
        xaxis = self.data[self.x_num][0]
        xunit = self.data[self.x_num][1]
        yaxis = self.data[self.y_num][0]
        yunit = self.data[self.y_num][1]
        
        self.x2_num = 0
        self.y2_num = 0
        self.x2_num = self.ui.comboBox_x_2.currentIndex() - 1
        self.y2_num = self.ui.comboBox_y_2.currentIndex() - 1
        x2axis = self.data[self.x2_num][0]
        x2unit = self.data[self.x2_num][1]
        y2axis = self.data[self.y2_num][0]
        y2unit = self.data[self.y2_num][1]
        
        if self.x2_num == -1:
            self.ui.lineEdit_x.setText(xaxis + ' (' + xunit + ')')
            self.x_value = self.data[self.x_num][2]
        elif self.x2_num >= 0:
            
            if self.ui.radioButton_x_divide.isChecked():
                self.x_value = numpy.array(self.data[self.x_num][2], dtype = 'float') / numpy.array(self.data[self.x2_num][2], dtype = 'float')
                x_title_mod = xaxis + '/' + x2axis
                self.ui.lineEdit_x.setText(x_title_mod + ' (' + xunit + '/' + x2unit + ')')
            elif self.ui.radioButton_x_multiply.isChecked():
                self.x_value = numpy.array(self.data[self.x_num][2], dtype = 'float') * numpy.array(self.data[self.x2_num][2], dtype = 'float')
                x_title_mod = xaxis + '*' + x2axis
                self.ui.lineEdit_x.setText(x_title_mod + ' (' + xunit + '*' + x2unit + ')')
            elif self.ui.radioButton_x_plus.isChecked():
                self.x_value = numpy.array(self.data[self.x_num][2], dtype = 'float') + numpy.array(self.data[self.x2_num][2], dtype = 'float')
                x_title_mod = xaxis + ' + ' + x2axis
                self.ui.lineEdit_x.setText(x_title_mod + ' (' + xunit + ' + ' + x2unit + ')')
            elif self.ui.radioButton_x_minus.isChecked():
                self.x_value = numpy.array(self.data[self.x_num][2], dtype = 'float') - numpy.array(self.data[self.x2_num][2], dtype = 'float')
                x_title_mod = xaxis + ' - ' + x2axis
                self.ui.lineEdit_x.setText(x_title_mod + ' (' + xunit + ' - ' + x2unit + ')')
        if self.ui.checkBox_x_value.isChecked():
            self.x_value = numpy.absolute(self.x_value)
            
        if self.y2_num == -1:
            self.ui.lineEdit_y.setText(yaxis + ' (' + yunit + ')')
            self.y_value = self.data[self.y_num][2]
        elif self.y2_num >= 0:
            
            if self.ui.radioButton_y_divide.isChecked():
                self.y_value = numpy.array(self.data[self.y_num][2], dtype = 'float') / numpy.array(self.data[self.y2_num][2], dtype = 'float')
                y_title_mod = yaxis + '/' + y2axis
                self.ui.lineEdit_y.setText(y_title_mod + ' (' + yunit + '/' + y2unit + ')')
            elif self.ui.radioButton_y_multiply.isChecked():
                self.y_value = numpy.array(self.data[self.y_num][2], dtype = 'float') * numpy.array(self.data[self.y2_num][2], dtype = 'float')
                y_title_mod = yaxis + '*' + y2axis
                self.ui.lineEdit_y.setText(y_title_mod + ' (' + yunit + '*' + y2unit + ')')
            elif self.ui.radioButton_y_plus.isChecked():
                self.y_value = numpy.array(self.data[self.y_num][2], dtype = 'float') + numpy.array(self.data[self.y2_num][2], dtype = 'float')
                y_title_mod = yaxis + ' + ' + y2axis
                self.ui.lineEdit_y.setText(y_title_mod + ' (' + yunit + ' + ' + y2unit + ')')
            elif self.ui.radioButton_y_minus.isChecked():
                self.y_value = numpy.array(self.data[self.y_num][2], dtype = 'float') - numpy.array(self.data[self.y2_num][2], dtype = 'float')
                y_title_mod = yaxis + ' - ' + y2axis
                self.ui.lineEdit_y.setText(y_title_mod + ' (' + yunit + ' - ' + y2unit + ')')
        if self.ui.checkBox_y_value.isChecked():
            self.y_value = numpy.absolute(self.y_value)
            
        if self.x2_num == -1 and self.y2_num == -1:
            self.ui.lineEdit_name.setText(yaxis + ' vs. ' + xaxis)
        elif self.x2_num >= 0 and self.y2_num == -1:
            self.ui.lineEdit_name.setText(yaxis + ' vs. ' + x_title_mod)
        elif self.x2_num == -1 and self.y2_num >= 0:
            self.ui.lineEdit_name.setText(y_title_mod + ' vs. ' + xaxis)
        else:
            self.ui.lineEdit_name.setText(y_title_mod + ' vs. ' + x_title_mod)
        
        self.ui.pushButton_change_name.setEnabled(True)
        self.ui.groupBox_modify.setEnabled(True)
        self.Pre_plot()
    
    def Pre_plot(self):
        if self.ui.radioButton_zbridge.isChecked():
            self.x_value = numpy.array(self.x_value, dtype = 'float') 
            self.y_value = numpy.array(self.y_value, dtype = 'float') / 1E3
            if len(self.data[self.y_num][3]) > 0:
                self.x_plot = numpy.delete(self.x_value, self.data[self.y_num][3])
                self.Plot(self.x_plot, self.y_value)
                self.ui.label_ymin.setText('(' + str(format(numpy.min(self.y_value), '.3f')) + ')')
                self.ui.label_ymax.setText('(' + str(format(numpy.max(self.y_value), '.3f')) + ')')
                self.ui.label_xmin.setText('(' + str(format(numpy.min(self.x_plot), '.3f')) + ')')
                self.ui.label_xmax.setText('(' + str(format(numpy.max(self.x_plot), '.3f')) + ')')
            else:
                self.Plot(self.x_value, self.y_value)
                self.ui.label_ymin.setText('(' + str(format(numpy.min(self.y_value), '.3f')) + ')')
                self.ui.label_ymax.setText('(' + str(format(numpy.max(self.y_value), '.3f')) + ')')
                self.ui.label_xmin.setText('(' + str(format(numpy.min(self.x_value), '.3f')) + ')')
                self.ui.label_xmax.setText('(' + str(format(numpy.max(self.x_value), '.3f')) + ')')
        else:
            self.x_value = numpy.array(self.x_value, dtype = 'float') 
            self.y_value = numpy.array(self.y_value, dtype = 'float')
            self.Plot(self.x_value, self.y_value)
            self.ui.label_ymin.setText('(' + str(format(numpy.min(self.y_value), '.3f')) + ')')
            self.ui.label_ymax.setText('(' + str(format(numpy.max(self.y_value), '.3f')) + ')')
            self.ui.label_xmin.setText('(' + str(format(numpy.min(self.x_value), '.3f')) + ')')
            self.ui.label_xmax.setText('(' + str(format(numpy.max(self.x_value), '.3f')) + ')')
    
    def Modify(self):
        try:
            x_modify = numpy.array([])
            y_modify = numpy.array([])

            if self.ui.radioButton_zbridge.isChecked():
                if len(self.data[self.y_num][3]) > 0:
                    x_modify = self.x_plot
                    y_modify = numpy.array(self.y_value)
            else:
                x_modify = numpy.array(self.x_value)
                y_modify = numpy.array(self.y_value)
            
            x_exc = []
            y_exc = []
            if self.ui.lineEdit_y_min.text() != '':
                y_min = float(self.ui.lineEdit_y_min.text())
                for i in range(0, len(y_modify)):
                    if y_modify[i] < y_min:
                        x_exc.append(i)
                        y_exc.append(i)
            x_modify = numpy.delete(x_modify, x_exc)
            y_modify = numpy.delete(y_modify, y_exc)
            x_exc = []
            y_exc = []            
            if self.ui.lineEdit_y_max.text() != '':
                y_max = float(self.ui.lineEdit_y_max.text())
                for i in range(0, len(y_modify)):
                    if y_modify[i] > y_max:
                        x_exc.append(i)
                        y_exc.append(i)
            x_modify = numpy.delete(x_modify, x_exc)
            y_modify = numpy.delete(y_modify, y_exc)
            x_exc = []
            y_exc = []
            if self.ui.lineEdit_x_min.text() != '':
                x_min = float(self.ui.lineEdit_x_min.text())
                for i in range(0, len(x_modify)):
                    if x_modify[i] < x_min:
                        x_exc.append(i)
                        y_exc.append(i)
            x_modify = numpy.delete(x_modify, x_exc)
            y_modify = numpy.delete(y_modify, y_exc)
            x_exc = []
            y_exc = []
            if self.ui.lineEdit_x_max.text() != '':
                x_max = float(self.ui.lineEdit_x_max.text())
                
                for i in range(0, len(x_modify)):
                    if x_modify[i] > x_max:
                        x_exc.append(i)
                        y_exc.append(i)
            x_modify = numpy.delete(x_modify, x_exc)
            y_modify = numpy.delete(y_modify, y_exc)
            
            self.ui.label_ymin.setText('(' + str(format(numpy.min(y_modify), '.3f')) + ')')
            self.ui.label_ymax.setText('(' + str(format(numpy.max(y_modify), '.3f')) + ')')
            self.ui.label_xmin.setText('(' + str(format(numpy.min(x_modify), '.3f')) + ')')
            self.ui.label_xmax.setText('(' + str(format(numpy.max(x_modify), '.3f')) + ')')
            self.Plot(x_modify, y_modify)
            
        except ValueError:
            self.ui.lineEdit_condition.setText('Please enter valid Min and Max.')
            
    def Return(self):
        x_return = []
        y_return = []
        
        if self.ui.radioButton_zbridge.isChecked():
            if len(self.data[self.y_num][3]) > 0:
                x_return = self.x_plot
                y_return = numpy.array(self.y_value)
        else:
            x_return = numpy.array(self.x_value)
            y_return = numpy.array(self.y_value)
        
        self.ui.label_ymin.setText('')
        self.ui.label_ymax.setText('')
        self.ui.label_xmin.setText('')
        self.ui.label_xmax.setText('')
        self.ui.lineEdit_y_min.setText('')
        self.ui.lineEdit_y_max.setText('')
        self.ui.lineEdit_x_min.setText('')
        self.ui.lineEdit_x_max.setText('')
        self.Plot_ready()
    
    def Plot(self, x, y):
        self.reset_plot()
        self.axes.plot(x, y, marker = '.', linestyle = ':')
        self.axes.grid()
        self.axes.set_title(self.ui.lineEdit_name.text())
        self.axes.set_xlabel(self.ui.lineEdit_x.text())
        self.axes.set_ylabel(self.ui.lineEdit_y.text())
        self.ui.mplwidget.draw()
        
        self.ui.lineEdit_condition.setText('Plot successfully.')
        
    
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
        
        if self.ui.radioButton_zbridge.isChecked() or self.ui.radioButton_frontpanel.isChecked():
            xv = self.data[0][2]
        else:
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
        if self.ui.radioButton_zbridge.isChecked() or self.ui.radioButton_frontpanel.isChecked():
            self.axes_first_step.set_xlabel('Time (s)')
        else:
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
        
        if self.ui.radioButton_zbridge.isChecked() or self.ui.radioButton_frontpanel.isChecked():
            xv = self.data[0][2]
        else:
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
        if self.ui.radioButton_zbridge.isChecked() or self.ui.radioButton_frontpanel.isChecked():
            self.axes_first_step.set_xlabel('Time (s)')
        else:
            self.axes_first_step.set_xlabel('Unit Step (1)')
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
    
    def convert_time(self, d):
        date, times = d.split(" ")
        year, month, day = date.split("-")
        hour, minute, second = times.split(":")
    
        t = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        t_sec = time.mktime(t.timetuple())

        return t_sec
    
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
        
