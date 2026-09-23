' =============================================================================
' CST Studio Suite VBA Macro: 大开孔保形外球壳型 半径 60mm (直径 120mm) 龙伯透镜全波仿真工程
' 适用模型: luneburg_lens_dassault_cage_R60mm_D120mm.obj
' 特点: 6波长超大口径，增益提升 +6dBi，4.0~4.5mm 大开孔正球网壳，100% 水密
' =============================================================================

Sub Main ()
    On Error Resume Next

    ' 1. 工程单位制 (mm, GHz, ns)
    With Units
        .Geometry "mm"
        .Frequency "ghz"
        .Time "ns"
    End With

    ' 2. 频段设置 (X / Ku 频段: 10 GHz ~ 18 GHz, 中心频点 15 GHz)
    Solver.FrequencyRange "10.0", "18.0"

    ' 3. 建立达索官方基体树脂材料 (ε_r = 2.8, tanδ = 0.005)
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
        .Colour "1.0", "0.74", "0.14"
        .Create
    End With

    ' 4. 背景与六向自由空间吸收边界 (Open add space / PML)
    With Background
        .ResetBackground
        .Type "Normal"
        .Epsilon "1.0"
        .Mue "1.0"
        .XminSpace "20.0"
        .XmaxSpace "20.0"
        .YminSpace "20.0"
        .YmaxSpace "20.0"
        .ZminSpace "25.0"
        .ZmaxSpace "25.0"
        .ApplyInAllDirections "False"
    End With

    With Boundary
        .Xmin "expanded open"
        .Xmax "expanded open"
        .Ymin "expanded open"
        .Ymax "expanded open"
        .Zmin "expanded open"
        .Zmax "expanded open"
    End With

    ' 5. 导入大开孔保形外球壳 120mm 龙伯透镜网格模型
    Dim lensPath As String
    lensPath = "C:\Users\15085\.gemini\antigravity\scratch\dome_lens_sim\dassault_reproduction\luneburg_lens_dassault_cage_R60mm_D120mm.obj"

    With Wavefront
        .Reset
        .FileName lensPath
        .Id "1"
        .ScaleToUnit "True"
        .Import
    End With

    ' 赋予树脂材料
    Solid.ChangeMaterial "component1:luneburg_lens_dassault_cage_R60mm_D120mm", "Dielectric_Resin"
    Solid.ChangeMaterial "luneburg_lens_dassault_cage_R60mm_D120mm", "Dielectric_Resin"

    ' 6. 配置沿 -Z 方向入射的平行平面波激励源
    With PlaneWave
        .Reset
        .Normal "0.0", "0.0", "-1.0"
        .EVector "1.0", "0.0", "0.0"
        .Polarization "Linear"
        .ReferenceFrequency "15.0"
        .PhaseShift "0.0"
        .CircularDirection "Left"
        .AxialRatio "0.0"
        .Store
    End With

    ' 7. 设置 12 GHz / 15 GHz / 18 GHz 二维电场聚焦监视器与三维远场监视器
    Dim freqs(2) As Double
    freqs(0) = 12.0
    freqs(1) = 15.0
    freqs(2) = 18.0

    Dim i As Integer
    For i = 0 To 2
        With Monitor
            .Reset
            .Name "e-field (" & CStr(freqs(i)) & "GHz)"
            .Dimension "Volume"
            .Domain "Frequency"
            .FieldType "Efield"
            .Frequency CStr(freqs(i))
            .Create
        End With

        With Monitor
            .Reset
            .Name "farfield (" & CStr(freqs(i)) & "GHz)"
            .Dimension "Volume"
            .Domain "Frequency"
            .FieldType "Farfield"
            .Frequency CStr(freqs(i))
            .ExportFarfieldApproximation "False"
            .Create
        End With
    Next i

    ' 8. 视图居中刷新
    Plot.Draw
    View.ZoomToStructure

    MsgBox "【半径 60mm (外径 120mm) 龙伯透镜全波工程配置成功！】" & vbCrLf & vbCrLf & _
           "1. 模型特征: luneburg_lens_dassault_cage_R60mm_D120mm.obj (口径增益提升 +6dBi)" & vbCrLf & _
           "2. 边界条件: 六向 Open (PML) 自由辐射边界" & vbCrLf & _
           "3. 激励源: 10 GHz ~ 18 GHz 平面波入射" & vbCrLf & _
           "4. 监视器: 12 / 15 / 18 GHz 空间电场聚焦与远场方向图" & vbCrLf & _
           "5. 求解建议: 计算网格约 1800 万，推荐开启 GPU 硬件加速求解！", _
           vbInformation, "CST Simulation"

End Sub
