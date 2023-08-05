class Writer:
	def __init__(self, file):
		self.__file = file
		
	def write(self, text):
		msg = text
		text = open(self.__file.path(), 'a')
		text.write(msg)
		text.close()