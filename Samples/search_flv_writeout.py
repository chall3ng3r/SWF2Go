import socket
import sys
import os
import os.path

class SearchFLV:
	""" Seaches Video dirs on C: and E: for FLV video and saves list in Flash Lite readable data file."""
	def __init__(self):
		"Setup script path and debug log."
		self.app_path = sys.argv[0].replace(u'default.py', u'')
		self.log_path = self.app_path + u'debug.log'
		if os.path.isfile(self.log_path):
			os.remove(self.log_path)

	def log(self, mesg):
		"Writes the debug.log file"
		mesg = mesg + u'\n'
		print mesg
		f = open(self.log_path, 'a+')
		f.write(mesg)
		f.close()

	def run(self):
		"Start the search."
		
		# set waiting status code in datafile
		datafile = open(self.app_path + u'datafile.txt', 'w')
		datafile.write(u'&status=100')
		datafile.close()
		
		# get list of files in video folder
		files = self.getVideos("c:/Data/Videos")
		if os.path.exists("e:/Videos"):
			files.extend(self.getVideos("e:/Videos"))
		strTemp = (u'&status=200&count=%d' % len(files))
		
		i = 0
		for f in files:
			i = i + 1
			strTemp += (u'&file%d=' % i) + f

		# write files in datafile
		datafile = open(self.app_path + u'datafile.txt', 'w')
		datafile.write(strTemp)
		datafile.close()

	def getVideos(self, searchPath):
		"Find FLV files in path"
		
		self.fileList = []
		
		#Enumerate the entries in the tree
		#tree = os.walk(path)
		#for directory in tree:
		#    self.searchDirectory(directory)
		files = os.listdir(searchPath)
		self.log(u'\n'.join(files))
		for f in files:
		    #self.searchDirectory(directory)
		    if f.endswith(u'.flv'):
		    	self.log(u'Adding ' + searchPath + "/" + f)
		    	self.fileList.append(searchPath + "/" + f)
		    
		return self.fileList

	def addFiles(self, dirList, dirPath):
		for file in dirList:
			if file.endswith('.flv'):
				self.log("Adding " + dirPath + "/" + file)
				self.fileList.append(dirPath + "/" + file)

	def searchDirectory(self, dirEntry):
		self.log("Searching files in " + dirEntry[0])
		self.addFiles(dirEntry[2], dirEntry[0])

if __name__ == '__main__':
	SearchFLV().run()