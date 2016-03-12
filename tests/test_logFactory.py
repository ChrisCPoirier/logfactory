import unittest
from logfactory import LogFactory
import time


class TestLogFactory(unittest.TestCase):

	def setUp(self):
		self.startTime = time.time()

	def tearDown(self):
		t = time.time() - self.startTime
		print "%s: %.3f" % (self.id(), t)

	def test_simple_log_cache_count(self):
		"""
		test length of cache with repeats and non repeats
		expected result 2
		"""
		cur_time = time.time()
		logger = LogFactory('/tmp/test1.log')
		logger.log('test logging ' + str(cur_time))
		logger.log('test logging ' + str(cur_time))
		logger.log('test logging 2')
		self.assertEqual(len(logger.messageCache), 2)

	def test_simple_log_cache_with_key(self):
		"""
		test length of cache with repeats and non repeats using identical key
		expected result 1
		"""
		cur_time = time.time()
		logger = LogFactory('/tmp/test1.log')
		logger.log('test logging ' + str(cur_time), 'x')
		logger.log('test logging ' + str(cur_time), 'x')
		logger.log('test logging 2', 'x')
		self.assertEqual(len(logger.messageCache), 1)

	def test_simple_cache_length(self):
		"""
		test length of cache based on constant changing log names
		expected result: 11
		"""
		logger = LogFactory('/tmp/test2.log')
		logger.lagTime = .01
		for i in xrange(0, 11):
			logger.log('test logging' + str(i))

		self.assertEqual(len(logger.messageCache), 11)

	def test_repeated_insert_log_size(self):
		"""
		testing that the intended amount of messages are written to file.
		expecting 4 messages to be logged to file
		"""
		cur_time = time.time()
		myfile = '/tmp/test_repeated_insert_log_size.log'
		logger = LogFactory(myfile)
		logger.lagTime = 0.1
		while time.time() - cur_time < 0.4:
			logger.log('test logging')

		self.assertEqual(sum(1 for line in open(myfile)), 4)

	def test_simple_wrong_log_type(self):
		try:
			LogFactory('/tmp/test_wrong_log_type.log', 'xfile')
		except ValueError as e:
			self.assertEqual('log type of xfile not supported!!!', e.message)
		else:
			self.fail("unexpected exception")


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestLogFactory)
	unittest.TextTestRunner(verbosity=0).run(suite)

