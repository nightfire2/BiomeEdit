from ConfigFieldBase import ConfigFieldBase
import wx
import wx.grid
class ConfigFieldAttribute(ConfigFieldBase):
	linePattern=r"^([a-zA-Z0-9_]+)\:(.*)"
	valuePattern=r"^()(.*)"
	def Parse(self,line):
		if self.optionalLabel != None:
			self.label = self.optionalLabel
			self.value=line
		else:
			super(ConfigFieldAttribute,self).Parse(line)
			
	def __str__(self):
		return "%s:%s"% (self.label, self.value)
		
		
class ConfigFieldText(ConfigFieldAttribute):
	def NativeType(self):
		return wx.grid.GRID_VALUE_STRING