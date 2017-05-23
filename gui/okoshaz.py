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
strAM="AM"
strPM="PM"
class Clock(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)
        #self.msecdiff=0
        self.lastCmd=""
        self.speed=0
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
        '''
        tabs=QtGui.QTabWidget()
        tab1=QtGui.QWidget()
        tab2=QtGui.QWidget()
        '''
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
        self.sPointer = QtGui.QPolygon([
            QtCore.QPoint(1, 1),
            QtCore.QPoint(-1, 1),
            QtCore.QPoint(0, -90)
        ])
        #colors
        self.bColor = QtGui.QColor('#0000aa') #hours and minutes
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
        #buttons
        #btnreset = QtGui.QPushButton("Reset", self)
        #btnreset.clicked.connect(lambda: self.handleBtn("Reset"))
        btnfaster = QtGui.QPushButton("Faster", self)
        btnfaster.clicked.connect(lambda: self.handleBtn("Faster"))
        btnfaster.move(100,0)
        btnslower = QtGui.QPushButton("Slower", self)
        btnslower.clicked.connect(lambda: self.handleBtn("Slower"))
        btnslower.move(200,0)
        #api buttons
        btn1=QtGui.QPushButton("btn1", self)
        btn1.clicked.connect(lambda: self.handleBtn("btn1"))
        btn1.move(475,135)
        btn2=QtGui.QPushButton("btn2", self)
        btn2.clicked.connect(lambda: self.handleBtn("btn2"))
        btn2.move(647,129)
        btn3=QtGui.QPushButton("btn3", self)
        btn3.clicked.connect(lambda: self.handleBtn("btn3"))
        btn3.move(645,281)
        btn4=QtGui.QPushButton("btn4", self)
        btn4.clicked.connect(lambda: self.handleBtn("btn4"))
        btn4.move(424,340)
        btn5=QtGui.QPushButton("btn5", self)
        btn5.clicked.connect(lambda: self.handleBtn("btn5"))
        btn5.move(400,450)
        btn6=QtGui.QPushButton("btn6", self)
        btn6.clicked.connect(lambda: self.handleBtn("btn6"))
        btn6.move(500,450)
        #self.btnampm=QtGui.QLabel(self,"ampm")
        self.btnampm=QtGui.QPushButton("ampm",self)
        self.btnampm.move(0,30)
        self.btnampm.clicked.connect(self.handleAmpm)

    def handleAmpm(self,x):
        self.tik=self.tik.addSecs(12*3600)
        print self.tik

    def handleBtn(self,btnname):
        if btnname=="Reset":
            self.tik=QtCore.QTime.currentTime()
            self.speed=0
        elif btnname == "Faster":
            self.speed=min(self.speed+1,8)
            print "speed",self.speed
        elif btnname == "Slower":
            self.speed=max(self.speed-1,0)
            print "speed",self.speed
        elif btnname == "btn1":
            self.ajaxCall(apicall["btn1"],False)
        elif btnname == "btn2":
            self.ajaxCall(apicall["btn2"],False)
        elif btnname == "btn3":
            self.ajaxCall(apicall["btn3"],False)
        """
        elif btnname == "":
        elif btnname == "":
        print _
        """

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
                    if self.btnampm.text()==strPM: hour+=12
                    self.tik.setHMS(hour,minu,sec,msec)
                    #ct=QtCore.QTime.currentTime()
                    #self.msecdiff=((((hour-ct.hour())*60)+minu-ct.minute())*60+sec-ct.second())*1000+msec-ct.msec()
                    print hour,minu,sec,msec
                elif distforigo<20:
                    self.handleBtn("Reset")
                elif x>74 and x<113 and y>425 and y<453:
                    self.handleBtn("Slower")
                elif x>259 and x<298 and y>425 and y<453:
                    self.handleBtn("Faster")
                print "click:",x,y,distforigo

    def paintEvent(self, event):
        rec = min(self.width(), self.height())
        #self.tik = self.ts.addMSecs(self.ts.msecsTo(QtCore.QTime.currentTime())*self.speed+self.msecdiff)
        self.tik = self.tik.addMSecs(timermsec*2**self.speed)
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
        drawPointer(self.sColor, (6 * self.tik.second()), self.sPointer)
        ampm=strPM if self.tik.hour()>=12 else strAM
        self.btnampm.setText(ampm)
        #display time
        self.hhmm.setText("{:02}:{:02}".format(self.tik.hour(),self.tik.minute()))
        #draw face
        painter.setPen(QtGui.QPen(self.bColor))
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
    if fullscreen: win.showFullScreen()
    win.show()
    exit(app.exec_())
