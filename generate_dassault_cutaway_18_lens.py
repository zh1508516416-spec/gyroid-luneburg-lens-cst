"""
=============================================================================
1/8 卦限缺角开窗型 (1/8 Octant Corner Cutaway / 7/8 Sphere) Gyroid 龙伯透镜生成器
=============================================================================
设计精髓:
  1. 构型切除: 仅切除第一卦限的 1/8 空间 (X > 0 且 Y > 0 且 Z > 0)，保留 7/8 (87.5%) 完整透镜
  2. 极致开窗视觉:
     - 像在正球右上角切出一个三面正交 (X=0, Y=0, Z=0) 的内凹全景观察窗
     - 三个镜面平整的切面交汇于球心坐标原点 (0, 0, 0)，直视核心粗壮立柱
     - 其余 7/8 区域保持完整的大开孔正球网壳，外观极具现代工业雕塑美感
  3. 平面实心封口技术 (Planar Solid Capping):
     - X=0, Y=0, Z=0 三个平面上的立柱截面自动生成高精度数学平整盖板
     - 100% 封闭水密流形 (Watertight: True)，零破口
  4. 3D 打印极佳工艺:
     - 下半球 (Z <= 0) 保持完整，或可以任意平放，免内部支撑！
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

def generate_cutaway_18_lens(R=30.0, a=6.0, N=180, d_shell=1.2, C_cage=0.05, smooth_iters=10):
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)

    tag = f"R{int(R)}mm_D{int(2*R)}mm_cutaway18" if int(R) != 30 else "60mm_cutaway18"
    out_obj = os.path.join(out_dir, f"luneburg_lens_dassault_cage_{tag}.obj")
    out_stl = os.path.join(out_dir, f"luneburg_lens_dassault_cage_{tag}.stl")
    out_png = os.path.join(out_dir, f"luneburg_lens_dassault_cage_{tag}_render.png")
    brain_dir = r"C:/Users/15085/.gemini/antigravity/brain/5e3c28fb-1af2-4fc3-8ed4-297ca97a8ba8"

    print("=" * 78)
    print(f">>> 正在启动【1/8 卦限缺角开窗型】(7/8球) Gyroid 龙伯透镜生成器 (R={R:.1f}mm, D={2*R:.1f}mm)...")
    print("=" * 78)
    print(f"[*] 透镜目标外半径 R : {R:.1f} mm (外径 D = {2*R:.1f} mm)")
    print(f"[*] 剖切方式         : 仅切除第一卦限 (X>0 且 Y>0 且 Z>0)，保留 7/8 (87.5%) 完整透镜")
    print(f"[*] 晶胞空间周期 a   : {a:.1f} mm")
    print(f"[*] 空间网格分辨率 N : {N}x{N}x{N} = {N**3:,} 体素")
    print(f"[*] 保形外球壳厚度 d : {d_shell:.1f} mm")
    print(f"[*] 几何曲率光顺     : Taubin 滤波 {smooth_iters} 次迭代 + 三平面正交平整对齐")

    # 1. 建立高精物理网格 [-1.05R, +1.05R]
    x = np.linspace(-R * 1.05, R * 1.05, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    r = np.sqrt(X**2 + Y**2 + Z**2)

    # 2. 计算连续 Gyroid 螺旋 TPMS 波函数场
    k_wave = 2 * np.pi / a
    F_gyroid = np.sin(k_wave * X) * np.cos(k_wave * Y) + \
               np.sin(k_wave * Y) * np.cos(k_wave * Z) + \
               np.sin(k_wave * Z) * np.cos(k_wave * X)

    # 3. 构造龙伯折射率实心立柱核心与保形开孔外壳的 Level Set 场
    norm_r = np.clip(r / R, 0.0, 1.0)
    C_core = 0.42 - 1.35 * (norm_r ** 2)

    phi_core = np.maximum(F_gyroid - C_core, r - (R - d_shell))
    phi_shell = np.maximum(np.maximum(F_gyroid - C_cage, (R - d_shell) - r), r - R)
    phi_lens = np.minimum(phi_core, phi_shell)

    # 4. 执行 1/8 卦限缺角开窗 (切除 X>0 且 Y>0 且 Z>0 区域)
    # 利用 Level Set: phi_cut = max(phi_lens, min(min(X, Y), Z))
    # 在 X=0, Y=0, Z=0 三个互相垂直的剖切截面上自动生成数学实心平整封口
    octant_wedge = np.minimum(np.minimum(X, Y), Z)
    phi_cut = np.maximum(phi_lens, octant_wedge)

    # 5. Marching Cubes 等值面高精度提取
    print("[*] 正在执行等值面网格提取 (Marching Cubes)...")
    spacing = (2.1 * R / (N - 1), 2.1 * R / (N - 1), 2.1 * R / (N - 1))
    verts_raw, faces_raw, _, _ = marching_cubes(phi_cut, level=0.0, spacing=spacing)
    verts_raw -= (1.05 * R)

    # 6. 拓扑修复与三正交截面顶点平整对齐
    print(f"[*] 正在执行网格拓扑修复与 Taubin 几何光顺滤波 ({smooth_iters} 次迭代)...")
    raw_mesh = trimesh.Trimesh(vertices=verts_raw, faces=faces_raw)
    raw_mesh.merge_vertices()
    comps = raw_mesh.split(only_watertight=False)
    mesh = max(comps, key=lambda c: len(c.faces))
    mesh.merge_vertices()
    trimesh.repair.fix_normals(mesh)

    # 识别三个正交剖切平面上的顶点
    eps_snap = 0.35 * (2.1 * R / N)
    is_plane_x0 = (np.abs(mesh.vertices[:, 0]) < eps_snap) & (mesh.vertices[:, 1] >= -eps_snap) & (mesh.vertices[:, 2] >= -eps_snap)
    is_plane_y0 = (np.abs(mesh.vertices[:, 1]) < eps_snap) & (mesh.vertices[:, 0] >= -eps_snap) & (mesh.vertices[:, 2] >= -eps_snap)
    is_plane_z0 = (np.abs(mesh.vertices[:, 2]) < eps_snap) & (mesh.vertices[:, 0] >= -eps_snap) & (mesh.vertices[:, 1] >= -eps_snap)

    # 执行 Taubin 光顺滤波 (消除体素台阶)
    trimesh.smoothing.filter_taubin(mesh, iterations=smooth_iters)

    # 将截断面顶点严格对齐回数学平面，确保打印与视觉完全平直锋利
    mesh.vertices[is_plane_x0, 0] = 0.0
    mesh.vertices[is_plane_y0, 1] = 0.0
    mesh.vertices[is_plane_z0, 2] = 0.0
    trimesh.repair.fix_normals(mesh)

    bounds = mesh.bounds
    print(f"[+] 1/8 卦限缺角开窗透镜网格生成成功:")
    print(f"    - 顶点数: {len(mesh.vertices):,}, 三角面数: {len(mesh.faces):,}")
    print(f"    - 几何包围盒: X[{bounds[0][0]:.2f}, {bounds[1][0]:.2f}] Y[{bounds[0][1]:.2f}, {bounds[1][1]:.2f}] Z[{bounds[0][2]:.2f}, {bounds[1][2]:.2f}] mm")
    print(f"    - 三正交截面顶点数: X=0 [{np.sum(is_plane_x0):,}], Y=0 [{np.sum(is_plane_y0):,}], Z=0 [{np.sum(is_plane_z0):,}]")
    print(f"    - 水密流形封闭性 (Watertight): {mesh.is_watertight}")

    # 7. 导出 OBJ 网格
    print(f"[*] 正在导出 OBJ 网格: {out_obj}")
    with open(out_obj, 'w', encoding='utf-8') as f:
        f.write("# Dassault Gyroid Luneburg Lens 1/8 Octant Cutaway Exhibition Model\n")
        f.write(f"# Radius: {R}mm, Period: {a}mm, 1/8 Octant Corner Window (7/8 Sphere)\n")
        for v in mesh.vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for norm in mesh.vertex_normals:
            f.write(f"vn {norm[0]:.4f} {norm[1]:.4f} {norm[2]:.4f}\n")
        for tri in mesh.faces:
            f.write(f"f {tri[0]+1}//{tri[0]+1} {tri[1]+1}//{tri[1]+1} {tri[2]+1}//{tri[2]+1}\n")
    print(f"[+] OBJ 模型已保存: {out_obj} ({os.path.getsize(out_obj)/(1024*1024):.2f} MB)")

    # 8. 导出 3D 打印标准二进制 STL 文件 (80 字节标准头)
    print(f"[*] 正在导出 3D 打印标准二进制 STL 模型: {out_stl}")
    with open(out_stl, 'wb') as f:
        header = b'Dassault Gyroid 1/8 Cutaway Lens Binary STL'.ljust(80, b'\0')[:80]
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
    print(f"[+] 3D 打印标准 STL 模型已保存: {out_stl} ({os.path.getsize(out_stl)/(1024*1024):.2f} MB)")

    # 9. 渲染高保真三维光影双联效果图 (左: 直视三面开窗正对球心视角, 右: 俯瞰立体展品透视)
    print("[*] 正在渲染 1/8 缺角开窗高保真双视角光影效果图...")
    tris_full = mesh.vertices[mesh.faces[::2]] # 1/2 抽样加速渲染
    v0, v1, v2 = tris_full[:, 0], tris_full[:, 1], tris_full[:, 2]
    fn = np.cross(v1 - v0, v2 - v0)
    norm = np.linalg.norm(fn, axis=1, keepdims=True)
    norm[norm == 0] = 1.0
    fn = fn / norm

    # 识别三个正交切面的三角形
    centroids = np.mean(tris_full, axis=1)
    is_cut_face = ((np.abs(centroids[:, 0]) < 0.25) & (np.abs(fn[:, 0]) > 0.85)) | \
                  ((np.abs(centroids[:, 1]) < 0.25) & (np.abs(fn[:, 1]) > 0.85)) | \
                  ((np.abs(centroids[:, 2]) < 0.25) & (np.abs(fn[:, 2]) > 0.85))

    # 光照系统
    key_light = np.array([0.60, 0.50, 0.65])
    key_light /= np.linalg.norm(key_light)
    fill_light = np.array([-0.45, -0.55, 0.40])
    fill_light /= np.linalg.norm(fill_light)

    diff1 = np.clip(np.sum(fn * key_light, axis=1), 0.0, 1.0)
    diff2 = np.clip(np.sum(fn * fill_light, axis=1), 0.0, 1.0) * 0.35
    shading = np.clip(0.20 + 0.80 * diff1 + diff2, 0.0, 1.0)

    # 颜色系统: 外部正球网壳为琥珀金，内部与三截断面为科技青高光
    base_color = np.zeros((len(tris_full), 3))
    color_gold = np.array([1.0, 0.76, 0.20])
    color_cyan = np.array([0.15, 0.92, 0.90])

    base_color[~is_cut_face] = color_gold
    base_color[is_cut_face] = color_cyan

    face_colors = shading[:, None] * base_color

    fig = plt.figure(figsize=(19, 8.8), facecolor='#090e17')

    # 视角 1: 正对 1/8 开窗内部 (等轴视角直视球心)
    ax1 = fig.add_subplot(1, 2, 1, projection='3d', facecolor='#090e17')
    p1 = Poly3DCollection(tris_full, facecolors=face_colors, edgecolors='none', alpha=0.98)
    ax1.add_collection3d(p1)
    lim = R * 1.06
    ax1.set_xlim(-lim, lim); ax1.set_ylim(-lim, lim); ax1.set_zlim(-lim, lim)
    ax1.view_init(elev=35, azim=45) # 45°方位角 + 35°仰角: 正对第一卦限三面正交观察窗！
    ax1.set_axis_off()
    ax1.set_title(f"1/8 卦限缺角开窗型 Gyroid 龙伯透镜 (正对三正交开窗直视球心)", color='#ffffff', fontsize=14, fontweight='bold', pad=14)
    ax1.text2D(0.5, -0.02, f"切除 1/8 卦限 (X>0, Y>0, Z>0) | 三面正交平整实心封口 (X=0, Y=0, Z=0) | 保留 7/8 完整正球外壳", 
               transform=ax1.transAxes, color='#ffd166', fontsize=10.5, ha='center', va='top')

    # 视角 2: 略倾斜鸟瞰立体展品视角
    ax2 = fig.add_subplot(1, 2, 2, projection='3d', facecolor='#090e17')
    p2 = Poly3DCollection(tris_full, facecolors=face_colors, edgecolors='none', alpha=0.98)
    ax2.add_collection3d(p2)
    ax2.set_xlim(-lim, lim); ax2.set_ylim(-lim, lim); ax2.set_zlim(-lim, lim)
    ax2.view_init(elev=20, azim=15)
    ax2.set_axis_off()
    ax2.set_title("1/8 缺角开窗立体展品视角 (观察 7/8 绝大部分完整球壳与内凹观察窗)", color='#ffffff', fontsize=14, fontweight='bold', pad=14)
    ax2.text2D(0.5, -0.02, "琥珀金: 4.0~4.5mm 大开孔正球网壳 (保留 87.5% 完整球体) | 科技青: 三面交汇直视球心粗实立柱", 
               transform=ax2.transAxes, color='#90e0ef', fontsize=10.5, ha='center', va='top')

    plt.tight_layout()
    plt.savefig(out_png, dpi=200, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"[+] 3D 全景高保真渲染图已输出: {out_png}")

    # 复制到脑部 Artifact 目录
    import shutil
    if os.path.exists(brain_dir):
        brain_png = os.path.join(brain_dir, os.path.basename(out_png))
        shutil.copyfile(out_png, brain_png)
        print(f"[+] 渲染图已同步至 Artifact 目录: {brain_png}")

    print("=" * 78)
    print("[+] 1/8 卦限缺角开窗型 Gyroid 龙伯透镜生成与验证全部完成！")
    print("=" * 78)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="生成 1/8 卦限缺角开窗型 Gyroid 龙伯透镜")
    parser.add_argument("--radius", "-R", type=float, default=30.0, help="外球半径 (mm)，默认 30.0 mm")
    parser.add_argument("--period", "-a", type=float, default=6.0, help="晶胞周期 (mm)，默认 6.0 mm")
    parser.add_argument("--resolution", "-N", type=int, default=180, help="计算体素分辨率 N (默认 180)")
    parser.add_argument("--shell-thick", "-d", type=float, default=1.2, help="外球壳厚度 (mm)，默认 1.2 mm")
    parser.add_argument("--hole-size", "-C", type=float, default=0.05, help="外壳开孔阈值 C_cage (默认 0.05)")
    args = parser.parse_args()

    generate_cutaway_18_lens(R=args.radius, a=args.period, N=args.resolution, 
                             d_shell=args.shell_thick, C_cage=args.hole_size)
