# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 20:31:06 2020

@author: jschuurmans
"""

#%% =============================================================================
# imports
from psychopy import core, gui, data
import os
import numpy as np
import glob
import copy
import math
from PIL import Image
import numpy.random as rnd          # for random number generators
import random

#%% =============================================================================
#paths
baseFolder = ''
#commented out, this is just for testing in Spyder
#baseFolder = 'C:\\Users\\jolien\\Documents\\3T_RPinV1\\recurrentSF_3T_CodeRepo\\mainExpCode\\'

dataPath = baseFolder + 'data'
stimPath = baseFolder + 'stimuli'
backPath = baseFolder + 'background'
seqLocation = baseFolder + 'sequence_withinBlock.txt'


#%% =============================================================================
# a block contains 20 unique images + their mask
monRR = 60 # refresh rate on monitor is 60Hz
frame = 1000/monRR # one 
durCond = [3, 5, 6, 9] #50, 83.33, 100, 150 ms
durCondNames = [str(int(durCond[0]*frame)),str(int(durCond[1]*frame)),str(int(durCond[2]*frame)),str(int(durCond[3]*frame))]
typCond = ['Int', 'Neg', 'Scr']
sfType = ['LSF', 'HSF']
nCond = len(durCond)*len(typCond)*len(sfType) #nr of conditions = 24

nBlockPerCond = 20 #nr of blocks per condition (in total)
nUniBlocks = int(nBlockPerCond/2) #nr of unique blocks per condition = 10 (10 sequences to make)
nBlocks = nCond*nBlockPerCond # 264 blocks in total

nRuns = 20 # runs for whole exp
nBlocksRun = nBlocks/nRuns # so... 24 blocks per run --> PICKLE IT :)

durBlock = 10 # seconds
nStim = 20 # stimuli per block
nPositions = 24 # 24 positions in a block (for stim distribution)

fixStEn = 12 # Duration of fixation at begin/end of run in ms

colourChange = (0.8, 1.0, 1.0) #(0, 1.0, 1.0) = too red

#%% =============================================================================

# Get subject participant ID through a dialog box
expName = 'Sequence creator'
expInfo = {
        '1. Participant ID': '',
        '2. Screen hight in px': '1080', #1080
        '3. Screen width in px': '1920', #1920
        '4. Screen hight in cm': '39', #39
        '5. distance to screen': '200', #200cm
        }

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

dataPath = os.path.join(dataPath, expInfo['1. Participant ID'])
# Make sure there is a path to write away the data
if not os.path.isdir(dataPath):
    os.makedirs(dataPath)
    
#http://whatismyscreenresolution.net/
scrsize = (int(expInfo['3. Screen width in px']),int(expInfo['2. Screen hight in px']))
r = scrsize[1] # Vertical resolution of the monitor
h = int(expInfo['4. Screen hight in cm']) # Monitor height in cm
d = int(expInfo['5. distance to screen']) # Distance between monitor and participant in cm
    

#%% =============================================================================
#make checkerboard face/background and their inverts
size_in_deg = 0.6 # The checker size in degrees
# Calculate the number of degrees that correspond to a single pixel. This will
# generally be a very small value, something like 0.03.
deg_per_px = math.degrees(math.atan2(.5*h, d)) / (.5*r)
print(str(deg_per_px) + 's degrees correspond to a single pixel')
# Calculate the size of the stimulus in degrees
check_size = int(size_in_deg / deg_per_px) #The size of the checkers in pixels
n_checks = math.ceil((550/check_size)/2)
checkerboard = np.kron([[255, 0] * n_checks, [0, 255] * n_checks] * n_checks, np.ones((check_size, check_size)))
checkerboard = np.delete(np.delete(checkerboard,np.s_[550:],0),np.s_[550:],1)
masks  = glob.glob(os.path.join(baseFolder + '*.bmp'))
masks.sort()

for maskim in masks:
    checkycheck = copy.deepcopy(checkerboard)
    themask = np.array(Image.open(maskim))
    checkycheck[themask] = 127.5
    checkerOri = checkycheck.astype(np.uint8)
    checkerOri = Image.fromarray(checkerOri)
    #checkerOri.show()
    toSave = os.path.join(dataPath, 'checkerOri_'+ maskim[-8:])
    checkerOri.save(toSave)
    del checkerOri
    checkycheck = copy.deepcopy(checkerboard)
    checkycheck = 255-checkycheck
    checkycheck[themask] = 127.5
    checkerInv = checkycheck.astype(np.uint8)
    checkerInv = Image.fromarray(checkerInv)
    toSave = os.path.join(dataPath, 'checkerInv_'+ maskim[-8:])
    checkerInv.save(toSave)
    del checkerInv

#%% =============================================================================
#make a list for the nr of blocks
#making sure that same conditions never follow eachother
#and some conditions dont follow a specific condition more often than others

print('Making block sequences...')
blockSeq = []
cond = (list(range(nCond)))
posCombi = np.zeros((nCond,nCond))
step = nCond-1
for run in range(nRuns):# 20 times
    #print('Making block sequence for run: ' + str(run))
    rnd.shuffle(cond) #shuffle the conditions
    restart = True
    while restart:
        temPosCombi = copy.deepcopy(posCombi) #copy the pos positions
        for time in range(step): #for all the possible steps in conditions
            num1 = cond[time]#take a number from the condition list
            num2 = cond[time+1]#take a second number from cond list
            #print('time: ' +str(time)+ ', numbers: '+str(num1) + 'and'+ str(num2))
            
            if num1 == num2 or temPosCombi[num1,num2] == 2: #if numbers are the same or following each other
                #print('booop! Same num: ' + str(num1 == num2) +', bouble step: '+ str(temPosCombi[num1,num2] == 2))
                rnd.shuffle(cond) #shuffle the condition list again
                temPosCombi = copy.deepcopy(posCombi) #reset the possible conditions
                break #get out of this loop
            elif time == 22:
                #print('check: is it time 22?')
                toAdd = copy.deepcopy(cond)
                blockSeq.append(toAdd)
                restart = False
                temPosCombi[num1,num2] += 1

                
        posCombi = copy.deepcopy(temPosCombi)    
#print('done: ' +str(blockSeq))


logLocationBlockSeq = os.path.join(dataPath, expInfo['1. Participant ID'] + 'blockSeq.txt')


with open(logLocationBlockSeq, 'w') as f:
    for item in blockSeq:
        for x in item:
            f.write("%s," % x)
        f.write("\n") 


#%% =============================================================================
#20 blocks per condition (10 unique ones times 2)

print('Making background sequences...')
#sequence for background:
backSeq = []
backList = (list(range(nUniBlocks)))
k=0
while k < nCond:# every row is a conditon/run
    random.shuffle(backList) #every column is a block
    toAdd = copy.deepcopy(backList) # every number is a background type
    toAdd2 = copy.deepcopy(backList)
    random.shuffle(toAdd2)
    toAdd.extend(toAdd2)
    backSeq.append(toAdd) 
    k +=1

logLocationBackSeq = os.path.join(dataPath, expInfo['1. Participant ID'] + 'backSeq.txt')

with open(logLocationBackSeq, 'w') as f:
    for item in backSeq:
        for x in item:
            f.write("%s," % x)
        f.write("\n")  
  

#%% =============================================================================
# blockSeq is the order of blocks within a run..
#stimSeq is the order of stimuli within each block

print('Making stimulus sequences...')
#seqLocation = 'sequence_withinBlock.txt'
stimSeq = []
stimSeq = np.genfromtxt(seqLocation,dtype='int',delimiter=',') #seq within blocks

np.random.shuffle(stimSeq)
toAdd = copy.deepcopy(stimSeq)
np.random.shuffle(toAdd)
stimSeq = np.append(stimSeq,toAdd,axis=0) # 10 unique blocks, repeted twice for p
# 20 stim per block (columns) + their position for all blocks (20per cond)


logLocationStimSeq = os.path.join(dataPath, expInfo['1. Participant ID'] + 'stimSeq.txt')


with open(logLocationStimSeq, 'w') as f:
    for item in stimSeq:
        for x in item:
            f.write("%s," % x)
        f.write("\n")


#%% =============================================================================

print('DONE!! TIME FOR THE EXPERIMENT!')