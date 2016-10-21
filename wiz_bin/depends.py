# -*- coding: utf-8 -*-

## \package wiz_bin.depends


import wx
from wx.lib.mixins import listctrl as wxMixinListCtrl

from dbr.buttons        import ButtonAdd
from dbr.buttons        import ButtonAppend
from dbr.buttons        import ButtonClear
from dbr.buttons        import ButtonDel
from dbr.language       import GT
from dbr.log            import Logger
from dbr.wizard         import WizardPage
from globals.ident      import ID_DEPENDS, ID_APPEND
from globals.tooltips   import SetPageToolTips
from dbr.help           import HelpButton


## TODO: Doxygen
class Panel(WizardPage):
    def __init__(self, parent):
        WizardPage.__init__(self, parent, ID_DEPENDS)
        
        # Bypass checking this page for build
        self.prebuild_check = False
        
        # --- DEPENDS
        self.dep_chk = wx.RadioButton(self, -1, GT(u'Depends'), name=u'Depends', style=wx.RB_GROUP)
        
        # --- PRE-DEPENDS
        self.pre_chk = wx.RadioButton(self, -1, GT(u'Pre-Depends'), name=u'Pre-Depends')
        
        # --- RECOMMENDS
        self.rec_chk = wx.RadioButton(self, -1, GT(u'Recommends'), name=u'Recommends')
        
        # --- SUGGESTS
        self.sug_chk = wx.RadioButton(self, -1, GT(u'Suggests'), name=u'Suggests')
        
        # --- ENHANCES
        self.enh_chk = wx.RadioButton(self, -1, GT(u'Enhances'), name=u'Enhances')
        
        # --- CONFLICTS
        self.con_chk = wx.RadioButton(self, -1, GT(u'Conflicts'), name=u'Conflicts')
        
        # --- REPLACES
        self.rep_chk = wx.RadioButton(self, -1, GT(u'Replaces'), name=u'Replaces')
        
        # --- BREAKS
        self.break_chk = wx.RadioButton(self, -1, GT(u'Breaks'), name=u'Breaks')
        
        
        # Input for dependencies
        self.txt_version = wx.StaticText(self, label=GT(u'Package Version'), name=u'version')
        self.txt_package = wx.StaticText(self, label=GT(u'Package Name'), name=u'package')
        
        self.input_package = wx.TextCtrl(self, size=(300,25), name=u'package')
        
        version_options = (u'>=', u'<=', u'=', u'>>', u'<<')
        self.operator = wx.Choice(self, choices=version_options)
        self.operator.SetSelection(0)
        
        self.input_version = wx.TextCtrl(self, name=u'version')
        
        # Button to display help information about this page
        btn_help = HelpButton(self)
        
        layout_G1 = wx.GridBagSizer()
        
        # Row 1
        layout_G1.Add(self.txt_package, pos=(0, 0), flag=wx.ALIGN_BOTTOM, border=0)
        layout_G1.Add(self.txt_version, pos=(0, 2), flag=wx.ALIGN_BOTTOM)
        
        # Row 2
        layout_G1.Add(self.input_package, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        layout_G1.Add(self.operator, pos=(1, 1))
        layout_G1.Add(self.input_version, pos=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        
        layout_H1 = wx.BoxSizer(wx.HORIZONTAL)
        layout_H1.Add(layout_G1, 0, wx.ALIGN_BOTTOM)
        layout_H1.AddStretchSpacer(1)
        layout_H1.Add(btn_help)
        
        self.input_package.SetSize((100,50))
        
        # Add KEY_DOWN events to text areas
        wx.EVT_KEY_DOWN(self.input_package, self.SetDepends)
        wx.EVT_KEY_DOWN(self.input_version, self.SetDepends)
        
        # Buttons to add and remove dependencies from the list
        self.depadd = ButtonAdd(self)
        self.depadd.SetName(u'add')
        self.depapp = ButtonAppend(self)
        self.depapp.SetName(u'append')
        self.deprem = ButtonDel(self)
        self.deprem.SetName(u'remove')
        self.depclr = ButtonClear(self)
        self.depclr.SetName(u'clear')
        
        wx.EVT_BUTTON(self.depadd, -1, self.SetDepends)
        wx.EVT_BUTTON(self.depapp, -1, self.SetDepends)
        wx.EVT_BUTTON(self.deprem, -1, self.SetDepends)
        wx.EVT_BUTTON(self.depclr, -1, self.SetDepends)
        
        # ----- List
        self.dep_area = AutoListCtrl(self)
        self.dep_area.SetName(u'list')
        self.dep_area.InsertColumn(0, GT(u'Category'), width=150)
        self.dep_area.InsertColumn(1, GT(u'Package(s)'))
        # FIXME: wx. 3.0
        if (wx.MAJOR_VERSION < 3):
            self.dep_area.SetColumnWidth(100, wx.LIST_AUTOSIZE)
        
        wx.EVT_KEY_DOWN(self.dep_area, self.SetDepends)
        
        # Start some sizing
        radio_box = wx.StaticBoxSizer(wx.StaticBox(self, -1, GT(u'Categories')), wx.VERTICAL)
        rg1 = wx.GridSizer(4, 2, 5, 5)
        rg1.AddMany( [
        (self.dep_chk, 0),
        (self.pre_chk, 0),
        (self.rec_chk, 0),
        (self.sug_chk, 0),
        (self.enh_chk, 0),
        (self.con_chk, 0),
        (self.rep_chk, 0),
        (self.break_chk, 0) ])
        
        radio_box.Add(rg1, 0)
        
        layout_H2 = wx.BoxSizer(wx.HORIZONTAL)
        layout_H2.Add(radio_box, 0, wx.RIGHT, 5)
        layout_H2.Add(self.depadd, 0, wx.ALIGN_CENTER|wx.LEFT, 5)
        layout_H2.Add(self.depapp, 0, wx.ALIGN_CENTER|wx.LEFT, 5)
        layout_H2.Add(self.deprem, 0, wx.ALIGN_CENTER|wx.LEFT, 5)
        layout_H2.Add(self.depclr, 0, wx.ALIGN_CENTER|wx.LEFT, 5)
        
        '''
        self.border = wx.StaticBox(self, -1)
        border_box = wx.StaticBoxSizer(self.border, wx.VERTICAL)
        border_box.Add(depH1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        #border_box.AddSpacer(5)
        border_box.Add(layout_H2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        '''
        
        layout_H3 = wx.BoxSizer(wx.HORIZONTAL)
        layout_H3.Add(self.dep_area, 1, wx.EXPAND)
        
        # ----- Main Sizer
        layout_Vmain = wx.BoxSizer(wx.VERTICAL)
        layout_Vmain.Add(layout_H1, 0, wx.EXPAND|wx.ALL, 5)
        layout_Vmain.Add(layout_H2, 0, wx.ALL, 5)
        layout_Vmain.Add(layout_H3, 1, wx.ALL, 5)
        
        # ----- Layout
        self.SetAutoLayout(True)
        self.SetSizer(layout_Vmain)
        self.Layout()
        '''
        # ----- List not needed anymore
        self.setlabels = {	self.border: u'Border', self.txt_package: u'Pack', self.txt_version: u'Ver',
                            self.depadd: u'Add', self.depapp: u'App', self.deprem: u'Rem'}
        
        self.categories = {	self.dep_chk: u'Depends', self.pre_chk: u'Pre-Depends', self.rec_chk: u'Recommends',
                            self.sug_chk: u'Suggests', self.enh_chk: u'Enhances', self.con_chk: u'Conflicts',
                            self.rep_chk: u'Replaces', self.break_chk: u'Breaks'}
        '''
        
        
        SetPageToolTips(self)
    
    
    ## TODO: Doxygen
    def ImportPageInfo(self, d_type, d_string):
        Logger.Debug(__name__, GT(u'Importing {}: {}'.format(d_type, d_string)))
        
        values = d_string.split(u', ')
        
        for V in values:
            self.dep_area.InsertStringItem(0, d_type)
            self.dep_area.SetStringItem(0, 1, V)
    
    
    ## Resets all fields on page to default values
    def ResetPageInfo(self):
        self.dep_area.DeleteAllItems()
    
    
    ## TODO: Doxygen
    def SelectAll(self):
        total_items = self.dep_area.GetItemCount()
        count = -1
        while count < total_items:
            count += 1
            self.dep_area.Select(count)
    
    
    ## TODO: Doxygen
    def SetDepends(self, event):
        try:
            key_mod = event.GetModifiers()
            key_id = event.GetKeyCode()
        except AttributeError:
            key_mod = None
            key_id = event.GetEventObject().GetId()
        
        addname = self.input_package.GetValue()
        oper = self.operator.GetStringSelection()
        ver = self.input_version.GetValue()
        addver = u'(%s%s)' % (oper, ver)
            
        if key_id == wx.WXK_RETURN or key_id == wx.WXK_NUMPAD_ENTER:
            for item in self.categories:
                if item.GetValue() == True:
                    if addname != u'':
                        self.dep_area.InsertStringItem(0, self.categories[item])
                        if ver == u'':
                            self.dep_area.SetStringItem(0, 1, addname)
                        else:
                            self.dep_area.SetStringItem(0, 1, u'%s %s' % (addname, addver))
        
        elif key_id == ID_APPEND:
            listrow = self.dep_area.GetFocusedItem()  # Get row of selected item
            colitem = self.dep_area.GetItem(listrow, 1)  # Get item from second column
            prev_text = colitem.GetText()  # Get the text from that item
            if addname != u'':
                if ver != u'':
                    self.dep_area.SetStringItem(listrow, 1, u'%s | %s %s' % (prev_text, addname, addver))
                else:
                    self.dep_area.SetStringItem(listrow, 1, u'%s | %s' % (prev_text, addname))
        
        elif key_id == wx.ID_DELETE: # wx.WXK_DELETE:
            selected = None
            while selected != -1:
                selected = self.dep_area.GetFirstSelected()
                self.dep_area.DeleteItem(selected)
        
        elif key_id == 65 and key_mod == 2:
            self.SelectAll()
        
        elif key_id == wx.WXK_ESCAPE:
            # Create the dialog
            confirm = wx.MessageDialog(self, GT(u'Clear all dependencies?'), GT(u'Confirm'),
                    wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
            if confirm.ShowModal() == wx.ID_YES:
                self.dep_area.DeleteAllItems()
        
        event.Skip()
    
    
    
    ## TODO: Doxygen
    def SetFieldDataLegacy(self, data):
        self.dep_area.DeleteAllItems()
        for item in data:
            item_count = len(item)
            while item_count > 1:
                item_count -= 1
                self.dep_area.InsertStringItem(0, item[0])
                self.dep_area.SetStringItem(0, 1, item[item_count])



## A ListCtrl that automatically expands columns
class AutoListCtrl(wx.ListCtrl, wxMixinListCtrl.ListCtrlAutoWidthMixin):
    def __init__(self, parent, window_id=wx.ID_ANY):
        wx.ListCtrl.__init__(self, parent, window_id, style=wx.BORDER_SIMPLE|wx.LC_REPORT)
        wxMixinListCtrl.ListCtrlAutoWidthMixin.__init__(self)
        
        self.prev_width = self.Size[0]
        
        if wx.MAJOR_VERSION == 3 and wx.MINOR_VERSION == 0:
            wx.EVT_SIZE(self, self.OnResize)
    
    
    ## Fixes sizing problems with ListCtrl in wx 3.0
    def OnResize(self, event):
        if event:
            event.Skip(True)
        
        # FIXME: -10 should be a dynamic number set by the sizer's padding
        self.SetSize(wx.Size(self.GetParent().Size[0] - 10, self.Size[1]))
