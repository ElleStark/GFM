# Overlay PLIF and PIV data together in a snapshot of scalar & velocity data
# E Stark Oct 2025

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import rcParams
import cmasher as cmr

# load data
plif_data = np.load()
v_data = np.load('ignore/data/v_30cmsDiffuseFractalNeutral.npy')
u_data = np.load('ignore/data/u_30cmsDiffuseFractalNeutral.npy')
x = np.load('ignore/data/x_30cmsDiffuseFractalNeutral.npy')
y = np.load('ignore/data/y_30cmsDiffuseFractalNeutral.npy')
x_min = np.min(x)
x_max = np.max(x)
y_min = np.min(y)
y_max = np.max(y)

save_file = 'ignore/plots/overlay_PIV_PLIF_30cms_diffuse_fractal_neutralHe.png'

# Plotting parameter selections
vmin= 0.0
vmax= 0.5
cmap = cmr.chroma
norm = colors.Normalize(vmin=vmin, vmax=vmax)
frame_to_plot = 40

vel_mag = np.sqrt(u_data**2 + v_data**2)

# QC with one frame
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(25.6, 14.4))

# plt.imshow(vel_mag[:, :, 0], extent=[x_min, x_max, y_min, y_max], cmap=cmap, norm=norm)

# quiver plot
vec_stride = 18
qv = ax.quiver(x[::vec_stride, ::vec_stride], y[::vec_stride, ::vec_stride], u_data[::vec_stride, ::vec_stride, 0], 
            v_data[::vec_stride, ::vec_stride, 0], vel_mag[::vec_stride, ::vec_stride, 0], norm=norm, scale=20, headlength=3.65, headaxislength=3, cmap=cmap)
cbar = fig.colorbar(qv, ax=ax, label='Magnitude')
ax.set_aspect('equal', adjustable='box')
ax.set_xticks([])
ax.set_yticks([])

# overlay PLIF plot
plif_data[plif_data<vmin] = vmin
img_display = ax.imshow(plif_data[:, :, 0], cmap=cmap, norm=norm)
plt.colorbar(img_display)
# ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])


plt.show()
