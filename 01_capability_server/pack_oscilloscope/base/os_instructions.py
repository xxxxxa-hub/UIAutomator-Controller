"""
  cmd设置规则：
  1、指令使用双引号进行封装
  2、如果指令里边包含双引号等类似特殊字符，请用\"进行转义
  例如：
  vbs 'app.Display.GridMode = "xx"'：
  "vbs 'app.Display.GridMode = \"{}\"'"
"""

TekMDO3054_instructions = {
    # 示波器恢复默认设置
    'Factory': "FACTORY",
    # 设置示波器的波形抢断
    'WaveIntensity': "DISPLAY:INTENSITY:WAVEFORM 100",
    # 设置刻度亮度
    'GraticuleIntensity': "DISPLAY:INTENSITY:GRATICULE 75",
    # 设置示波器时间
    'SetTime': "TIME \"{nowTime}\"",
    # 设置示波器日期
    'SetData': "DATE \"{date}\"",
    # 开启指定通道
    'OpenCh': "SELECT:{CH} 1",
    # 关闭指定通道
    'CloseCh': "SELECT:{CH} 0",
    # 设置示波器记录长度
    'SetRecordLength': "HORIZONTAL:RECORDLENGTH {length}",
    # 设置带宽为指定数值或FULL
    'SetBandWidth': "{ch}:BANDWIDTH {bandwidth}",
    # 设置通道名称
    'SetChannelLabel': "{ch}:LABEL \"{name}\"",
    # 设置通道偏置
    'SetOffset': "{ch}:OFFSET {offset_value}",
    # 设置指定通道的垂直比例
    'SetScale': "{ch}:SCAle {scale}",
    # 设置指定通道的垂直位置
    'SetPosition': "{CH}:POSITION {position}",
    # 设置时基
    'HorizontalScale': "HORIZONTAL:SCALE {scale}",
    # 以百分比为单位指定水平位置（在延迟关闭时起作用）
    'HorizontalPosition': "HORIZONTAL:POSITION {position}",
    # 设置通道的耦合方式（直流或交流）
    'SetChCoupling': "{ch}:COUPLING {ch_coupling}",
    # 设置通道的的反向状态:开启(ON)或关闭(OFF)
    'SetChInvert': "{ch}:INVERT {invert_state}",

    # 设置水平延迟状态（ON或OFF）
    'HorizontalDelay': "HORIZONTAL:DELAY:MODE {state}",
    # 关闭水平延迟开关
    'CloseHorizontalDelay': "HORIZONTAL:DELAY:MODE OFF",
    # 设置水平延时位置（触发位置）
    'SetHorizontalDelay': "HORIZONTAL:DELay:TIMe {horizontal_delay}",
    # 查询水平时基
    'QueryHorScale': "HORIZONTAL:SCALE?",
    # 查询水平位置
    'QueryHORIZONTAL': "HORizontal:POSition?",

    # 以下为触发的相关指令(边沿触发)
    # 设置A触发器的类型，type的值为EDGE(边沿)、LOGIC（逻辑）、PULSE（脉冲）、BUS（总线）、VIDEO（视频）中的任一个。
    # 默认触发方式是边沿触发。
    'SetTriggerType': "TRIGGER:A:TYPE {type}",
    # 设置B边触发器的耦合类型为HFREJ
    'TriggerB1': ":TRIGGER:B:EDGE:COUPLING HFREJ",
    # 设置A边触发器的耦合类型，coupling_type的值可以为AC（交流）、DC（直流）、
    # HFRej（高频抑制）、LFRej（低频抑制）、NOISErej（噪声过滤）中的任一个
    'TriggerACoupling': ":TRIGGER:A:EDGE:COUPLING {coupling_type}",
    # 将CHx波形指定为源波形
    'SetTriggerASource': "TRIGGER:A:EDGE:SOURCE {ch}",
    # 指定边触发器的类型：上升、下降或两者之一,trigger_type的值为RISE或FALL
    'SetTriggerAEdge': "TRIGGER:A:EDGE:SLOPE {trigger_type}",
    # 设置触发数字通道波形时用于边缘或脉冲宽度触发器的阈值电压电平
    'SetTriggerALevel': "TRIGGER:A:LEVEL:{ch} {level}",
    # 设置触发模式的，trigger_mode的值为AUTO（自动）或NORMAL（正常）
    'SetTriggerMode': "TRIGGER:A:MODE {trigger_mode}",
    # 设置脉冲宽度
    'SetPulseWidth': "TRIGGER:A:PULSEWIDTH:WIDTH {pulse_width}",

    # 以下为触发的相关指令(脉冲触发)
    # 设置脉冲触发的类：{RUNt|WIDth|TRANsition|TIMEOut}
    'PulseClass': "TRIGGER:A:PULSE:CLASS {Pulse_class}",
    # 设置脉冲触发的触发条件：{LESSthan|MOREthan|EQual|UNEQual|WIThin|OUTside}
    'PulseWhen': "TRIGger:A:PULSEWidth:WHEn {pulse}",
    # 设置脉宽触发的下限
    'PulseLow': "TRIGger:A:PULSEWidth:LOWLimit {pulse_low}",
    # 设置脉宽触发的上限
    'PulseHigh': "TRIGger:A:PULSEWidth:HIGHLimit {pulse_high}",
    # 设置脉冲的极性: {NEGative|POSitive}
    'PulsePolarity': "TRIGger:A:PULSEWidth:POLarity {pulse_polarity}",
    # 设置脉冲触发的源
    'PulseSource': "TRIGger:A:PULSEWidth:SOUrce {pulse_source}",
        


    # 以下为ZOOM的相关指令
    # 打开ZOOM功能
    'OpenZoom': "ZOOM:STATE ON",
    # 关闭ZOOM功能
    'CloseZoom': "ZOOM:STATE OFF",
    # 以百分比形式设置缩放位置
    'SetZoomPosition': "ZOOm:ZOOM1:POSITION {position}",
    # 指定缩放框的水平比例
    'SetZoomScale': "ZOOm:ZOOM1:SCAle {scale}",

    # 以下为光标的相关指令
    # 开启联动光标
    'TrackCursor': "CURSOR:MODE TRACK",
    # 关闭联动光标
    'IndependentCursor': "CURSOR:MODE INDEPENDENT",
    # 设置光标模式为“波形”
    'SetWaveCursor': "CURSor:FUNCTION WAVEFORM",
    # 设置光标模式为“屏幕”
    'SetScreenCursor': "CURSor:FUNCTION SCREEN",
    # 关闭光标
    'CloseCursor': "CURSor:FUNCTION OFF",
    # 指定光标源波形(CH1~CH4)
    'SetCursorSource': "CURSor:SOURCE {ch}",
    # 指定垂直条光标的单位,units的值可以为SECONDS(秒)，HERTZ（频率），DEGREES(相位)，PERCENT(比率)
    'SetCursorUnit': "CURSOR:VBARS:UNITS {units}",
    # 设置光标a的垂直位置
    'SetCursorAVPosition': "CURSOR:VBARS:POSITION1 {position}",
    # 设置光标b的垂直位置
    'SetCursorBVPosition': "CURSOR:VBARS:POSITION2 {position}",
    # 设置光标a的水平位置
    'SetCursorAHPosition': "CURSOR:HBARS:POSITION1 {position}",
    # 设置光标b的水平位置
    'SetCursorBHPosition': "CURSOR:HBARS:POSITION2 {position}",
    # 查询两个光标之间的时间差
    'QueryVDELTa': "CURSor:VBARS:DELTA?",
    # 查询两个光标之间的幅值差
    'QueryHDELTa': "CURSor:HBARS:DELTA?",

    # 以下为搜索的相关指令
    # 打开搜索功能
    'OpenSearch': "SEARCH:SEARCH1:STATE ON",
    # 关闭搜索功能
    'CloseSearch': "SEARCH:SEARCH1:STATE OFF",
    # 设置搜索的源（CH1~CH4）
    'SetSearchSource': "SEARCH:SEARCH1:TRIGGER:A:EDGE:SOURCE {ch}",
    # 设置搜索的斜率，search_slope的值可以为RISE、FALL、EITHER
    'SetSearchSlope': "SEARCH:SEARCH1:TRIGGER:A:EDGE:SLOpe {search_slope}",
    # 设置搜索的阈值
    'SetSearchLevel': "SEARCH:SEARCH1:TRIGGER:A:LEVel:{ch} {search_level}",
    # 返回满足搜索条件的数量
    'QueryMarkNumber': "SEARCH:SEARCH1:TOTal?",
    # 返回搜索列表
    'QuerySearchList': "SEARCH:SEARCH1:LIST?",

    # 以下为保存的相关指令
    # 保存屏幕图像
    'SaveTypeImage': "SAVE:ASSIGN:TYPe IMAGE",
    # 储存波形
    'SaveTypeWave': "SAVE:ASSIGN:TYPe WAVEFORM",
    # 储存设置
    'SaveTypeSet': "SAVE:ASSIGN:TYPe SETUP",
    # 设置保存屏幕图像的文件格式：PNG、BMP、TIFf
    'SaveImageForm': "SAVE:IMAGE:FILEFORMAT {save_image_format}",
    # 设置保存屏幕图像的保存路径
    'SaveImagePath': "SAVE:IMAGE {file path}",
    # 设置储存波形的源和目标：source为ALL（所有显示的波形），或为CH1~CH4;Destination:可以为R1~R4,或为存储路径
    'SaveWavePath': "SAVE:WAVEFORM {Source},{Destination}",
    # 设置储存波形的波形选通，NONE：对应关（全部记录）、CURSORS：介于光标之间、SCREEN：屏幕
    'SaveWaveGating': "SAVe:WAVEFORM:GATING {gating_type}",
    # 设置储存波形的文件格式：INTERNAL为isf格式，SPREADSHEET为.CSV格式
    'SaveWaveFormat': "SAVe:WAVEFORM:FILEFORMAT {save_wave_format}",
    # 设置波形输出的编码格式
    'WaveEncode': "WFMOUTPRE:ENCdg ASCII",
    # 设置编码格式
    'SetEncodeForm': "CURVe asc curve",
    # curve查询
    'QueryCurve': "CURVE?",

    # 以下为测量的相关指令
    # 设置测量的源,num(1~4)
    'SetMeasureSource': "MEASUREMENT:MEAS{num}:SOURCE {ch}",
    # MEASUREMENT:IMMED:SOURCE{num} {ch}
    # 添加测量项,measure_type的值可以为：
    # AMPLITUDE：幅值
    # PK2Pk：峰峰值
    # MAXIMUM：最大值
    # MINIMUM:最小值
    # RMS：均方根
    # NWIDTH:负脉冲宽度
    # PWIDTH：正脉冲宽度
    # RISE:上升时间
    # FALL：下降时间
    # HIGH:高
    # LOW：低
    # FREQUENCY:频率
    # PERIOD：周期
    'AddMeasureType': "MEASUREMENT:MEAS{num}:TYPE {measure_type}",
    # 测量“选通”设置，可设置为OFF(关)、SCREEN（屏幕）、CURSOR（介于光标之间）
    'SetMeasureGating': "MEASUREMENT:GATing {gating_type}",
    # 移除测量快照
    'RemoveMeasure': "MEASUREMENT:CLEARSNAPSHOT",
    # Returns a calculate value for the measurement specified by <x>, which ranges from 1 through 8
    # (only 4 in MDO3000 models)
    'SetMeasurementMEASState': ":MEASUREMENT:MEAS{i}:STATE 0",
    # For SOURce1: This command specifies the source for all single channel measurements. For delay or phase
    # measurements, this command specifies the waveform to measure "from". This is equivalent to setting the "From:"
    # waveform in the "Measure Delay" side menu or the "Measure Phase" side menu. SOUrce is equivalent to SOURCE1.
    # For SOUrce2: This command specifies the waveform to measure "to" when taking a delay measurement or phase
    # measurement. This is equivalent to setting the "To:" waveform in the "Measure Delay" side menu or the
    # "MeasurePhase" side menu.
    'SetMeasurementSource': ":MEASUREMENT:IMMED:SOURCE1 {ch}",
    # specifies the immediate measurement type
    'SetMeasurementIMMED': ":MEASUREMENT:IMMED:TYPE {change_type}",
    # This command specifies the measurement type defined for the specified measurement slot. The measurement slot is
    # specified by <x>, which ranges from 1 through 8 in all models except MDO3000, which only support 4 simultaneous
    # measurements.
    'SetMeasurementMEASTpye': ":MEASUREMENT:MEAS{source_num}:TYPE {change_type}",
    # For SOURce1: This command specifies the source for all single channel
    # measurements. For delay or phase measurements, This command specifies the
    # waveform to measure "from". This is equivalent to setting the "From:" waveform
    # in the "Measure Delay" side menu or the "Measure Phase" side menu. SOUrce is
    # equivalent to SOURCE1.
    # For SOUrce2: This command specifies the waveform to measure "to" when taking
    # a delay measurement or phase measurement. This is equivalent to setting the "To:"
    # waveform in the "Measure Delay" side menu or the "Measure Phase" side menu.
    # Measurements are specified by <x>, which ranges from 1 to 8.
    'MeasurementSource': ":MEASUREMENT:MEAS{source_num}:SOURCE1 {ch}",
    # This command specifies whether the specified measurement slot is computed and displayed. The measurement slot
    # is specified by <x>, which ranges from 1 through 8.
    'MeasurementMeas1': ":MEASUREMENT:MEAS{source_num}:STATE 1",

    # 设置图片保存格式
    'SaveFormatter': "SAVE:IMAG:FILEF PNG",
    # 设置文件的保存路径
    'SavePath': "SAVe:SETUp {save_path}",
    # 将代表当前屏幕图像的数据块发送到请求的端口，HARDCopy START
    'HardCopyStart': "HARDCOPY START",
    # specifies that the oscilloscope will continually acquire data, if
    # ACQuire:STATE is turned on
    'AcquireRunStop': "ACQUIRE:STOPAFTER RUNSTOP",

    # 开始采集
    'StartAcquisitions': "ACQuire:STATE RUN",
    # 停止采集
    'StopAcquisitions': ":ACQUIRE:STATE 0",
    # 设置示波器的采集方式,RUNSTOP、SEQUENCE
    'SetAcquireType': "ACQuire:STOPAfter {acquire_type}",
    # 查询示波器的采集方式
    'QueryAcquireType': "ACQuire:STATE?",

    # 设置传输波形的源
    'DataSource': "DATa:SOURCE {ch}",
    # 设置编码格式为ASCII格式
    'DataEncode': "DATa:ENCdg ASCII",
    # 设置波形输出的数据宽度（每个数据点的字节）为4
    'DataByte': "WFMOUTPRE:BYT_Nr 4",
    # 设置波形输出的起始数据点
    'SetDataStart': "DATa:STARt 1",
    # 设置波形输出的终止数据点
    'SetDataStop': "DATA:STOP 250e6",

    # 设置示波器余晖的状态
    'SetPERSistence':"DISplay:PERSistence {persistence_status}",
    # 查询示波器的余晖的状态
    'AcquirePERSistence':"DISplay:PERSistence?"}


WAVERUNNER8254_instructions = {
    # 设置界面显示波形
    'DisplayGridMode': "vbs 'app.Display.GridMode = \"{DisplayGridMode}\"'",
    # 恢复默认设置
    'DefaultSetup': "vbs 'app.settodefaultsetup'",
    # 打开/关闭Cn通道
    'ChannelStatus': "vbs 'app.acquisition.C{n}.View ={TrueOrFalse}'",
    # 设置通道名称
    'SetChannelName':"VBS 'app.acquisition.C{n}.LabelsText = \"{SetChannelName}\"'",
    # 通道名称可见
    'ViewLabels':"vbs 'app.acquisition.C{n}.ViewLabels = {TrueOrFalse}",
    # 勾选VarGain（才可设置400mV）
    'SetVarGain':"VBS 'app.Acquisition.C{n}.VerScaleVariable = {TrueOrFalse}'",
    # 设置通道Cn垂直刻度
    'VerScale': "VBS 'app.Acquisition.C{n}.VerScale={VerScale}'",
    # 设置偏置
    'VerOffset': "VBS 'app.Acquisition.C{n}.VerOffset ={VerOffset}",
    # 每格时间调整
    'TimeSet': "vbs 'app.Acquisition.horizontal.HorScale = {Time1}'",
    # 设置采样模式
    'SetSampleRate': "vbs 'app.acquisition.horizontal.maximize = \"{SetSampleRate}\"'",
    # 调整时基偏置
    'SetHorOffset': "vbs 'app.acquisition.horizontal.HorOffset = {Time1}'",
    # 打开/关闭统计
    'statistics': "vbs 'app.measure.statson = {TrueOrFalse}'",
    # 测量通道
    'TestChannelNo':"vbs 'app.Measure.P{n}.View = {TestChnnalNo}'",
    # 添加测量值
    'AddMeasure': "vbs 'app.Measure.P{n}.ParamEngine = \"{Measure}\"'",
    # 打开/关闭测量
    'MeasureStatus':"vbs 'app.Measure.P{n}.View = {TrueOrFalse}'",
    # 设置触发类型
    'SetType': "vbs 'app.Acquisition.Trigger.Type = \"{Type}\"'",
    # 选择触发通道
    'TriggerSource': "vbs 'app.Acquisition.Trigger.Edge.Source = \"{Source}\"'",
    # 选择耦合
    'SetCoupling': "vbs 'app.Acquisition.Trigger.Edge.Coupling = \"{Coupling}\"'",
    # 设置上升沿/下降沿触发
    'SetSlope': "vbs 'app.Acquisition.Trigger.Edge.Slope = \"{SetSlope}\"'",
    # 设置触发电平
    'SetLevel': "vbs 'app.Acquisition.Trigger.Edge.Level ={SetLevel}'",
    # 设置触发模式
    'SetTriggermode': "vbs 'app.acquisition.triggermode = \"{SetTriggermode}\"'",
    # 启用/停止抖动测试
    'OpenJitter': "vbs 'app.SDA3.ShowJitterMeasure = {TrueOrFalse}'",
    # 设置抖动测试
    'SetJitter1': "vbs 'app.SDA3.L{n}.JitterMeasure.Pattern.ShowISIPlot = {TrueOrFalse}'",
    'SetJitter2': "vbs 'app.SDA3.L{n}.JitterMeasure.Pattern.ShowDDjHisto = {TrueOrFalse}'",
    'SetJitter3': "vbs 'app.SDA3.L{n}.JitterMeasure.Pattern.ShowPattern = {TrueOrFalse}'",
    'SetJitter4': "vbs 'app.SDA3.L{n}.JitterMeasure.Pattern.ShowSnCycle = {TrueOrFalse}'",
    # 保存模式
    'SaveMode':"vbs 'app.SaveRecall.{SaveMode}'",
    # 图片保存名称
    'PictureName':"vbs 'app.HardCopy.PreferredFilename = \"{PictureName}\"'",
    # 图片保存路径
    'PictureSaveRoute': "vbs 'app.HardCopy.Directory = \"{PictureSaveRoute}\"'",
    # 保存图片
    'SavePicture':"vbs 'app.HardCopy.print",
    # 设置波形保存格式
    'WaveformSaveFormat':"vbs 'app.SaveRecall.Waveform.WaveFormat = \"{WaveformSaveFormat}\"'",
    # 设置波形文件保存名称
    'WaveformName':"vbs 'app.SaveRecall.Waveform.TraceTitle = \"{WaveformSaveFormat}\"'",
    # 波形保存路径
    'WaveformSaveRoute': "vbs 'app.SaveRecall.Waveform.WaveformDir = \"{WaveformSaveRoute}\"'",
    # 保存波形
    'SaveWaveform':"vbs 'app.SaveRecall.Waveform.SaveFile",
    # 设置带宽
    'SetBandwidth':"vbs 'app.Acquisition.C{n}.BandWidthLimit = \"{SetBandwidth}\"'",
    # 查询返回值
    'ReturnMeasure':"VBS? 'return = app.Measure.P{ch}.ParamEngine'",
    # 打开/关闭游标
    'CursorsStatus':"vbs 'app.Cursors.View = {TrueOrFalse}'",
    # 设置游标类型
    'CursorsType':"vbs 'app.Cursors.Type = \"{CursorsType}\"'",
    # 设置游标位置
    'CursorsXPos1':"vbs 'app.Cursors.XPos1 = {}'",
    'CursorsXPos2':"vbs 'app.Cursors.XPos2 = {}'",
    'CursorsYPos1':"vbs 'app.Cursors.YPos1 = {}'",
    'CursorsYPos2':"vbs 'app.Cursors.YPos2 = {}'",
    # 打开/关闭Zoom
    'ZoomStatus':"vbs 'app.Zoom.MultiZoomOn = {TrueOrFalse}'",
    # 1.0G保存波形模式
    '1.0SaveWaveform':"vbs 'app.SaveRecall.Waveform.DoSave",
    # 查询返回垂直刻度值
    'AcquisitionVerScale': "VBS? 'return = app.Acquisition.C{n}.VerScale'",
    # 输出测试值
    'MeasureResult':"VBS? 'return = app.measure.p{n}.{Measure}.Result.Value'",
    # 删除所有测量值
    'DeleteMeasure':"vbs 'app.Measure.ClearAll",
    # 打开游标
    'OpenCursors':"vbs 'app.Cursors.View = {TrueOrFalse}'",
    # 关闭/打开波形文件保存统计
    'SetWaveformCounter':"vbs 'app.SaveRecall.Waveform.EnableCounterSuffix = {TrueOrFalse}'",
    # 关闭/打开图片文件保存统计
    'SetPictureCounter':"vbs 'app.HardCopy.EnableCounterSuffix = {TrueOrFalse}'",
    # 查询触发：停止/运行
    'TriggerMode':"VBS? 'return = app.Acquisition.TriggerMode'",
    # 保存为模式,如全屏模式
    'ScreenArea':"vbs 'app.HardCopy.HardcopyAreaToFile = \"{ScreenArea}\"'",
    # 关闭源
    'closeCh':"vbs 'app.SaveRecall.Waveform.EnableSourcePrefix = {TrueOrFalse}'",
    # 2周期触发方式
    # 'SetType': "vbs 'app.Acquisition.Trigger.Type = \"{Type}\"'",
    'TriggerMeasuremant':"vbs 'app.Acquisition.Trigger.Measurement.Measurement = {DeltaPeriodAtLevel}'",
    # 多周期源设置
    'MeasurementSource':"vbs 'app.Acquisition.Trigger.Measurement.Source = {MeasurementSource}'",
    # 多周期电平设置
    'MeasurementLevel':"vbs 'app.Acquisition.Trigger.Measurement.Level = {MeasurementLevel}'",
    # 采样率设置：激活的通道
    'ActivationChannel':"vbs 'app.acquisition.horizontal.ActiveChannels = \"{Auto}\"'",
    # 设置采样率为20Gs/s
    'SampleRate':"vbs 'app.acquisition.horizontal.SampleRate = {20.0GS/s}'",
    # 触发类型设置为Auto
    'AutoType':"vbs 'app.Acquisition.TriggerMode = \"{AutoType}\"'",
    # 触发类型设置为Normal
    'NormalType':"vbs 'app.Acquisition.TriggerMode= \"{NormalType}\"'",
    # 触发为停止触发
    'StopType':"vbs 'app.Acquisition.TriggerMode= \"{StopType}\"'",
    # 通道设置inputB
    'ChannelInputB':"vbs 'app.Acquisition.C{n}.ActiveInput = \"{InputB}\"'",
    # 打开Zoom
    'OpenZoom':"vbs 'app.Zoom.Z{n}.View = {TrueOrFalse}'",
    # 设置Zoom放大至游标位置
    'ZoomSet':"vbs 'app.Zoom.Z{n}.Zoom.HorCenter = {CenterPoint}'",
    # 设置Zoom放大的程度
    'ZoomScale':"vbs 'app.Zoom.Z{n}.Zoom.HorScale = {HorScale}",
    # 设置目的地保存为File
    'SetDestination':"vbs 'app.HardCopy.Destination = \"{SetDestination}\"'",
    # 设置图片保存格式
    'PictureFormat':"vbs 'app.HardCopy.ImageFileFormat = \"{PictureFormat}\"'",
    # 设置zoom分屏
    'ZoomSplitScreen':"vbs 'app.Zoom.Z{n}.UseGrid = \"{PictureFormat}\"'",
    # 打开/关闭余晖
    'OPenPersisted':"vbs 'app.Display.Persisted = {TrueOrFalse}'",
    # 余晖全部锁定
    'AllLock':"vbs 'app.Display.LockPersistence = \"{AllLocked}\"'",
    # 余晖模拟
    'PersistenceStyle':"vbs 'app.Display.PersistenceStyle = \"{Analog}\"'",
    # 设置余晖时间
    'PersistedTime':"vbs 'app.Display.PersistenceTime = \"{PersistedTime}\"'",
    # 触发抑制
    'HoldoffTime':"vbs 'app.Acquisition.Trigger.Edge.HoldoffTime = {HoldoffTime}'",
    # 设置触发位置
    'TriggerHor':"vbs 'app.Acquisition.Horizontal.HorOffSet = {HorOffSet}'",
    # 抑制类型
    'HoldoffType':"vbs 'app.Acquisition.Trigger.Edge.HoldoffType = \"{HoldoffType}\"'",
    # 查询余晖次数，一般看rise/fall次数，主要看是上升/下降沿触发
    'PersistedNum':"VBS? 'return=app.Measure.P{n}.{num}.Result.Value'",
    # 显示表格
    'ShowMeasure':"vbs 'app.Measure.ShowMeasure = {TrueOrFalse}'",
}
