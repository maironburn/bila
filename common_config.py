import os.path

# RUN Settings
'''...........
Thread Stuff
..............
'''
FOREGROUND_THREAD = False
TIME_SLEEP = 10
TIME_WAIT_AFTER_KILLING = 10
KILL_THE_ENEMY = False

'''
Doc parser Stuff
'''
SAVE_MAPPING = False

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS = os.path.join(ROOT_DIR, 'settings')
WORKFLOWS = os.path.join(ROOT_DIR, 'workflow_macros')

APP_NAME = 'Plataforma de programas de ayuda'
LOGGER_NAME = 'BilaLogger.log'
LOG_FILE = "{}{}{}{}{}".format(ROOT_DIR, os.path.sep, 'loggin', os.path.sep, LOGGER_NAME)

IMG_DIRS = os.path.join(ROOT_DIR, 'img')

INPUT_FOLDER = "{}{}{}{}".format(IMG_DIRS, os.path.sep, "input_folder", os.path.sep)
OUTPUT_FOLDER = "{}{}{}{}".format(IMG_DIRS, os.path.sep, "output_folder", os.path.sep)
TEMP_IMGS = "{}{}{}{}".format(IMG_DIRS, os.path.sep, "temps_imgs", os.path.sep)
DATASET_IMGS = "{}{}{}{}".format(IMG_DIRS, os.path.sep, "dataset_images", os.path.sep)
MAPPED_WINDOWS = os.path.join(ROOT_DIR, 'mapped_windows')
SCHEMES = "{}{}{}".format(SETTINGS, os.path.sep, 'screen_schemes')
