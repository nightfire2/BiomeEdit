from ConfigFieldBase import ConfigFieldBase

class ConfigFieldFunc(ConfigFieldBase):
	linePattern = r"^([a-zA-Z0-9_]+)(\(.*\))"
	valuePattern= r"^([a-zA-Z0-9_]+)(\(.*\))"
	def GetValue(self):
		return "%s%s" % (self.label,self.value)
	def GetLabel(self):
		if self.optionalLabel!=None:
			return self.optionalLabel
		else:
			return self.label
	def SetValue(self,value):
		if value.strip()!="":	
			if self.IsValidValue(value):
				self.Parse(value)
			else:
				self.label=""
				self.value=""
		else:
			self.label=""
			self.value=""	
	
	def __str__(self):
		return "%s%s" % (self.label,self.value)