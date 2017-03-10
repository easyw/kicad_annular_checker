# -*- coding: utf-8 -*-
#
# A script to check for annular ring violations
# both for TH pads and vias 
# requirements: KiCAD pcbnew >= 4.0
# annular.py release "1.5.1"
# 
# annular.py checking PCB for Annular Ring in Vias and TH Pads
# (SMD, Connector and NPTH are skipped)
# default Annular Ring >= 0.15 both for TH Pads and Vias
# to change values modify:
# 
#     AR_SET = 0.150   #minimum annular accepted for pads
#     AR_SET_V = 0.150  #minimum annular accepted for vias
# 
# 
## Open Python Scripting console in pcbnew and digit:
## execfile("annular.py")
#

## todo
# add colors to print

import sys
import pcbnew
from pcbnew import *

___version___="1.5.3"

mm_ius = 1000000.0
# (consider always drill +0.1)
DRL_EXTRA=0.1
DRL_EXTRA_ius=DRL_EXTRA * mm_ius

AR_SET = 0.150   #minimum annular accepted for pads
MIN_AR_SIZE = AR_SET * mm_ius

AR_SET_V = 0.125  #minimum annular accepted for vias
MIN_AR_SIZE_V = AR_SET_V * mm_ius

def annring_size(pad):
    # valid for oval pad/drills
    annrX=(pad.GetSize()[0] - (pad.GetDrillSize()[0]+DRL_EXTRA_ius))/2
    annrY=(pad.GetSize()[1] - (pad.GetDrillSize()[1]+DRL_EXTRA_ius))/2
    #annr=min(pad.GetSize()) - max(pad.GetDrillSize())
    #if annr < MIN_AR_SIZE:
    #print annrX
    #print annrY
    #print pad.GetSize()[0]/mm_ius
    #print pad.GetSize()[0]#/mm_ius
    #print pad.GetDrillSize()[0]#/mm_ius
    #print DRL_EXTRA_ius
    #print pad.GetDrillSize()[0]/mm_ius
    #print (pad.GetDrillSize()[0]+DRL_EXTRA_ius)/mm_ius
    #print annrX/mm_ius
    return min(annrX,annrY)

def annringNP_size(pad):
    # valid for oval pad/drills
    annrX=(pad.GetSize()[0] - (pad.GetDrillSize()[0]))/2
    annrY=(pad.GetSize()[1] - (pad.GetDrillSize()[1]))/2
    #annr=min(pad.GetSize()) - max(pad.GetDrillSize())
    #if annr < MIN_AR_SIZE:
    #print annrX
    #print annrY
    #print pad.GetSize()[0]/mm_ius
    #print pad.GetSize()[0]#/mm_ius
    #print pad.GetDrillSize()[0]#/mm_ius
    #print DRL_EXTRA_ius
    #print pad.GetDrillSize()[0]/mm_ius
    #print (pad.GetDrillSize()[0]+DRL_EXTRA_ius)/mm_ius
    #print annrX/mm_ius
    #return min(annrX,annrY)
    return annrX,annrY

def vias_annring_size(via):
    # calculating via annular
    annr=(via.GetWidth() - (via.GetDrillValue()+DRL_EXTRA_ius))/2
    #print via.GetWidth()
    #print via.GetDrillValue()
    return annr
    
def f_mm(raw):
    return repr(raw/mm_ius)

board = pcbnew.GetBoard()
PassC=FailC=0
PassCV=FailCV=0

PassCN=FailCN=0
PassCVN=FailCVN=0


print("'annular.py'\nTesting PCB for Annular Ring TH Pads >= "+repr(AR_SET)+" Vias >= "+repr(AR_SET_V)+"\nPHD margin on PTH = "+ repr(DRL_EXTRA))

print("version = "+___version___)

# print "LISTING VIAS:"
for item in board.GetTracks():
    if type(item) is pcbnew.VIA:
        pos = item.GetPosition()
        drill = item.GetDrillValue()
        width = item.GetWidth()
        ARv = vias_annring_size(item)
        if ARv  < MIN_AR_SIZE_V:
        #            print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
            XYpair =  item.GetPosition()
            print("AR Via violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) )
            FailCV = FailCV+1
        else:
            PassCV = PassCV+1
    #print type(item)
print("VIAS that Pass = "+repr(PassCV)+" Fails = "+repr(FailCV))

for module in board.GetModules():
    for pad in module.Pads():
        #print(pad.GetAttribute())
        if pad.GetAttribute() == PAD_ATTRIB_STANDARD: #TH pad
            ARv = annring_size(pad)
            #print(f_mm(ARv))
            if ARv  < MIN_AR_SIZE:
#                print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
                XYpair =  pad.GetPosition()
                print("AR PTH violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) )
                FailC = FailC+1
            else:
                PassC = PassC+1
        if pad.GetAttribute() == PAD_ATTRIB_HOLE_NOT_PLATED:
            ARvX, ARvY = annringNP_size(pad)
            #print(f_mm(ARvX));print(f_mm(ARvY))
            if (ARvX) != 0 or ARvY != 0:
                ARv = min(ARvX, ARvY)
                if ARv < MIN_AR_SIZE:
#                    print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
                    XYpair =  pad.GetPosition()
                    print("AR NPTH warning of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) )
                    FailCN = FailCN+1
                else:
                    PassCN = PassCN+1
            else:
                PassCN = PassCN+1
            
print("TH PADS that Pass = "+repr(PassC)+" Fails = "+repr(FailC))

print("NPTH PADS that Pass = "+repr(PassCN)+" Fails = "+repr(FailCN))


#  execfile("annular.py")
# annular.py Testing PCB for Annular Ring >= 0.15
# AR violation of 0.1 at XY 172.974,110.744
# VIAS that Pass = 100 Fails = 1
# AR violation of 0.1 at XY 172.212,110.744
# AR violation of 0.0 at XY 154.813,96.52
# PADS that Pass = 49 Fails = 2

