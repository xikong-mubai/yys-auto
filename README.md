# yys-auto
解决痒痒鼠上班难题，从我做起~

## todo

~~取色点比例需要更改，原始比例为 1152/681，游戏版本更新会影响该比例值，可能需要换算~~

系统dpi会影响窗口总像素大小稳定

## windows dpi 缩放计算

~~在使用windows api函数 `SetWindowPos` 设置窗体位置时，windows会根据系统设置的 dpi 值来对其进行缩放。~~
~~这里经过多次实验之后推导出其缩放机制如下：~~

~~+ 一般情况下优先调整纵轴长度（即调整高度为主要操作，横轴宽度调整可忽略）~~
  ~~+ 这部分程序应当可自定义，默认而言是横轴优先，纵轴可忽略~~
~~+ 在计算时会将系统赋予窗体程序的边框部分（也即程序本身画面范围以外的 边框、投影区域）切割开来分别参与缩放计算~~
  ~~+ 边框线不论多大的窗体都默认为 1 个像素大小，即上下左右永远都是四根 1 个像素宽的边框线~~
  ~~+ 投影区域最终结果必为左右下三个 11 个像素宽的区域。顶部因为有标题栏所以是没有投影的~~
  ~~+ 除去边框线和投影区域，还有一个顶部的标题栏，标题栏最终显示结果必为45像素宽~~

~~最终的计算过程为：~~

~~+ 因为边界区域最终结果恒定，所以其计算是反推的，因为最后会有一个45宽的标题栏，所以程序会在传入的参数 y 上减去30像素~~
  ~~+ 即 dpi * ( y - 30)~~

先算横轴，再算纵轴，对于一些固定比例的程序一般是算了横轴之后自动适配纵轴，不排除程序会自定义该过程的可能。


### dpi感知

1. windows系统实现有dpi感知的功能，默认关闭，只有开启了dpi感知的程序可以直接获取到当前系统的实际dpi。
开发人员可以通过 `SetProcessDpiAwareness()` 函数为自己编写的程序启用api感知功能。

    ```python
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    hdc = win32gui.GetDC(0)
    x_dpi: int = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
    dpi = x_dpi / dpi
    ```

2. 不过在未开启 dpi 感知时，也可以通过间接计算的方式得到实际dpi。
微软在自己的win32api文档中隐藏了函数 `GetDeviceCaps` 的参数 `DESKTOPHORZRES` 的存在。
该参数可以在未开启dpi感知时获取到系统设置的分辨率大小，该分辨率是被缩放过的，于是将其除以真实的分辨率大小即可得到dpi值。

    ```python
    system_pixel = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
    real_pixel = win32print.GetDeviceCaps(hdc, win32con.HORZRES)
    dpi = system_pixel / real_pixel
    ```

两种方法不可通用。
