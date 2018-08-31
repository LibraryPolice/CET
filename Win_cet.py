#coding:UTF-8

import wx
from cet import *
import os
#窗口类
class MyDialog(wx.Dialog): 
   def __init__(self, parent, title): 
      super(MyDialog, self).__init__(parent, title = 'error', size = (200,140)) 
      panel = wx.Panel(self) 
      wx.StaticText(panel,-1,"请输入必要参数!!",style=wx.ALIGN_CENTER,size=(200,20),pos=(-1,10))
      self.btn2 = wx.Button(panel, wx.ID_OK, label = "确定", size = (70,30),pos=(65,50))

class StaticTextFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"四六级暴力破解",pos=(650,350),size=(500,280))
        panel=wx.Panel(self,-1)
        vbox = wx.BoxSizer(wx.VERTICAL) 
        #基本静态文本
        wx.StaticText(panel,-1,"请输入准考证前十位:",(30,10),style=wx.ALIGN_LEFT,size=(200,20))
        self.idten=wx.TextCtrl(panel, -1, u'',(240,5), size=(200, -1))

        wx.StaticText(panel,-1,"请输入姓名:",(30,45),style=wx.ALIGN_LEFT,size=(200,20))
        self.name=wx.TextCtrl(panel, -1, u'',(240,42), size=(200, -1))

        wx.StaticText(panel,-1,"请输入开始查的考场:",(30,85),style=wx.ALIGN_LEFT,size=(200,20))
        self.start = wx.TextCtrl(panel, -1, u'',(240,80), size=(200, -1))
        self.cb1 = wx.RadioButton(panel, label = '四级',pos = (170,135)) 
        self.cb2 = wx.RadioButton(panel, label = '六级',pos = (240,135)) 

        self.btn = wx.Button(panel,-1,"开始破解",pos=(190,180)) 
        vbox.Add(self.btn,-1,wx.ALIGN_CENTER)
        self.btn.Bind(wx.EVT_BUTTON, self.OnClick, self.btn)
        self.btn.SetDefault()   
    def OnClick(self, event):  
        idten = self.idten.GetValue()
        name = self.name.GetValue()
        start = self.start.GetValue()
        if start =='':
            start = '1'
        if idten=='' or name=='':
            MyDialog(self, "Dialog").ShowModal() 
        else:
            if not self.cb1.GetValue() and not self.cb2.GetValue():
                MyDialog(self, "Dialog").ShowModal()
            else:
                if self.cb1.GetValue():
                    jibie = 'CET4_172_DANGCI'
                elif self.cb2.GetValue():
                    jibie = 'CET6_171_DANGCI'
                push_value_to_query(idten,name,start,jibie)
                return query()
def main():
    print("Welcome To Use this Program!")
    app=wx.App()
    frame=StaticTextFrame()
    frame.Show()
    app.MainLoop()
if __name__ == "__main__":
    main()