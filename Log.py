class LogObject:
	#this is an comment
	def __init__(self,name):
		self.name = name
		f = open(self.name+".txt","w")
		f.close()
	def writeToLog(self,string):
		f = open(self.name+".txt","a")
		f.write(string)
		f.close()