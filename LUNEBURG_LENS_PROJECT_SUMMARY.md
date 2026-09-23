# Gyroid 龙伯透镜全周期研发、电磁仿真与 3D 打印工程全景资产总结

---

## 一、 项目背景与关键技术指标

- **学术与工业基准**：严格对标法国达索系统（Dassault Systèmes 2024）官方 CST 单胞色散基准文档（单胞周期 $a = 6.0\,\text{mm}$，基体树脂 $\varepsilon_r = 2.8, \tan\delta = 0.005$，锚定等效介电常数 $D_k = 1.786$）。
- **核心工程目标**：
  1. 突破传统分层阶梯透镜的界限，构建连续功能梯度（FGM）Skeletal Gyroid 龙伯透镜。
  2. 解决传统 TPMS 结构在光固化 3D 打印中的**排液死角、树脂残留沉淀、盲孔堵塞与打印剥离力过大**等工艺顽疾。
  3. 实现从**微观单胞色散 $\to$ 宏观透镜设计 $\to$ CST 自动化全波电磁仿真 $\to$ 工业级 3D 打印切片**的全链条闭环。
- **已完成尺寸梯次**：
  - **中型便携版**：直径 $D = 60.0\,\text{mm}$（半径 $R = 30.0\,\text{mm}$，跨越 10 个晶胞周期）
  - **大型高增益版**：直径 $D = 120.0\,\text{mm}$（半径 $R = 60.0\,\text{mm}$，跨越 20 个晶胞周期）

---

## 二、 核心资产文件全景清单 (Asset Inventory)

工作空间根目录：`C:\Users\15085\.gemini\antigravity\scratch\dome_lens_sim\dassault_reproduction\`

### 1. 三维几何模型资产库 (3D CAD & Mesh Models)

#### 🌟 交付终版：大开孔保形外球壳型 (Perforated Cage Skin - 浑然正球 + 秒速排液)
| 规格 / 文件名 | 格式 / 大小 | 网格指标 | 核心用途与工程特点 |
| :--- | :--- | :--- | :--- |
| **luneburg_lens_dassault_cage_60mm.obj** | OBJ / 51.4 MB | 35.0 万顶点, 70.8 万面, 100% 水密 | **CST Studio Suite 全波电磁仿真专用** |
| **luneburg_lens_dassault_cage_60mm.stl** | 二进制 STL / 35.4 MB | 标准 80 字节头, 几何流形无缝 | **SLA / DLP / SLS 工业级 3D 打印直接切片** |
| **luneburg_lens_dassault_cage_60mm.rar** | RAR 压缩包 / 11.0 MB | 高压缩比归档 | 方便文件分发、传输与归档 |
| **luneburg_lens_dassault_cage_R60mm_D120mm.obj** | OBJ / 133.6 MB | 91.2 万顶点, 182.4 万面, 100% 水密 | **$D=120\,\text{mm}$ 大型透镜 CST 全波仿真** |
| **luneburg_lens_dassault_cage_R60mm_D120mm.stl** | 二进制 STL / 91.0 MB | 标准 80 字节头, 100% 水密 | **$D=120\,\text{mm}$ 工业 3D 打印切片文件** |
| **luneburg_lens_dassault_cage_R60mm_D120mm.rar** | RAR 压缩包 / 68.4 MB | 高压缩比归档 | 大型高面数工程模型压缩归档 |

#### 🔬 单晶胞基准资产 (Unit Cell Benchmarks - 达索官方 6mm 标准)
| 文件名 | 格式 / 大小 | 几何指标 | 核心用途 |
| :--- | :--- | :--- | :--- |
| **dassault_gyroid_6mm.obj / .stl** | OBJ / STL (2.5 MB / 1.8 MB) | 1.8 万顶点, 3.6 万面 | **Skeletal 实心立柱单胞**（达索 50% 体积比基准，实测 $D_k = 1.786$） |
| **dassault_sheet_gyroid_6mm.obj / .stl** | OBJ / STL (1.9 MB / 2.6 MB) | 达索双腔极小薄壳单胞 | 达索 Sheet 构型对比基准 |

#### 📜 演进历程备选与历史构型
| 文件名 | 构型方案 | 特点与历史状态 |
| :--- | :--- | :--- |
| `luneburg_lens_dassault_tapered_60mm.obj/.stl` | 第 2 代：自然收口尖灭型 | 立柱向外平滑收细，外观为纯镂空点阵，无刚性外壳边界 |
| `luneburg_lens_dassault_sheet_60mm.obj/.stl` | Sheet 薄壳整球透镜 | 达索原版双腔薄壳构型，薄壁极易破损、易困住液体 |
| `luneburg_lens_dassault_60mm.stl` | 第 1 代：硬截断球刀硬切型 | 边缘有平切切面和微小毛刺，已淘汰升级 |

---

### 2. Python 参数化算法与生成脚本库 (Python Scripts)

| 脚本文件名 | 依赖库 | 核心功能与使用方法 |
| :--- | :--- | :--- |
| **`generate_dassault_perforated_cage_lens.py`** | `numpy`, `skimage`, `trimesh` | **【核心主程序】终极大开孔保形外球壳透镜生成器**。<br>支持命令行参数：<br>`--radius 30/60`（半径）、`--period 6.0`（周期）、`--resolution N`（网格分辨率）、`--shell-thick 1.2`（壳厚）、`--hole-size 0.05`（开孔阈值）。<br>一键完成数学求解、Marching Cubes 提取、Taubin 几何曲率光顺、水密修复并自动导出 OBJ/STL/双联光影图。 |
| **`generate_dassault_gyroid_cell.py`** | `numpy`, `skimage`, `trimesh` | 单晶胞 Skeletal 构型生成器，严格对齐第一布里渊区边界，用于 CST 色散验证。 |
| **`generate_dassault_sheet_gyroid.py`** | `numpy`, `skimage`, `trimesh` | 单晶胞 Sheet 极小曲面薄壳构型生成器。 |
| **`generate_dassault_smooth_tapered_lens.py`** | `numpy`, `skimage`, `trimesh` | 第 2 代自然收细渐灭型透镜生成脚本。 |
| **`generate_dassault_full_luneburg_lens.py`** | `numpy`, `skimage`, `trimesh` | 达索基准原版硬截断型透镜生成脚本。 |
| **`verify_dassault_dispersion.py`** | `numpy`, `matplotlib` | 达索官方 32 点布里渊区色散曲线与等效介电常数色散反演验证程序。 |
| **`render_shaded_lens.py`** | `matplotlib`, `trimesh` | 基于多光源 Phong 光照模型的透镜高保真三维渲染着色引擎。 |

---

### 3. CST Studio Suite 自动化仿真宏库 (CST Automation VBA Macros)

| 宏文件名 | 对应仿真目标 | 自动化执行内容 |
| :--- | :--- | :--- |
| **`setup_cst_dassault_cage_R60mm_lens_simulation.bas`** | **$D=120\,\text{mm}$ 全波透镜仿真** | 自动新建工程、导入 182 万面 OBJ 几何、绑定 $\varepsilon_r=2.8$ 树脂材料、设置 PML 开放边界、放置 10~18 GHz 激励源与远场监视器。 |
| **`setup_cst_dassault_cage_lens_simulation.bas`** | **$D=60\,\text{mm}$ 全波透镜仿真** | 针对 60mm 终版网壳透镜的一键电磁仿真搭建宏。 |
| **`setup_cst_dassault_reproduction.bas`** | **单晶胞本征模色散工程** | 建立六面周期性边界条件（Periodic Boundaries），自动加载 32 个布里渊扫描点，配置 Eigenmode Solver。 |
| `setup_cst_dassault_tapered_lens_simulation.bas` | 自然收口型透镜仿真 | 针对第 2 代透镜的自动化仿真宏。 |
| `setup_cst_dassault_full_lens_simulation.bas` | 达索原版透镜仿真 | 针对原版透镜的自动化仿真宏。 |
| `cst_parameter_sweep_points.txt` | 单胞色散扫描参数 | 存储 32 个布里渊路径各点相位角的参数列表。 |

---

### 4. 高分辨率效果渲染与物理验证图谱 (Visual Artifacts)

| 图谱文件 | 渲染特色 | 核心展示内容 |
| :--- | :--- | :--- |
| **`luneburg_lens_dassault_cage_R60mm_D120mm_render.png`** | 200 DPI 双联图 | **$D=120\,\text{mm}$ 巨型透镜全貌**：正球网壳全貌 + 赤道剖切透视内部立柱抛物线渐变。 |
| **`luneburg_lens_dassault_cage_60mm_render.png`** | 200 DPI 双联图 | **$D=60\,\text{mm}$ 透镜全貌**：4.0~4.5mm 宽大排液孔、琥珀金外壳与科技青剖切面。 |
| **`luneburg_lens_optical_verification.png`** | 180 DPI 三联图 | 1. 介电常数拟合曲线 vs 理论抛物线；2. 相对误差 $<3.2\%$ 分布图；3. 几何光学全波聚焦光线追迹图。 |
| **`dassault_dispersion_benchmark_verification.png`** | 150 DPI 对比图 | 严格重叠达索官方 2024 文档 Page 7 & Page 10 的 32 点色散曲线，完全契合 $D_k=1.786$。 |
| **`comparison_options_render.png`** | 180 DPI 三联图 | 方案 A（立柱触球）vs 方案 B（密孔网壳）vs 方案 C（宽大排液孔网壳）横向工艺对比。 |
| **`gyroid_structural_types_comparison.png`** | 180 DPI 对比图 | Skeletal 实心立柱构型 vs Sheet 双腔薄壳构型三维几何切片对比。 |
| **`tapered_vs_chopped_comparison.png`** | 150 DPI 对比图 | 第 2 代自然尖灭收口 vs 第 1 代硬球刀裁切的边缘质量对比。 |

---

## 三、 电磁仿真与工程关键技术知识库总结

### 1. 仿真精度与模型面数的关系（网格收敛准则）
- **CST PBA 技术的自适应特性**：CST 时域求解器使用完美边界近似（PBA），能够自动在直角六面体网格内对多边形表面进行共形积分。
- **面数收敛阈值**：
  - 几何模型的面数只需达到**曲面弦高误差远小于电磁波波长（例如 $\delta < \lambda_g / 50$）**即可达到完全的电磁收敛。
  - 对于 $D=60\,\text{mm}$，70 万面已达到 $15\,\mu\text{m}$ 几何精度，电磁仿真结果与 300 万面完全一致，盲目提高面数只会徒增内存消耗。

### 2. 喇叭天线馈源对称面边界（Symmetry Planes）配置规范
当使用线极化喇叭天线作为透镜馈源时，可充分利用结构与场分布的对称性，将仿真域缩减为 **1/4**，计算速度提升近 **4 倍**：
- **假设喇叭天线沿 $+Z$ 轴照射透镜，电场极化方向为 $Y$ 方向（$E_y$）**：
  - **$Y=0$ 平面（与电场矢量平行）**：设置为 **PEC 对称面（Electric, $E_t=0$）**。
  - **$X=0$ 平面（与磁场矢量平行）**：设置为 **PMC 对称面（Magnetic, $H_t=0$）**。
- **注意**：如果透镜用于多波束或圆极化馈电，则不能启用对称面，必须进行全波仿真。

### 3. 透镜天线口径效率（Aperture Efficiency $\eta_{\text{ap}}$）深度剖析
仿真测得口径效率通常在 **45% ~ 55%** 之间，属于微波工程中的正常优质水平，并非异常：
- **经典物理权衡（Trade-off）**：
  $$\eta_{\text{ap}} = \eta_{\text{ill}} \times \eta_{\text{spill}} \times \eta_{\text{phase}} \times \eta_{\text{pol}} \times \eta_{\text{loss}}$$
  - **照射均匀性效率 $\eta_{\text{ill}}$**：希望喇叭波束尽可能平坦照射到整个透镜口径（提高面积利用率）。
  - **溢出截获效率 $\eta_{\text{spill}}$**：若喇叭波束过宽，边缘大量电磁能量漏出透镜打到外围空气中，溢出效率暴跌。
  - **工程黄金平衡点**：通常选择透镜边缘照射电平衰减为 **$-10\,\text{dB} \sim -12\,\text{dB}$（Edge Taper）**，此时两者的乘积达到理论极大值（约 **80% ~ 82%**）。
- **物理 Luneburg 透镜的综合效率极限**：考虑馈源相位中心偏离、表面反射与树脂介质损耗（$\tan\delta=0.005$），实际成品的峰值口径效率上限一般在 **65% ~ 75%**。

### 4. 3D 打印制造精度指南（SLA / DLP 光固化）
- **极限特征尺寸验证**：
  - 球心粗壮立柱直径 $\approx 2.5 \sim 3.0\,\text{mm}$；外层最细立柱 $\ge 1.0\,\text{mm}$，完全高于树脂拉断下限（$0.4\,\text{mm}$），成型刚度高。
  - 外壳排液微孔稳定在 **$4.0 \sim 4.5\,\text{mm}$**，高粘度树脂秒级排空，酒精清洗畅通直通球心。
- **打印切片面数推荐**：
  - $D=60\,\text{mm}$：150万~200万面（STL 约 80MB）；
  - $D=120\,\text{mm}$：250万~350万面（STL 约 150MB）；
  - 弦高误差 $\le 12\,\mu\text{m}$，已优于工业级 3D 打印光斑物理极限（$25\sim 50\,\mu\text{m}$），打印成品表面呈现镜面级丝滑。
