# Read in .im7 files and create .mp4 animation for PLIF data
# Elle Stark Sept 2025

import matplotlib.pyplot as plt
import numpy as np
import cmasher as cmr
import logging
import lvpyio as lv


# Set up logging for convenient messages
logger = logging.getLogger('MOXLIFTests')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s"))
logger.addHandler(handler)
INFO = logger.info
WARN = logger.warn
DEBUG = logger.debug

# read in .im7 files using lavision io package
# set path1 to data of laser that fires first, path2 to second
path1 = 'D:/Elle/PLIF_MOX_2023-07-21/data_r57_L3/r57_Subtract_bg_L3/AboveBelow/Divide_ff63_L3/Divide_instantaneous_sourceAvg/Reflectance_adjustment/AddCameraAttributes/ImageCorrection_calibrate.set'
path2 = 'D:/Elle/PLIF_MOX_2023-07-21/data_r57_L3/r57_subtract_bg_L4/Above0/Divide_ff63_L4/Divide_instantaneous_sourceAvg/Reflectance_adjustment/AddCameraAttributes/ImageCorrection_calibrate.set'
save_file = 'C:/Users/LaVision/Documents/Data_processing/r57_finalData_25to300s.npy'



