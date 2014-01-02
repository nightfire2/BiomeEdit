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

from BiomeEditUI import BiomeEdit
###########################################################################
## Class BiomeEditApp
###########################################################################
class BiomeEditApp ( BiomeEdit ):
	
	def __init__( self ,parent):
		super(BiomeEditApp,self).__init__(parent)
		self.all_biomes_tab.SetName("all@biomes")
		self.tab_container.SetWindowStyleFlag((wx.aui.AUI_NB_DEFAULT_STYLE|wx.aui.AUI_NB_WINDOWLIST_BUTTON|wx.NO_BORDER) & ~wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB  )
		self.biome_table = BiomeTable(self.biome_grid)
		self.biome_grid.SetDefaultEditor(wx.grid.GridCellTextEditor())
		self.biome_grid.SetTable(self.biome_table)
		self.current_page=self.all_biomes_tab
		
	# Virtual event handlers, overide them in your derived class
	def open_folder_func( self, event ):
		#event.Skip()
		dialog = wx.DirDialog(None,'Choose a folder',os.getcwd())
		if dialog.ShowModal() == wx.ID_OK:
			allFiles = glob.glob(dialog.GetPath()+"/*BiomeConfig.ini")
			for file in allFiles:
				try:
					biome = Biome(self,file)
					self.biome_table.AddBiome(biome)
					biome.SetName(biome.GetUniqueName())
					self.tab_container.AddPage( biome, biome.GetName(), False, wx.NullBitmap )
				except IOError as e:
					#alert 
					dlg = wx.MessageDialog(None,str(e),"Error opening file",wx.OK |wx.ICON_WARNING)
					dlg.ShowModal()
					dlg.Destroy()
		dialog.Destroy()
		self.update_menu()
	
	def open_file_func( self, event ):
		#event.Skip()
		dialog = wx.FileDialog(None,'Choose files to open',os.getcwd(),"", "*BiomeConfig.ini",wx.OPEN|wx.FD_MULTIPLE)
		if dialog.ShowModal() == wx.ID_OK:
			allFiles = dialog.GetPaths()
			#for file in allFiles:
			for filepath in dialog.GetPaths():
				try:
					biome = Biome(self,filepath)
					self.biome_table.AddBiome(biome)
					biome.SetName(biome.GetUniqueName())
					self.tab_container.AddPage( biome, biome.GetName(), False, wx.NullBitmap )
					
					
				except IOError as e:
					#alert 
					dlg = wx.MessageDialog(None,str(e),"Error opening file",wx.OK |wx.ICON_WARNING)
					dlg.ShowModal()
					dlg.Destroy()
		dialog.Destroy()
		self.update_menu()
	
	def update_menu(self):
		name= self.current_page.GetName()
		if self.biome_table.GetNumberCols() <= 0:
			self.close_all.Enable(False)
			self.save_all.Enable(False)
			self.save_all_to_folder.Enable(False)
		else:
			self.close_all.Enable()
			self.save_all.Enable()
			self.save_all_to_folder.Enable()
		if name == "all@biomes":
			self.close_file.Enable(False)
			self.save_file.Enable(False)
			self.save_as.Enable(False)
		else:
			self.close_file.Enable()
			self.save_file.Enable()
			self.save_as.Enable()
			
	def close_biome(self,biome):
		canclose=True
		if biome.IsModified():
			dlg = wx.MessageDialog(None,"Save changes to "+biome.GetName(),"Save changes",wx.YES_NO|wx.CANCEL |wx.ICON_WARNING)
			action = dlg.ShowModal()
			
			if action !=wx.ID_CANCEL:
				if action == wx.ID_YES:
					biome.Save()
			else:
				canclose=False
			dlg.Destroy()
		if canclose:
			self.biome_table.RemoveBiome(biome.GetUniqueName())
		
		return canclose
	
	def close_file_func( self, event ):
		self.close_biome(self.current_page)
		index = self.tab_container.GetBiomeIndex(biome)
		self.tab_container.DeletePage(index)
		self.update_menu()
	
	def close_all_func( self, event ):
		biomes = dict( self.biome_table.biomes)
		for key,biome in biomes.iteritems():
			#self.biome_table.RemoveBiome(biome.GetUniqueName())
			if self.close_biome(biome):
				index = self.tab_container.GetPageIndex(biome)
				self.tab_container.DeletePage(index)
			
			
		self.update_menu()
		
	def save_all_func( self, event ):
		for key,biome in self.biome_table.biomes.iteritems():
			biome.save()
		
	def save_file_func( self, event ):
		self.current_page.Save()
	
	def save_as_func( self, event ):
		dialog = wx.FileDialog(None,'Save As',os.getcwd(),"", "*BiomeConfig.ini",wx.SAVE)
		if dialog.ShowModal() == wx.ID_OK:
			uname = self.current_page.GetUniqueName()
			self.current_page.SaveAs(dialog.GetPath())
			self.biome_table.ChangeBiomeName(uname,self.current_page.GetUniqueName())
		dialog.Destroy()
	
	def save_all_to_folder_func( self, event ):
		dialog = wx.DirDialog(None,'Choose a folder',os.getcwd())
		if dialog.ShowModal() == wx.ID_OK:
			
			for key,biome in self.biome_table.biomes.iteritems():
				biome.SaveAs(dialog.GetPath()+os.path.sep+biome.GetName()+"BiomeConfig.ini")
			dialog.Destroy()
		else:
			dialog.Destroy()
	def exit_app_func(self,event):
		self.Close()
	def exit_func( self, event ):
		biomes = dict( self.biome_table.biomes)
		willclose = True
		for key,biome in biomes.iteritems():
			if self.close_biome(biome):
				index = self.tab_container.GetPageIndex(biome)
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
		if(page.GetName()=="all@biomes"):
			self.tab_container.SetWindowStyleFlag((wx.aui.AUI_NB_DEFAULT_STYLE|wx.NO_BORDER|wx.aui.AUI_NB_WINDOWLIST_BUTTON) & ~wx.aui.AUI_NB_CLOSE_BUTTON & ~wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
		else:
			self.tab_container.SetWindowStyleFlag(wx.aui.AUI_NB_DEFAULT_STYLE|wx.NO_BORDER|wx.aui.AUI_NB_WINDOWLIST_BUTTON)
		
	def view_biome_func( self, event ):
		if event.GetCol()>= 0 and event.GetRow()==-1:
			biome = self.biome_table.GetBiomeByIndex(event.GetCol())
			index = self.tab_container.GetPageIndex(biome)
			self.tab_container.SetSelection(index)
			
	def tab_close_func( self, event ):
		index = event.GetSelection()
		page = self.tab_container.GetPage(index)
		if not self.close_biome(page):
				event.Veto()
		
    # end of class BiomeEdit

	
	
class Biome(wx.ScrolledWindow):
	Fields=list()
	FieldTypes=dict()
	def __init__(self,parent,filepath):
		self.parent=parent
		self.modified=False
		self.filelines=list()
		self.properties=collections.OrderedDict()
		
		#Load the file. I might move this out of the class later
		try:
			fh = open(filepath,"r")
			self.filelines = fh.read().splitlines()
			fh.close()
			
		except:
			raise IOError("Unable to open the file\n"+filepath)
			
		super(Biome,self).__init__(parent.tab_container, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
		#extract biome name
		self.SetName(filepath[filepath.rfind(os.path.sep)+1:filepath.rfind(r"BiomeConfig.ini")])
		self.folderpath=os.path.dirname(filepath)
		self.uniqueName = self.GetName()
		self.SetLabel(self.uniqueName)
		self.SetScrollRate( 5, 5 )

		
		#the file is loaded lets parse the lines
		self._ParseLines()
		#update global field list with any new fields
		newfields = list(Biome.Fields)
		
		if len(Biome.Fields)==0:
			#if no Fields are in the list make one
			Biome.Fields=self.properties.keys()
		else:
			#intelegetly merge the fields while attempting to preserve the original order
			keylist = list(self.properties.keys())
			#loop through the new list
			for idx,field in enumerate(keylist):
				if field not in newfields:
					#if the field is not in the global list
					#get the position of element previous to where it appeard in the current list
					tindex=keylist.index(field)-1
					#if the index is out of range 
					if tindex < 0:
						#insert it at the front of the new list
						newfields.insert(0,field)
					else:
						#otherwise insert it after the element it came after in the newlist
						newfields.insert(newfields.index(keylist[tindex])+1,field)
			Biome.Fields=newfields

	def __len__(self):
		return len(self.properties)
		
	def __getitem__(self,key):
		if(isinstance( key, ( int, long ) )):
			key = Biome.Fields[key]
		if key not in self.properties:
			return None
		return self.properties[key]
		
	def __setitem__(self,key,value):
		if(isinstance( key, ( int, long ) )):
			key = Biome.Fields[key]
		
		if key in self.properties:
			oldvalue=self.properties[key].GetCellValue()
			
			self.properties[key].SetCellValue(value)
			if oldvalue!=value:
				self.SetModified(True)
		else:
			if key in Biome.FieldTypes[key]:
				line = value
				if Biome.FieldTypes[key] == BiomeAttribute:
					line = key+":"+value
				if Biome.FieldTypes[key].IsValid(line):
					self.properties[key] =Biome.FieldTypes[key](line,len(self.filelines))
					self.filelines.append(' ')
					self.SetModified(True)
			else:
				self.properties[key] = BiomeUnknown(line,len(self.filelines))
				self.filelines.append(' ')
				self.SetModified(True)	
			
	def __contains__(self,item):
		return item in self.properties
		
	def _ParseLines(self):	
		r_count = 0
		s_count = 0
		o_count = 0
		for idx,line in enumerate(self.filelines):
		
			#if the line is empty
			if len(line.strip())==0:
				continue
			#if the line is commented
			if line[0] =='#':
				continue
		
			key=''
			field=None
			FieldType=None
			if BiomeAttribute.IsValid(line):
				
				field=BiomeAttribute(line,idx)
				FieldType=BiomeAttribute
				key = field.GetLabel()
				
			elif BiomeFunc.IsValid(line):
				field=BiomeFunc(line,idx)
				FieldType=BiomeFunc
				if field.GetLabel()=='Sapling':
					key='Sapling '+str(s_count)
					s_count+=1
				else:
					key='Resources Queue '+str(r_count)
					r_count+=1
			else:
			
				field = BiomeUnknown(line,idx)
				FieldType=BiomeUnknown
				key = 'Other '+str(o_count)
				print 'unexpected line at '+str(idx+1)
				o_count+=1
			if key not in Biome.FieldTypes:
				Biome.FieldTypes[key]=FieldType
			#store based on type key
			self.properties[key] = field
		
	def keys():
		return self.properties.keys()
		
	def SetUniqueName(self,uname):
		self.uniqueName=uname
		self.SetLabel(self.uniqueName)
	def GetUniqueName(self):
		return self.uniqueName
	def SetLabel(self,uname):
		super(Biome,self).SetLabel(uname)
		pos = self.parent.tab_container.GetPageIndex(self)
		if pos!=-1:
			self.parent.tab_container.SetPageText(pos,uname)
	
	def SetModified(self,modified):
		if self.modified!=modified:	
			self.modified=modified
			if(modified):
				self.SetLabel("*"+self.uniqueName)
			else:
				self.SetLabel(self.uniqueName)
	
	def IsModified(self):
		return self.modified
		
	def _commitChanges(self):
		for key,field in self.properties.iteritems():
			self.filelines[field.GetLineNumber()]=str(field)
		
	def Save(self):
		self._commitChanges()
		with open(self.folderpath+os.path.sep+self.GetName()+"BiomeConfig.ini",mode='w') as myfile:
			myfile.write('\n'.join(self.filelines))
		
		self.SetModified(False)
	
	def SaveAs(self,filepath):
		self.SetName(filepath[filepath.rfind(os.path.sep)+1:filepath.rfind(r"BiomeConfig.ini")])
		self.folderpath=os.path.dirname(filepath)
		self.uniqueName = self.GetName()
		self.SetLabel(self.uniqueName)
		self.Save()
			
		self.SetModified(False)
	

class BiomeFieldBase():
	
	matchPattern="Invalid"
	def __init__(self ,line,linenumber):
		self.line=line
		self.Parse(line)
		self.linenumber=linenumber
	def GetLineNumber(self):
		return self.linenumber
	@classmethod
	def IsValid(self,line):
		lineparts = re.match(self.matchPattern,line)
		if lineparts != None:
			return True
		else:
			return False
	def GetLabel(self):
		return self.label
	def GetValue(self):
		return self.value
	def GetLineNumber(self):
		return self.linenumber
	def Parse(self,line):
		lineparts = re.match(self.matchPattern,line)
		if lineparts != None:
			self.label=lineparts.group(1)
			self.value = lineparts.group(2)
			return True
		else:
			return False
		
		
class BiomeAttribute(BiomeFieldBase):
	matchPattern = r"^([a-zA-Z0-9_]+)\:(.*)"
	
	def SetCellValue(self ,value):
		self.value=value
		
	def GetCellValue(self):
		return self.value
		
	def __str__(self):
		return "%s:%s"% (self.label, self.value)
	
class BiomeFunc(BiomeFieldBase):
	
	matchPattern = r"^([a-zA-Z0-9_]+)(\(.*\))"
	def SetCellValue(self ,value):
		if value.strip()!="":	
			if self.IsValid(value):
				self.Parse(value)
		else:
			self.label=""
			self.value=""	
				
	def GetCellValue(self):
	
		return "%s%s" % (self.label,self.value)
		
	def __str__(self):
		return "%s%s" % (self.label,self.value)
		
class BiomeUnknown(BiomeFieldBase):
	matchPattern = r"^()(.*)"
	def SetCellValue(self ,value):
		self.Parse(value)
	def GetCellValue(self):
		return self.value
	def __str__(self):
		return self.value
		
class BiomeTable(wx.grid.PyGridTableBase):
	
	
	def __init__(self,grid):
		self.grid=grid
		super(BiomeTable,self).__init__()
		
		self.biomefields=list()
		self.rowLables=list()
		self.columnLabels=list()
		self.biomes=dict()
		self.uniqueNames=dict()
		self.oldRows=Biome.Fields
		self.currentCols=0
		self.currentRows=0
		
	def AddBiome(self,biome):
		names = self.uniqueNames
		bname = biome.GetName()
		uname=""
		if bname in self.uniqueNames:
			self.uniqueNames[bname]+=1
		else:
			self.uniqueNames[bname]=1
		if self.uniqueNames[bname]>1:
			uname=bname+" ("+str(self.uniqueNames[bname])+")"
		else:
			uname = bname
		self.columnLabels.append(uname)
		biome.SetUniqueName(uname)
		self.biomes[uname] = biome
		self.ResetView()
		for i in range(0,self.currentRows):
			if biome[i] != None:
				self.grid.SetCellValue(i,self.currentCols-1,biome[i].GetCellValue())
		self.grid.AutoSizeColLabelSize(self.GetNumberCols()-1)
		if self.grid.GetColSize(self.GetNumberCols()-1)<150 :
			self.grid.SetColSize(self.GetNumberCols()-1,150)
		biome.SetLabel(uname)
		biome.SetModified(False)
		
	def GetBiomeByIndex(self,index):
		return self.biomes[self.columnLabels[index]]
	def ResetView(self):
		"""Trim/extend the control's rows and update all values"""
		self.grid.BeginBatch()
		for current, new, delmsg, addmsg in [
				(self.currentRows, self.GetNumberRows(), wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
				(self.currentCols, self.GetNumberCols(), wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED, wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
		]:
			if new < current:
				msg = wx.grid.GridTableMessage(
						self,
						delmsg,
						new,    # position
						current-new,
				)
				self.grid.ProcessTableMessage(msg)
			elif new > current:
				msg = wx.grid.GridTableMessage(
						self,
						addmsg,
						new-current
				)
				self.grid.ProcessTableMessage(msg)
		self.UpdateValues()
		self.grid.EndBatch()
		
		# The scroll bars aren't resized (at least on windows)
		# Jiggling the size of the window rescales the scrollbars
		h,w = self.grid.GetSize()
		self.grid.SetSize((h+1, w))
		self.grid.SetSize((h, w))
		self.grid.Refresh()
		self.grid.ForceRefresh()
		
		
		self.currentRows=self.GetNumberRows()
		self.currentCols=self.GetNumberCols()

	def ChangeBiomeName(self,olduname,newname):
		biome = self.biomes.pop(olduname)
		names = self.uniqueNames
		bname = newname
		uname=""
		if bname in self.uniqueNames:
			self.uniqueNames[bname]+=1
		else:
			self.uniqueNames[bname]=1
		if self.uniqueNames[bname]>1:
			uname=bname+" ("+str(self.uniqueNames[bname])+")"
		else:
			uname = bname
		biome.SetUniqueName(uname)
		self.biomes[uname]=biome
		self.columnLabels[self.columnLabels.index(olduname)]=uname
		
	def UpdateValues( self ):
		"""Update all displayed values"""
		msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
		self.grid.ProcessTableMessage(msg)
	
	def RemoveBiome(self,uname):
		self.grid.DeleteCols(self.columnLabels.index(uname),True)
		self.ResetView()
		
	def DeleteCols(self,pos=0,numCols=1,updateLabels=True):
		self.biomes.pop(self.columnLabels[pos],None)
		self.columnLabels.pop(pos)
		return True
	def GetNumberRows(self):
		return len(Biome.Fields)

	def GetNumberCols(self):
		return len(self.biomes)

	def IsEmptyCell(self, row, col):
		return not Biome.Fields[row] in self.biomes[self.columnLabels[col]]		
	
	def CanGetValueAs(self,row,col,t):
		return True
	def CanSetValueAs(self,row,col,t):
		return True
	def GetTypeName(self, row, col):
		"""Return the name of the data type of the value in the cell"""
		return "string"
	def GetValue(self, row, col):
		if not self.IsEmptyCell(row,col):
			return self.biomes[self.columnLabels[col]][Biome.Fields[row]].GetCellValue()
		else:
			return " "
	def GetColLabelValue(self, col):
		return self.biomes[self.columnLabels[col]].GetLabel()
		
	def GetRowLabelValue(self, row):
		return Biome.Fields[row]
		
	def SetValue(self, row, col, value):
		self.biomes[self.columnLabels[col]][Biome.Fields[row]]=value	
		self.grid.Refresh()
		
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    appframe = BiomeEditApp(None)
    app.SetTopWindow(appframe)
    appframe.Show()
    app.MainLoop()