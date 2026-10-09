"""
=============================================================================
方案三：【手性三联反重力悬浮托架】(Tri-Chiral Levitation Tripod Stand)
=============================================================================
设计精髓:
  1. 拓扑同源性 (C3 Chiral Symmetry):
     - 契合 Gyroid 的三配位拓扑骨架，三根流线型手性弯爪呈 120° 旋转对称优雅反卷升起
  2. 反重力悬浮视觉:
     - 托架在球心下方 (Z=38mm) 形成高精度球窝支承，透镜底部距离桌面悬空 8mm
     - 产生强烈的“球体在三爪之间反重力磁悬停”的科幻空灵感
  3. 中央暗室能量井 (Central Light Well):
     - 底座中央设有 28mm 直径通光孔，底部放置灯光可将光线射入透镜内部全反射点亮
  4. 完美打印工艺:
     - 底面在 Z=0 绝对水平平整，直接牢固吸附在打印平台上，底部 100% 免支撑！
     - 模型 100% 封闭水密 (Watertight: True)
=============================================================================
"""

import os
import struct
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage.measure import marching_cubes
import trimesh

# 配置中文字体
font_path = 'C:/Windows/Fonts/msyh.ttc'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def generate_tripod_stand(R_sphere=30.0, Z_c=38.0, Nx=180, Ny=180, Nz=90, smooth_iters=8):
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)

    out_stl = os.path.join(out_dir, "luneburg_lens_stand_chiral_tripod.stl")
    out_obj = os.path.join(out_dir, "luneburg_lens_stand_chiral_tripod.obj")
    out_png = os.path.join(out_dir, "luneburg_lens_stand_chiral_tripod_render.png")
    brain_dir = r"C:/Users/15085/.gemini/antigravity/brain/5e3c28fb-1af2-4fc3-8ed4-297ca97a8ba8"

    print("=" * 78)
    print(">>> 正在启动【手性三联反重力悬浮托架】(Tri-Chiral Levitation Tripod) 3D 模型生成器...")
    print("=" * 78)
    print(f"[*] 适配透镜球体半径 : R = {R_sphere:.1f} mm (外径 D = {2*R_sphere:.1f} mm)")
    print(f"[*] 透镜悬浮球心高度 : Z_c = {Z_c:.1f} mm (透镜球底离桌面悬空 {Z_c - R_sphere:.1f} mm)")
    print(f"[*] 底座网格计算精度 : {Nx} x {Ny} x {Nz} 体素")
    print("[*] 核心功能特征     : 3爪手性流线环抱 | 100% 水密底板 | 中央 28mm LED 导光能量井")

    # 1. 建立空间物理网格 [-48, 48] x [-48, 48] x [-2, 44]
    x = np.linspace(-48.0, 48.0, Nx)
    y = np.linspace(-48.0, 48.0, Ny)
    z = np.linspace(-2.0, 44.0, Nz)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    P = np.stack([X, Y, Z], axis=-1)

    R_xy = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)

    # 2. 底盘三瓣外凸环翼几何 (Base Three-lobed Ring)
    # 外径: 在 0°, 120°, 240° 外凸至 43.5mm (跨距 87mm)，在 60°, 180°, 300° 内收至 34.5mm
    R_out = 39.0 + 4.5 * np.cos(3.0 * Theta)
    R_in = 14.0 # 28mm 直径中央透光孔
    d_r = np.maximum(R_in - R_xy, R_xy - R_out)
    d_z = np.maximum(-Z, Z - 4.5) # 底座厚度 4.5mm
    phi_base = np.maximum(d_r, d_z)

    # 3. 三根手性悬臂弯爪 (Three Chiral Swept Aerodynamic Arms)
    phi_arms = np.full_like(X, 100.0)
    u_samples = np.linspace(0.0, 1.0, 30)
    z_curve = 2.0 + 34.0 * u_samples
    r_curve = 38.5 - 12.8 * (u_samples**1.1) # 从 38.5 向内收至 25.7
    th_twist = 0.46 * (u_samples**1.2) # 约 26° 手性空间螺旋扭转
    rad_curve = 4.2 - 1.3 * u_samples # 根部粗 8.4mm，顶部细 5.8mm

    for k in range(3):
        th_base = k * (2.0 * np.pi / 3.0)
        nodes = np.column_stack([
            r_curve * np.cos(th_base + th_twist),
            r_curve * np.sin(th_base + th_twist),
            z_curve
        ])
        for i in range(len(nodes) - 1):
            A = nodes[i]
            B = nodes[i+1]
            AB = B - A
            AB2 = np.dot(AB, AB)
            AP = P - A
            t_proj = np.clip(np.sum(AP * AB, axis=-1) / AB2, 0.0, 1.0)
            closest = A + t_proj[..., None] * AB
            dist = np.linalg.norm(P - closest, axis=-1) - (0.5 * (rad_curve[i] + rad_curve[i+1]))
            phi_arms = np.minimum(phi_arms, dist)

    # 4. 底座与三爪布尔平滑融合 (Smooth Minimum Union)
    def smin(a, b, k=2.2):
        h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
        return b * (1.0 - h) + a * h - k * h * (1.0 - h)

    phi_solid = smin(phi_base, phi_arms, k=2.0)

    # 5. 透镜自适应球窝切削 (Sphere Cradle Pocket with 0.3mm tolerance)
    R_cradle = R_sphere + 0.30 # 30.3 mm，保证透镜顺畅放落不卡滞
    d_sphere = R_cradle - np.sqrt(X**2 + Y**2 + (Z - Z_c)**2)
    phi_stand = np.maximum(phi_solid, d_sphere)

    # 6. 底面 Z=0 绝对平整截断面
    phi_stand = np.maximum(phi_stand, -Z)

    # 7. Marching Cubes 等值面网格提取
    print("[*] 正在执行等值面网格提取 (Marching Cubes)...")
    verts, faces, _, _ = marching_cubes(phi_stand, level=0.0)
    verts[:, 0] = verts[:, 0] * (96.0 / (Nx - 1)) - 48.0
    verts[:, 1] = verts[:, 1] * (96.0 / (Ny - 1)) - 48.0
    verts[:, 2] = verts[:, 2] * (46.0 / (Nz - 1)) - 2.0

    mesh = trimesh.Trimesh(vertices=verts, faces=faces)
    mesh.merge_vertices()

    # 8. 网格光顺与底面绝对水平对齐
    print(f"[*] 正在执行 Taubin 几何平滑与底面吸附对齐 ({smooth_iters} 次迭代)...")
    is_bottom = mesh.vertices[:, 2] < 0.25
    trimesh.smoothing.filter_taubin(mesh, iterations=smooth_iters)
    mesh.vertices[is_bottom, 2] = 0.0 # 强制贴合绝对水平面 Z=0
    trimesh.repair.fix_normals(mesh)

    bounds = mesh.bounds
    print("[+] 手性三联托架网格生成指标:")
    print(f"    - 顶点数: {len(mesh.vertices):,}, 三角面数: {len(mesh.faces):,}")
    print(f"    - 物理尺寸: 宽度 X[{bounds[0][0]:.1f}, {bounds[1][0]:.1f}], 深度 Y[{bounds[0][1]:.1f}, {bounds[1][1]:.1f}], 高度 Z[{bounds[0][2]:.1f}, {bounds[1][2]:.1f}] mm")
    print(f"    - 最大展开跨距: {np.max(np.sqrt(mesh.vertices[:,0]**2 + mesh.vertices[:,1]**2))*2:.1f} mm")
    print(f"    - 底面平整顶点数: {np.sum(is_bottom):,}")
    print(f"    - 水密流形封闭性 (Watertight): {mesh.is_watertight}")

    # 9. 导出 3D 打印标准二进制 STL
    print(f"[*] 正在导出二进制 STL 文件: {out_stl}")
    with open(out_stl, 'wb') as f:
        header = b'Tri-Chiral Levitation Tripod Stand Binary STL'.ljust(80, b'\0')[:80]
        f.write(header)
        f.write(struct.pack('<I', len(mesh.faces)))
        for tri in mesh.faces:
            v0, v1, v2 = mesh.vertices[tri[0]], mesh.vertices[tri[1]], mesh.vertices[tri[2]]
            n = np.cross(v1 - v0, v2 - v0)
            norm = np.linalg.norm(n)
            if norm > 0: n /= norm
            f.write(struct.pack('<3f', *n))
            f.write(struct.pack('<3f', *v0))
            f.write(struct.pack('<3f', *v1))
            f.write(struct.pack('<3f', *v2))
            f.write(struct.pack('<H', 0))
    print(f"[+] STL 文件已导出: {out_stl} ({os.path.getsize(out_stl)/(1024*1024):.2f} MB)")

    # 10. 导出 OBJ 文件
    print(f"[*] 正在导出 OBJ 文件: {out_obj}")
    with open(out_obj, 'w', encoding='utf-8') as f:
        f.write("# Tri-Chiral Levitation Tripod Stand for Luneburg Lens D=60mm\n")
        for v in mesh.vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for norm in mesh.vertex_normals:
            f.write(f"vn {norm[0]:.4f} {norm[1]:.4f} {norm[2]:.4f}\n")
        for tri in mesh.faces:
            f.write(f"f {tri[0]+1}//{tri[0]+1} {tri[1]+1}//{tri[1]+1} {tri[2]+1}//{tri[2]+1}\n")
    print(f"[+] OBJ 文件已导出: {out_obj} ({os.path.getsize(out_obj)/(1024*1024):.2f} MB)")

    # 11. 渲染高保真三维效果图 (左图: 托架单独展示, 右图: 托架托举 1/8 开窗透镜的组合实物展示)
    print("[*] 正在渲染托架与透镜装配高保真光影图...")
    fig = plt.figure(figsize=(19, 8.8), facecolor='#090e17')

    tris_stand = mesh.vertices[mesh.faces[::2]] # 抽样
    v0, v1, v2 = tris_stand[:, 0], tris_stand[:, 1], tris_stand[:, 2]
    fn_stand = np.cross(v1 - v0, v2 - v0)
    norm = np.linalg.norm(fn_stand, axis=1, keepdims=True)
    norm[norm == 0] = 1.0
    fn_stand = fn_stand / norm

    key_light = np.array([0.65, 0.45, 0.60])
    key_light /= np.linalg.norm(key_light)
    fill_light = np.array([-0.40, -0.60, 0.50])
    fill_light /= np.linalg.norm(fill_light)

    diff1 = np.clip(np.sum(fn_stand * key_light, axis=1), 0.0, 1.0)
    diff2 = np.clip(np.sum(fn_stand * fill_light, axis=1), 0.0, 1.0) * 0.35
    shading_stand = np.clip(0.22 + 0.78 * diff1 + diff2, 0.0, 1.0)
    color_titanium = np.array([0.15, 0.85, 0.82]) # 科技青冷钛合金色

    # 左图: 托架单独全貌
    ax1 = fig.add_subplot(1, 2, 1, projection='3d', facecolor='#090e17')
    p1 = Poly3DCollection(tris_stand, facecolors=shading_stand[:, None] * color_titanium, edgecolors='none', alpha=0.98)
    ax1.add_collection3d(p1)
    ax1.set_xlim(-45, 45); ax1.set_ylim(-45, 45); ax1.set_zlim(0, 50)
    ax1.view_init(elev=28, azim=42)
    ax1.set_axis_off()
    ax1.set_title("手性三联反重力托架 (Tri-Chiral Stand 单独特写)", color='#ffffff', fontsize=14, fontweight='bold', pad=14)
    ax1.text2D(0.5, -0.02, "3爪120°手性流线升起 | 中央28mm导光井 | Z=0水平免支撑底面 | R=30.3mm自适应球窝", 
               transform=ax1.transAxes, color='#38bdf8', fontsize=10.5, ha='center', va='top')

    # 右图: 托架托举 1/8 开窗透镜装配效果图
    ax2 = fig.add_subplot(1, 2, 2, projection='3d', facecolor='#090e17')
    # 重新画托架
    p2 = Poly3DCollection(tris_stand, facecolors=shading_stand[:, None] * color_titanium, edgecolors='none', alpha=0.98)
    ax2.add_collection3d(p2)

    # 加载已有的 1/8 开窗透镜模型并平移至 Z_c=38mm
    lens_stl = os.path.join(out_dir, "luneburg_lens_dassault_cage_60mm_cutaway18.stl")
    if os.path.exists(lens_stl):
        lens_mesh = trimesh.load(lens_stl)
        lens_verts = lens_mesh.vertices.copy()
        # 将透镜球心平移到 Z_c
        lens_verts[:, 2] += Z_c
        tris_lens = lens_verts[lens_mesh.faces[::4]] # 抽样
        lv0, lv1, lv2 = tris_lens[:, 0], tris_lens[:, 1], tris_lens[:, 2]
        fn_lens = np.cross(lv1 - lv0, lv2 - lv0)
        norm_l = np.linalg.norm(fn_lens, axis=1, keepdims=True)
        norm_l[norm_l == 0] = 1.0
        fn_lens = fn_lens / norm_l

        diff1_l = np.clip(np.sum(fn_lens * key_light, axis=1), 0.0, 1.0)
        diff2_l = np.clip(np.sum(fn_lens * fill_light, axis=1), 0.0, 1.0) * 0.35
        shading_lens = np.clip(0.20 + 0.80 * diff1_l + diff2_l, 0.0, 1.0)
        color_gold = np.array([1.0, 0.76, 0.20])

        p_lens = Poly3DCollection(tris_lens, facecolors=shading_lens[:, None] * color_gold, edgecolors='none', alpha=0.95)
        ax2.add_collection3d(p_lens)

    ax2.set_xlim(-45, 45); ax2.set_ylim(-45, 45); ax2.set_zlim(0, 75)
    ax2.view_init(elev=24, azim=48)
    ax2.set_axis_off()
    ax2.set_title("透镜装配展示 (60mm 透镜反重力悬浮于托架之中)", color='#ffffff', fontsize=14, fontweight='bold', pad=14)
    ax2.text2D(0.5, -0.02, "琥珀金: 1/8 开窗龙伯透镜 (球底悬空 8mm) | 青钛冷光: 手性三联托架 (稳固无遮挡托举)", 
               transform=ax2.transAxes, color='#fde047', fontsize=10.5, ha='center', va='top')

    plt.tight_layout()
    plt.savefig(out_png, dpi=200, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"[+] 3D 全景高保真渲染图已输出: {out_png}")

    if os.path.exists(brain_dir):
        import shutil
        brain_png = os.path.join(brain_dir, os.path.basename(out_png))
        shutil.copyfile(out_png, brain_png)
        print(f"[+] 渲染图已同步至 Artifact 目录: {brain_png}")

    print("=" * 78)
    print("[+] 手性三联反重力托架生成全部完成！")
    print("=" * 78)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="生成手性三联反重力悬浮托架")
    parser.add_argument("--radius", "-R", type=float, default=30.0, help="适配透镜半径 (mm)")
    parser.add_argument("--height", "-Z", type=float, default=38.0, help="球心悬浮高度 Z_c (mm)")
    args = parser.parse_args()

    generate_tripod_stand(R_sphere=args.radius, Z_c=args.height)
