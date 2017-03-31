class MarkovChain:
	def __init__(self, rand01):
		self._rand01 = rand01
		self._inputs = {}
		self._compiled = None

	def add(self, inp, outp, instances=1):
		if inp not in self._inputs:
			self._inputs[inp] = {}

		if outp not in self._inputs[inp]:
			self._inputs[inp][outp] = 0

		self._inputs[inp][outp] += 1

	def compile(self):
		self._compiled = {}
		for inp in self._inputs:
			compiled = []
			outputs = self._inputs[inp]

			cumulative = 0
			for outp in outputs:
				cumulative += outputs[outp]
				compiled.append((outp, cumulative))

			# cumulative = total number of output items now. Normalize.
			compiled = list(map(lambda co: (co[0], co[1] / cumulative), compiled))

			self._compiled[inp] = compiled

	def get(self, inp):
		if inp not in self._compiled:
			return None

		r = self._rand01()
		for co in self._compiled[inp]:
			if r <= co[1]:
				return co[0]

		# Above loop should not fall through if r <= 1
		return RuntimeError("Choice variable greater than largest cumulative probability. Does the generator return values >1?")
