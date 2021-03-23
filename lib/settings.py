import pickle
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config import get_config
class settings_class:
    def __init__(self, test_mode_settings=False,debug=False):
        self.test_mode_settings = test_mode_settings
        self.debug_mode_settings = debug
        
        self.save_settings()
    def test_mode(self,value=None):
        if not value == None:
            self.test_mode_settings = value
            self.save_settings()
        else:
            return self.test_mode_settings
    def debug_mode(self,value=None):
        if not value == None:
            self.debug_mode_settings = value
            self.save_settings()
        else:
            return self.debug_mode_settings
    def save_settings(self):
        old_cwd = os.getcwd()
        os.chdir(get_config().main_folder)
        with open('db/settings.decentra_network', 'wb') as settings_file:
            pickle.dump(self, settings_file,protocol=2)
        os.chdir(old_cwd)



def the_settings():
    try:
        old_cwd = os.getcwd()
        os.chdir(get_config().main_folder)
        with open('db/settings.decentra_network', 'rb') as settings_file:
            return pickle.load(settings_file)  
        os.chdir(old_cwd)
    except:
        return settings_class()   