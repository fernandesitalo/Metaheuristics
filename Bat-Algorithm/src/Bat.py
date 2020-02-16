import copy

def dist2(a,b):
	d = 0
	for i in range(len(a)):
		d = d + (a[i]-b[i])**2
	return d

def sumBatLocation(c,d):
	print(type(c), " ++++++ " , type(d) )
	return [(c[i]+d[i]) for i in range(len(c))]

def sumBatLocationScalar(a,b):
	return [(a[i]+b) for i in range(len(a))]

class Bat():
	def __init__(self, amplitude, pulseEmissionRate, frequency, velocity, location,fitness):
		self.amplitude = amplitude
		self.pulseEmissionRate = pulseEmissionRate
		self.frequency = frequency
		self.velocity = velocity
		self.location = location
		self.fitness = fitness

	def __add__(self, other):
		result = copy.deepcopy(other)
		for dimension in range(len(result.location)):
			result.location[dimension] = result.location[dimension] + self.location[dimension]
		return result

	def __sub__(self, other):
		result = copy.deepcopy(other)
		for dimension in range(len(other.location)):
			result.location[dimension] = result.location[dimension] - self.location[dimension]
		return result

	def __lt__(self, other):
		return  (True if (self.fitness < other.fitness) else False)