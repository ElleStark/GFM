# Read in .im7 files and create .mp4 animation for PLIF data
# Elle Stark Sept 2025

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib import rcParams
import numpy as np
import cmasher as cmr
import logging
import lvpyio as lv


# Set up logging for convenient messages
logger = logging.getLogger('PLIFplots')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s"))
logger.addHandler(handler)
INFO = logger.info
WARN = logger.warning
DEBUG = logger.debug

# read in .im7 files using lavision io package
# set path1 to data of laser that fires first, path2 to second
path1 = 'D:/Elle/8.29.2025_Buoyancy_PLIF/data_8.29_30cms_smTG15cm_dense45pctHe0.816_55pctair1.0_PIV0.02_Iso_L4/Subtract_bg_L4_01/Divide_ffmbg_L4/Divide_C0_11.4/AddCameraAttributes/ImageCorrection/Resize.set'
path2 = 'D:/Elle/8.29.2025_Buoyancy_PLIF/data_8.29_30cms_smTG15cm_dense45pctHe0.816_55pctair1.0_PIV0.02_Iso_L4/Subtract_bg_L3_01/Divide_ffmbg_L3/Divide_C0_11.1/AddCameraAttributes/ImageCorrection/Resize.set'
save_file_data = 'ignore/data/PLIF_30cms_smTG15cm_45pctHe.npy'
save_file_ani = 'ignore/animations/PLIF_30cms_smTG15cm_45pctHe.mp4'

# Plotting parameter selections
vmin=0.015
vmax=0.75
cmap = cmr.cosmic
norm = colors.LogNorm(vmin=vmin, vmax=vmax)
# norm = colors.Normalize(vmin=vmin, vmax=vmax)
QC = False  # True for individual plots at each timestep
save_data = True
title = None

# misc. user-set params
offset = 0  # frame to start on

# set up buffer objects (see lavision pyio manual)
s1 = lv.read_set(path1)
s2 = lv.read_set(path2)
# check size and n frames
buffer = s1[0]
arr = buffer.as_masked_array()
dims = np.shape(arr.data)
DEBUG(dims) 
total_frames = len(s1) + len(s2)  
INFO(f'total frames: {total_frames}')
#  nframes_to_plot = total_frames  # manually select subset in time if needed
nframes_to_plot = 300

# initialize array for storing collated data
combined_data = np.zeros((dims[0], dims[1], nframes_to_plot))
avg_sensor_ts = np.zeros(nframes_to_plot)
avg_compare_ts = np.zeros(nframes_to_plot)

# collate images into single sequential stack
frame_list = [x+offset for x in list(range(nframes_to_plot))]
# frame_list = range(nframes_to_plot)
for i in frame_list:
    # if even, read from first set, if odd from second set
    if i%2==0:  
        buffer = s1[int(i/2)]
    else:
        buffer = s2[int((i-1)/2)]

    arr = buffer.as_masked_array()  # necessary conversion (see lavision pyio manual)
    tempdata = arr.data  # check if needed

    # QC plot: data image with sensor box overlay
    if QC:
        plt.imshow(tempdata, cmap=cmap, norm=norm)
        plt.colorbar()
        plt.show()

    combined_data[:, :, i-offset] = tempdata

DEBUG(f'combined data dims: {combined_data.shape}')

# save stack of raw data (if desired)
if save_data:
    np.save(save_file_data, combined_data)

##### CREATE ANIMATION ######

# Set up figure and axes
fig, ax = plt.subplots(figsize=(25.6, 14.4))

# Initialize image plot
combined_data[combined_data<vmin] = vmin
img_display = ax.imshow(combined_data[:, :, 0], cmap=cmap, norm=norm)
plt.colorbar(img_display)
ax.set_aspect('equal')
ax.set_title(title)
ax.set_xticks([])
ax.set_yticks([])

# Animation function
def update(frame):
    img_display.set_array(combined_data[:, :, frame])  # Update image
    return img_display

# Create animation
ani = animation.FuncAnimation(fig, update, frames=nframes_to_plot, interval=50, blit=False)
# Set FFmpeg writer path
rcParams['animation.ffmpeg_path'] = r"C:/Users/LaVision/AppData/Local/Programs/ffmpeg-7.1-essentials_build/bin/ffmpeg.exe"  # Replace with your actual path

# Create writer object
Writer = animation.FFMpegWriter(fps=20, bitrate=1800)

# Save or display animation
ani.save(save_file_ani, writer=Writer, dpi=150)  
plt.show()
