import numpy as np
import imageio
import os
import cmasher as cmr


# --- USER SETTINGS ---
input_npy = 'ignore/data/FTLE_0.4s_30cmsDiffusiveFractalNeutral.npy'  # shape: (n_frames, ny, nx)
output_dir = 'ignore/data/ftle_heightmaps'
vmin = None  # e.g. 0.1 for log-like fields
vmax = None  # e.g. 2.0 for log-like fields
clip_outliers = False  # Optional clipping for extreme values
colormap_output = True  # Set True to export colormapped version

# --- Create output directory ---
os.makedirs(output_dir, exist_ok=True)

# --- Load FTLE movie data ---
ftle_series = np.load(input_npy)  # shape: (n_frames, ny, nx)
n_frames = ftle_series.shape[0]

# --- Optional: import colormap for color versions ---
if colormap_output:
    cmap = cmr.eclipse

# --- Process each frame ---
for i in range(n_frames):
    field = ftle_series[i]

    # Optional: clip outliers for visual consistency
    if clip_outliers:
        field = np.clip(field, np.percentile(field, 1), np.percentile(field, 99))

    # Normalize each frame independently unless vmin/vmax are specified
    min_val = vmin if vmin is not None else field.min()
    max_val = vmax if vmax is not None else field.max()
    norm = (field - min_val) / (max_val - min_val + 1e-10)
    norm = np.clip(norm, 0, 1)

    # Convert to grayscale image (uint8)
    img_gray = (norm * 255).astype(np.uint8)

    # Save grayscale heightmap
    gray_path = os.path.join(output_dir, f'ftle_frame_{i:04d}.png')
    imageio.imwrite(gray_path, img_gray)

    # Optional: save colormap version
    if colormap_output:
        img_color = (cmap(norm)[:, :, :3] * 255).astype(np.uint8)
        color_path = os.path.join(output_dir, f'ftle_colormap_{i:04d}.png')
        imageio.imwrite(color_path, img_color)

    print(f"Saved frame {i+1}/{n_frames} → {gray_path}")

print(f"\n Completed. {n_frames} FTLE frames saved to → {output_dir}")
