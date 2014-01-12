import wx
import wx.xrc
import wx.aui
import wx.grid

class ConfigManager(wx.grid.PyGridTableBase):
	def __init__(self,grid,tabContainer,fieldManager):
		super(ConfigManager,self).__init__()
		self.tabContainer=tabContainer
		self.fieldManager=fieldManager
		self.grid=grid
		self.configs = list()
		self.names=dict()
		self.currentCols=0
		self.currentRows=0
		
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
	
	def UpdateValues( self ):
		"""Update all displayed values"""
		msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
		self.grid.ProcessTableMessage(msg)
	def UpdateAllLabels(self):
		for config in self.configs:
			self.UpdateLabel(config)

	def UpdateLabel(self,config):
		pos = self.tabContainer.GetPageIndex(config)
		if pos!=-1:
			self.tabContainer.SetPageText(pos,self.GetColLabelValue(self.configs.index(config)))
		
	def ChangeConfigName(self,config,newName):
		if newName!=config.GetName():
			oldName = config.GetName()	
			self.names[oldName].remove(config.GetDuplicateID())
			dupID=0
			if newName in self.names:
				dupID=self._getnext(self.names[newName])
				self.names[newName].append(dupID)
			else:
				dupID=1
				self.names[newName]=[1]
				
			config.SetDuplicateID(dupID)
			config.SetName(newName)
			self.UpdateLabel(config)
			
	def _getnext(self,counters):
		for i in range(1,len(counters)+2):
			if i not in counters:
				return i
		
				
	def AddConfig(self,config):
		name = config.GetName()
		dupID = 0
		if name in self.names:
			dupID=self._getnext(self.names[name])
			self.names[name].append(dupID)
		else:
			self.names[name]=[1]
			dupID=1
		config.SetDuplicateID(dupID)
		self.configs.append(config)
		self.ResetView()
		
		for i in range(0,self.currentRows):
			if config.GetFieldValueByIndex(i) != "":
				self.grid.SetCellValue(i,self.currentCols-1,config.GetFieldValueByIndex(i))
		self.grid.AutoSizeColLabelSize(self.GetNumberCols()-1)
		if self.grid.GetColSize(self.GetNumberCols()-1)<150 :
			self.grid.SetColSize(self.GetNumberCols()-1,150)
		config.SetLabel(name)
		config.SetModified(False)
		#refresh
	def GetConfigByIndex(self,index):
		if index < len(self.configs):
			return self.configs[index]
		else:
			return None
	def RemoveConfig(self,config):
	
		self.grid.DeleteCols(self.configs.index(config))
		
		self.ResetView()
		#tell the s to delete its self
		
		
	def DeleteCols(self,pos=0,numCols=1,updateLabels=True):
		cols = self.configs[pos:pos+numCols]
		for column in cols:
			name = column.GetName()
			self.names[name].remove(column.GetDuplicateID())
			self.configs.remove(column)
			
			
		return True
	def GetNumberRows(self):
		return len(self.fieldManager)

	def GetNumberCols(self):
		return len(self.configs)

	def IsEmptyCell(self, row, col):
		return not self.configs[col].HasFieldByIndex(row)
		
	def CanGetValueAs(self,row,col,t):
		if t==wx.grid.GRID_VALUE_STRING:
			return True
		else:
			return False
			
	def CanSetValueAs(self,row,col,t):
		if t==wx.grid.GRID_VALUE_STRING:
			return True
		else:
			return False
	def GetTypeName(self, row, col):
		"""Return the name of the data type of the value in the cell"""
		field = self.configs[col].GetFieldByIndex(col)
		if field != None:
			#return wx.grid.GRID_VALUE_STRING
			return field.NativeType()
		else:
			return wx.grid.GRID_VALUE_STRING

	def GetValue(self, row, col):
		return self.configs[col].GetFieldValueByIndex(row)
		
	def GetColLabelValue(self, col):
		duplicateID = self.configs[col].GetDuplicateID()
		modified = self.configs[col].IsModified()
		label = self.configs[col].GetName()
		
		if modified:
			label="*"+label
		if len(self.names[self.configs[col].GetName()]) > 1:
			label = label+" ("+str(duplicateID)+")"
			
		return label
		
	def GetRowLabelValue(self, row):
		return self.fieldManager.GetLabel(row)
		
	def SetValue(self, row, col, value):
	
		if not self.configs[col].SetFieldValueByIndex(row,value):
			fieldType = self.fieldManager.GetFieldTypeByIndex(row)
			if fieldType.IsValidValue(value):
				self.configs[col].SetFieldByIndex(row,self.fieldManager.CreateFieldByIndex(row,value))
				
		
		self.UpdateLabel(self.configs[col])
		self.grid.Refresh()
	

