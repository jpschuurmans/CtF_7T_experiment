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

#base_path = 'C:/Users/Adminuser/Documents/04_CtF-7T/Experiment/mainExpCode/'
base_path = '/home/schuurmans@spinozacentre.knaw.nl/Documents/Experiment/mainExpCode/'

stim_path = f'{base_path}stimuli/'
mask_path = f'{base_path}masks/'
back_path = f'{base_path}background/'
data_path = f'{base_path}data/'
save_path = f'{base_path}saved_images/' ####### for screenshotting a trial

#%% ===========================================================================
# imports


import os
os.chdir(base_path)
import csv
import _pickle as pickle
from psychopy import visual, event, core, gui, data
import numpy as np
import glob
from PIL import Image, ImageOps
from functions_7TCtF import *
from lowerSNRtest import *



#%% ===========================================================================
# different conditions in experiment
screennr=2

stimSize = 550

sfType = ['BB']
durCond = ['50','75','100','150'] #### change however. 


nBlockPerCond = 20 #nr of blocks per condition (in total)

nRuns = 20 # runs for whole exp

durBlock = 10 # seconds
nStim = 20 # unique stimuli per block (nr of faces)
nBack = 20 # nr of different backgrounds
nPositions = 24 # 24 positions in a block (for stim distribution)

fixDur = 10 #seconds
fixStEn = 12 # Duration of fixation at begin/end of run in ms

checkerDur = 10 # seconds
checkerHz = 4

colourChange = (0.25, 1.0, 1.0) #(0, 1.0, 1.0) = too red #(0.8, 1.0, 1.0) = not red enough

maskDur = 166.66667 # ms
trialDur = 416.666667 # ms


#%% ===========================================================================
# monitor setup + subject info

exp_name = 'Backward masking 7T'
exp_info = {
        '1. Subject (e.g. sub-00)' : 'sub-',
        '2. Session' : ('ses-01','ses-02'),
        '3. Run number': ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'),
        '4. Make sequence' : ('no','yes'), 
        '5. Screen' : ('BOLD', 'Dell'),
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


if exp_info['5. Screen'] == 'BOLD':
    framerate = 120
    screensize = [1920, 1080]
elif exp_info['5. Screen'] == 'Dell':
    framerate = 60
    screensize = [1920, 1200]
    
framelength = 1000/(float(framerate))
maskFr = round(maskDur/framelength)
trialFr = round(trialDur/framelength)
endfixFr = round((fixStEn*1000)/framelength)


language = exp_info['6. Prefered language'] 
debugging = int(exp_info['7. Debugging'])

data_path_sub = data_path + exp_info['1. Subject (e.g. sub-00)'] + '/'
# prepare log file to write the data
if not os.path.isdir(data_path_sub):
    os.makedirs(data_path_sub)
logname = data_path_sub + exp_info['1. Subject (e.g. sub-00)']


if debugging == 1:
    fixStEn = 2
    fixDur = 2
    typCond = ['60', '35', '0'] 
else:
    if exp_info['4. Make sequence'] == 'yes':
        # run lower SNR code
        # it should return 
        # typCond = ['60', '35', '0'] 
        typCond = lowerSNRtest(base_path,exp_info,data_path_sub)
        print(f'condition types are: {typCond}')

# save file with subject info ############################## made some changes here. Check
info_name = f'{logname}_subject-info.csv'
info_file = open(info_name,'a',encoding='UTF8', newline='')
runnr = int(int(exp_info['3. Run number']) -1)

# write header if it is the first session
header_names = list(exp_info.keys())
writer_log = csv.DictWriter(info_file, fieldnames=header_names)

writer_log.writerow(exp_info)
info_file.close()

#%% ===========================================================================
# make / get sequences
sequences_pickle = f'{logname}_alltrials-list.pickle'

if exp_info['4. Make sequence'] == 'yes':
    sequences = makeSequences(logname,typCond,sfType,durCond) # self.logname / self.typCond / self.sfType = sfType / self.durCond
    sequences.makeBlockSeq(nRuns) ## Making and saving the sequence of blocks within runs self.blockSeq
    sequences.makeBackSeq(nBack) # self.blockSeq
    sequences.makeStimSeq(nBlockPerCond,nPositions,nStim) # self.stimSeq
    sequences.conditions() # self.conditions dict with all conditions listed (and numbered)

    sequences.makeTrialList(framelength, colourChange, stim_path,mask_path,back_path) # self.allRuns are all runs-blocks-trials in correct order          

    with open(sequences_pickle, 'wb') as file:
        pickle.dump(sequences, file)
        
else:
    #load sequences dict (unpickle it)
    with open(sequences_pickle, 'rb') as file:
        sequences = pickle.load(file)
    
    
#int(time_in_ms/framelength)

#%% =============================================================================
#loading the checkerboards for the last part of the run
checkerboards = []
checkerboards.append(glob.glob(os.path.join(base_path, 'checkerBack*.bmp')))
checkerboards.append(glob.glob(os.path.join(base_path, 'checkerFace*.bmp')))

#load a mask of the face
image = Image.open(f'{mask_path}alphamask.bmp')
facemask = ImageOps.invert(image)
facemask = np.asarray(facemask)

# Convert from integers to floats
facemask = facemask.astype('float32')

# Normalize to the range 0-1
facemask /= 255.0
facemask = 2.*(facemask - np.min(facemask)) / np.ptp(facemask)-1
#%% =============================================================================
# open log file
dataName = f'{logname}_{exp_info["2. Session"]}_run-{exp_info["3. Run number"]}_{exp_info["date"]}.csv'
logfile = open(dataName,'a',encoding='UTF8', newline='')

# write header if it is the first session
header_names = list(sequences.allRuns['run-0']['block-0']['trial0'].keys())
writer_log = csv.DictWriter(logfile, fieldnames=header_names)
writer_log.writeheader()
#logfile.close()


eventfile_info = {
    'onset' : '',
    'duration' : '',
    'trial_type' : ''}
# make a event file to save data with 'comma-separated-values'
eventName = f'{logname}_{exp_info["2. Session"]}_task-mainExp_run-{exp_info["3. Run number"]}_events.csv'
eventfile = open(eventName, 'a',encoding='UTF8', newline='')

header_names = list(eventfile_info.keys())
writer_event = csv.DictWriter(eventfile, fieldnames=header_names)
writer_event.writeheader()
#eventfile.close()


#%% =============================================================================
#window setup

win = visual.Window(size=screensize, color='grey', units='pix', fullscr=True, screen=screennr)
instructiontexts = load_txt_as_dict(f'{base_path}instructions.txt')
textpage = visual.TextStim(win, height=32, color= 'black')
keyList = list(instructiontexts['button1'])
keyList.append('escape')

#create fixation cross
fix1=visual.Line(win,start=(-stimSize,-stimSize),end=(stimSize, stimSize),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')
fix2=visual.Line(win,start=(-stimSize,stimSize),end=(stimSize, -stimSize),
                 pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')
win.mouseVisible = False

for instnr in range(1,3):
    instructions = textpage
    instructions.text = instructiontexts[f'inst{instnr}_{language}']
    instructions.draw()
    win.flip()
    if debugging == 1:
        win.getMovieFrame() ####### for screenshotting a trial
        win.saveMovieFrames(f'{save_path}_instructions{instnr}_.bmp')
    check4key = list(instructiontexts[f'button{instnr}'])
    check4key.append('escape')
    keys = event.waitKeys(keyList=check4key)#core.wait(.1)
    escape_check(keys,win,logfile,eventfile)
    #win.close()


#%% =============================================================================
#main experiment
trialsReady = sequences.allRuns[f'run-{runnr}']



#draw fixation
fix1.setAutoDraw(True)
fix2.setAutoDraw(True)

# prepare clock
clock = core.Clock()

# clear any previous presses/escapes
response = []
corrResp = 0
catchStart = '' #so the code does not crash for keyCheck (only first call)
caught = 1
rt = None
totalCatch = 0
after = {'face' : '',
        'mask' : '',
        'back' : ''}

for blocknr, block in enumerate(trialsReady):
    #start fixation
    fixStart  = clock.getTime()
    eventfile_info['onset'] = str(fixStart)
    eventfile_info['trial_type'] = 'fixation'
    win.flip()
    
    rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)
    
    #preload all stimuli for upcoming block
    toDraw, numFrames = loadblocktrials(win,trialsReady[block],stimSize,maskFr,trialFr, 'circle',0)
    secondDraw, numFrames = loadblocktrials(win,trialsReady[block],stimSize,maskFr,trialFr, facemask,1)
    #if clock hits the fixation time for start/end in seconds, end the fixation
    loadEnd = clock.getTime()
    loadTime = loadEnd-fixStart
    fixdur = loadTime
    print(f'Loading time: {loadTime}')
    
    if blocknr == 0: # first fixation has a different duration
        fixation_dur = fixStEn-1
    else:
        fixation_dur = fixDur-1 

    while fixdur <= fixation_dur: # wait untill there is only 1 sec of fixation left
        fixNow = clock.getTime()
        fixdur = fixNow-fixStart
        rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)
         
    for nFrames in range(round((1000)/framelength)):  #last second of fixation start flipping, to prevent frame drops later on
        win.flip()  
        rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)
        
    #end fixation
    fixEnd = clock.getTime()
    
    #write info to log files
    eventfile_info['duration'] = str(fixEnd-fixStart)
    writer_event.writerow(eventfile_info)
    trial = trialsReady[block]['trial1'] #### for logging info
    fixation_inf = fixinfo(trial, 'fixation', fixStart, fixEnd, loadTime)
    writer_log.writerow(fixation_inf)

    print(f'fixation, dur: {round((fixEnd-fixStart)*1000)} ms, load dur: {round(loadTime*1000)} ms') 
    print(f'Block {blocknr} - vis{trial["SNR"]}_dur{trial["duration"]}')
    if debugging == 1:
        shot = 0 # for screenshotting
    else:
        shot = 1
    
    # ---------------------------------------------------------------------------------        
    #start trials
    for trialnr in trialsReady[block]:
        trial = trialsReady[block][trialnr]
        
        eventfile_info['onset'] = str(fixEnd)
        trial_type = f'vis{trial["SNR"]}_dur{trial["duration"]}' 
        eventfile_info['trial_type'] = trial_type
        
        backFr = trialFr-(int(trial['nframes']) + maskFr)
        
        startTrial = clock.getTime()
        rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)
        
        if trial['catchtrial'] == True: #if its a catchtrail, start the clock
            
            totalCatch += 1
            catchStart = clock.getTime()
            if caught == 1:
                corrResp += 1
            caught = 0
        
        if shot == 0:
            win.getMovieFrame() ####### for screenshotting a trial
            win.saveMovieFrames(f'{save_path}{trial_type}_fix_{trialnr}.bmp')
        
        ############################ flipping of stimuli -> actual trials
        for imtype in toDraw[trialnr]:
            for frame in range(numFrames[imtype]): #stimulus
                toDraw[trialnr][imtype].draw()
                secondDraw[trialnr][imtype].draw()
                win.flip()
                rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)
            after[imtype] = clock.getTime()
            if shot == 0:
                win.getMovieFrame() ####### for screenshotting a trial
                win.saveMovieFrames(f'{save_path}{trial_type}_{imtype}_{trialnr}.bmp')
                if imtype == 'back' and blocknr != 0:
                    shot = 1

        trial['trialStart'] = startTrial
        trial['trialDur'] = round((after['back'] - startTrial) * 1000) 
        trial['stimDur'] = round((after['face'] - startTrial) * 1000)
        trial['maskDur'] = round((after['mask'] - after['face'])*1000)
        trial['rt'] = rt
        rt = None
        writer_log.writerow(trial)

    # end trials
    eventfile_info['duration'] = str(after['back']-fixEnd)
    writer_event.writerow(eventfile_info)
    

# ---------------------------------------------------------------------------------
#one more normal fixation
fixStart = clock.getTime()
for nFrames in range(int((fixDur*1000)/framelength)): # 600 = 10 seconds
    win.flip()
    rt, caught = keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught)
fixEnd = clock.getTime()

#write info to log files
eventfile_info['onset'] = str(fixStart)
eventfile_info['trial_type'] = 'fixation'
eventfile_info['duration'] = str(fixEnd-fixStart)
writer_event.writerow(eventfile_info)
toSave = fixinfo(trial, 'fixation', fixStart, fixEnd, None)
writer_log.writerow(toSave)


# ---------------------------------------------------------------------------------
# checkers
frPerChecker = int(framerate/checkerHz)
checkerRep = int((framerate / (2*frPerChecker)) * checkerDur)

#final face chackerboard, then background checkerboard    
for checks in checkerboards: #checks=1 is face checks=0 is background
    #per part, 10 seconds. 1 cicle (ori+inv) will show 4 times per sec. 
    checkerOri = visual.ImageStim(win=win,size=[stimSize,stimSize], image=Image.open(checks[1]),mask='circle')
    checkerInv = visual.ImageStim(win=win,size=[stimSize,stimSize], image=Image.open(checks[0]),mask='circle')
    checkerTimeStart= clock.getTime()
    for times in range(checkerRep):
        for nFrames in range(frPerChecker): #6 frames = 100ms each -> 5Hz(or10)
            checkerOri.draw()
            win.flip()
        for nFrames in range(frPerChecker): #10 frames = 166.6ms each -> 3Hz (or6)
            checkerInv.draw()
            win.flip()
    checkerTimeEnd = clock.getTime()
    if checks == 1:
        checkName = 'checkers_face'
    else:
        checkName = 'checkers_back'
    print(f'{checkName} {checkerTimeEnd-checkerTimeStart} sec')
    
    #annnddd write it away
    eventfile_info['onset'] = str(checkerTimeStart)
    eventfile_info['trial_type'] = 'checkName'
    eventfile_info['duration'] = str(checkerTimeEnd-checkerTimeStart)
    writer_event.writerow(eventfile_info)
    
    toSave = fixinfo(trial, checkName, checkerTimeStart, checkerTimeEnd, f'{str(checkerHz)}Hz')
    writer_log.writerow(toSave)
    

# ---------------------------------------------------------------------------------
#finalfixationnnn
fixStart = clock.getTime()
for nFrames in range(endfixFr): # 12 sec --> end fixation*refreshrate
    win.flip()
fixEnd = clock.getTime()

#write info to log files
eventfile_info['onset'] = str(fixStart)
eventfile_info['trial_type'] = 'fixation'
eventfile_info['duration'] = str(fixEnd-fixStart)
writer_event.writerow(eventfile_info)
toSave = fixinfo(trial, 'fixation', fixStart, fixEnd, None)
writer_log.writerow(toSave)


# ---------------------------------------------------------------------------------  
# wrap it up
fix1.setAutoDraw(False)
fix2.setAutoDraw(False)
win.mouseVisible = True


timeExp = clock.getTime()
print(f'time exp: {int(timeExp/60)} min ({int(timeExp)} sec)')

percCorr = (100/totalCatch)*corrResp

instruc03 = f'This is the end of run {int(runnr+1)} out of {nRuns}\n\nYou have a score of {round(percCorr)}% \nThank you for paying attention :)\n\nPress \'x\' to close the screen.'
instruc03 = visual.TextStim(win, color='black',height=32,text=instruc03)
instruc03.draw()
win.flip()
while not 'x' in event.getKeys():
    core.wait(0.1)


  
logfile.close()
eventfile.close()
win.close()



