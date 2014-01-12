#!/usr/bin/env python

import wx
import wx.xrc
import wx.aui
import wx.grid
import os
import os.path
import glob
import re
import collections
import difflib
from TCConfig import *

#from UI.BiomeEditUI import BiomeEdit
###########################################################################
## Class BiomeEditApp
###########################################################################
class BiomeEditApp ( BiomeEdit ):
	
	def __init__( self ,parent):
		super(BiomeEditApp,self).__init__(parent)
		#Use characters that can appear in a filename to ensure this tab name can't conflict with another tab.
		self.all_biomes_tab.SetName("all*:*biomes")
		self.tab_container.SetWindowStyleFlag((wx.aui.AUI_NB_DEFAULT_STYLE|wx.aui.AUI_NB_WINDOWLIST_BUTTON|wx.NO_BORDER) & ~wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB  )
		self.field_manager = FieldManager("")
		self.config_table = ConfigManager(self.config_grid,self.tab_container,self.field_manager)
		self.config_grid.SetDefaultEditor(wx.grid.GridCellTextEditor())
		self.config_grid.SetDefaultCellOverflow(False)
		self.config_grid.SetTable(self.config_table)
		self.current_page=self.all_biomes_tab
		self.activeUndoRedo= UndoRedoManager()
		self.app_status.SetStatusWidths([1,-1,-1])
	def undo_func( self, event ):
		self.activeUndoRedo.Undo()
		self.config_grid.ForceRefresh()
	def redo_func( self, event ):
		self.activeUndoRedo.Redo()
		self.config_grid.ForceRefresh()
	# Virtual event handlers, overide them in your derived class
	def open_folder_func( self, event ):
		dialog = wx.DirDialog(None,'Choose a folder',os.getcwd())
		if dialog.ShowModal() == wx.ID_OK:
			allFiles = glob.glob(dialog.GetPath()+"/*BiomeConfig.ini")
			for filepath in allFiles:
				config = self.open_config(filepath)
				if config != None:
					self.config_table.AddConfig(config)
					self.tab_container.AddPage( config, config.GetName(), False, wx.NullBitmap )
				
		dialog.Destroy()
		self.update_menu()
	
	def open_config(self,filePath):
		try:
			fh = open(filePath,"r")
			data = fh.read()
			fh.close()
			pathInfo =self.parse_biome_path(filePath)
			
			return TCConfig(data,pathInfo['path'],pathInfo['name'],self.field_manager,self)
	
		except Exception as e:
			dlg = wx.MessageDialog(None,"Unable to open the file\n"+filePath,"Error opening file",wx.OK |wx.ICON_WARNING)
			dlg.ShowModal()
			dlg.Destroy()
			return None

	def open_file_func( self, event ):
		#event.Skip()
		dialog = wx.FileDialog(None,'Choose files to open',os.getcwd(),"", "*BiomeConfig.ini",wx.OPEN|wx.FD_MULTIPLE)
		if dialog.ShowModal() == wx.ID_OK:
			allFiles = dialog.GetPaths()
			#for file in allFiles:
			print len(allFiles)
			for filepath in dialog.GetPaths():
				config = self.open_config(filepath)
				if config != None:
					self.config_table.AddConfig(config)
					self.tab_container.AddPage( config, config.GetName(), False, wx.NullBitmap )
	
		dialog.Destroy()
		self.update_menu()
		self.config_table.UpdateAllLabels()
	
	def update_menu(self):
		name= self.current_page.GetName()
		if self.config_table.GetNumberCols() <= 0:
			self.close_all.Enable(False)
			self.save_all.Enable(False)
			self.save_all_to_folder.Enable(False)
		else:
			self.close_all.Enable()
			self.save_all.Enable()
			self.save_all_to_folder.Enable()
		#if name == self.all_biomes_tab.GetName()"all:biomes":
		if name == self.all_biomes_tab.GetName():
			self.close_file.Enable(False)
			self.save_file.Enable(False)
			self.save_as.Enable(False)
		else:
			self.close_file.Enable()
			self.save_file.Enable()
			self.save_as.Enable()
		
		self.app_status.SetStatusText("{0}: Fields       {1}: Biomes".format(len(self.field_manager),self.config_table.GetNumberCols()),1)
		
	def parse_biome_path(self,filePath):
		name = filePath[filePath.rfind(os.path.sep)+1:filePath.rfind(r"BiomeConfig.ini")]
		folderPath = os.path.dirname(filePath)
		return {'name':name,'path':folderPath}
		
	def close_config(self,config):
		canclose=True
		if config.IsModified():
			dlg = wx.MessageDialog(None,"Save changes to "+config.GetName(),"Save changes",wx.YES_NO|wx.CANCEL |wx.ICON_WARNING)
			action = dlg.ShowModal()
			
			if action !=wx.ID_CANCEL:
				if action == wx.ID_YES:
					
					self.save_config(config)
			else:
				canclose=False
			dlg.Destroy()
		if canclose:
			self.config_table.RemoveConfig(config)
			self.activeUndoRedo.ClearHistoryByID(config.GetUniqueID())
		return canclose
		
	def save_config(self,config):

		with open(config.GetFilePath()+os.path.sep+config.GetName()+"BiomeConfig.ini",mode='w') as myfile:
			myfile.write(str(config))
		config.SetModified(False)
		self.config_table.UpdateAllLabels()
		
		
		
	def save_config_as(self,config,newpath):
		pathInfo =self.parse_biome_path(newpath)

		config.SetFilePath(pathInfo['path'])
		self.config_table.ChangeConfigName(config,pathInfo['name'])
		self.save_config(config)
		self.update_menu()
		
	def close_file_func( self, event ):
		self.close_config(self.current_page)
		index = self.tab_container.GetPageIndex(self.current_page)
		self.tab_container.DeletePage(index)
		self.config_table.UpdateAllLabels()
		self.update_menu()
	
	def close_all_func( self, event ):
		configs = list( self.config_table.configs)
		for config in configs:
			#self.biome_table.RemoveBiome(biome.GetUniqueName())
			if self.close_config(config):
				index = self.tab_container.GetPageIndex(config)
				self.tab_container.DeletePage(index)
				
		self.config_table.UpdateAllLabels()
		self.update_menu()
		
	def save_all_func( self, event ):
		for config in self.config_table.configs:
			self.save_config(config)
		
	def save_file_func( self, event ):
		self.save_config(self.current_page)
	
	def save_as_func( self, event ):
		
		dialog = wx.FileDialog(None,'Save As',os.getcwd(),self.current_page.GetName()+"BiomeConfig.ini", "*BiomeConfig.ini",wx.SAVE|wx.FD_OVERWRITE_PROMPT)
		if dialog.ShowModal() == wx.ID_OK:
			self.save_config_as(self.current_page,dialog.GetPath())
		dialog.Destroy()
	
	def save_all_to_folder_func( self, event ):
		dialog = wx.DirDialog(None,'Choose a folder',os.getcwd())
		if dialog.ShowModal() == wx.ID_OK:
			for config in self.config_table.configs:
				self.save_config_as(config,dialog.GetPath()+os.path.sep+config.GetName()+"BiomeConfig.ini")
			dialog.Destroy()
		else:
			dialog.Destroy()
			
	def exit_app_func(self,event):
		self.Close()
	def exit_func( self, event ):
		configs = list( self.config_table.configs)
		willclose = True
		for config in configs:
			if self.close_config(config):
				index = self.tab_container.GetPageIndex(config)
				self.tab_container.DeletePage(index)
			else:
				willclose = False
				
		if not willclose:
			event.Veto()

		else:
			event.Skip()
		
		
	
	def tab_change_func( self, event ):
		index = event.GetSelection()
		page = self.tab_container.GetPage(index)
		self.current_page = page
		self.update_menu()
		if(page.GetName()==self.all_biomes_tab.GetName()):
			self.tab_container.SetWindowStyleFlag((wx.aui.AUI_NB_DEFAULT_STYLE|wx.NO_BORDER|wx.aui.AUI_NB_WINDOWLIST_BUTTON) & ~wx.aui.AUI_NB_CLOSE_BUTTON & ~wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
		else:
			self.tab_container.SetWindowStyleFlag(wx.aui.AUI_NB_DEFAULT_STYLE|wx.NO_BORDER|wx.aui.AUI_NB_WINDOWLIST_BUTTON)
		
	def view_biome_func( self, event ):
		if event.GetCol()>= 0 and event.GetRow()==-1:
			config = self.config_table.GetConfigByIndex(event.GetCol())
			index = self.tab_container.GetPageIndex(config)
			self.tab_container.SetSelection(index)
			
	def tab_close_func( self, event ):
		index = event.GetSelection()
		page = self.tab_container.GetPage(index)
		if not self.close_config(page):
				event.Veto()
		
    # end of class BiomeEdit
		
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    appframe = BiomeEditApp(None)
    app.SetTopWindow(appframe)
    appframe.Show()
    app.MainLoop()