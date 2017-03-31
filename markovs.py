import markov

import random

class Markovs:
	MC1_ALL = object()
	MC2_BEGIN = object()
	MC2_END = object()
	MC2R_END = object()
	MC2R_BEGIN = object()

	def __init__(self, filename):
		self.mc1 = markov.MarkovChain(random.random)
		self.mc2 = markov.MarkovChain(random.random)
		self.mc2r = markov.MarkovChain(random.random)
		self.process_lines_from(filename)
		self.compile()

	def process_lines_from(self, filename):
		with open(filename, 'r') as f:
			for line in f:
				line = line.strip()
				if len(line) > 0:
					self.process_line(line)

	def process_line(self, line):
		for word in line.split():
			self.mc1.add(self.MC1_ALL, word)

		prev = self.MC2_BEGIN
		for word in line.split():
			self.mc2.add(prev, word)
			prev = word
		self.mc2.add(prev, self.MC2_END)

		prev = self.MC2R_END
		for word in reversed(line.split()):
			self.mc2r.add(prev, word)
			prev = word
		self.mc2r.add(prev, self.MC2R_BEGIN)

	def compile(self):
		self.mc1.compile()
		self.mc2.compile()
		self.mc2r.compile()
