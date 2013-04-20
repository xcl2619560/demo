__all__ = ['DocEngine']
import sys
import os
import numpy as np
class DocEngine(object):
    tPos = 0
    vPos = 1
    dPos = 2
    varPos = 3
    lbPos = 4

    def __init__(self, fname):
        self._fname = fname
        self._records = []
        self._labels = []
        self._variables = []
        self.comment = None


    def readDoc(self):
        with open(self._fname) as fin:
            for l in fin:
                if 0 == len(l.strip()): continue
                elif l.startswith('#Title:'):
                    pass
                elif l.startswith('#Version:'):
                    pass
                elif l.startswith('#Date:'):
                    pass
                elif l.startswith('#Variables:'):
                    try:
                        self._labels.append(grpLabels)
                        self._records.append(grpRecords)
                    except UnboundLocalError: pass
                    grpLabels = []
                    grpRecords = []
                    l = l.strip()
                    toks = l.split()
                    varCnt = int(toks[1], 10)

                    # read varCnt row continuously
                    variables = []
                    cnt = varCnt
                    for l in fin:
                        cnt -= 1
                        if cnt < 0: break
                        l = l.strip()
                        toks = l.split()
                        variables.append(toks[2])
                    self._variables.append(variables)

                elif l.startswith('#Label:'):
                    l = l.strip()
                    toks = l.split()
                    grpLabels.append(toks[1])
                    for l in fin:
                        if 0 == len(l.strip()): break
                        l = l.strip()
                        #one data of every group is a tuple
                        toks = tuple(l.split())
                        length =len(toks)
                        if length%varCnt != 0: raise ValueError
                        #every group is a dict,including a series of tuples
                        grpRecords.append(toks)
            else:
                try:
                    self._labels.append(grpLabels)
                    self._records.append(grpRecords)
                except UnboundLocalError: pass

    def getColumn(self):
        pass
    def getRecords(self):
        return self._records

    def getVars(self):
        return self._variables

    def getLabels(self):
        return self._labels

    def writeDoc(self):
        with open(self._fname, 'w') as fout:
            self.commentOut(fout)

    def updateComment(self, comment=None):
        '''
        :param comment: A dict including five elements as title,version,date,variables,label
        '''
        self.comment = comment

    def commentOut(self, fout):
        fout.write('#Title:\t%s\n#Version:\t%s\n#Date: %s\n\n' %\
                   tuple(self.comment[:3]))

        varCnt = len(self.comment[3])
        fout.write('#Variables:\t%s\n' % varCnt)
        for idx in range(varCnt):
            fout.write('#\t%d\t%s\t[%s]\n' % \
                       (idx+1, self.comment[self.varPos][idx][0], self.comment[self.varPos][idx][1]))





if __name__ == "__main__":
    #fname = '/home/xcl/fTest.dat'
    comment = ['Gnuplot File Created by Genius TCAD Simulation',
               'pyCREME 1.0',
               'Fri Jan  7 22:10:26 2011',
               [('time','day'),('longitude','deg'),('latitude','deg')]]
    fname = '/home/xcl/docTest.dat'
    _docEngine = DocEngine(fname)
    #_docEngine.readDoc()
    _docEngine.updateComment(comment)
    _docEngine.writeDoc()
    print "&&&&&&  vars =",_docEngine.getVars()
    print "$$$$$$  records =",_docEngine.getRecords()
    print "@@@@@@  labels =", _docEngine.getLabels()