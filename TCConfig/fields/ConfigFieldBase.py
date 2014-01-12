import re
import wx
import wx.grid
class ConfigFieldBase(object):
	linePattern="Invalid"
	valuePattern="Invalid"
	def __init__(self,lineData,optionalLabel=None):
		self.optionalLabel = optionalLabel
		self.Parse(lineData)
	
	@classmethod
	def IsValidLine(self,line):
		lineparts = re.match(self.linePattern,line)
		if lineparts != None:
			return True
		else:
			return False	
	@classmethod
	def IsValidValue(self,value):
		valueParts = re.match(self.valuePattern,value)
		if valueParts !=None:
			return True
		else:
			return False
		
		
	@classmethod	
	def GetIdentifier(self,line):
		lineparts = re.match(self.linePattern,line)
		if lineparts != None:
			return lineparts.group(1)
		else:
			return ""
			
	
	def SetValue(self,value):
		self.value=value
	
	def GetLabel(self):
		return self.label
	def GetValue(self):
		return self.value
		
	def Parse(self,line):
		lineparts = re.match(self.linePattern,line)
		if lineparts != None:
			self.label=lineparts.group(1)
			self.value = lineparts.group(2)
			return True
		else:
			return False
	def NativeType(self):
		return wx.grid.GRID_VALUE_STRING
