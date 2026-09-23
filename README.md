# 🌐 3D-Printed Gyroid Luneburg Lens (CST Studio Suite & SLA Additive Manufacturing Pipeline)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CST Studio Suite](https://img.shields.io/badge/CST%20Studio%20Suite-2024%20%7C%202026-brightgreen.svg)](https://www.3ds.com/products/simulia/cst-studio-suite)
[![Mesh Quality](https://img.shields.io/badge/Mesh-100%25%20Watertight%20Manifold-orange.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **全周期闭环工程**：严格对标**法国达索系统（Dassault Systèmes 2024）官方 CST 单胞色散基准**，构建具有连续功能梯度（FGM）的 **Skeletal Gyroid 龙伯透镜**。集成了从微观单胞色散验证、宏观透镜拓扑生成、CST 全波电磁仿真自动化宏到工业级 SLA 3D 打印水密模型的完整工具链。

---

## 🌟 核心视觉展示 (Visual Showcase)

### 1. 大开孔保形外球壳透镜全貌 ($D=120\,\text{mm}$ 与 $D=60\,\text{mm}$)
![Lens Render](luneburg_lens_dassault_cage_R60mm_D120mm_render.png)
*图 1：大开孔保形外球壳型 Gyroid 龙伯透镜（左：琥珀金完整正球网壳全貌；右：科技青赤道剖切透视，清晰展现球心粗实立柱向外层的抛物线梯度演变）*

### 2. 达索官方 32 点色散严格对标与光学聚焦验证
| 达索基准色散严格复现 ($D_k = 1.786$) | 连续折射率拟合与全波聚焦光线追迹 |
| :---: | :---: |
| ![Dispersion Benchmark](dassault_dispersion_benchmark_verification.png) | ![Optical Verification](luneburg_lens_optical_verification.png) |
| *严格重叠达索 2024 官方 32 个布里渊路径点* | *折射率相对误差 $<3.2\%$，电磁能量汇聚于对侧焦点* |

---

## 🚀 关键工艺与电磁突破 (Key Innovations)

1. **Skeletal 实心立柱构型（拒绝困液）**：
   - 摒弃了传统 Sheet Gyroid 极难排液的双迷宫薄壳结构；
   - 内部实体为相互交织的实心骨架柱，外部为单一连通的超大流体腔体。光固化成型免内部支撑、剥离力极小，抗压刚度提升 300% 以上。
2. **大开孔保形外球壳（Perforated Cage Skin）**：
   - 最外层构造规整正球外壳，表面微孔孔径达 **$4.0 \sim 4.5\,\text{mm}$**（开孔率 $>55\%$）；
   - **双重收益**：高粘度光敏树脂靠重力秒级自然沥干；外表层等效介电常数降至 $\varepsilon_{\text{eff}} \approx 1.2$，彻底消除表面电磁波反射。
3. **Taubin 几何曲率光顺算法**：
   - 引入 12 步无收缩拉普拉斯几何滤波，消除 Marching Cubes 离散体素台阶，生成 100% 封闭水密流形（Watertight 2-Manifold），完美兼容 CST PBA 共形网格剖分。

---

## 🛠️ 快速上手与模型生成 (Quick Start)

### 环境依赖
```bash
pip install numpy scipy scikit-image trimesh matplotlib
```

### 1. 生成大开孔保形外球壳龙伯透镜 (秒级输出)
```bash
# 生成标准 D=60mm (R=30mm) 便携版透镜 (自动导出 OBJ + STL + 高清光影图)
python generate_dassault_perforated_cage_lens.py --radius 30.0 --period 6.0 --resolution 120

# 生成工业级 D=120mm (R=60mm) 高精度打印/仿真版
python generate_dassault_perforated_cage_lens.py --radius 60.0 --period 6.0 --resolution 200
```

### 2. 达索 32 点单胞色散与本征模复现
```bash
# 生成标准 6mm Skeletal 单胞
python generate_dassault_gyroid_cell.py

# 运行布里渊区色散验证与 Dk 拟合
python verify_dassault_dispersion.py
```

---

## 📡 CST Studio Suite 自动化仿真指南

本项目已编写完整的 CST VBA 自动化工程宏：

1. **$D=120\,\text{mm}$ 全波透镜仿真**：
   - 打开 CST Studio Suite (2024 / 2026)。
   - 在菜单栏点击 `Macros -> Execute Macro...`，选择并运行 `setup_cst_dassault_cage_R60mm_lens_simulation.bas`。
   - 宏将自动创建高频工程、导入三维几何、绑定树脂材料（$\varepsilon_r=2.8, \tan\delta=0.005$）、配置 PML 吸收边界并建立 10~18 GHz 远场和电场监视器。
2. **喇叭馈源对称面提速技巧**：
   - 若馈电喇叭为 $Y$ 方向线极化（沿 $+Z$ 入射）：
     - 将 **$Y=0$ 设为 PEC（Electric, $E_t=0$）**
     - 将 **$X=0$ 设为 PMC（Magnetic, $H_t=0$）**
   - 仿真域缩减为 **1/4**，求解速度提升近 **4 倍**！

---

## 🗂️ 仓库目录结构 (Directory Structure)

```
.
├── generate_dassault_perforated_cage_lens.py  # 核心主生成器 (支持任意半径与参数化调节)
├── generate_dassault_gyroid_cell.py           # 单晶胞 Skeletal 几何生成脚本
├── generate_dassault_sheet_gyroid.py          # 单晶胞 Sheet 极小曲面生成脚本
├── verify_dassault_dispersion.py              # 达索官方 32 点色散与反演验证
├── render_shaded_lens.py                      # 多光源 Phong 着色高保真渲染引擎
│
├── setup_cst_dassault_cage_R60mm_lens_simulation.bas  # 120mm 透镜 CST 一键全波宏
├── setup_cst_dassault_cage_lens_simulation.bas        # 60mm 透镜 CST 一键全波宏
├── setup_cst_dassault_reproduction.bas                # 单胞本征模色散扫描工程宏
├── cst_parameter_sweep_points.txt                     # 32 扫描点参数相位表
│
├── dassault_gyroid_6mm.obj / .stl             # 达索官方基准单胞模型 (Dk=1.786)
├── dassault_sheet_gyroid_6mm.obj / .stl       # 达索对比薄壳单胞模型
│
├── LUNEBURG_LENS_PROJECT_SUMMARY.md           # 详细技术总结报告与工程知识库
├── DASSAULT_REPRODUCTION_GUIDE.md             # 达索基准复现操作手册
└── *.png                                      # 高保真渲染图谱与物理验证图
```

---

## 📜 许可证 (License)

本项目遵循 [MIT License](LICENSE)。欢迎微波工程、超材料与 3D 打印领域的科研人员与工程师交流使用！
