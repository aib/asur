import os
import pickle

class Scorer:
	def __init__(self):
		self._words = {}
		self._pairs = {}

	def _sort(self, w1, w2):
		if w1 < w2:
			return (w1, w2)
		else:
			return (w2, w1)

	def _add_word(self, w):
		if w not in self._words:
			self._words[w] = 0

		self._words[w] += 1

	def _add_pair(self, w1, w2):
		(w1, w2) = self._sort(w1, w2)

		if w1 not in self._pairs:
			self._pairs[w1] = {}

		if w2 not in self._pairs[w1]:
			self._pairs[w1][w2] = 0

		self._pairs[w1][w2] += 1

	def _get_word_count(self, w):
		if w not in self._words:
			return 0

		return self._words[w]

	def _get_pair_count(self, w1, w2):
		(w1, w2) = self._sort(w1, w2)

		if w1 not in self._pairs:
			return 0

		if w2 not in self._pairs[w1]:
			return 0

		return self._pairs[w1][w2]

	def add_words(self, words):
		words = list(set(words))

		for w in words:
			self._add_word(w)

		for i in range(0, len(words)-1):
			for j in range(i+1, len(words)):
				self._add_pair(words[i], words[j])

	def score_pair(self, w1, w2):
		c1 = self._get_word_count(w1)
		c2 = self._get_word_count(w2)

		if c1 == 0 or c2 == 0:
			return 0

		return self._get_pair_count(w1, w2) / (c1 * c2)

	def score_words(self, words):
		score = 0
		words = list(set(words))

		for i in range(0, len(words)-1):
			for j in range(i+1, len(words)):
				score += self.score_pair(words[i], words[j])
		score /= len(words)
		return score

	def save_cache(self, filename):
		with open(filename, 'wb') as f:
			cache = { 'words': self._words, 'pairs': self._pairs }
			pickle.dump(cache, f)

	def load_cache(self, filename):
		try:
			with open(filename, 'rb') as f:
				cache = pickle.load(f)
				self._words = cache['words']
				self._pairs = cache['pairs']
			return True
		except:
			return False
