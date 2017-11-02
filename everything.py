#/usr/bin/python
#-*-<coding=UTF-8>-*-

"""
本例为windows下everything程序的linux版本.后端基于locate实现.
"""

import wx
import os
import subprocess

class GuiMainFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self,parent=None,id=-1,title="",pos=wx.DefaultPosition,size=wx.DefaultSize)
        
        #添加面板.
        panel = wx.Panel(self)
        
        #创建菜单栏
        menubar = wx.MenuBar()
        
        #File menu
        fileMenu = wx.Menu()
        fileMenu.Append(-1,"&Open","")
        menubar.Append(fileMenu,"&File")

        #Edit menu
        editMenu = wx.Menu()
        editMenu.Append(-1,"&Copy","")
        menubar.Append(editMenu,"&Edit")

        #Help/About menu
        helpMenu = wx.Menu()
        helpMenu.Append(-1,"About","")
        menubar.Append(helpMenu,"&Help")
        
        #调用SetMenuBar，使其在框架中显示出来
        self.SetMenuBar(menubar)
        
        #在面板中添加查找输入框
        #filterInput = wx.TextCtrl(panel,-1,"")
        self.filter = wx.SearchCtrl(panel,style=wx.TE_PROCESS_ENTER)
        self.filter.Bind(wx.EVT_TEXT_ENTER,self.DoSearch)
        #self.filter.Bind(wx.EVT_TEXT,self.DoSearch)　　#这个会导致程序长时间无响应,所以还在找更有效率的方法.
        
        #在面板中添加类型选择框
        typeList=["all:*.*","document:*.doc,*.xls,*.ppt","audio:*.mp3","vedio:*.rmvb,*.mkv","application:*.exe"]
        fileType = wx.ComboBox(panel,-1,"",choices=typeList)

        #在面板中添加输出结果显示框
        self.multiText = wx.TextCtrl(panel,-1,"",style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.multiText.SetMinSize((800,600))

        #添加状态栏,是否要加入到sizer中管理.
        statusbar = self.CreateStatusBar()
    
        #管理布局.创建两个sizer,主sizer管理filterSizer,结果显示框两个控件
        #filterSizer管理查找输入框和类型选择框
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        filterSizer = wx.GridSizer(rows=1,cols=2)
        filterSizer.Add(self.filter,0,wx.EXPAND)
        filterSizer.Add(fileType,0,wx.EXPAND)

        #这句话导致文本框显示有空隙. 为什么不能这样用? menubar是否不需要添加进mainSizer
        #mainSizer.Add(menubar)
        mainSizer.Add(filterSizer,0,wx.EXPAND)
        mainSizer.Add(self.multiText,2,wx.EXPAND|wx.ALL)
        #frame中创建的statusbar,不需要添加到sizer中进行管理.
        #mainSizer.Add(statusbar,0,wx.EXPAND)
        
        #这个是关键之处，将sizer与frame关联起来.
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def DoSearch(self,event):
        pattern = self.filter.GetValue()
        print pattern
        cmd = "/usr/bin/locate"
        arg1 = "-i"
        arg2 = "-d"
        arg3 = "/var/lib/mlocate/mlocate.db"
        arg4 = pattern

        p1=subprocess.Popen([cmd,arg1,arg2,arg3,arg4],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdoutdata,stderrdata) = p1.communicate()
        #stdoutdata = "Just test"
        self.multiText.SetValue(stdoutdata)

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = GuiMainFrame()
    frame.Show()
    app.MainLoop()
