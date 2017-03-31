import math
import time

class Progress:
	def __init__(self, goal, start=True):
		self._progress = 0
		self._goal = goal
		if start:
			self.start()

	def start(self):
		self._progress = 0
		self._start_time = time.monotonic()

	def advance(self, amount=1):
		self._progress += amount

	def is_done(self):
		return not (self._progress < self._goal)

	def get_progress(self):
		return self._progress

	def get_goal(self):
		return self._goal

	def get_remaining(self):
		return self._goal - self._progress

	def get_fraction(self):
		if self._goal == 0:
			return 1
		return self._progress / self._goal

	def get_elapsed(self):
		return time.monotonic() - self._start_time

	def get_progress_per_second(self):
		if self.get_elapsed() == 0:
			return 0
		return self._progress / self.get_elapsed()

	def get_eta(self):
		pps = self.get_progress_per_second()
		if pps == 0:
			return float("inf")
		return self.get_remaining() / pps

	def get_bar(self, width=50, fill="=", edges="|", space=" "):
		f = min(round(self.get_fraction() * width), width)
		s = min(width - f, width)
		l_edge = edges[0] if len(edges) >= 1 else ""
		r_edge = edges[1] if len(edges) >= 2 else l_edge
		return l_edge + (fill * f) + (space * s) + r_edge

	def get_percent(self):
		return self.get_fraction() * 100

class ProgressBar(Progress):
	def __str__(self):
		rate = self.get_progress_per_second()
		if rate > 1.0 or rate == 0:
			rate_str = "%.3f/s" % (rate,)
		else:
			rate_str = "%.3fs/" % ((1 / rate),)

		bar = "%s%3d%% ETA: %.0fs, %s" % (
			self.get_bar(width=40), self.get_percent(),
			self.get_eta(), rate_str
		)
		return bar
