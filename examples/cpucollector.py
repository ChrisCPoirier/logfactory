import psutil
import logfactory


class CpuCollector:
	
	def __init__(self):
		self.interval = 0.1

	def get_percentages(self):
		cpu_percents = psutil.cpu_percent(interval=self.interval, percpu=True)
		result = []
		for i in xrange(0, len(cpu_percents)):
			result.append(["CPU" + str(i), "Cpu " + str(i) + " at " + str(cpu_percents[i]) + " % utilization"])

		return result

	def run(self):
		log = logfactory.LogFactory('/tmp/cpu.log')
		while True:
			values = self.get_percentages()
			for val in values:
				print val[0], val[1]
				log.log(val[1], val[0])


if __name__ == '__main__':
	collector = CpuCollector()
	collector.run()
