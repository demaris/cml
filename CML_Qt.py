# -*- coding: utf-8 -*-
"""
Hybrid CML displayed via a RawImageWidget in QT
"""

from pyqtgraph.graphicsItems.GradientEditorItem import GradientEditorItem
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.widgets import RawImageWidget


from numpy import *
from numpy.random import rand
from scipy.signal import convolve2d
from scipy.ndimage import zoom
from diffusiveCML import DiffusiveCML
from competitiveCML import CompetitiveCML
from pyo import *
from initCML import *
sidelen=80
#cells=sidelen**2

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])

win = QtGui.QMainWindow()
win.setWindowTitle('pyqtgraph example: VideoSpeedTest')
win.setObjectName("MainWindow")
win.resize(sidelen*8, sidelen*8)
#rawImg = RawImageWidget(scaled=True)
rawImg = RawImageWidget.RawImageWidget()
win.setCentralWidget(rawImg)
win.show()

LUT = None
n = 256
gei = GradientEditorItem()
# see definition of GradientEditorItem() to define an LUT
# presets cyclic, spectrum, thermal, flame, yellowy, bipolar, greyclip, grey
gei.loadPreset('flame')
LUT = gei.getLookupTable(n, alpha=False)

#initLattice=imageCML('/Users/daviddemaris/Dropbox/Public/JungAionFormula.jpg')
#win.resize(size(initLattice,0),size(initLattice,1))

initLattice=randomPing(sidelen,sidelen)

#initLattice=magicSquare(sidelen)

#initLattice=primesSquare(sidelen)

#initLattice=randbin(sidelen,sidelen)
#print initLattice
cml = DiffusiveCML(initLattice,kern='magic11')
#cml = CompetitiveCML(initLattice)
"""
s = Server(sr=44100, nchnls=2,  buffersize=2048, duplex=0).boot()

SCALES = [[0,2,5,7,9,11], [0,2,3,7,8,11], [0,3,5,7,8,10]]

class Melo:
   def __init__(self, amp=.1, speed=1, midirange=(48,84)):
       # table to record new melody fragment
       self.table = NewTable(2)
       # loopseg generation
       self.base_mel = XnoiseMidi(dist=12, freq=8, x1=1, x2=.25, scale=0, mrange=midirange)
       # snap on scale and convert to hertz
       self.base_melo = Snap(self.base_mel, choice=[0,2,4,5,7,9,11], scale=1)
       # record a new fragment every 10 seconds
       self.trig_rec = Metro(time=10).play()
       self.tab_rec = TrigTableRec(self.base_melo, self.trig_rec, self.table)
       # rise amp of the oscillators after the first recording
       self.amp = Counter(self.tab_rec["trig"], min=1, max=2, mul=amp)
       # random speed for the oscillator reading the melody table + portamento
       self.speed = Choice(choice=[.0625,.125,.125,.125,.25,.5], freq=1.0*speed)
       self.freq = Osc(self.table, self.speed*speed)
       self.freq_port = Port(self.freq, risetime=.01, falltime=.01)
       # 8 randis (freq and amp) to create a chorus of oscillators
       self.rnd_chorus = Randi(min=.99, max=1.01, freq=[random.uniform(3,6) for i in range(8)])
       self.rnd_amp = Randi(min=0, max=.15, freq=[random.uniform(.2,.5) for i in range(8)])
       # oscillators...
       self.osc = LFO(self.freq_port*self.rnd_chorus, type=3, sharp=.75,
                      mul=Port(self.amp, mul=self.rnd_amp)).out(inc=1)

   def setScale(self, scl):
       self.base_melo.choice = scl

def choose_scale():
   scl = random.choice(SCALES)
   for obj in objs:
       obj.setScale(scl)

a = Melo(amp=.3, speed=1, midirange=(60,84))
b = Melo(amp=.6, speed=0.5, midirange=(48,72))
c = Melo(amp=1, speed=0.25, midirange=(36,60))
objs = [a,b,c]
pat = Pattern(time=20, function=choose_scale).play()
"""
drawmod=20
i=0

def update():

    global i, drawmod
    useLut = LUT
    i=i+1

    # diffusion
    cml.iterate()

    if (i>1 and i % drawmod==0): 
        #llshow=cml.matrix*128

        llshow=zoom(((cml.matrix)+1)*128, 8, order=2)
        ## Display the data
        rawImg.setImage(llshow, lut=useLut)


app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    #s.start()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
