import os
import pickle
import math

class RomScorer:
	def __init__(self):
		self._allwords = {}
		self._allcount = 0
		self._romwords = {}
		self._romcount = 0;
		self._processed_words = {}

	def add_words(self, words):
		for w in words:
			if w not in self._allwords:
				self._allwords[w] = 0

			self._allwords[w] += 1
			self._allcount += 1

	def add_romwords(self, words):
		for w in words:
			if w not in self._romwords:
				self._romwords[w] = 0

			self._romwords[w] += 1
			self._romcount += 1

	def process(self):
		for rw in self._romwords:
			rs = self._romwords[rw] / self._romcount

			if rw in self._allwords:
				nrs = self._allwords[rw] / self._allcount
			else:
				nrs = 1 / self._allcount

			score = math.log (rs / nrs)
			self._processed_words[rw] = score

		for nrw in self._allwords:
			if nrw not in self._processed_words:
				nrs = self._allwords[nrw] / self._allcount
				score = math.log (1 / self._allcount)
				self._processed_words[nrw] = score

	def get_words_score(self, words):
		score = 0
		for w in words:
			if w in self._processed_words:
				score += self._processed_words[w]
		return score

	def save_cache(self, filename):
		with open(filename, 'wb') as f:
			cache = { 'words': self._processed_words }
			pickle.dump(cache, f)

	def load_cache(self, filename):
		try:
			with open(filename, 'rb') as f:
				cache = pickle.load(f)
				self._processed_words = cache['words']
			return True
		except:
			return False
