import socket
import sys
import os
import os.path

class PyServer:
	""" Searches the Video dirs of C: and E: and returns list of files."""
	def __init__(self):
		"Binds the server to the given port."
		self.log_path = sys.argv[0]
		self.log_path = self.log_path.replace(u'default.py', u'debug.log')
		if os.path.isfile(self.log_path):
			os.remove(self.log_path)

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('127.0.0.1',2048))
		#Queue up to five requests before turning clients away.
		self.socket.listen(5)
		self.running = True

	def log(self, mesg):
		"Writes the debug.log file"
		mesg = mesg + u'\n'
		print mesg
		f = open(self.log_path, 'a+')
		f.write(mesg)
		f.close()

	def run(self):
		"Handles incoming requests forever."
		while self.running:
			self.log(u'>> started. waiting...')
			request, client_address = self.socket.accept()
			self.log(u'>> new client: %s:%d' % (client_address[0], client_address[1]))
			while True:
				try:
					#data = input.read()
					data = request.recv(1024).replace(u'\0', u'')
					self.log(u'<< client:\n%s' % data)
					
					if data.find(u'policy-file-request') >= 0:
						text_tosend = """<cross-domain-policy><allow-access-from domain="*" to-ports="2048" /></cross-domain-policy>\0"""
						self.log(u'>> sending:\n%s' % text_tosend)
						request.send(text_tosend)
						request.shutdown(2)
						continue
					elif data.startswith(u'close'):
						self.log(u'<< close request...')
						request.shutdown(2) #Shut down both reads and writes.
						self.log(u'>> server closed.')
						self.running = False
						break
					elif data.startswith(u'getVideos'):
						self.log(u'<< getVideos request')
						text_tosend = u'flvs|' + u';'.join(self.getVideos())
						self.log(u'>> Sending:\n%s' % text_tosend)
						request.send(text_tosend + u'\0')
					else:
						text_tosend = u'echo: %s\0' % data
						self.log(u'>> sending:\n%s' % text_tosend)
						request.send(text_tosend)
				except socket.error:
					#Most likely the client disconnected.
					self.log(u'<< client disconnected')
					break

	def getVideos(self):
		"Send list of FLV files to iPlay"
		
		self.fileList = []
		path = "c:/Data/Videos"
		
		#Enumerate the entries in the tree
		#tree = os.walk(path)
		#for directory in tree:
		#    self.searchDirectory(directory)
		files = os.listdir(path)
		self.log(u'\n'.join(files))
		for f in files:
		    #self.searchDirectory(directory)
		    if f.endswith(u'.flv'):
		    	self.log(u'Adding ' + path + "/" + f)
		    	self.fileList.append(path + "/" + f)
		    
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
	PyServer().run()