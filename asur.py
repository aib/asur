#!/usr/bin/python3

import badwords
import dupfinder
import generators
import markovs
import progress
import romscore
import score
import strutil

import locale
import os
import random
import re
import sys
import time

def _process_romvectors(poemdir, romlines, cachefile):
	romscorer = romscore.RomScorer()
	if romscorer.load_cache(cachefile):
		print("Loaded %d words in romantism vector cache" % (len(romscorer._processed_words,)))
	else:
		n = 0
		for filename in os.listdir(poemdir):
			path = os.path.join(poemdir, filename)
			with open(path, 'r', encoding='utf-8') as f:
				words = f.read().split()
				romscorer.add_words(words)
			n += 1
			print("Processed poem %d" % (n,))

		with open(romlines, 'r', encoding='utf-8') as f:
			n = 0
			for line in f:
				line = line.strip()
				if len(line) > 0:
					romscorer.add_romwords(line.split())
				n += 1
				print("Processed line %d" % (n,))

		romscorer.process()
		romscorer.save_cache(cachefile)
	return romscorer

def _process_poems(dirname, cachefile):
	scorer = score.Scorer()
	if scorer.load_cache(cachefile):
		print("Loaded %d words from cache" % (len(scorer._words),))
	else:
		n = 0
		for filename in os.listdir(dirname):
			path = os.path.join(dirname, filename)
			with open(path, 'r', encoding='utf-8') as f:
				words = f.read().split()
				scorer.add_words(words)
			n += 1
			print("Processed poem %d" % (n,))
		scorer.save_cache(cachefile)
		print("Saved %d words to cache" % (len(scorer._words),))
	return scorer

def syllable_count(min_syllable_count, max_syllable_count=None):
	if max_syllable_count is None:
		max_syllable_count = min_syllable_count
	return random.randint(min_syllable_count, max_syllable_count)

def generate_poem(rhyme_markovs, rhyme_type, rhyme_length,min_syllable_count,max_syllable_count):
	def _get_non_rhyming_line(markovs):
		return generators.get_begin_line(markovs, syllable_count(min_syllable_count,max_syllable_count))

	def _get_rhyming_line(markovs, rhyme):
		return generators.get_end_reverse_with_rhyme(markovs, syllable_count(min_syllable_count,max_syllable_count), rhyme)

	poem = []
	rhymes = {}
	for i in range(len(rhyme_type)):
		rhyme = rhyme_type[i]
		mvs = rhyme_markovs[i]

		if rhyme == ' ':
			line = ""
		elif rhyme not in rhymes:
			line = _get_non_rhyming_line(mvs)
			rhymes[rhyme] = strutil.last_n_letters(line, rhyme_length)
		else:
			line = _get_rhyming_line(mvs, rhymes[rhyme])

		poem.append(line.strip())

	return poem

def main():
	if len(sys.argv) < 2:
		print("Usage:\n\tasur N [outfile]\n")
		sys.exit(2)
	else:
		poems_to_generate = int(sys.argv[1])

	if len(sys.argv) >= 3:
		outfile = open(sys.argv[2], 'w')
	else:
		outfile = sys.stdout

	verbose = False

	print("Processing asksozleri romantism vectors...")
	romscorer_as = _process_romvectors('siirVeriTabani', 'asksozleri.txt', 'romscorer_as.cache')
	print("Processing asksozleri lines...")
	as_markovs = markovs.Markovs('asksozleri.txt')
	print("Bad words checker...")
	bwf = badwords.BadWordChecker('badwords.txt')
	print("Generating poems...")

	prog = progress.ProgressBar(poems_to_generate)

	min_syllable_count=5
	max_syllable_count=12
	max_poem_length=10000
	rom_score_limit=0
	rhyme_types = ['aaba']
	rhyme_markovs = list(map(lambda g: as_markovs, 'aaaa'))

	while not prog.is_done():
		print(prog)
		try:
			rhyme_type = random.choice(rhyme_types)
			rhyme_length = random.randint(2, 4)
			poem = generate_poem(rhyme_markovs, rhyme_type, rhyme_length,min_syllable_count,max_syllable_count)
			poem_str = "\n".join(poem)

			if len(poem_str) > max_poem_length:
				if verbose:
					print("len check failed")
				continue

			is_bad = bwf.check_words(strutil.postprocess(poem_str).split())
			if is_bad:
				if verbose:
					print("badword check failed")
				continue

			romscore_as = romscorer_as.get_words_score(poem_str.split())
			if romscore_as < rom_score_limit:
				if verbose:
					print("romscore_as check failed")
				continue

			poem = map(strutil.postprocess, poem)

			print("\n".join(poem), file=outfile)
			print("------------------------------------------", file=outfile)
			outfile.flush()
		except generators.TookTooLong:
			if verbose:
				print("generator took too long")
			continue

		prog.advance()

	print("Elapsed", prog.get_elapsed())

	if outfile != sys.stdout:
		outfile.close()

if __name__ == '__main__':
	main()
