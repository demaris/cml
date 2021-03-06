__author__ = 'nigel'

"""
The generator of the CML matrix:  responsible for generating, iterating and managing the matrix
"""


from numpy import *
from numpy.random import rand
from scipy.signal import convolve2d




class CMLGenerator:

    def __init__(self, xsize, ysize):
        """
        Create a new matrix, and populate it with a default random population
        """
        #global matrix, numCells
        self.matrix = rand(xsize, ysize)
        self.numCells = xsize * ysize
        # good parms gg=.1,gl=.4,a=1.7
        # gg.05, same
        # gg 0.05, gl 0.5
        self.a=1.7
        self.drawmod=20
        self.gg=0.1
        self.gl=0.4
        self.cc=self.gl/5
        self.dkern=array([(0,self.cc,0.0),(self.cc,0,self.cc),(0,self.cc,self.cc)])
        self.iter=0

    def iterate(self):
        """
        Iterate / convolve the matrix
        """



        self.iter += self.iter
        # diffusion
        # save last for spin calc
        #last=ll
        diff=convolve2d(self.matrix, self.dkern, mode='same', boundary='wrap')
        # scale before adding to keep value in <-1,+1> bounds
        diffScaled=((1-self.gl) * self.matrix + diff)
        # scale before adding to keep value in <-1,+1> bounds
        #ll = 1-(a*(diffScaled**2))
        self.matrix = (1-self.gg) * (1- (self.a* (diffScaled**2))) + (self.gg/self.numCells) * sum(self.matrix)

        if (self.iter>1 and self.iter % self.drawmod==0):
            if (self.iter % 80 == 0):
                self.gg=self.gg+.001
                #a=a-.001
                if self.gg<.04 : self.gg=self.gg+.02
