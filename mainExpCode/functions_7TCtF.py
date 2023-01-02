# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:04:16 2022

@author: JSchuurmans

Experiment code - temporal masking, blocked-design
intact, negated and scrambled faces with their phase scrambled mask. 
4 durations

"""
#%% ===========================================================================
#imports
import json
import numpy.random as rnd   
from math import ceil
import numpy as np
import copy
import os
import random
from PIL import Image
from psychopy import visual, event, core, gui, data

#%% ===========================================================================

## functions

def escape_check(keys,win,logfile,eventfile):
    # close window and logfile if escape is pressed
    if 'escape' in keys[0]:
        win.close()
        logfile.close()
        eventfile.close()
        core.quit()
        
##### key check 
def keyCheck(keyList, win, clock, logfile, eventfile, catchStart, rt, caught):     
    
    keys = event.getKeys(keyList=keyList, timeStamped=clock)
    if not keys == [] and caught == 0:
        escape_check(keys,win,logfile,eventfile)  
        last_response = keys[-1][0] # most recent response, first in tuple
        response_time = keys[-1][1]
        rt = (response_time - catchStart)*1000
        caught = 1
        print(f'Reactiontime is {int(rt)} ms' )
    else:
        rt = 'NaN'
    return rt, caught 

def load_txt_as_dict(path):
    with open(path, 'r', encoding='utf-8') as f:
        instructions = f.read()
    instructiontexts = json.loads(instructions)
    return instructiontexts

def loadblocktrials(win,trialsReady,stimSize):
    stimlist = {}
    #preload all stimuli for upcoming block
    for trialnr in trialsReady:
        trial = trialsReady[trialnr]
        stimuli = {'face' : 'stim',
                   'mask' : 'mask',
                   'background' : 'back'}
        for stim in stimuli:
            # load stimuli --> BG, face and mask
            image = Image.open(os.path.join(trial[f'{stimuli[stim]}_path'], trial[stim]))
            stimuli[stim] = visual.ImageStim(win, size=[stimSize,stimSize],image=image,color=trial['colour'])
        stimlist[trialnr] = stimuli
    return stimlist

def fixinfo(trial, name, fixStart, fixEnd, loadTime):
    eventfile_info = copy.deepcopy(trial)
    for key in trial: # empty the dictionary 
        eventfile_info[key] = None
    # fill out important info
    eventfile_info['block'] = name
    eventfile_info['trialStart'] = str(fixStart)
    eventfile_info['trialDur'] = str(fixEnd-fixStart)
    eventfile_info['maskDur'] = str(loadTime)
    return eventfile_info



#%% ===========================================================================
#classes

class makeSequences(object):
    
    def __init__(self,logname,typCond,sfType,durCond):
        self.logname = logname
        self.typCond = typCond
        self.sfType = sfType
        self.durCond = durCond


    ### Making sequence of blocks within runs
    def makeBlockSeq(self,nRuns): 
        self.nCond = len(self.durCond)*len(self.typCond)*len(self.sfType)
        self.nRuns = nRuns
        print('Making block sequences...')
        rep = 2
        blockSeq = []
        cond = (list(range(self.nCond)))
        posCombi = np.zeros((self.nCond,self.nCond))
        step = self.nCond-1
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
                    
                    if num1 == num2 or temPosCombi[num1,num2] == int(rep-1): #if numbers are the same or following each other
                        #print('booop! Same num: ' + str(num1 == num2) +', bouble step: '+ str(temPosCombi[num1,num2] == 2))
                        rnd.shuffle(cond) #shuffle the condition list again
                        temPosCombi = copy.deepcopy(posCombi) #reset the possible conditions
                        break #get out of this loop
                    elif time == self.nCond-2:
                        #print('check: is it time 22?')
                        toAdd = copy.deepcopy(cond)
                        blockSeq.append(toAdd)
                        restart = False
                        temPosCombi[num1,num2] += 1
        
                posCombi = copy.deepcopy(temPosCombi)    
        #print('done: ' +str(blockSeq))
        self.blockSeq = blockSeq
        
        print(f"""There are {self.nCond} experimental conditions.
              The order of experimental blocks is randomised
              with the constraint that no condition follows
              any other particular condition more than
              {rep} times during the course of the experiment.\n""")
    
        logLocationBlockSeq = os.path.join(self.logname + '_blockSeq.txt')
        
        
        with open(logLocationBlockSeq, 'w') as f:
            for item in blockSeq:
                for x in item:
                    f.write("%s," % x)
                f.write("\n") 
    
    
    def makeBackSeq(self,nBack):
        print('Making background sequences..')
        # every condition has nRuns(20) blocks and gets a background once..
        self.nRuns
        self.nCond
        self.conditionList = []
        for condition in range(self.nCond):
            condbacklist = list(range(20))
            rnd.shuffle(condbacklist)
            self.conditionList.append(condbacklist)
           
    
    def makeStimSeq(self,nBlockPerCond,nPositions,nStim):
        print('Making stimulus sequences...')
        self.PositionList = list(range(nPositions)) # list of 24 possible positions
        totalPos = round(nStim*nBlockPerCond) # 20 stim per block, 20 blocks per condition in total
        # all positions of stimuli in the whole experiment 
        #posReps = ceil(totalPos/nPositions)
        
        # every stimulus has 20 different spots 
        #all 24 positions in a block should be equally filled over the 20 blocks
        theMean = (nPositions-1)/2
        randomise = True
        while randomise:
            blockSeq = []
            jittSeq = []
            catchSeq = []
            allPosi = self.PositionList*nPositions
            for block in range(int(nBlockPerCond)):
                #catch trials --> 4 per block..
                # 2 at the first half, 2 at second half
                # not the first or last trial of the block
                jittertrials = random.sample(range(1,int(nPositions/2)), 2) + random.sample(range(int(nPositions/2),int(nPositions-1)), 2)
                catchtrials = random.sample(range(1,int(nPositions/2)), 2) + random.sample(range(int(nPositions/2),int(nPositions-1)), 2)
                row = []
                tmp = copy.deepcopy(allPosi)
                for elem in tmp:
                    if elem in jittertrials:
                        tmp.remove(elem)
                for trial in range(nStim):
                    pick = np.random.choice(tmp)
                    if pick in row:
                        pick = np.random.choice(tmp)
                    row.append(pick)
                    for elem in tmp:
                        if elem == pick:
                            tmp.remove(elem)
                if block == 0:
                    blockSeq = row
                    jittSeq = jittertrials
                    catchSeq = catchtrials
                else:
                    blockSeq = np.vstack([blockSeq, row])
                    jittSeq = np.vstack([jittSeq, jittertrials])
                    catchSeq = np.vstack([catchSeq, catchtrials])
            means = []
            for bla in range(blockSeq.shape[1]):
                x= np.mean(blockSeq[:,bla])
                means.append(x)
            
            checkMean = np.mean(means)
            checkSTD = np.std(means)
            checkMin = checkMean - np.amin(means)
            checkMax = np.amax(means) - checkMean
            if checkMin > 2.5 or checkMax > 2.5 or checkMean > (theMean + 0.2) or checkMean < (theMean - 0.2):
                #print('min: ' + str(checkMin) + ' ...... max: ' + str(checkMax))
                randomise = True
            else:
                randomise = False
        self.stimSeq = blockSeq
        self.jittSeq = jittSeq
        self.catchSeq = catchSeq
        
        print(f"""The order of the {nStim} stimulus trials in a block is randomised
          with the constraint that each trial is equally likely
          to appear at the beginning, middle and end of the block.\n""")
          
        logLocationBlockSeq = os.path.join(self.logname + '_stimSeq.txt')
        with open(logLocationBlockSeq, 'w') as f:
            for item in blockSeq:
                for x in item:
                    f.write("%s," % x)
                f.write("\n") 


    def conditions(self):
        count = 0
        conddict = {}
        for condsf in self.sfType:
            for condtype in self.typCond:
                for conddur in self.durCond:
                    cond_specs = {'sf'  : condsf,
                                  'type' : condtype,
                                  'dur' : conddur}
                    
                    conddict[str(count)] = cond_specs
                    count += 1
        self.conditions = conddict         
                    
        
    def makeTrialList(self,framelength,colourChange,stim_path,mask_path,back_path):
        #self.blockSeq is sequence of blocks in all runs
        #self.stimSeq is sequence of stimuli within block
        runlist = {}
        for runnr,run in enumerate(self.blockSeq):
            sequence_list = self.stimSeq[runnr]
            triallist = {}
            for blockpos,block in enumerate(run):
                block_info = self.conditions[str(block)]
                bg = int(self.conditionList[block][runnr] + 1)
                block_list = {}
                for trialpos,trialnr in enumerate(self.PositionList):
                    if trialnr in self.catchSeq[runnr]:
                        catch = 1
                        col = colourChange
                    else:
                        catch = 0
                        col = (1.0, 1.0, 1.0)
                    if trialnr in sequence_list:
                        stimulus = [i for i, x in enumerate(sequence_list) if x == trialnr][0]+1
                        facestim = f"BG{bg}_ID{stimulus}-{block_info['type']}.bmp"
                        face_path = stim_path
                        mask = f"BG{bg}_ID{stimulus}-{block_info['sf']}.bmp"
                        mask_dir = mask_path
                        jittertrial = '0'
                    else:
                        facestim = f'BG{bg}.bmp'
                        face_path = back_path
                        mask = f'BG{bg}.bmp'
                        mask_dir = back_path
                        jittertrial = '1'
                    block_list[f'trial{trialpos}'] = {
                                        'block' : block,
                                        'blockpos' : blockpos,
                                        'trialno' : trialnr,
                                        'trialpos' : trialpos,
                                        'conditionName' : f'vis{block_info["type"]}_dur{block_info["dur"]}',
                                        'SF' : block_info['sf'],
                                        'visibility' : block_info['type'],
                                        'duration' : block_info['dur'],
                                        'trialStart' : None,
                                        'trialDur' : None,
                                        'stimDur' : None,
                                        'maskDur' : None,
                                        'nframes' : str(int(int(block_info['dur'])/framelength)),
                                        'face' : facestim,
                                        'mask' : mask,
                                        'background' : f'BG{bg}.bmp',
                                        'catchtrial' : catch,
                                        'colour' : col,
                                        'jittertrial' : jittertrial,
                                        'rt' : None,
                                        'stim_path' : face_path,
                                        'mask_path' : mask_dir,
                                        'back_path' : back_path}
                    
                triallist[f'block-{blockpos}'] = block_list
            runlist[f'run-{runnr}'] = triallist        
        self.allRuns = runlist

    

