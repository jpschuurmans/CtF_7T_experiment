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


#%% ===========================================================================

## functions

def escape_check(keys,win,f):
    # close window and logfile if escape is pressed
    if 'escape' in keys:
        win.close()
        f.close()
        core.quit()
        
        
def load_txt_as_dict(path):
    with open(path, 'r', encoding='utf-8') as f:
        instructions = f.read()
    instructiontexts = json.loads(instructions)
    return instructiontexts