# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:04:16 2022

@author: JSchuurmans

Experiment code - temporal masking, blocked-design
intact, negated and scrambled faces with their phase scrambled mask. 
4 durations

"""
#%% ===========================================================================
# paths

base_path = 'C:/Users/Adminuser/Documents/04_CtF-7T/Experiment/mainExpCode/'
#base_path = ''

stim_path = f'{base_path}stimuli/'
mask_path = f'{base_path}masks/'
back_path = f'{base_path}background/'
data_path = f'{base_path}data/'
#save_path = f'{base_path}saved_images/' ####### for screenshotting a trial

#%% ===========================================================================
# imports


import os
os.chdir(base_path)
import itertools
import csv
import _pickle as pickle
from psychopy import visual, event, core, gui, data
import numpy as np
import glob
from PIL import Image
import random
import copy
from functions_7TCtF import *







#%% ===========================================================================
# different conditions in experiment
screennr=2

stimSize = 550

typCond = ['Vis', 'Obs', 'Scr']
sfType = ['LSF','HSF']
durCond = ['50','75','100','150'] #### change however. 
#different_conditions = list(itertools.product(spatialfrequencies,durations))
nCond = len(durCond)*len(typCond)*len(sfType)


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


#%% ===========================================================================
# monitor setup + subject info

exp_name = 'Coarse-to-fine backward masking 7T'
exp_info = {
        '1. Subject (e.g. sub-00)' : 'sub-',
        '2. Session' : ('ses-01','ses-02'),
        '3. Run number': ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'),
        '4. Refreshrate(hz)' : ('120','60'), #BOLD screen = 120Hz 
        '5. Screensize' : ('1920 x 1080', '1920 x 1200'),
        '6. Prefered language' : ('en','nl'),
        '7. Debugging' : ('0','1')
        }
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    
# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name
session = exp_info['2. Session']

framerate = exp_info['4. Refreshrate(hz)'] 
framelength = 1000/(float(framerate))

screensizes = exp_info['5. Screensize'].split(' x ')
scrsize = [int(screensizes[0]), int(screensizes[1])]

language = exp_info['6. Prefered language'] 
debugging = int(exp_info['7. Debugging'])

# prepare log file to write the data
if not os.path.isdir(data_path):
    os.makedirs(data_path)
logname = data_path + exp_info['1. Subject (e.g. sub-00)']
    
# save file with subject info
info_name = f'{logname}_subject-info.csv'
info_file = open(info_name,'a',encoding='UTF8')

if exp_info['3. Run number'] == '01':
    header = ''
    for key in exp_info:
        header = header + key + ','
    info_file.write(header + '\n')
info = ''
for key in exp_info:
    info = info + exp_info[key] + ','
info_file.write(info + '\n')
info_file.close()

#%% ===========================================================================
# make / get sequences
if expInfo['5. Make sequence?'] == 'yes':
    ######################################################## 
    #make sequence
    
    
    # ---> block sequence
    # ---> background sequence
    # ---> stimulus sequence

    
    
int(time_in_ms/framelength)


#%% =============================================================================
# open log file

# named f
f = '' #for debugging

#%% =============================================================================
#window setup

win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True)
instructiontexts = load_txt_as_dict(f'{base_path}instructions.txt')
textpage = visual.TextStim(win, height=32, color= 'black')

#create fixation cross
fix1=visual.Line(win,start=(-stimSize,-stimSize),end=(stimSize, stimSize),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')
fix2=visual.Line(win,start=(-stimSize,stimSize),end=(stimSize, -stimSize),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')

for instnr in range(1,3):
    instructions = textpage
    instructions.text = instructiontexts[f'inst{instnr}_{language}']
    instructions.draw()
    win.flip()
    keys = event.waitKeys(keyList=list(instructiontexts[f'button{instnr}']))#core.wait(.1)
    escape_check(keys,win,f)
    #win.close()


#%% =============================================================================
#main experiment
win.mouseVisible = False

#draw fixation
fix1.setAutoDraw(True)
fix2.setAutoDraw(True)

# prepare clock
clock = core.Clock()

# clear any previous presses/escapes
last_response = ''; response_time = ''; reactionTime = '';
response = []




