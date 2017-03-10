A script to check for annular ring violations  
for PTH, NPTH pads and vias  

requirements: KiCAD pcbnew >= 4.0  
annular.py release "1.5.2"  

'annular.py' checking PCB for Annular Ring in PTH, NPTH and Vias  
(SMD, Connector and NPTH are skipped)  
default Annular Ring >= 0.15 both for TH Pads and Vias  
to change values modify:  

    AR_SET = 0.150   #minimum annular accepted for pads
    AR_SET_V = 0.150  #minimum annular accepted for vias
    DRL_EXTRA = 0.100 #extra drill margin size for production  

Open Python Scripting console in pcbnew and digit:  
execfile("your_full_path_to/annular.py")  

## todo
- add colors to print
