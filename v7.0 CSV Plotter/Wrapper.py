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
import matplotlib.pyplot as plt

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
        self.reset_plot()
        
        self.connect(self.ui.pushButton_browse, SIGNAL('clicked()'), self.Browse)
        self.connect(self.ui.pushButton_change_name, SIGNAL('clicked()'), self.Change_name)
        self.connect(self.ui.pushButton_open, SIGNAL('clicked()'), self.Open)
        self.connect(self.ui.pushButton_Plot, SIGNAL('clicked()'), self.Plot_ready)
        self.connect(self.ui.pushButton_Next, SIGNAL('clicked()'), self.Next)
        self.connect(self.ui.pushButton_Previous, SIGNAL('clicked()'), self.Previous)
        self.connect(self.ui.pushButton_find, SIGNAL('clicked()'), self.Find)
        self.connect(self.ui.pushButton_modify, SIGNAL('clicked()'), self.Modify)
        self.connect(self.ui.pushButton_return, SIGNAL('clicked()'), self.Return)

        self.ui.pushButton_browse.setEnabled(True)
        self.modify = False
        self.first_round = True
        self.open_dir = ''
        self.open_files_number = 0
        self.all_info = []
            
    def Browse(self):
        self.Num = 0
        self.Files = []
        self.Names = []
        
        prev_dir = os.getcwd()
        fileDir = QFileDialog.getOpenFileNames(self, 'Select Files to Open', self.ui.lineEdit_address.text())
        if fileDir != '':
            self.comboBox_update = True
            self.Files = fileDir
            open_dir = ''
            file_list = str(fileDir[0]).split('\\')
            for i in range(0, len(file_list) - 1):
                if i < len(file_list) - 2:
                    open_dir += file_list[i] + '\\'
                elif i == len(file_list) - 2:
                    open_dir += file_list[i]
            self.ui.lineEdit_address.setText(open_dir)
            
            self.ui.pushButton_open.setEnabled(True)
            self.first_round = False
            filedir = str(fileDir).split('\\')
            for i in range(0, len(fileDir)):
                temp = fileDir[i].split('\\')
                name = temp[len(temp) - 1]
                self.Names.append(name)
            if len(fileDir) > 1:
                self.ui.label_condition.setText(str(len(fileDir)) + ' files selected, click Open')
            elif len(fileDir) == 1:
                self.ui.label_condition.setText(str(len(fileDir)) + ' file selected, click Open')
        else:
            self.ui.lineEdit_address.setText('None')
            self.ui.label_condition.setText('Failed to Read File')
        
    def Open(self):
        
        # Every you click the "Open File" button, the content in the plot combox is refreshed
        self.reset_plot()
        self.ui.mplwidget.draw()
        self.ui.lineEdit_x.setText('')
        self.ui.lineEdit_y.setText('')
        self.ui.lineEdit_name.setText('')
        self.ui.label_condition.setText('')
        self.ui.lineEdit_minute.setText('')
        self.ui.label_date.setText('')
        
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
        length = 0
        # This count is the number of the reading loops for labels. If count is over 1000, that means there's something wrong with the divider line and it helps to stop the program
        count = 0
        
        # It is false when program cannot find the line divider and runs the while loop 1000 times
        self.divider_found = True

        fp = open(self.Files[self.Num])
        while True:
            if count > 1000:
                self.ui.label_condition.setText('Line divider is not found.')
                self.divider_found = False
                break
            line = fp.readline()
            linelist = line.split(',')
            if linelist[0].upper() == 'COLLECTED DATA\n':
                break
            for i in range(0, len(linelist)):
                labels += linelist[i]
            count += 1
            
        if self.divider_found == True:
            self.ui.textEdit_labels.setText(labels)
            parameters = fp.readline().replace("\n", '')
            temp_parameters = parameters.split(',')
            if temp_parameters[0] == 'Date':
                parameters = temp_parameters[1:]
            else:
                parameters = temp_parameters
            
            # The following is for the units
            units = fp.readline().replace("\n", '')
            units = units.split(",")
            if temp_parameters[0] == 'Date':
                units = units[1:]
            
            if self.comboBox_update:
                self.ui.comboBox_x.clear()
                self.ui.comboBox_y1.clear()
                self.ui.comboBox_y2.clear()
                self.ui.comboBox_y3.clear()
                self.ui.comboBox_y4.clear()
                self.ui.comboBox_y5.clear()
                self.ui.comboBox_y6.clear()
                self.ui.comboBox_y2.addItem('None')
                self.ui.comboBox_y3.addItem('None')
                self.ui.comboBox_y4.addItem('None')
                self.ui.comboBox_y5.addItem('None')
                self.ui.comboBox_y6.addItem('None')
                for i in range(0, len(parameters)):
                    self.ui.comboBox_x.addItem(parameters[i])
                    self.ui.comboBox_y1.addItem(parameters[i])
                    self.ui.comboBox_y2.addItem(parameters[i])
                    self.ui.comboBox_y3.addItem(parameters[i])
                    self.ui.comboBox_y4.addItem(parameters[i])
                    self.ui.comboBox_y5.addItem(parameters[i])
                    self.ui.comboBox_y6.addItem(parameters[i])
                self.ui.comboBox_y1.setCurrentIndex(1)
                self.comboBox_update = False
            
            for i in range(0, len(parameters)):
                new_data = [parameters[i], units[i], [], []]
                self.data.append(new_data)
                
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
                if temp_parameters[0] == 'Date':
                    date_info = val[0].split(' ')
                    if '/' not in date_info[0]:
                        weekday = datetime.datetime.strptime(date_info[0], '%Y-%m-%d').strftime('%a')
                    else:
                        weekday = datetime.datetime.strptime(date_info[0], '%m/%d/%Y').strftime('%a')
                    date = date_info[0] + ' ' + weekday + ' ' + date_info[1]
                    self.date_time.append(date)
                    start = 1
                else:
                    start = 0
                for i in range(start, len(val)):
                    self.data[i - start][2].append(val[i])
            
            self.ui.pushButton_Plot.setEnabled(True)
            if self.Num == 0:
               self.ui.pushButton_Previous.setEnabled(False)
            if len(self.Files) == 1:
                self.ui.label_condition.setText(str(len(self.Files)) + ' file ready to Plot')
            else:
                self.ui.label_condition.setText(str(len(self.Files)) + ' files ready to Plot')
        
    def Find(self):
        try:
            time = float(self.ui.lineEdit_minute.text())
            if time <= float(self.data[0][2][0]):
                self.ui.label_date.setText(self.date_time[0])
            elif time >= float(self.data[0][2][len(self.data[0][2]) - 1]):
                self.ui.label_date.setText(self.date_time[len(self.date_time) - 1])
            else:
                item = 0
                while float(self.data[0][2][item]) - time < 0:
                    item += 1
                if abs(float(self.data[0][2][item - 1]) - time) <= abs(float(self.data[0][2][item]) - time):
                    self.ui.label_date.setText(self.date_time[item - 1])
                else:
                    self.ui.label_date.setText(self.date_time[item])
                        
        except ValueError:
            self.ui.label_date.setText('')
            self.ui.label_condition.setText('Please enter valid time.')
        
    def Plot_ready(self):
        self.x_value = []
        self.y1_value = []
        self.y2_value = []
        self.y3_value = []
        self.y4_value = []
        self.y5_value = []
        self.y6_value = []
        
        # The corresponding number of the comboBox
        self.x_num = 0
        self.x_num = self.ui.comboBox_x.currentIndex()
        self.y1_num = 0
        self.y1_num = self.ui.comboBox_y1.currentIndex()
        self.y2_num = 0
        self.y2_num = self.ui.comboBox_y2.currentIndex() - 1
        self.y3_num = 0
        self.y3_num = self.ui.comboBox_y3.currentIndex() - 1
        self.y4_num = 0
        self.y4_num = self.ui.comboBox_y4.currentIndex() - 1
        self.y5_num = 0
        self.y5_num = self.ui.comboBox_y5.currentIndex() - 1
        self.y6_num = 0
        self.y6_num = self.ui.comboBox_y6.currentIndex() - 1
        
        x_axis = self.data[self.x_num][0]
        x_unit = self.data[self.x_num][1]
        y1_axis = self.data[self.y1_num][0]
        y1_unit = self.data[self.y1_num][1]
        y2_axis = self.data[self.y2_num][0]
        y2_unit = self.data[self.y2_num][1]
        y3_axis = self.data[self.y3_num][0]
        y3_unit = self.data[self.y3_num][1]
        y4_axis = self.data[self.y4_num][0]
        y4_unit = self.data[self.y4_num][1]
        y5_axis = self.data[self.y5_num][0]
        y5_unit = self.data[self.y5_num][1]
        y6_axis = self.data[self.y6_num][0]
        y6_unit = self.data[self.y6_num][1]
        
        self.y1_color_num = 0
        self.y1_color_num = self.ui.comboBox_color_y1.currentIndex()
        self.y1_color = self.Color(self.y1_color_num)
        self.y2_color_num = 0
        self.y2_color_num = self.ui.comboBox_color_y2.currentIndex()
        self.y2_color = self.Color(self.y2_color_num)
        self.y3_color_num = 0
        self.y3_color_num = self.ui.comboBox_color_y3.currentIndex()
        self.y3_color = self.Color(self.y3_color_num)
        self.y4_color_num = 0
        self.y4_color_num = self.ui.comboBox_color_y4.currentIndex()
        self.y4_color = self.Color(self.y4_color_num)
        self.y5_color_num = 0
        self.y5_color_num = self.ui.comboBox_color_y5.currentIndex()
        self.y5_color = self.Color(self.y5_color_num)
        self.y6_color_num = 0
        self.y6_color_num = self.ui.comboBox_color_y6.currentIndex()
        self.y6_color = self.Color(self.y6_color_num)
        
        self.y1_legend = self.ui.comboBox_y1.currentText()
        self.y2_legend = self.ui.comboBox_y2.currentText()
        self.y3_legend = self.ui.comboBox_y3.currentText()
        self.y4_legend = self.ui.comboBox_y4.currentText()
        self.y5_legend = self.ui.comboBox_y5.currentText()
        self.y6_legend = self.ui.comboBox_y6.currentText()
        
        self.x_value = self.data[self.x_num][2]
        self.y1_value = self.data[self.y1_num][2]
        if self.y2_num != -1:
            self.y2_value = self.data[self.y2_num][2]
        if self.y3_num != -1:
            self.y3_value = self.data[self.y3_num][2]
        if self.y4_num != -1:
            self.y4_value = self.data[self.y4_num][2]
        if self.y5_num != -1:
            self.y5_value = self.data[self.y5_num][2]
        if self.y6_num != -1:
            self.y6_value = self.data[self.y6_num][2]
            
        self.ui.lineEdit_x.setText(x_axis + ' (' + x_unit + ')')
        self.ui.lineEdit_y.setText(y1_axis + ' (' + y1_unit + ')')
        self.ui.lineEdit_name.setText(self.Names[self.Num])
        
        self.ui.pushButton_change_name.setEnabled(True)
        if len(self.Files) > 1:
            self.ui.pushButton_Next.setEnabled(True)
        self.Pre_plot()
    
    def Color(self, num):
        if num == 0:
            return 'b'
        elif num == 1:
            return 'g'
        elif num == 2:
            return 'r'
        elif num == 3:
            return 'y'
        elif num == 4:
            return 'k'
        elif num == 5:
            return 'm'
        
    def Pre_plot(self):
        self.reset_plot()
        self.axes.grid()
        
        self.x_value = numpy.array(self.x_value, dtype = 'float') 
        self.y1_value = numpy.array(self.y1_value, dtype = 'float')
        self.Plot(self.x_value, self.y1_value, self.y1_color, self.y1_legend)
        if self.y2_num != -1:
            self.y2_value = numpy.array(self.y2_value, dtype = 'float')
            self.Plot(self.x_value, self.y2_value, self.y2_color, self.y2_legend)
        if self.y3_num != -1:
            self.y3_value = numpy.array(self.y3_value, dtype = 'float')
            self.Plot(self.x_value, self.y3_value, self.y3_color, self.y3_legend)
        if self.y4_num != -1:
            self.y4_value = numpy.array(self.y4_value, dtype = 'float')
            self.Plot(self.x_value, self.y4_value, self.y4_color, self.y4_legend)
        if self.y5_num != -1:
            self.y5_value = numpy.array(self.y5_value, dtype = 'float')
            self.Plot(self.x_value, self.y5_value, self.y5_color, self.y5_legend)
        if self.y6_num != -1:
            self.y6_value = numpy.array(self.y6_value, dtype = 'float')
            self.Plot(self.x_value, self.y6_value, self.y6_color, self.y6_legend)
        
        self.ui.label_condition.setText('File' + ' (' + str(self.Num + 1) + '/' + str(len(self.Files)) + ')' + ': ' + self.Names[self.Num])
        
        self.Draw()
    
    def Next(self):
        self.Num = self.Num + 1
        self.Open()
        self.Plot_ready()
        if self.Num == len(self.Files) - 1:
            self.ui.pushButton_Next.setEnabled(False)
        self.ui.pushButton_Previous.setEnabled(True)
    
    def Previous(self):
        self.Num = self.Num - 1
        self.Open()
        self.Plot_ready()
        if self.Num == -1:
            self.ui.pushButton_Previous.setEnabled(False)
        self.ui.pushButton_Next.setEnabled(True)
    
    def Modify(self):
        try:
            self.modify = True
            if self.ui.lineEdit_x_range.text() != '':
                self.modify_x = True
                self.x_min = float(self.ui.lineEdit_x_range.text().split(',')[0])
                self.x_max = float(self.ui.lineEdit_x_range.text().split(',')[1])
            else:
                self.modify_x = False
            if self.ui.lineEdit_y_range.text() != '':
                self.modify_y = True
                self.y_min = float(self.ui.lineEdit_y_range.text().split(',')[0])
                self.y_max = float(self.ui.lineEdit_y_range.text().split(',')[1])
            else:
                self.modify_y = False
            if self.ui.checkBox_logx.isChecked():
                self.log_x = True
            else:
                self.log_x = False
            if self.ui.checkBox_logx.isChecked():
                self.log_y = True
            else:
                self.log_y = False
            self.Plot_ready()
        except ValueError:
            self.ui.label_condition.setText('Please enter valid Min and Max.')
            
    def Return(self):
        self.modify = False
        self.ui.lineEdit_x_range.setText('')
        self.ui.lineEdit_y_range.setText('')
        self.ui.checkBox_logx.setCheckState(False)
        self.ui.checkBox_logx.setCheckState(False)
        self.ui.pushButton_return.setEnabled(False)
        self.Plot_ready()
    
    def Change_name(self):
        self.axes.set_title(self.ui.lineEdit_name.text())
        self.axes.set_xlabel(self.ui.lineEdit_x.text())
        self.axes.set_ylabel(self.ui.lineEdit_y.text())
        self.Draw()
            
    def Plot(self, x, y, c, l):
        self.axes.plot(x, y, color = c, marker = '.', linestyle = ':', label= l)
        self.axes.set_title(self.ui.lineEdit_name.text())
        self.axes.set_xlabel(self.ui.lineEdit_x.text())
        self.axes.set_ylabel(self.ui.lineEdit_y.text())
        self.axes.legend()
        if self.modify:
            if self.modify_x:
                self.axes.set_xlim(self.x_min, self.x_max)
            if self.modify_y:
                self.axes.set_ylim(self.y_min, self.y_max)
            if self.log_x:
                self.axes.set_xscale('log')
            if self.log_y:
                self.axes.set_yscale('log')
        self.ui.label_condition.setText('Plot successfully.')
        
    def Draw(self):
        self.ui.mplwidget.draw()
    
    def reset_plot(self):
        self.ui.mplwidget.figure.clear()        
        self.axes = self.ui.mplwidget.figure.add_subplot(111)
        self.ui.mplwidget.figure.subplots_adjust(left=0.06, right=0.94, top=0.92, bottom=0.08)
    
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
        
