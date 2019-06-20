import os.path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIRS = os.path.join(ROOT_DIR, 'img')
INPUT_FOLDER = "{}{}{}{}".format(IMG_DIRS, os.path.sep, "input_folder", os.path.sep)
OUTPUT_FOLDER = "{}{}{}{}".format(IMG_DIRS, os.path.sep, "output_folder", os.path.sep)
TEMP_IMGS = "{}{}{}{}".format(IMG_DIRS, os.path.sep, "temps_imgs", os.path.sep)
DATASET_IMGS = "{}{}{}{}".format(IMG_DIRS, os.path.sep, "dataset_images", os.path.sep)