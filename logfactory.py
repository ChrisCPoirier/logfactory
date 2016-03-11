import time


class LogFactory:
	def __init__(self, location, log_type='file'):
		self.messageCache = {}
		self.logCounter = 0
		self.lagTime = 1
		self.cleanRatio = 1000 
		self.log_type = log_type
		self.writer = None
		self.location = location

		if self.log_type == 'web':
			self.writer = self.WebWriter(self.location)
		elif self.log_type == 'file':
			self.writer = self.FileWriter(self.location)
		else:
			print "log type of " + log_type + " not supported!!!"

	def log(self, message, message_key=None):
		cur_time = time.time()
		if not message_key:
			message_key = message

		record = self.messageCache.get(message_key, None)
		if not record or cur_time - record > self.lagTime:
			self.writer.write(time.strftime('%Y-%m-%d %H:%M:%S') + " " + message)
			self.messageCache[message_key] = cur_time

			self.logCounter += 1
			if self.logCounter > self.cleanRatio:
				self.clean()

	def clean(self):
		"""
		over time the cache may get very large.
		This procedure is designed to move all valid entries
		into a new dictionary and then assign self._msCache to 
		the new dictionary.
		"""
		cur_time = time.time()
		d = {}
		for key, t in self.messageCache.iteritems():
			if cur_time - t < self.lagTime:
				d[key] = t

		self.messageCache = d
		self.logCounter = 0

	class FileWriter:
		def __init__(self, log_location):
			self.file = None
			self.logLocation = log_location

		def openfile(self):
			self.file = open(self.logLocation, 'w', 1)

		def write(self, message):
			if not self.file:
				self.openfile()

			self.file.write(message + '\n')

	class WebWriter:
		def __init__(self, url_location):
			self.urlLocation = url_location

		def write(self, message):
			print "not yet implemented!!!" \
				"\nYour message is " + message + "\nYour url is " + self.urlLocation
			pass
