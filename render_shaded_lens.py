import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh

font_path = 'C:/Windows/Fonts/msyh.ttc'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

out_dir = r'C:/Users/15085/.gemini/antigravity/scratch/dome_lens_sim/dassault_reproduction'
obj_path = os.path.join(out_dir, 'luneburg_lens_dassault_tapered_60mm.obj')
out_png = os.path.join(out_dir, 'luneburg_lens_shaded_render.png')
brain_png = r'C:/Users/15085/.gemini/antigravity/brain/5e3c28fb-1af2-4fc3-8ed4-297ca97a8ba8/luneburg_lens_shaded_render.png'

print('Loading mesh...')
mesh = trimesh.load(obj_path)
print(f'Loaded: {len(mesh.vertices)} verts, {len(mesh.faces)} faces')

# We can sample faces for clean, fast rendering (e.g. step=2 gives 446k faces)
faces_sample = mesh.faces[::2]
tris = mesh.vertices[faces_sample]

# Compute normals for sampled faces
v0, v1, v2 = tris[:, 0], tris[:, 1], tris[:, 2]
fn = np.cross(v1 - v0, v2 - v0)
norm = np.linalg.norm(fn, axis=1, keepdims=True)
norm[norm == 0] = 1.0
fn = fn / norm

# Compute directional lighting (Key light + Fill light + Ambient)
key_light = np.array([0.5, 0.4, 0.75])
key_light /= np.linalg.norm(key_light)

fill_light = np.array([-0.5, -0.3, 0.4])
fill_light /= np.linalg.norm(fill_light)

key_diffuse = np.clip(np.sum(fn * key_light, axis=1), 0.0, 1.0)
fill_diffuse = np.clip(np.sum(fn * fill_light, axis=1), 0.0, 1.0) * 0.35
ambient = 0.22

intensity = np.clip(ambient + 0.78 * key_diffuse + fill_diffuse, 0.0, 1.0)

base_cyan = np.array([0.05, 0.82, 0.95])
face_colors = intensity[:, None] * base_cyan

fig = plt.figure(figsize=(18, 8.2), facecolor='#080c14')

# Subplot 1: Full 3D Sphere with Depth & Shading
ax1 = fig.add_subplot(1, 2, 1, projection='3d', facecolor='#080c14')
p1 = Poly3DCollection(tris, facecolors=face_colors, edgecolors='none', alpha=0.98)
ax1.add_collection3d(p1)

R = 30.0
lim = R * 1.06
ax1.set_xlim(-lim, lim)
ax1.set_ylim(-lim, lim)
ax1.set_zlim(-lim, lim)
ax1.view_init(elev=22, azim=48)
ax1.set_axis_off()
ax1.set_title('【纯镂空实心立柱】高保真三维光影全貌 (完整球体)', color='#ffffff', fontsize=14, fontweight='bold', pad=14)
ax1.text2D(0.5, -0.02, '构型: Skeletal Gyroid 实心网络立柱 | 风格: 纯镂空科技风格 (零外壳) | 边缘: 水滴状光滑自然尖灭', 
           transform=ax1.transAxes, color='#70e000', fontsize=11, ha='center', va='top')

# Subplot 2: Equatorial Cutaway
# Use vertices to filter faces where centroid Y <= 0.1
centroids = np.mean(tris, axis=1)
cut_mask = (centroids[:, 1] <= 0.1)
tris_cut = tris[cut_mask]
fn_cut = fn[cut_mask]

key_diff_cut = np.clip(np.sum(fn_cut * key_light, axis=1), 0.0, 1.0)
fill_diff_cut = np.clip(np.sum(fn_cut * fill_light, axis=1), 0.0, 1.0) * 0.35
intensity_cut = np.clip(ambient + 0.78 * key_diff_cut + fill_diff_cut, 0.0, 1.0)
base_gold = np.array([1.0, 0.72, 0.12])
face_colors_cut = intensity_cut[:, None] * base_gold

ax2 = fig.add_subplot(1, 2, 2, projection='3d', facecolor='#080c14')
p2 = Poly3DCollection(tris_cut, facecolors=face_colors_cut, edgecolors='none', alpha=0.98)
ax2.add_collection3d(p2)

ax2.set_xlim(-lim, lim)
ax2.set_ylim(-lim, lim)
ax2.set_zlim(-lim, lim)
ax2.view_init(elev=32, azim=-45)
ax2.set_axis_off()
ax2.set_title('【内部剖切透视】三维立柱由粗到细的螺旋渐变', color='#ffffff', fontsize=14, fontweight='bold', pad=14)
ax2.text2D(0.5, -0.02, '球心粗壮实体立柱 (Dk≈2.02, 占比~67%) ──> 达索基准点 (Dk=1.786) ──> 外沿纤细水滴自然收束 (Dk→1.0)', 
           transform=ax2.transAxes, color='#ffd166', fontsize=11, ha='center', va='top')

plt.tight_layout()
print('Saving figure...')
plt.savefig(out_png, dpi=180, facecolor=fig.get_facecolor(), bbox_inches='tight')
import shutil
shutil.copyfile(out_png, brain_png)
print('Saved shaded render to:', out_png)
