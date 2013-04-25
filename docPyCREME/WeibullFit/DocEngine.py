__all__ = ['DocEngine']
import sys
import os
import numpy as np
import time
class DocEngine(object):
    '''Class implementing a file to read and write
    '''
    sTitle   = '#Title:'
    sVersion = '#Version:'
    sDate    = '#Date:'
    sDescrip = '#Description:'
    sVars    = '#Variables:'
    sTbName  = '#TbName:'

    tPos = 0
    vPos = 1
    dPos = 2
    date = time.strftime('%a %b %d %H:%M:%S %Y', time.localtime(time.time()))

    def __init__(self, fname, cmtHeader=[]):
        '''
        :param fname reference to file name when need to be opened (string)
        :param cmtHeader reference to  including three elements as [title,version,date] (list)
        '''
        if not fname: return
        self._fname = fname
        self._cmtHeader = cmtHeader
        self.fout = None

        #if cmtHeader is None, read file ,else write file
        if not cmtHeader:

            self._cmtHeader = ['']*3
            self._records = []
            self._tbNames = []
            self._variables = []
            self.readDoc()
        else:
            self.openFile()
            cmtHeader[self.dPos] = self.date
            self.commentHeader()

    def __del__(self):
        '''Private method to close opened file after write file
        '''
        self.closeFile()

    def readDoc(self):
        '''Public method to read file
        '''
        if not os.path.exists(self._fname): return
        blkRecords = None
        with open(self._fname) as fin:
            for l in fin:
                if 0 == len(l.strip()): continue
                elif l.startswith(self.sTitle) or\
                     l.startswith(self.sVersion) or\
                     l.startswith(self.sDate):
                    l = l.strip()
                    toks = l.split(':',1)
                    if toks[0]+':' == self.sTitle:
                        self._cmtHeader[self.tPos] = toks[1]
                    elif toks[0]+':' == self.sVersion:
                        self._cmtHeader[self.vPos] = toks[1]
                    else:
                        self._cmtHeader[self.dPos] = toks[1]
                elif l.startswith(self.sDescrip):
                    for l in fin:
                        if 0 == len(l.strip()): break
                elif l.startswith(self.sVars):
                    if isinstance(blkRecords, list):
                        self._records.append(blkRecords)
                    blkRecords = []
                    l = l.strip()
                    toks = l.split(':')
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

                elif l.startswith(self.sTbName):
                    l = l.strip()
                    toks = l.split(':')
                    for l in fin:
                        if 0 == len(l.strip()): break
                        l = l.strip()
                        #one data of every group is a tuple
                        toks = tuple(l.split())
                        length =len(toks)
                        if length%varCnt != 0: raise ValueError
                        #every group is a dict,including a series of tuples
                        blkRecords.append(toks)
                elif not l.startswith('#'):
                        l = l.strip()
                        toks = tuple(l.split())
                        length =len(toks)
                        if length%varCnt != 0: raise ValueError
                        blkRecords.append(toks)
            else:
                if isinstance(blkRecords, list):
                    self._records.append(blkRecords)

    def getCommentHeader(self, idx=0):
        '''
        :param idx reference to get which one of title,version,and date
        :      idx=0 -> title
        :      idx=1 -> version
        :      idx=2 -> date
        '''
        if not isinstance(idx, int): return
        try:
            header = self._cmtHeader[idx]
        except IndexError: return
        return header

    def getRecords(self, idx=0):
        '''
        :param idx reference to get records belong to which block
        '''
        #if not isinstance(idx, int): return
        #try:
            #records = self._records[idx]
        #except IndexError: return
        #return records
        return self._records

    def getVars(self,idx=0):
        '''
        :param idx reference to get the format belong to which block
        '''
        #if not isinstance(idx, int): return
        #try:
            #variables = self._variables[idx]
        #except IndexError: return
        #return variables
        return self._variables

    def getTbNames(self):
        return self._tbNames

    def commentHeader(self):
        '''
        :param cmtHeader reference to title,version,date (list)
        '''
        self.fout.write('%s\t%s\n%s\t%s\n%s\t%s\n' % (self.sTitle,   self._cmtHeader[self.tPos],\
                                                      self.sVersion, self._cmtHeader[self.vPos],\
                                                      self.sDate,    self._cmtHeader[self.dPos]))

    def commentDescrip(self,descrip=None):
        if not isinstance(descrip, basestring): return
        self.fout.write('\n%s\n%s\n' % (self.sDescrip, descrip))

    def commentVar(self, variables=None):
        '''
        :param variables reference to block records' format (list)
        :eg:[('time','day'),('latitude','deg'),('altitude','km')]
        '''
        if not isinstance(variables, list) or not variables: return
        varCnt = len(variables)
        self.fout.write('\n%s\t%d\n' % (self.sVars, varCnt))
        for idx in range(varCnt):
            var = variables[idx]
            self.fout.write('#\t%d\t%s\t[%s]\n' % (idx+1, var[0], var[1]))

    def saveBlockRecords(self, blockRecords=None, blockTbNames=None, fmt='%12g'):
        '''
        :param blockRecords reference to records with same format (list)
        :param blockTbNames reference to names of data groups (list)
        '''
        if not isinstance(blockRecords, list) or not blockRecords: return
        fout = self.fout
        for idx, grpData in enumerate(blockRecords):
            if not blockTbNames:
                fout.write('\n')
            else:
                fout.write('\n%s\t%s\n' % (self.sTbName, blockTbNames[idx]))
            np.savetxt(fout, grpData,fmt=fmt)

    def openFile(self):
        self.fout = open(self._fname, 'w')

    def closeFile(self):
        if not self.fout: return
        self.fout.close()




if __name__ == "__main__":
    commentHeader = ['Gnuplot File Created by Genius TCAD Simulation',
               'pyCREME 1.0',
               None]
    variables = [('Energy','Mev'), ('Fluxes','protons/m**2-sr-s')]
    descrip = '''#Created by CREME96:GTRANS_DRIVER Version  210 on  20130331 at 083435.7
    #Incl =  51.600 deg  Apo = 0.5000E+03 Peri = 0.5000E+03 km   0.00   0.00   0.00
    #ISTORM = 1 IPRECALC = 0  Grid Epoch = 1980.0   L Bin: 0.0000E+00 0.1000E+07
    #Relative dwell time = 0.1000E+01'''
    hData = np.column_stack(([1,2,3,4,5], [2,3,4,5,6]))
    eData = np.column_stack(([12,43,23,14,165,222], [123,43,54,23,23,555]))

    blockRecords = [hData, eData]
    fname = '/home/xcl/docTest_1.dat'

    #_docEngine = DocEngine(fname, commentHeader)
    #_docEngine.commentDescrip(descrip)
    #_docEngine.commentVar(variables)
    #_docEngine.saveBlockRecords(blockRecords)


    _docEngine = DocEngine(fname)
    print '@@@@@@@  header =',_docEngine.getCommentHeader()
    print "&&&&&&  vars =",_docEngine.getVars()
    print "$$$$$$  records =",_docEngine.getRecords()