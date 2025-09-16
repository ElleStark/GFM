# Read in .npy velocity data files and create .mp4 animation for PIV data
# Elle Stark Sept 2025

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib import rcParams
import numpy as np
import cmasher as cmr
import logging


# Set up logging for convenient messages
logger = logging.getLogger('PLIFplots')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s"))
logger.addHandler(handler)
INFO = logger.info
WARN = logger.warning
DEBUG = logger.debug


# load data
v_data = np.load('ignore/data/v_30cmsDiffuseFractalNeutral.npy')
u_data = np.load('ignore/data/u_30cmsDiffuseFractalNeutral.npy')
x = np.load('ignore/data/x_30cmsDiffuseFractalNeutral.npy')
y = np.load('ignore/data/y_30cmsDiffuseFractalNeutral.npy')
x_min = np.min(x)
x_max = np.max(x)
y_min = np.min(y)
y_max = np.max(y)

save_file_ani = 'ignore/plots/PIV_uplot_30cms_diffuse_fractal_neutralHe.mp4'

# Plotting parameter selections
vmin= 0.0
vmax= 0.5
cmap = cmr.chroma
norm = colors.Normalize(vmin=vmin, vmax=vmax)
nframes_to_plot = 100

vel_mag = np.sqrt(u_data**2 + v_data**2)
DEBUG(f'vel_mag min, max: {np.min(vel_mag), np.max(vel_mag)}')

# QC with one frame
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(25.6, 14.4))

# plt.imshow(vel_mag[:, :, 0], extent=[x_min, x_max, y_min, y_max], cmap=cmap, norm=norm)

# quiver plot?
vec_stride = 18
qv = ax.quiver(x[::vec_stride, ::vec_stride], y[::vec_stride, ::vec_stride], u_data[::vec_stride, ::vec_stride, 0], 
            v_data[::vec_stride, ::vec_stride, 0], vel_mag[::vec_stride, ::vec_stride, 0], norm=norm, scale=20, headlength=3.65, headaxislength=3, cmap=cmap)
cbar = fig.colorbar(qv, ax=ax, label='Magnitude')
ax.set_aspect('equal', adjustable='box')
ax.set_xticks([])
ax.set_yticks([])


plt.show()


##### CREATE ANIMATION ######

# Animation function
def update(frame):
    u = u_data[::vec_stride, ::vec_stride, frame]
    v = v_data[::vec_stride, ::vec_stride, frame] 
    c = vel_mag[::vec_stride, ::vec_stride, frame]
    qv.set_UVC(u, v, c)  # Update image
    return qv

# Create animation
ani = animation.FuncAnimation(fig, update, frames=nframes_to_plot, interval=50, blit=False)
# Set FFmpeg writer path
rcParams['animation.ffmpeg_path'] = r"C:/Users/elles/AppData/Local/ffmpeg-6.0-essentials_build/bin/ffmpeg.exe" 

# Create writer object
Writer = animation.FFMpegWriter(fps=10)

# Save or display animation
ani.save(save_file_ani, writer=Writer, dpi=150)  
plt.show()
