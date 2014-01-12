class UndoRedoManager:
	def __init__(self):
		print 'hi'
		self.undoStack=list()
		self.redoStack=list()
		self.state=list()
		
	def Do(self,id,undoAction,redoAction):
		self.state.append({'undo':undoAction,'redo':redoAction,'id':id})
		
	def PushState(self):
		self.undoStack.append(self.state)
		self.redoStack=list()
		self.state=list()
		
	
	def ClearHistory(self):
		self.undoStack=list()
		self.redoStack=list()
	def ClearHistoryByID(self,id):
		self.redoStack=list()
		for a in list(self.undoStack):
			if a['id']==id:
				self.undoStack.remove(a)
		
	def Undo(self):
		if len(self.undoStack)>0:
			state = self.undoStack.pop()
			self.redoStack.append(state)	
			for x in state: x['undo']()
	
	def Redo(self):
		if len(self.redoStack)>0:
			state = self.redoStack.pop()	
			self.undoStack.append(state)
			for x in state: x['redo']()
			
	