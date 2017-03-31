import itertools

class Dupfinder:
	def __init__(self, line_file):
		with open(line_file, 'r') as f:
			self._lines = list(enumerate(f.readlines()))

	def is_dup(self, lines):
		all_lines = list(map(lambda l: self._get_indices(l), lines))
		for t in itertools.product(*all_lines):
			dist = max(t) - min(t)
			if dist <= 2:
				return True
		return False

	def _get_indices(self, line):
		answer = []
		for (num, dbline) in self._lines:
			if line in dbline:
				answer.append(num)
		return answer
