# read in .vc7 data and write as u, v data in stacked .npy arrays
# Elle Stark, Sept 2025

import matplotlib.pyplot as plt
import pivpy as pp
from pivpy import io
import numpy as np
import logging
from glob import glob
import os

# Set up logging for convenient messages
logger = logging.getLogger('PIVread')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s"))
logger.addHandler(handler)
INFO = logger.info
WARN = logger.warning
DEBUG = logger.debug

# specify source directory and get list of files. assumes PIV data is in .vc7 format
piv_dir = 'D:/Elle/Source_config_PIV/9.10_30cms_FractalTG_diffusiveSource_53pctneuHe0.857_47pctAir0.771_PIV0.2/StereoPIV_MPd(3x12x12_75%ov)/PostProc_interp_3x3smooth/Resize'
vc7_files = sorted(glob(os.path.join(piv_dir, '*.vc7')))
n_frames = len(vc7_files)  # specify subset if needed

QC_plot = True

# specify file names for saving arrays
ufile = 'ignore/data/u_30cmsDiffuseFractalNeutral.npy'
vfile = 'ignore/data/v_30cmsDiffuseFractalNeutral.npy'
xfile = 'ignore/data/x_30cmsDiffuseFractalNeutral.npy'
yfile = 'ignore/data/y_30cmsDiffuseFractalNeutral.npy'

# extract vector data for first frame to get x and y grids
vec_data = io.load_vc7(vc7_files[0])
x_vec, y_vec = vec_data['x'].values, vec_data['y'].values
DEBUG(f'x_vec shape: {x_vec.shape}')
DEBUG(f'xmin: {np.min(x_vec)}, xmax: {np.max(x_vec)}, ymin: {np.min(y_vec)}, ymax: {np.max(y_vec)}')
DEBUG(f'origin position: {np.where((-0.38 < x_vec) & (x_vec < 0.38))}, {np.where((-0.38 < y_vec) & (y_vec < 0.38))}')
xg, yg = np.meshgrid(x_vec, y_vec)
DEBUG(f'x and y grid shape: {xg.shape}')
spatial_res = x_vec[2] - x_vec[1]
DEBUG(f'spatial resolution: {spatial_res}')

# QC plot u and v if needed
if QC_plot:
    u_grid, v_grid = np.squeeze(vec_data['u'].values), np.squeeze(vec_data['v'].values)
    DEBUG(f'vval1:{v_grid[350, 395]}')
    v_grid = -1*v_grid  # vertical positive and negative directions are opposite for DaVis vs Python
    DEBUG(f'u_vec shape: {u_grid.shape}')

    vec_stride = 16
    fig, ax = plt.subplots()
    qv = ax.quiver(xg[::vec_stride, ::vec_stride], yg[::vec_stride, ::vec_stride], u_grid[::vec_stride, ::vec_stride], 
                v_grid[::vec_stride, ::vec_stride], scale=15, color='black')
    ax.set_aspect('equal', adjustable='box')
    plt.show()

# initialize .npy arrays for storing u, v data
u_stack = np.zeros((u_grid.shape[0], u_grid.shape[1], n_frames))
v_stack = np.zeros((v_grid.shape[0], v_grid.shape[1], n_frames))

for i in range(n_frames):
    vec_data = io.load_vc7(vc7_files[i])
    u = np.squeeze(vec_data['u'].values)
    v = np.squeeze(vec_data['v'].values)
    v = -1 * v  # correct for vertical positive/negative in DaVis vs Python

    u_stack[:, :, i] = u
    v_stack[:, :, i] = v

# save u, v, x, and y arrays
np.save(ufile, u_stack)
np.save(vfile, v_stack)
np.save(xfile, xg)
np.save(yfile, yg)

