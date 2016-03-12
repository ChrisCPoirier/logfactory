import time


class LogFactory(object):
	"""This factory logs new messages and repeat messages if they have not been seen for some frequency.

	If the class has public attributes, they may be documented here
	in an ``Attributes`` section and follow the same formatting as a
	function's ``Args`` section. Alternatively, attributes may be documented
	inline with the attribute's declaration (see __init__ method below).

	Attributes
	----------
	location : string
		location of log file. If writing to a path provided a path and file name.
		If writing to a url provide url.
		EXAMPLE:
			file = /tmp/temp.log
			url = www.example.com/api

	log_type : optional[string]
		are we writing to file or url? default=file
	lagTime : optional[float]
		time in seconds to wait before logging a message again if it has already been received.
	cleanRatio : Optional[int]
		how often do you want to clean the cache. this variable is used to compare against amount of records logged.
		Example: if cleanRatio is set to 100 and 100 messages are logged the clean operation will be executed.
	"""

	def __init__(self, location, log_type='file'):
		self.location = location
		self.log_type = log_type
		self.lagTime = 1
		self.cleanRatio = 1000
		self.writer = self.writer_factory()
		self.logCounter = 0
		self.messageCache = {}

	def log(self, message, message_key=None):
		"""logs the designated message. Uses message_key versus log entry time to determine if message is valid.

		Parameters
		----------
		message: string
			the message you want to log
		message_key optional[string] defaults to None
			an optional key can be passed if you want to exclude messages based on key instead of message.
			if no message_key is passed message is used instead

		Returns
		-------
		bool
		True if message logged, False otherwise.

		"""
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

			return True
		return False

	def clean(self):
		"""
		over time the cache may get very large.
		This procedure is designed to move all valid entries
		into a new dictionary and then assign cache to
		the new dictionary.
		"""
		cur_time = time.time()
		d = {}
		for key, t in self.messageCache.iteritems():
			if cur_time - t < self.lagTime:
				d[key] = t

		self.messageCache = d
		self.logCounter = 0

	def writer_factory(self):
		"""
		looks at the location property and returns the appropriate writer class

		Returns
		-------
		the appropriate writer subclass
		"""
		if self.log_type == 'url':
			return self.WebWriter(self.location)
		elif self.log_type == 'file':
			return self.FileWriter(self.location)
		elif self.log_type == 'memory':
			return self.MemoryWriter(self.location)
		else:
			raise ValueError("log type of " + self.log_type + " not supported!!!")

	class FileWriter:
		"""This is designed to write messages to a file.

		Attributes
		----------
		log_location : string
			location of file to write.
			EXAMPLE:
				file = /tmp/temp.log
		"""
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
		"""This is designed to write messages to a file.

		Attributes
		----------
		url_location : string
			location of file to write.
			EXAMPLE:
				url = www.example.com/url
		"""
		def __init__(self, url_location):
			self.urlLocation = url_location

		def write(self, message):
			print "not yet implemented!!!" \
				"\nYour message is " + message + "\nYour url is " + self.urlLocation
			pass

	class MemoryWriter:
		"""This is designed to write messages to memory.
		"""
		def __init__(self):
			self.log = []
			self.logSize = 1000

		def write(self, message):
			if len(self.log) == self.logSize:
				# TODO: review speed
				self.log.pop(0)

			self.log.append(message)

		def read(self):
			return self.log

		def delete(self):
			self.log = []