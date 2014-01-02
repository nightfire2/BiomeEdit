# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2013)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import wx.grid

###########################################################################
## Class BiomeEdit
###########################################################################

class BiomeEdit ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Biome Edit", pos = wx.DefaultPosition, size = wx.Size( 838,725 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_menubar = wx.MenuBar( 0 )
		self.file_menu = wx.Menu()
		self.open_folder = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Open Folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.open_folder )
		
		self.open_file = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Open File", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.open_file )
		
		self.close_file = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Close", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.close_file )
		self.close_file.Enable( False )
		
		self.close_all = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Close All", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.close_all )
		self.close_all.Enable( False )
		
		self.save_all = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Save All", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.save_all )
		self.save_all.Enable( False )
		
		self.save_file = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.save_file )
		self.save_file.Enable( False )
		
		self.save_as = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Save As", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.save_as )
		self.save_as.Enable( False )
		
		self.save_all_to_folder = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Save All To Folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.save_all_to_folder )
		self.save_all_to_folder.Enable( False )
		
		self.exit_app = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.exit_app )
		
		self.m_menubar.Append( self.file_menu, u"File" ) 
		
		self.SetMenuBar( self.m_menubar )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.tab_container = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE|wx.aui.AUI_NB_WINDOWLIST_BUTTON|wx.NO_BORDER )
		self.all_biomes_tab = wx.Panel( self.tab_container, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		all_biomes_sizer = wx.GridSizer( 0, 1, 0, 0 )
		
		self.biome_grid = wx.grid.Grid( self.all_biomes_tab, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		
		# Grid
		self.biome_grid.CreateGrid( 0, 0 )
		self.biome_grid.EnableEditing( True )
		self.biome_grid.EnableGridLines( True )
		self.biome_grid.EnableDragGridSize( True )
		self.biome_grid.SetMargins( 0, 0 )
		
		# Columns
		self.biome_grid.AutoSizeColumns()
		self.biome_grid.EnableDragColMove( False )
		self.biome_grid.EnableDragColSize( True )
		self.biome_grid.SetColLabelSize( 30 )
		self.biome_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.biome_grid.AutoSizeRows()
		self.biome_grid.EnableDragRowSize( True )
		self.biome_grid.SetRowLabelSize( 200 )
		self.biome_grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.biome_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		all_biomes_sizer.Add( self.biome_grid, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.all_biomes_tab.SetSizer( all_biomes_sizer )
		self.all_biomes_tab.Layout()
		all_biomes_sizer.Fit( self.all_biomes_tab )
		self.tab_container.AddPage( self.all_biomes_tab, u"All Biomes", True, wx.NullBitmap )
		
		bSizer1.Add( self.tab_container, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.exit_func )
		self.Bind( wx.EVT_MENU, self.open_folder_func, id = self.open_folder.GetId() )
		self.Bind( wx.EVT_MENU, self.open_file_func, id = self.open_file.GetId() )
		self.Bind( wx.EVT_MENU, self.close_file_func, id = self.close_file.GetId() )
		self.Bind( wx.EVT_MENU, self.close_all_func, id = self.close_all.GetId() )
		self.Bind( wx.EVT_MENU, self.save_all_func, id = self.save_all.GetId() )
		self.Bind( wx.EVT_MENU, self.save_file_func, id = self.save_file.GetId() )
		self.Bind( wx.EVT_MENU, self.save_as_func, id = self.save_as.GetId() )
		self.Bind( wx.EVT_MENU, self.save_all_to_folder_func, id = self.save_all_to_folder.GetId() )
		self.Bind( wx.EVT_MENU, self.exit_app_func, id = self.exit_app.GetId() )
		self.tab_container.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.tab_change_func )
		self.tab_container.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.tab_close_func )
		self.tab_container.Bind( wx.EVT_SIZE, self.resize_func )
		self.biome_grid.Bind( wx.grid.EVT_GRID_COL_SIZE, self.col_resize_func )
		self.biome_grid.Bind( wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.view_biome_func )
		self.biome_grid.Bind( wx.grid.EVT_GRID_ROW_SIZE, self.row_resize_func )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def exit_func( self, event ):
		event.Skip()
	
	def open_folder_func( self, event ):
		event.Skip()
	
	def open_file_func( self, event ):
		event.Skip()
	
	def close_file_func( self, event ):
		event.Skip()
	
	def close_all_func( self, event ):
		event.Skip()
	
	def save_all_func( self, event ):
		event.Skip()
	
	def save_file_func( self, event ):
		event.Skip()
	
	def save_as_func( self, event ):
		event.Skip()
	
	def save_all_to_folder_func( self, event ):
		event.Skip()
	
	def exit_app_func( self, event ):
		event.Skip()
	
	def tab_change_func( self, event ):
		event.Skip()
	
	def tab_close_func( self, event ):
		event.Skip()
	
	def resize_func( self, event ):
		event.Skip()
	
	def col_resize_func( self, event ):
		event.Skip()
	
	def view_biome_func( self, event ):
		event.Skip()
	
	def row_resize_func( self, event ):
		event.Skip()
	

