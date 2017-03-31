import strutil

class BadWordChecker:
	def __init__(self, filename):
		self._badwords = set()
		with open(filename, 'r') as f:
			for line in f:
				self._badwords.add(strutil.lower(line.strip()))

	def check_words(self, words):
		for word in words:
			for bw in self._badwords:
				if word.startswith(bw):
					return True
		return False
