'''
Created on Jan 14, 2015

@author: roderickmeaney
'''
from utils.config import PMConfig
class PMWeb(object):
    '''
    Helper functions for the project
    '''

    def __init__(self):
        '''
        load up file with configuration items as key-value pairs
        separated by an '=' (equal) sign.  For URL's this could be an issue
        '''
        wf = PMConfig('wf')
        self.WIFI_SSID = wf.getConfig('WIFI_SSID')
        self.WIFI_PASSWORD = wf.getConfig('WIFI_PASSWORD')

    def webpage(self, temperature):
        #Template HTML
        html = f"""
                <!DOCTYPE html>
                <html>
                <form action="./home?b=1">
                <input type="submit" value="???" />
                </form>
                <form action="./lighton">
                <input type="submit" value="Light on" />
                </form>
                <form action="./lightoff">
                <input type="submit" value="Light off" />
                </form>
                <form action="./close">
                <input type="submit" value="Stop server" />
                </form>
                <p>Temperature is {temperature}</p>
                </body>
                </html>
                """
        return str(html)
    
    def ParseParams(self, params):
        print(params)
        #eg 
        #name=3Lines&linex=
        #tram|stopNo|routeNo
        #scroll|color|text
        #reverse_scroll|color|text
        #clock|color
        #text|color
