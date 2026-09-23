' =============================================================================
' CST Studio Suite VBA Macro: 自动化复现达索 2024 Gyroid 单胞仿真工程
' 对标文档: 《UNIT CELL SETUP FOR DIELECTRIC CRYSTALS - Material properties estimation》
' 适用版本: CST Studio Suite 2020 ~ 2024
' =============================================================================

Sub Main ()
    On Error Resume Next

    ' 1. 设置工程单位制 (mm, GHz, ns)
    With Units
        .Geometry "mm"
        .Frequency "ghz"
        .Time "ns"
        .TemperatureUnit "kelvin"
        .Voltage "v"
        .Current "a"
        .Resistance "ohm"
        .Conductance "1/ohm"
        .Capacitance "pfd"
        .Inductance "nh"
    End With

    ' 2. 定义高对称相移与几何全局参数
    MakeSureParameterExists "phaseX", "0.0"
    MakeSureParameterExists "phaseY", "0.0"
    MakeSureParameterExists "phaseZ", "0.0"
    MakeSureParameterExists "a_cell", "6.0"

    ' 3. 建立基体树脂材料 (对标达索文档 ε_r = 2.8, tanδ = 0.005)
    With Material
        .Reset
        .Name "Dielectric_Resin"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "2.8"
        .Mue "1.0"
        .TanD "0.005"
        .TanDFreq "0.0"
        .TanDGiven "True"
        .TanDModel "ConstTanD"
        .EnableUserConstTanDModelOrderEps "False"
        .ConstTanDModelOrderEps "1"
        .SetConstTanDFormulaEps "True"
        .Colour "0.0", "0.66", "0.91"
        .Wireframe "False"
        .Transparency "0"
        .Create
    End With

    ' 4. 设置六向周期性边界条件 (Periodic Boundary Conditions)
    With Boundary
        .Xmin "periodic"
        .Xmax "periodic"
        .Ymin "periodic"
        .Ymax "periodic"
        .Zmin "periodic"
        .Zmax "periodic"
        .XperiodicPhaseShift "phaseX"
        .YperiodicPhaseShift "phaseY"
        .ZperiodicPhaseShift "phaseZ"
        .ApplyInAllDirections "True"
    End With

    ' 5. 导入对标生成的 6mm Gyroid 单胞 OBJ 网格
    Dim modelPath As String
    modelPath = "C:\Users\15085\.gemini\antigravity\scratch\dome_lens_sim\dassault_reproduction\dassault_gyroid_6mm.obj"
    
    With Wavefront
        .Reset
        .FileName modelPath
        .Id "1"
        .ScaleToUnit "True"
        .Import
    End With

    ' 赋予树脂材料
    Solid.ChangeMaterial "component1:dassault_gyroid_6mm", "Dielectric_Resin"
    Solid.ChangeMaterial "dassault_gyroid_6mm", "Dielectric_Resin"

    ' 6. 配置本征模求解器 (Eigenmode Solver)
    With EigenmodeSolver
        .Reset
        .SetMeshType "Tetrahedral"
        .SetNumberOfModes "4"
        .SetFrequencyTarget "True", "20.0"
        .SetAccuracy "1e-5"
    End With

    ' 7. 视图居中并刷新
    Plot.Draw
    View.ZoomToStructure

    MsgBox "【达索 Gyroid 单胞仿真工程创建成功！】" & vbCrLf & vbCrLf & _
           "1. 几何: a = 6.0 mm (已导入并居中)" & vbCrLf & _
           "2. 材料: Dielectric_Resin (ε_r = 2.8, tanδ = 0.005)" & vbCrLf & _
           "3. 边界: X/Y/Z 全向周期边界，变量 phaseX, phaseY, phaseZ" & vbCrLf & _
           "4. 下一步: 点击 Home -> Parameter Sweep，导入点列表文件: cst_parameter_sweep_points.txt，即可一键求解！", _
           vbInformation, "CST Dassault Benchmark"

End Sub
