# -*- coding: utf-8 -*-
"""
Lower SNR test per subject
Created on Tue Jan 17 13:12:29 2023

@author: jschuurmans
"""

#%% =============================================================================
# imports

from psychopy import visual, event, core, gui, data
import os  
import numpy.random as rnd          # for random number generators
import glob
import numpy as np
import random
import copy
from PIL import Image
import _pickle as pickle
import itertools
import csv

#%% =============================================================================
# Experimental settings
def lowerSNRtest(base_path,exp_info,data_path_sub):
    # ================================================================
    ## experimental settings
    maskpresent = 0
    
    screennr=2
    stimSize = 550
    
    #### settings; check paper of alexia
    nStim = ['25', '30', '35'] # signals to test
    #nStim = ['15', '25', '35'] # signals to test
    nTrials = 20 # trials per condition
    nFaces = 10 # per gender
    cond = ['male', 'female'] # or inversion ['upright' 'inverted']
    ## ID 1-10 = female / 11-20 = male
    
    desiredAcc = 80 # desired percentage correct 
    
    # one trial is 500ms minimally
    trialFix = 100
    stimdur = 200 # ms to present stimulus for  
    isi = 200 # or untill response
    maskdur = 166
    
    background = '1'
    
    #keys at spinoza
    right_index_finger = 'b' ### male
    right_middle_finger = 'y' ### female
    #right_ring_finger = 'g'
    #right_pinky_finger = 'r'
    #left_index_finger = 'e' ### male
    #left_middle_finger = 'w' ### female
    #left_ring_finger = 'n'
    #left_pinky_finger = 'd'
    

    # ================================================================
    ## paths
    stim_path = f'{base_path}stimuli/'
    mask_path = f'{base_path}masks/'
    back_path = f'{base_path}background/'
    data_path = f'{base_path}data/'
    save_path = f'{base_path}saved_images/' ####### for screenshotting a trial


    # ================================================================
    ## define nested functions
    def escape_check(keys,win,logfile):
        if keys != []:
            # close window and logfile if escape is pressed
            if 'escape' in keys[0]:
                win.close()
                logfile.close()
                core.quit()
    
    def keyCheck(keyList, win, clock, logfile,  catchStart, rt, response_key,end_trial):
        if end_trial:
            keys = event.waitKeys(keyList=keyList, timeStamped=clock)
        else:
            keys = event.getKeys(keyList=keyList, timeStamped=clock)
        if not keys == []:
            escape_check(keys,win,logfile)  
            response_time = keys[-1][1]
            response_key = keys[-1][0]
            rt = (response_time - catchStart)*1000
            print(f'Reactiontime: {int(rt)}ms' )
        elif not keys == []:
            escape_check(keys,win,logfile)
        return rt,response_key
    
    def calc_acc_condition(seq, condition):
        corr = 0
        cond_list = []
        for item in seq:
            if item[0] == condition:
                cond_list.append(item)
                corr += int(item[1])
        return (100/len(cond_list))*corr

    def optimal_signal(input_list, input_value):
        array = []
        for value in input_list:
            array.append(input_list[value])
        arr = np.asarray(array)
        y = (np.abs(arr - input_value)).argmin()
        value = [i for i in input_list if input_list[i]==arr[y]]
        return int(value[0])


    # ================================================================
    ## monitor setup + subject info
    snr_info = copy.deepcopy(exp_info)
    
    snr_info['exp_name'] = 'Lower SNR test'
    snr_info['date'] = data.getDateStr()
    snr_info['3. Run number'] = '00'
    
    debugging = int(snr_info['7. Debugging'])

    if snr_info['5. Screen'] == 'BOLD':
        framerate = 120
        screensize = [1920, 1080]
    elif snr_info['5. Screen'] == 'Dell':
        framerate = 60
        screensize = [1920, 1200]
    
    framelength = 1000/(float(framerate))
    fixFr = round(trialFix/framelength)
    stimFr = round(stimdur/framelength)
    isiFr = round(isi/framelength)
    maskFr = round(maskdur/framelength) 

    logname = data_path_sub + snr_info['1. Subject (e.g. sub-00)']
    
    # save file with subject info
    info_name = f'{logname}_subject-info.csv'
    info_file = open(info_name,'a',encoding='UTF8', newline='')
    
    # write header if it is the first session
    header_names = list(snr_info.keys())
    writer_log = csv.DictWriter(info_file, fieldnames=header_names)
    writer_log.writeheader()
    writer_log.writerow(snr_info)
    info_file.close()

    # ================================================================
    ## make / get sequences
    ##### make a position list
    faceList = list(range(1, int(nTrials+1)))
    
    stimList = faceList * len(nStim)
    rnd.shuffle(stimList)
    condList = nStim * nTrials
    rnd.shuffle(condList)
    
    
    trialList = {}
    for trialnum, face in enumerate(stimList):
        signal = condList[trialnum]
        # female = BG1_ID1 - BG1_ID10
        # male = BG1_ID11 - BG1_ID20
        name = f'BG{background}_ID{face}-{signal}.bmp'
        mask = f'BG{background}_ID{face}-BB.bmp'
        back = f'BG{background}.bmp'
        if face < 11:
            gender = 'female'
        else:
            gender = 'male'
        
        trialList[f'trial-{trialnum}'] = {
            'faceID' : str(face),
            'signal' : signal,
            'gender' : gender,
            'start_trial' : '',
            'end_trial' : '',
            'response' : '',
            'acc' : '',
            'rt' : '',
            'fixPath' : os.path.join(back_path,back),
            'stimPath' : os.path.join(stim_path,name),
            'maskPath' : os.path.join(mask_path,mask),
            'isiPath' : os.path.join(back_path,back)}
        
    
    if maskpresent == 1:
        trial_screens = {'fix' : str(fixFr),
                         'stim' : str(stimFr),
                         'mask' : str(isiFr),
                         'isi' : str(maskFr)}
    else:
        trial_screens = {'fix' : str(fixFr),
                         'stim' : str(stimFr),
                         'isi' : str(maskFr)}
        
    # ================================================================
    ## open log file
    dataName = f'{logname}_SNRtest_{snr_info["date"]}.csv'
    logfile = open(dataName,'a',encoding='UTF8', newline='')
    
    # write header if it is the first session
    header_names = list(trialList['trial-0'].keys())
    writer_log = csv.DictWriter(logfile, fieldnames=header_names)
    writer_log.writeheader()
    #logfile.close()

    # ================================================================
    #window setup
    win = visual.Window(size=screensize, color='grey', units='pix', fullscr=True, screen = screennr)
    instructiontexts = {}
    instructiontexts['inst1'] = 'Welcome to the first part.\nHopefully you are comfortable.\n\nFor this part, faces will appear in the centre of the screen.\nWhile looking at the centre of the fixation cross, you\'ll have to indicate whether the face is male or female.\n\n\nPress a button to continue.'
    instructiontexts['inst2'] = 'If the face is male:\nPress with your index finger\n\nIf the face is female:\nPress with your middle finger\n\n\nPress a button to continue.'
    instructiontexts['inst3'] = 'Lets test the keys!\n\nPress the button\nwith your index finger.\n\n(male face)'
    instructiontexts['inst4'] = 'Great!\n\nNow press the button\nwith your middle finger.\n\n(female face)'
    instructiontexts['inst5'] = 'It works!\n\nJust to remind you..\nIf the face is male:\nPress with your index finger\n\nIf the face is female:\nPress with your middle finger\n\n\nAre you ready for the task?\n\nPress any button to start.'
    
    textpage = visual.TextStim(win, height=32, color= 'black')
    #keyList = list('bygrewnd')
    keyList = list('by')
    keyList.append('escape')
    
    #create fixation cross
    fix1=visual.Line(win,start=(-stimSize,-stimSize),end=(stimSize, stimSize),
                     pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')
    fix2=visual.Line(win,start=(-stimSize,stimSize),end=(stimSize, -stimSize),
                     pos=(0.0, 0.0),lineWidth=1.0,lineColor='black',units='pix')
    win.mouseVisible = False
    win.flip()
    for instnr in instructiontexts:
        instructions = textpage
        instructions.text = instructiontexts[instnr]
        instructions.draw()
        win.flip()
        if debugging == 1:
            win.getMovieFrame() ####### for screenshotting a trial
            win.saveMovieFrames(f'{save_path}_SNRtest_{instnr}.bmp')
        if instnr == 'inst3':
            waitkey = list(right_index_finger) ### male
            waitkey.append('escape')
        elif instnr == 'inst4':
            waitkey = list(right_middle_finger) ### female
            waitkey.append('escape')
        else:
            waitkey = keyList
        keys = event.waitKeys(keyList=waitkey)#core.wait(.1)
        escape_check(keys,win,logfile)
        win.flip()
        #win.close()
    
    
    # ================================================================
    ## SNR experiment
    
    #draw fixation
    fix1.setAutoDraw(True)
    fix2.setAutoDraw(True)
    
    # prepare clock
    clock = core.Clock()
    
    # clear any previous presses/escapes
    response = []
    corrResp = 0
    rt = None
    response_key = None
    acc_list = []
    
    #start with a short fixation of 3 seconds
    for nFrames in range(round((3000)/framelength)):  #last second of fixation start flipping, to prevent frame drops later on
        win.flip() 
    
    for trialnr,trialid in enumerate(trialList):
        print(trialid)
        # check response
        trialOnsetTime = clock.getTime()
        rt,  response_key = keyCheck(keyList, win, clock, logfile, trialOnsetTime, rt, response_key,0)
        
        
        #prepare images of the trial
        bitmap = {}
        for loadscreen in trial_screens:
            stim = Image.open(trialList[trialid][f'{loadscreen}Path'])
            bitmap[loadscreen]  = visual.ImageStim(win, size=[stimSize,stimSize],image=stim,mask='circle')
        
      
        for trialpart in trial_screens:
            for nFrames in range(int(trial_screens[trialpart])):
                bitmap[trialpart].draw()
                win.flip()
                rt,  response_key = keyCheck(keyList, win, clock, logfile, trialOnsetTime, rt, response_key,0)
            #afterStim = clock.getTime() 
        
        rt,  response_key = keyCheck(keyList, win, clock, logfile, trialOnsetTime, rt, response_key,1)    
        ### check response in the meantime...
        trialList[trialid]['response'] = response_key
        trialList[trialid]['rt'] = rt
        trialList[trialid]['start_trial'] = trialOnsetTime
        trialList[trialid]['end_trial'] = clock.getTime()    
        
        if response_key == right_index_finger and trialList[trialid]['gender'] == 'male' or response_key == right_middle_finger and trialList[trialid]['gender'] == 'female':
            trialList[trialid]['acc'] = 1
        elif response_key == right_middle_finger and trialList[trialid]['gender'] == 'male' or response_key == right_index_finger and trialList[trialid]['gender'] == 'female':
            trialList[trialid]['acc'] = 0
            
        writer_log.writerow(trialList[trialid])
        
        accuracy = [trialList[trialid]['signal'],str(trialList[trialid]['acc'])]
    
        acc_list.append(accuracy)
    
    acclist_per_signal = {}
    for signal_type in nStim:
        acclist_per_signal[signal_type] = calc_acc_condition(acc_list, signal_type)
        
    low_sign = optimal_signal(acclist_per_signal, 85) ################################################### signal closest to 85% correct
    high_sign = int(low_sign + 25)
    typCond = [str(high_sign), str(low_sign), '0'] 
    
    end_info = copy.deepcopy(trialList[trialid])
    end_info['faceID'] = f'signal{nStim[0]}'
    end_info['signal'] = acclist_per_signal[nStim[0]]
    end_info['gender'] = None
    end_info['start_trial'] = f'signal{nStim[1]}'
    end_info['end_trial'] = acclist_per_signal[nStim[1]]
    end_info['response'] = None
    end_info['acc'] = f'signal{nStim[2]}'
    end_info['rt'] = acclist_per_signal[nStim[2]]
    end_info['fixPath'] = None
    end_info['stimPath'] = None
    end_info['maskPath'] = None
    end_info['isiPath'] = None
    writer_log.writerow(end_info)
    
    # wrap it up
    fix1.setAutoDraw(False)
    fix2.setAutoDraw(False)
    
    endinstr = f'Great job!\n\nJust lay still and relax now\n\nYou can even close your eyes.\n\nThe experimenter will contact you shortly..'
    endinstr = visual.TextStim(win, color='black',height=32,text=endinstr)
    endinstr.draw()
    win.flip()
    
    while not 'x' in event.getKeys():
        core.wait(0.1)

    logfile.close()
    win.close()
    
    return typCond




 



