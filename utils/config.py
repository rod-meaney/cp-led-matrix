'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
import os
import json
class PMConfig(object):
    '''
    Helper functions for the project
    '''

    def __init__(self, file):
        '''
        load up file with configuration items as key-value pairs
        separated by an '=' (equal) sign.  For URL's this could be an issue
        '''
        self.items = {}
        with open(file) as f:
            content = f.readlines()
        for x in content:
            if not((x[0] == '#') or (x[0] == '\n')):
                y = x.replace('\n', '').split('=')
                self.items[y[0]] = y[1].strip()

    def getConfig(self, config_item):
        '''
        return configuration item based on key
        '''
        return self.items[config_item]
    
    def get_dir_list(self, directory):
        contents = os.listdir(f'./{directory}')
        ret = []
        for item in contents:
            #Bloody mac files
            if item[0] != ".":
                ret.append(item.split(".")[0].replace('_', ' '))
        ret.sort()
        return ret
    
    def get_all_matrix_config(self):
        saved = self.get_dir_list('saved')
        images = self.get_dir_list('img')
        animations = self.get_dir_list('animation')
        data = {"saved":saved, "images":images, "animations":animations}
        contents = os.listdir(f'./data')
        for item in contents:
            #Bloody mac files
            if item[0] != ".":
                with open(f'./data/{item}', "r") as file:
                    data[item.split(".")[0]] = json.load(file)
        return data        
