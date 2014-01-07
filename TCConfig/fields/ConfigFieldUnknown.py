from ConfigFieldBase import ConfigFieldBase

class ConfigFieldUnknown(ConfigFieldBase):
	linePattern = r"^()(.*)"
	valuePattern = r"^()(.*)"
	def SetValue(self ,value):
		self.Parse(value)
	def GetValue(self):
		return self.value
	def __str__(self):
		return self.value