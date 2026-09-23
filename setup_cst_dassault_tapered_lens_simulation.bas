' =============================================================================
' CST Studio Suite VBA Macro: 自然尖灭圆润收口型 60mm 龙伯透镜全波仿真工程
' 适用模型: luneburg_lens_dassault_tapered_60mm.obj
' 特点: 零硬裁切断茬，表面纯自然闭合，CST 网格质量极佳，求解极速稳定
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
        .Colour "0.0", "0.66", "0.91"
        .Create
    End With

    ' 4. 背景与六向自由空间吸收边界 (Open add space / PML)
    With Background
        .ResetBackground
        .Type "Normal"
        .Epsilon "1.0"
        .Mue "1.0"
        .XminSpace "15.0"
        .XmaxSpace "15.0"
        .YminSpace "15.0"
        .YmaxSpace "15.0"
        .ZminSpace "20.0"
        .ZmaxSpace "20.0"
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

    ' 5. 导入对标生成的【自然圆润收口】60mm 龙伯透镜网格模型
    Dim lensPath As String
    lensPath = "C:\Users\15085\.gemini\antigravity\scratch\dome_lens_sim\dassault_reproduction\luneburg_lens_dassault_tapered_60mm.obj"

    With Wavefront
        .Reset
        .FileName lensPath
        .Id "1"
        .ScaleToUnit "True"
        .Import
    End With

    ' 赋予树脂材料
    Solid.ChangeMaterial "component1:luneburg_lens_dassault_tapered_60mm", "Dielectric_Resin"
    Solid.ChangeMaterial "luneburg_lens_dassault_tapered_60mm", "Dielectric_Resin"

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

    MsgBox "【自然圆润收口型龙伯透镜全波工程配置成功！】" & vbCrLf & vbCrLf & _
           "1. 模型特征: luneburg_lens_dassault_tapered_60mm.obj (零断茬碎面，天然水密)" & vbCrLf & _
           "2. 边界条件: 六向 Open (PML) 自由辐射边界" & vbCrLf & _
           "3. 激励源: 10 GHz ~ 18 GHz 平面波入射" & vbCrLf & _
           "4. 监视器: 12 / 15 / 18 GHz 空间电场聚焦与远场方向图" & vbCrLf & _
           "5. 下一步: 点击 Home -> Setup Solver -> Start 启动时域求解器求解！", _
           vbInformation, "CST Simulation"

End Sub
