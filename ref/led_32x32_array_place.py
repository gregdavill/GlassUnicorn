# To run, open the KiCad scripting console and type: exec(open('../../ref/led_32x32_array_place.py').read())
# 
# This script will re-position D[1-1024] into a matrix filling the specified width and height, at the location provided below.
# After running you will have to press F11/F12 to force the screen to re-render.

import sys
from pcbnew import *
pcb = GetBoard()


initialX = FromMM(120.75)
initialY = FromMM(70.75)

width = FromMM(61)
height = FromMM(61)

padding = FromMM(1.1)

count = 32

spacingX = (width - (padding*2)) / (count - 1)
spacingY = (height - (padding*2)) / (count - 1)

print(f'Spacing X,Y = {spacingX},{spacingY}')


nCount = 1

print('Start Place')
for y in range(count):
    for x in range(count):
        Ref = f'D{nCount}'
        nCount = nCount + 1
        #print(Ref)
        try:
            nPart = pcb.FindModuleByReference(Ref)
            nPart.SetPosition(wxPoint(initialX + padding + (x*spacingX), (initialY + padding + y*spacingY)))  # Update XY
        except:
            pass
        
        
print('Finished Place')

