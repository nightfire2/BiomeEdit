import wx
import wx.xrc
import wx.aui
import wx.grid
import collections
from fields import *
from UndoRedoManager import UndoRedoManager

class TCConfig(wx.ScrolledWindow):
	UniqueIDCounter=0
	
	def __init__(self,fileData,filePath,name,fieldManager,parent):
		super(TCConfig,self).__init__(parent.tab_container, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
		self.parent=parent
		TCConfig.UniqueIDCounter += 1
		self.uniqueID= TCConfig.UniqueIDCounter
		self.modified=False
		self.labelGroup = {'Sapling':0,'#Resources Queue':0,'#Other':0}
		self.SetName(name)
		
		self.fieldManager=fieldManager
		self.filePath=filePath
		self.SetFilePath(filePath)
		self._ParseData(fileData)
		self.fieldManager.MergeFields(self.fields)
		
	def GetUniqueID(self):
		return self.uniqueID
		
	def SetFilePath(self,filePath):
		self.filePath=filePath
	def GetFilePath(self):
		return self.filePath
	def CreateField(self,line):
		field = None
		label = ""
		if ConfigFieldAttribute.IsValidLine(line):
			#we have an attribute
			label = ConfigFieldAttribute.GetIdentifier(line)
			if label in self.fieldManager:
				field = self.fieldManager[label](line)
			else:
				#if its not already in the field list just default to text
				field = ConfigFieldText(line)
		elif ConfigFieldFunc.IsValidLine(line):
			#we have function
			identifier = ConfigFieldFunc.GetIdentifier(line)
			labelCounter = 0
			label = ""
			if identifier in self.labelGroup:
				self.labelGroup[identifier] += 1
				label = "{0} {1}".format(identifier,self.labelGroup[identifier])
			else:
				self.labelGroup['#Resources Queue']+=1
				label = "Resources Queue {0}".format(self.labelGroup['#Resources Queue'])
			field = ConfigFieldFunc(line,label)
		
		return field
			
	def _ParseData(self,rawFileData):
		fileLines = rawFileData.splitlines()
		self.fileData=list()
		self.fields =collections.OrderedDict()
		for line in fileLines:
			#ignore empty lines
			if len(line.strip()) == 0:
				self.fileData.append(line)
				continue
			#ignore comments
			if line.strip()[0]=='#':
				self.fileData.append(line)
				continue
			#groups with a pound in front of them corispond to multiple possible things
			
			field = self.CreateField(line)
			if field != None:
				self.fields[field.GetLabel()] = field
				self.fileData.append(field)
			else:
			#we have something else
				self.labelGroup['#Other']+=1
				field = ConfigFieldUnknown(line)
				label ="{0} {1}".format("Other",self.labelGroup['#Other'])
				self.fields[label]=field
				self.fileData.append(field)
				
			
		
	def __str__(self):
		#generate final file representation for writing
		return '\n'.join(map(lambda line: str(line),self.fileData))
	def SetDuplicateID(self,num):
		self.duplicateID=num
	def GetDuplicateID(self):
		return self.duplicateID
	
	def index(self,field):
		return self.fieldManager.index(field)
	def GetField(self,fieldLabel):
		if fieldLabel in self.fields:
			return self.fields[fieldLabel]
		else:
			return None
	def GetFieldByIndex(self,index):
		if self.HasIndex(index):
			return self.GetField(self.fieldManager.GetLabel(index))
	def IsModified(self):
		return self.modified
	def SetModified(self,modified=True):
		if self.modified != modified:
			self.modified=modified
			return True
		return False
			#if self.modified:
			#	print ' modified'
				#set row and tab labels to reflect the updated status
			#else:
			#	print 'unmodified'
				#unset row and tab labels to reflect the update status
	
	def SetFieldByIndex(self,index,value):
	
		if len(self.fieldManager)>index:
			self.SetField(self.fieldManager.GetLabel(index),value)
			return True
		else:
			return False
	
	def _setRawFD(self,index,field):
		self.fileData[oldIndex]=field
	def _setRawF(self,fieldLabel,field):
		self.fields[fieldLabel]=field
		
	def SetField(self,fieldLabel,value):
		
		if fieldLabel in self.fieldManager:
			if self.fieldManager[fieldLabel]==type(value):
			
				contained = fieldLabel in self.fields
				if contained:
					oldfield = self.fields[fieldLabel]
					
					oldIndex = self.fileData.index(oldfield)
					#self.fileData[oldIndex]=""
					self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self._setRawFD(oldIndex,oldfield),lambda:self.setRawFD(oldIndex,value))
					self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self._setRawF(fieldLabel,oldfield),lambda :self._setRawF(fieldLabel,value))
					
				else:
					self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self.fileData.pop(),lambda:self.fileData.append(value))
					self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self.fields.pop(fieldLabel,None),lambda:self._setRawF(fieldLabel,value))
					self.fileData.append(value)
				
				self.fields[fieldLabel]=value				
				modified = self.modified
				if self.SetModified(True):
					self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self.SetModified(False),lambda:self.SetModified(True))
		
				self.parent.activeUndoRedo.PushState()
				return True
	
			
		return False
			
	
	def ClearField(self,fieldLabel):
		field = self.fields.pop(fieldLabel)
		index = self.fileData.index(field)
		self.fileData.splice(index,1)
		self.SetModified(True)
		
	def HasFieldByIndex(self,index):
		if index > len(self.fieldManager):
			if self.fieldManger.GetLabel(index) in self.fields:
				return True
			else:
				return False
		else:
			return False
	def HasIndex(self,index):
		if index<len(self.fieldManager):	
			if self.fieldManager.GetLabel(index) in self.fields:
				return True
		return False
				
	def HasField(self,field):
		return field in self.fields
		
	def GetFieldValue(self,fieldLabel):
		if fieldLabel in self.fields:
			return self.fields[fieldLabel].GetValue()
		else:
			return ""
		
		
	def GetFieldValueByIndex(self,index):
		if self.HasIndex(index):
			return self.GetFieldValue(self.fieldManager.GetLabel(index))
		else:
			return ""
	def _SetRawFV(self,fieldLabel,value):
		self.fields[fieldLabel].SetValue(value)
	def SetFieldValue(self,fieldLabel,value):
		if fieldLabel in self.fields:
			if self.fieldManager[fieldLabel]==type(value):					
				field = self.fields[fieldLabel]
				oldValue=field.GetValue()
				field.SetValue(value)
				if oldValue.strip()!=value.strip():
					
					self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self._SetRawFV(fieldLabel,oldValue),lambda:self._SetRawFV(fieldLabel,value))
					if self.SetModified(True):
						self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self.SetModified(False),lambda:self.SetModified(True))
					self.parent.activeUndoRedo.PushState() 
				return True
				
		return False
		
			
	def _SetRawFVByIndex(self,index,value):
		self.fields[self.fieldManager.GetLabel(index)].SetValue(value)
	def SetFieldValueByIndex(self,index,value):
		if self.HasIndex(index):
			field = self.fields[self.fieldManager.GetLabel(index)]
			oldValue = field.GetValue()
			field.SetValue(value)
			if oldValue.strip()!=value.strip():
				self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self._SetRawFVByIndex(index,oldValue),lambda:self._SetRawFVByIndex(index,value))
				if self.SetModified(True):
					self.parent.activeUndoRedo.Do(self.GetUniqueID(),lambda:self.SetModified(False),lambda:self.SetModified(True))
				self.parent.activeUndoRedo.PushState() 
				
				
			return True
		
			
		return False
				