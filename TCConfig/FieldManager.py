from fields import *

class FieldManager:
	def __init__(self,fieldConfig):
		self.fieldLabels=list()
		self.fieldTypes = dict()
		o_count=0
		self._parse(fieldConfig)
		
	def MergeFields(self,fields):
		newfields = list(self.fieldLabels)
		if len(self.fieldLabels)==0:
			#if no Fields are in the list make one
			self.fieldLabels=fields.keys()
			for field in self.fieldLabels:
				self.fieldTypes[field]=fields[field].__class__
		else:
			#intelegetly merge the fields while attempting to preserve the original order
			keylist = list(fields.keys())
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
					self.fieldTypes[field]=fields[field].__class__
			self.fieldLabels=newfields
		
	def _parse(self,fieldConfig):	
		print 'do parse'
	def AddField(self,fieldType=ConfigFieldUnknown,fieldLabel=''):
		if fieldLabel=='':
			fieldLabel = "Other %i" % o_count
			self.o_count += 1
		
		self.fieldLabels.append(fieldLabel)
		self.fieldTypes[fieldLabel]=fieldType
		
	def HasIndex(self,index):
		if index>len(self.fieldLabels):
			return False
		else:
			return True
	def index(self, field):
		return self.fieldLabels.index(field)
	def CreateField(self,fieldLabel,value):
		if fieldLabel in self.fieldTypes:
			
			return self.fieldTypes[fieldLabel](value,fieldLabel)
		
	def CreateFieldByIndex(self,index,value):
		if index<len(self.fieldLabels):
			return self.CreateField(self.fieldLabels[index],value)
		else:
			return None
	def GetFieldTypeByIndex(self,index):
		if index<len(self.fieldLabels):
			return self[self.fieldLabels[index]]
		else:
			return None
	def GetLabel(self,index):
		return self.fieldLabels[index]
		
	def __getitem__(self,fieldLabel):
		if fieldLabel in self.fieldTypes:
			return self.fieldTypes[fieldLabel]
			
		return None
	def __len__(self):
		return len(self.fieldLabels)
		
	def __contains__(self,fieldLabel):
		return fieldLabel in self.fieldTypes
		