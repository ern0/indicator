#!/usr/bin/env python

from okoshaz_conf import *
from sys import argv, exit
from PyQt4 import QtCore, QtGui
import math
import urllib
# http://stackoverflow.com/questions/24677882/implement-event-handlers-for-qwidget-and-derived-classes-and-avoid-code-duplicat
serverurl="http://localhost:8080/"
timermsec=100
clkpozscale=0.24
clksizescale=0.9
class Clock(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)
        #self.msecdiff=0
        self.lastCmd=""
        self.tik=QtCore.QTime.currentTime()
        #self.ts=self.tik
        #timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(timermsec)
        self.cnt=0
        #window
        self.setWindowIcon(QtGui.QIcon('Default.png'))
        self.setWindowTitle('Clock')
        #self.resize(800, 700)
        self.resize(800, 480)
        #tabs
        #hour pointer
        self.hPointer = QtGui.QPolygon([
            QtCore.QPoint(6, 7),
            QtCore.QPoint(-6, 7),
            QtCore.QPoint(0, -50)
        ])
        #minute pointer
        self.mPointer = QtGui.QPolygon([
            QtCore.QPoint(6, 7),
            QtCore.QPoint(-6, 7),
            QtCore.QPoint(0, -70)
        ])
        #second pointer
        """
        self.sPointer = QtGui.QPolygon([
            QtCore.QPoint(1, 1),
            QtCore.QPoint(-1, 1),
            QtCore.QPoint(0, -90)
        ])
        """
        #colors
        self.bColor = QtGui.QColor('#00e0e0') #hours and minutes
        self.sColor = QtGui.QColor('#aa0087')
        #image
        pic=QtGui.QLabel(self)
        pm=QtGui.QPixmap("alaprajzk.png")
        pic.setPixmap(pm)
        pic.move(self.width()-pm.width()-20,(self.height()-pm.height())/2)
        #current time label
        self.hhmm=QtGui.QLabel(self)
        self.hhmm.setText("00:00")
        self.hhmm.move(self.width()*clkpozscale-65,422)
        self.hhmm.setFont(QtGui.QFont("Fixed",30,QtGui.QFont.Bold))
        self.hhmm.setStyleSheet("QLabel {color : #00e0e0;}")
        #api buttons
        garage=QtGui.QPushButton("", self)
        garage.setIcon(QtGui.QIcon("switch_off.png"))
        garage.setIconSize(QtCore.QSize(48,48))
        garage.clicked.connect(lambda: self.handleBtn(garage,"garage"))
        garage.move(470,130)
        garage.setCheckable(True)
        telly=QtGui.QPushButton("", self)
        telly.setIcon(QtGui.QIcon("telly.png"))
        telly.setIconSize(QtCore.QSize(64,64))
        telly.clicked.connect(self.handleTelly)
        telly.move(517,326)
        telly.setCheckable(True)
        livingroom=QtGui.QPushButton("", self)
        livingroom.setIcon(QtGui.QIcon("switch_off.png"))
        livingroom.setIconSize(QtCore.QSize(48,48))
        livingroom.clicked.connect(lambda: self.handleBtn(livingroom,"livingroom"))
        livingroom.move(645,281)
        livingroom.setCheckable(True)
        bathroom=QtGui.QPushButton("", self)
        bathroom.clicked.connect(lambda: self.handleBtn(bathroom,"bathroom"))
        bathroom.setIcon(QtGui.QIcon("switch_off.png"))
        bathroom.setIconSize(QtCore.QSize(32,32))
        bathroom.move(420,340)
        bathroom.setCheckable(True)

    def handleAmpm(self):
        self.tik=self.tik.addSecs(12*3600)
        print self.tik

    def handleTelly(self):
        print "telly"
        #self.ajaxCall(apicall["telly"],False)

    def handleBtn(self,obj,btnname):
        if obj:
            if obj.isChecked():
                obj.setIcon(QtGui.QIcon("switch_on.png"))
            else:
                obj.setIcon(QtGui.QIcon("switch_off.png"))
        if btnname=="Reset":
            self.tik=QtCore.QTime.currentTime()
        else:
            self.ajaxCall(apicall[btnname],False)

    def mousePressEvent(self, event):
        if type(event) == QtGui.QMouseEvent:
            if event.button() == QtCore.Qt.LeftButton:
                x=event.x()
                y=event.y()
                w=self.width()*clkpozscale*2
                h=self.height()
                #    self.width()*clkpozscale, self.height()/2
                distforigo=math.sqrt((w-x-x)**2+(h-y-y)**2)/4.0
                if distforigo<90 and distforigo>60:
                    ti=6+math.atan2((w-x-x),(y+y-h))*6/math.pi
                    hour=int(ti)
                    ti=(ti-hour)*60
                    minu=int(ti)
                    ti=(ti-minu)*60
                    sec=int(ti)
                    msec=int((ti-sec)*1000)
                    if self.tik.hour()>=12: hour+=12
                    self.tik.setHMS(hour,minu,sec,msec)
                    print hour,minu,sec,msec
                elif distforigo<20:
                    self.handleBtn(False,"Reset")
                elif x>129 and x<252 and y>428 and y<457:
                    self.handleAmpm()
                elif (x-760)**2+(y-67)**2<400:
                    self.handleBtn(False,"rainbow")
                print "click:",x,y,distforigo

    def paintEvent(self, event):
        rec = min(self.width(), self.height())
        self.tik = self.tik.addMSecs(timermsec*60)
        #if self.tik.msec()<100: print self.tik
        #painter
        painter = QtGui.QPainter(self)
        #zipping code to draw pointers
        def drawPointer(color, rotation, pointer):
            painter.setBrush(QtGui.QBrush(color))
            painter.save()
            painter.rotate(rotation)
            painter.drawConvexPolygon(pointer)
            painter.restore()
        #tune up painter
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width()*clkpozscale, self.height()/2)
        painter.scale(rec/200, rec/200)
        painter.setPen(QtCore.Qt.NoPen)
        #draw pointers
        drawPointer(self.bColor, (30 * (self.tik.hour() + self.tik.minute() / 60.0)), self.hPointer)
        drawPointer(self.bColor, (6 * (self.tik.minute() + self.tik.second() / 60.0)), self.mPointer)
        #drawPointer(self.sColor, (6 * self.tik.second()), self.sPointer)
        #display time
        self.hhmm.setText("{:02}:{:02}".format(self.tik.hour(),self.tik.minute()))
        #draw face
        painter.setPen(QtGui.QPen(self.bColor,2))
        for i in range(0, 60):
            if (i % 5) != 0:
                painter.drawLine(87*clksizescale, 0, 97*clksizescale, 0)
            else:
                painter.drawLine(77*clksizescale, 0, 97*clksizescale, 0)
            painter.rotate(6)
        if self.cnt>=5:  #5 -> 5*100msec = 0.5sec
            self.checkSchedule(self.tik.hour(),self.tik.minute())
            self.cnt=0
        else:
            self.cnt+=1
        painter.end()

    def checkSchedule(self,hour,minu):
        res=-1
        for i in sorted(sched,reverse=True):
            if i<=hour*100+minu:
                res=i
                break
        if res==-1: res=list(sorted(sched,reverse=True))[0]
        self.ajaxCall(sched[res],True)

    def ajaxCall(self,cmd,remember):
        if cmd!=self.lastCmd:
            #print urllib.urlopen(serverurl + cmd).read()
            print cmd
            if remember: self.lastCmd=cmd

if __name__ == '__main__':
    app = QtGui.QApplication(argv)
    win = Clock()
    win.setStyleSheet("QWidget{ background-color: black; }")
    if fullscreen: win.showFullScreen()
    win.show()
    exit(app.exec_())
