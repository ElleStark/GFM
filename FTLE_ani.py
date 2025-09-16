import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib import rcParams
import numpy as np
import cmasher as cmr
import logging


# load data
input_npy = 'ignore/data/FTLE_0.4s_30cmsDiffusiveFractalNeutral.npy'  # shape: (n_frames, ny, nx)
ftle_data = np.load(input_npy)

# set plotting params
save_file_ani = 'ignore/plots/ftle_ridges_test.mp4'
cmap = cmr.amber
vmin = None
vmax = None
norm = norm = colors.Normalize(vmin=vmin, vmax=vmax)
nframes_to_plot = 1

##### CREATE ANIMATION ######

# Set up figure and axes
fig, ax = plt.subplots(figsize=(25.6, 14.4))

# Initialize image plot
# combined_data[combined_data<vmin] = vmin
img_display = ax.imshow(ftle_data[0, :, :], cmap=cmap, norm=norm)
plt.colorbar(img_display)
ax.set_aspect('equal')
ax.set_title("30 cm/s  fractal grid, neutral He, 50% dilution")
ax.set_xticks([])
ax.set_yticks([])

# Animation function
def update(frame):
    img_display.set_array(ftle_data[frame, :, :])  # Update image
    return img_display

# Create animation
ani = animation.FuncAnimation(fig, update, frames=nframes_to_plot, interval=50, blit=False)
# Set FFmpeg writer path
rcParams['animation.ffmpeg_path'] = r"C:/Users/elles/AppData/Local/ffmpeg-6.0-essentials_build/bin/ffmpeg.exe" 

# Create writer object
Writer = animation.FFMpegWriter(fps=20)

# Save or display animation
ani.save(save_file_ani, writer=Writer, dpi=150)  
plt.show()