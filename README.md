A script to check for annular ring violations
both for TH pads and vias 
requirements: KiCAD pcbnew >= 4.0
annular.py release "1.5.1"

annular.py checking PCB for Annular Ring in Vias and TH Pads
(SMD, Connector and NPTH are skipped)
default Annular Ring >= 0.15 both for TH Pads and Vias
to change values modify:

    AR_SET = 0.150   #minimum annular accepted for pads
    AR_SET_V = 0.150  #minimum annular accepted for vias


Open Python Scripting console in pcbnew and digit:
execfile("annular.py")

## todo
- add colors to print
