'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
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
