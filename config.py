import pickle
import os
class config_class:
    def __init__(self):
        self.main_folder = None
 
def get_config():
    try:
     
     old_cwd = os.getcwd()
     os.chdir(os.path.dirname(os.path.realpath(__file__)))
     with open('config.decentra_network', 'rb') as config_file:
        return pickle.load(config_file)
     os.chdir(old_cwd)

    except:
        save_folder()
        old_cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        with open('config.decentra_network', 'rb') as config_file:
            return pickle.load(config_file)
        os.chdir(old_cwd)


def save_folder():
    config = config_class()
    config.main_folder = os.path.dirname(os.path.realpath(__file__))
    os.chdir(config.main_folder)
    with open('config.decentra_network', 'wb') as config_file:
        pickle.dump(config, config_file)    


if __name__ == '__main__':
    try:
        get_config()
    except:
        save_folder()