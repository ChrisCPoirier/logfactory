import unittest
import logfactory
import time


class TestLogFactory(unittest.TestCase):

	def setUp(self):
		self.startTime = time.time()

	def tearDown(self):
		t = time.time() - self.startTime
		print "%s: %.3f" % (self.id(), t)

	def test_simple_log_cache_count(self):
		cur_time = time.time()
		logger = logfactory.LogFactory('/tmp/test1.log')
		logger.log('test logging ' + str(cur_time))
		logger.log('test logging ' + str(cur_time))
		logger.log('test logging 2')
		self.assertEqual(len(logger.messageCache), 2)

	def test_simple_cache_length(self):
		logger = logfactory.LogFactory('/tmp/test2.log')
		logger.lagTime = .01
		for i in xrange(0,11):
			logger.log('test logging' + str(i))

		self.assertEqual(len(logger.messageCache), 11)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestLogFactory)
	unittest.TextTestRunner(verbosity=0).run(suite)

