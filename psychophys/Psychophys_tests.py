# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:28:17 2023

@author: jschuurmans
"""


#%% ==========================================================================
# imports and paths
#base_path = 'C:/Users/Adminuser/Documents/04_CtF-7T/Experiment/psychophys/'
base_path = '/home/schuurmans@spinozacentre.knaw.nl/Documents/Experiment/psychophys/'
data_path = f'{base_path}data/'


import os
os.chdir(base_path)
from psychopy import gui,data
import csv
from Benton import *
from Handedness import *


#%% ==========================================================================
# subject info
exp_name = 'Psychophysical tests'
exp_info = {
    'subject' : 'sub-',
    'gender' : ('female', 'male'),
    'age' : '',
    'nationality' : ''
    }

dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name, sortKeys=False)


# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()

exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name


handedness_quotient, handedness_meaning = handedness()
benton_score = bentontask(base_path,exp_info['subject'])
#benton_score = 100

"""A score above 40 out of 54 (76%) on the BFRT
is considered evidence for normal 
individual face-matching ability;
39–40 is a borderline score;
37–38 reflects moderate impairment;
and people scoring below 37 out of 54 (i.e., below 68.5%)
are considered to be impaired (Benton et al., 1983)."""


exp_info['benton_score'] = benton_score
exp_info['handedness_quotient'] = handedness_quotient
exp_info['handedness_meaning'] = handedness_meaning


data_path_sub = f"{data_path}{exp_info['subject']}/"
# prepare log file to write the data
if not os.path.isdir(data_path):
    os.makedirs(data_path)

# save file with subject info 
info_name = f"{data_path}Psychophys.csv"
info_file = open(info_name,'a',encoding='UTF8', newline='')

# write header if it is the first session
header_names = list(exp_info.keys())
writer_log = csv.DictWriter(info_file, fieldnames=header_names)
#writer_log.writeheader()
writer_log.writerow(exp_info)
info_file.close()   





