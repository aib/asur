#!/usr/bin/python3

import markov

import random
import re

def main():
	mc = markov.MarkovChain(random.random)
	START_OF_LINE = object() # special "word" at the beginning of every line
	END_OF_LINE = object()   # special "word" at the end of every line

	with open('data.txt', 'r', encoding='utf-8') as f:
		for line in f.readlines():
			line = preprocess(line)
			if len(line) == 0: # ignore blank lines
				continue

			previous_word = START_OF_LINE
			for word in line.split():
				mc.add(previous_word, word)
				previous_word = word
			mc.add(previous_word, END_OF_LINE)

		mc.compile()

		for i in range(8):
			line = ""
			word = mc.get(START_OF_LINE)
			while True:
				if word == END_OF_LINE:
					break
				line += word + " "
				word = mc.get(word)

			print(line.strip())

def preprocess(line):
	# lowercase Turkish letters
	for pair in zip('ĞÜŞİÖÇIÂÎÛ', 'ğüşiöçıâîû'):
		line = line.replace(pair[0], pair[1])

	# lowercase all other letters
	line = line.lower()

	# remove accented Turkish letters
	for pair in zip('âîû', 'aıu'):
		line = line.replace(pair[0], pair[1])

	# remove apostrophes
	for char in '\'':
		line = line.replace(char, '')

	# replace everything else with a space
	line = re.sub(r'[^a-zğüşöçı]', ' ', line)

	return line

if __name__ == '__main__':
	main()
