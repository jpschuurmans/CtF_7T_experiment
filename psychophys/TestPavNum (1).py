# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 09:13:49 2020

@author: Neper
"""



#===============
# Import modules
#===============
import os                    
import numpy as np
import numpy.matlib as npm          # for file/folder operations
import numpy.random as rnd          # for random number generators
import operator
from psychopy import visual, event, core, gui, data, monitors
from psychopy.hardware import keyboard
from numpy import asarray
from PIL import Image


#==============================================
# Settings that we might want to tweak later on
#==============================================

datapath = 'data'                   # directory to save data in     
Cpath= 'Consignes'
Fpath= 'Faces'  # directory where images can be found

first = [1, 2, 3, 4, 5, 6]                  #first bloc of trials
second = [7, 8, 9, 10, 11, 12, 13, 14]      #second bloc of trials
third = [15, 16, 17, 18, 19, 20, 21, 22]    #third block of trials
Trial = 1
Trial0 = 0
score = 0
cons = [1, 2, 3, 4, 5, 6, 7]                # instructions

corAns = [
    ['r01E.bmp'],
    ['r02A.bmp'],
    ['r03B.bmp'],
    ['r04C.bmp'],
    ['r05F.bmp'],
    ['r06B.bmp'],
    ['r07B.bmp', 'r07E.bmp', 'r07F.bmp'],
    ['r08A.bmp', 'r08C.bmp', 'r08D.bmp'],
    ['r09B.bmp', 'r09D.bmp', 'r09F.bmp'],
    ['r10B.bmp', 'r10E.bmp', 'r10F.bmp'],
    ['r11A.bmp', 'r11D.bmp', 'r11F.bmp'],
    ['r12B.bmp', 'r12C.bmp', 'r12F.bmp'],
    ['r13A.bmp', 'r13C.bmp', 'r13E.bmp'],
    ['r14A.bmp', 'r14C.bmp', 'r14E.bmp'],
    ['r15B.bmp', 'r15C.bmp', 'r15D.bmp'],
    ['r16B.bmp', 'r16D.bmp', 'r16E.bmp'],
    ['r17A.bmp', 'r17D.bmp', 'r17F.bmp'],
    ['r18C.bmp', 'r18D.bmp', 'r18F.bmp'],
    ['r19B.bmp', 'r19C.bmp', 'r19D.bmp'],
    ['r20A.bmp', 'r20B.bmp', 'r20C.bmp'],
    ['r21A.bmp', 'r21E.bmp', 'r21F.bmp'],
    ['r22B.bmp', 'r22D.bmp', 'r22E.bmp']]

numbers = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']

#========================================
# Store info about the experiment session
#========================================
    
# Get subject name, gender, age, handedness through a dialog box
exp_name = 'Benton Task'
exp_info = {
    'participant': '',
    'gender': ('female', 'male'),
    'age':'',
    'left-handed':False,
    'screenwidth(cm)': '59',
    'screenresolutionhori(pixels)': '1920',
    'screenresolutionvert(pixels)': '1080',
    'refreshrate(hz)': '60'
    }

dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)     #open a dialog box
    

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name


# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = exp_info['participant'] + '_' + exp_info['date'] + '.csv'
data_fname = os.path.join(datapath, data_fname)


#set the window
mon = monitors.Monitor('mon1')
mon.setDistance(57)
mon.setWidth(float(exp_info['screenwidth(cm)']))
horipix = exp_info['screenresolutionhori(pixels)']
vertpix = exp_info['screenresolutionvert(pixels)']
framerate = exp_info['refreshrate(hz)']
scrsize = (float(horipix),float(vertpix))

# Open a window
mon.setSizePix(scrsize)
win = visual.Window(monitor = mon, 
                    size = scrsize,
                    color='black',
                    units='deg',
                    fullscr=True)
win.mouseVisible=False

# var for stim length
framelength = 1/(float(framerate)) #frame length in sec
stimframe = int(30/framelength) #number of frame in 30sec


# Define trial start text

bitmap1 = visual.ImageStim(win, size=[4.5, 5.2]) 
bitmap2 = visual.ImageStim(win, size=[4.5, 5.2]) 
bitmap3 = visual.ImageStim(win, size=[4.5, 5.2]) 
bitmap4 = visual.ImageStim(win, size=[4.5, 5.2]) 
bitmap5 = visual.ImageStim(win, size=[4.5, 5.2]) 
bitmap6 = visual.ImageStim(win, size=[4.5, 5.2]) 
bitmap7 = visual.ImageStim(win, size=[4.5, 5.2]) 
bitmap8 = visual.ImageStim(win)

rt_clock = core.Clock()

logfile = open(data_fname, 'w')
logfile.write('Trial, Response, , , ResponseTime, Score tot \n')

#========================================
# Start the first part of the experiment
#========================================

for instruc in cons[0:2]:
    cons_imname=os.path.join(Fpath,'consignes' + str(instruc) + '.bmp')
    bitmap8.setImage(cons_imname)
    bitmap8.pos=(0, 0)
    bitmap8.draw()
    win.flip() #fliping the screen to show images
    event.clearEvents()
    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in keys:
        core.quit()
    elif 'space' in keys :
        instruc += 1



for Trial in first:
    rt_clock.reset()
    #defining our images and their position
    face1_imname=os.path.join(Fpath,'r' + str(numbers[Trial0]) + 'A.bmp')
    bitmap1.setImage(face1_imname)
    bitmap1.pos=(-6, -0.5)
    face2_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'B.bmp')
    bitmap2.setImage(face2_imname)
    bitmap2.pos=(0, -0.5)
    face3_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'C.bmp')
    bitmap3.setImage(face3_imname)
    bitmap3.pos=(6, -0.5)
    face4_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'D.bmp')
    bitmap4.setImage(face4_imname)
    bitmap4.pos=(-6, -6.5)
    face5_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'E.bmp')
    bitmap5.setImage(face5_imname)
    bitmap5.pos=(0, -6.5)
    face6_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'F.bmp')
    bitmap6.pos=(6, -6.5)
    bitmap6.setImage(face6_imname)
    face7_imname=os.path.join(Fpath, 's' + str(numbers[Trial0]) + '_cropped.bmp')
    bitmap7.setImage(face7_imname)
    bitmap7.pos=(0, 6.5)
    
    
    for nFrame in range (stimframe):
        # drawing our images behind the screen
        bitmap1.draw()
        bitmap2.draw()
        bitmap3.draw()
        bitmap4.draw()
        bitmap5.draw()
        bitmap6.draw()
        bitmap7.draw()
        win.flip() #fliping the screen to show images
        event.clearEvents()
        keys = event.waitKeys(keyList=['1','2', '3', '4', '5', '6', 'num_1', 'num_2','num_3', 'num_4', 'num_5', 'num_6','escape'])
        resp = str(corAns[Trial0][0])   #name of the correct image
        if 'escape' in keys:
            core.quit()
        elif '1' in keys:
            if resp.find('A') != -1: #if there is an A, it is the image inposition 1
                score += 1
                break
            else:
                break
        elif 'num_4' in keys:
            if resp.find('A') != -1: #if there is an A, it is the image inposition 1
                score += 1
                break
            else:
                break

        elif '2' in keys:
            if resp.find('B') != -1:
                score += 1
                break
            else:
                break
        elif 'num_5' in keys:
            if resp.find('B') != -1:
                score += 1
                break
            else:
                break

        elif '3' in keys:
            if resp.find('C') != -1:
                score += 1
                break
            else:
                break
        elif 'num_6' in keys:
            if resp.find('C') != -1:
                score += 1
                break
            else:
                break

        elif '4' in keys:
            if resp.find('D') != -1:
                score += 1
                break
            else:
                break
        elif 'num_1' in keys:
            if resp.find('D') != -1:
                score += 1
                break
            else:
                break

        elif '5' in keys:
            if resp.find('E') != -1:
                score += 1
                break
            else:
                break
        elif 'num_2' in keys:
            if resp.find('E') != -1:
                score += 1
                break
            else:
                break

        elif '6' in keys:
            if resp.find('F') != -1:
                score += 1
                break
            else:
                break
        elif 'num_3' in keys:
            if resp.find('F') != -1:
                score += 1
                break
            else:
                break
    rt = rt_clock.getTime()
    #print(rt)
    Keys = []
    event.clearEvents()
    toSave = str(Trial) + ',' + str(keys[0]) + ',' + 'NA' + ','+ '"NA"' + ',' + str(rt) + ',' + str(score) + ',\n'
    logfile.write(toSave)
    Trial0 += 1
    win.flip()
    core.wait(1)
#print (score)



#========================================
# Start the second part of the experiment
#========================================


cons_imname=os.path.join(Fpath,'consignes4.bmp')
bitmap8.setImage(cons_imname)
bitmap8.pos=(0, 0)
bitmap8.draw()
win.flip() #fliping the screen to show images
event.clearEvents()
keys = event.waitKeys(keyList=['space', 'escape'])
if 'escape' in keys:
    core.quit()
elif 'space' in keys :
    win.flip()
    core.wait(0.5)

for Trial in second:
    rt_clock.reset()
    #defining our images and their position
    face1_imname=os.path.join(Fpath,'r' + str(numbers[Trial0]) + 'A.bmp')
    bitmap1.setImage(face1_imname)
    bitmap1.pos=(-6, -0.5)
    face2_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'B.bmp')
    bitmap2.setImage(face2_imname)
    bitmap2.pos=(0, -0.5)
    face3_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'C.bmp')
    bitmap3.setImage(face3_imname)
    bitmap3.pos=(6, -0.5)
    face4_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'D.bmp')
    bitmap4.setImage(face4_imname)
    bitmap4.pos=(-6, -6.5)
    face5_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'E.bmp')
    bitmap5.setImage(face5_imname)
    bitmap5.pos=(0, -6.5)
    face6_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'F.bmp')
    bitmap6.pos=(6, -6.5)
    bitmap6.setImage(face6_imname)
    face7_imname=os.path.join(Fpath, 's' + str(numbers[Trial0]) + '_cropped.bmp')
    bitmap7.setImage(face7_imname)
    bitmap7.pos=(0, 6.5)
    keyPressed = []
    
    for nFrame in range (stimframe):
        # drawing our images behind the screen
        bitmap1.draw()
        bitmap2.draw()
        bitmap3.draw()
        bitmap4.draw()
        bitmap5.draw()
        bitmap6.draw()
        bitmap7.draw()
        win.flip() #fliping the screen to show images
        keys = event.waitKeys(keyList=['1','2', '3', '4', '5', '6', 'num_1', 'num_2','num_3', 'num_4', 'num_5', 'num_6','escape'])
        resp = str(corAns[Trial0][0])
        #print(resp)
        if 'escape' in keys:
            core.quit()
        #print(keyPressed)
        if '1' in keys and '1' not in keyPressed:
            keyPressed.append('1')
        elif '2' in keys and '2' not in keyPressed:
            keyPressed.append('2')
        elif '3' in keys and '3' not in keyPressed:
            keyPressed.append('3')
        elif '4' in keys and '4' not in keyPressed:
            keyPressed.append('4')
        elif '5' in keys and '5' not in keyPressed:
            keyPressed.append('5')
        elif '6' in keys and '6' not in keyPressed:
            keyPressed.append('6')
        elif 'num_1' in keys and 'num_1' not in keyPressed:
            keyPressed.append('4')
        elif 'num_2' in keys and 'num_2' not in keyPressed:
            keyPressed.append('5')
        elif 'num_3' in keys and 'num_3' not in keyPressed:
            keyPressed.append('6')
        elif 'num_4' in keys and 'num_4' not in keyPressed:
            keyPressed.append('1')
        elif 'num_5' in keys and 'num_5' not in keyPressed:
            keyPressed.append('2')
        elif 'num_6' in keys and 'num_6' not in keyPressed:
            keyPressed.append('3')
        if len(keyPressed) == 3:
            rt = rt_clock.getTime()
            break
    for ans in corAns[Trial0] :
        for clic in keyPressed:
            if str(ans).find('A') != -1 and clic == '1':
                score +=1
            if str(ans).find('B') != -1 and clic == '2':
                score +=1
            if str(ans).find('C') != -1 and clic == '3':
                score +=1
            if str(ans).find('D') != -1 and clic == '4':
                score +=1
            if str(ans).find('E') != -1 and clic == '5':
                score +=1
            if str(ans).find('F') != -1 and clic == '6':
                score +=1
    toSave = str(Trial) + ',' + str(keyPressed[0]) + ',' + str(keyPressed[1]) + ',' + str(keyPressed[2]) + ',' + str(rt) + ',' + str(score) + ',\n'
    logfile.write(toSave)
    Trial0 += 1
    win.flip()
    core.wait(1)
#print (score)

#========================================
# Start the third part of the experiment
#========================================

cons_imname=os.path.join(Fpath,'consignes5.bmp')
bitmap8.setImage(cons_imname)
bitmap8.pos=(0, 0)
bitmap8.draw()
win.flip() #fliping the screen to show images
event.clearEvents()
keys = event.waitKeys(keyList=['space', 'escape'])
if 'escape' in keys:
    core.quit()
elif 'space' in keys :
    win.flip()
    core.wait(0.5)


for Trial in third:
    rt_clock.reset()
    #defining our images and their position
    face1_imname=os.path.join(Fpath,'r' + str(numbers[Trial0]) + 'A.bmp')
    bitmap1.setImage(face1_imname)
    bitmap1.pos=(-6, -0.5)
    face2_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'B.bmp')
    bitmap2.setImage(face2_imname)
    bitmap2.pos=(0, -0.5)
    face3_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'C.bmp')
    bitmap3.setImage(face3_imname)
    bitmap3.pos=(6, -0.5)
    face4_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'D.bmp')
    bitmap4.setImage(face4_imname)
    bitmap4.pos=(-6, -6.5)
    face5_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'E.bmp')
    bitmap5.setImage(face5_imname)
    bitmap5.pos=(0, -6.5)
    face6_imname=os.path.join(Fpath, 'r' + str(numbers[Trial0]) + 'F.bmp')
    bitmap6.pos=(6, -6.5)
    bitmap6.setImage(face6_imname)
    face7_imname=os.path.join(Fpath, 's' + str(numbers[Trial0]) + '_cropped.bmp')
    bitmap7.setImage(face7_imname)
    bitmap7.pos=(0, 6.5)
    keyPressed = []
    
    for nFrame in range (stimframe):
        # drawing our images behind the screen
        bitmap1.draw()
        bitmap2.draw()
        bitmap3.draw()
        bitmap4.draw()
        bitmap5.draw()
        bitmap6.draw()
        bitmap7.draw()
        win.flip() #fliping the screen to show images
        keys = event.waitKeys(keyList=['1','2', '3', '4', '5', '6', 'num_1', 'num_2','num_3', 'num_4', 'num_5', 'num_6','escape'])
        resp = str(corAns[Trial0][0])
        #print(resp)
        if 'escape' in keys:
            core.quit()
        #print(keyPressed)
        if '1' in keys and '1' not in keyPressed:
            keyPressed.append('1')
        elif '2' in keys and '2' not in keyPressed:
            keyPressed.append('2')
        elif '3' in keys and '3' not in keyPressed:
            keyPressed.append('3')
        elif '4' in keys and '4' not in keyPressed:
            keyPressed.append('4')
        elif '5' in keys and '5' not in keyPressed:
            keyPressed.append('5')
        elif '6' in keys and '6' not in keyPressed:
            keyPressed.append('6')
        elif 'num_1' in keys and 'num_1' not in keyPressed:
            keyPressed.append('4')
        elif 'num_2' in keys and 'num_2' not in keyPressed:
            keyPressed.append('5')
        elif 'num_3' in keys and 'num_3' not in keyPressed:
            keyPressed.append('6')
        elif 'num_4' in keys and 'num_4' not in keyPressed:
            keyPressed.append('1')
        elif 'num_5' in keys and 'num_5' not in keyPressed:
            keyPressed.append('2')
        elif 'num_6' in keys and 'num_6' not in keyPressed:
            keyPressed.append('3')
        if len(keyPressed) == 3:
            rt = rt_clock.getTime()
            break
    for ans in corAns[Trial0] :
        for clic in keyPressed:
            if str(ans).find('A') != -1 and clic == '1':
                score +=1
            if str(ans).find('B') != -1 and clic == '2':
                score +=1
            if str(ans).find('C') != -1 and clic == '3':
                score +=1
            if str(ans).find('D') != -1 and clic == '4':
                score +=1
            if str(ans).find('E') != -1 and clic == '5':
                score +=1
            if str(ans).find('F') != -1 and clic == '6':
                score +=1
    toSave = str(Trial) + ',' + str(keyPressed[0]) + ',' + str(keyPressed[1]) + ',' + str(keyPressed[2]) + ',' + str(rt) + ',' + str(score) + ',\n'
    logfile.write(toSave)
    Trial0 += 1
    win.flip()
    core.wait(1)
print (score)

cons_imname=os.path.join(Fpath,'consignes6.bmp')
bitmap8.setImage(cons_imname)
bitmap8.pos=(0, 0)
bitmap8.draw()
win.flip() #fliping the screen to show images
event.clearEvents()
keys = event.waitKeys(keyList=['space', 'escape'])
if 'escape' in keys:
    core.quit()
elif 'space' in keys :
    #win.flip()
    core.wait(0.5)

logfile.close()







