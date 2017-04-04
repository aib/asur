#!/usr/bin/python3

import markov

import random

def main():
	mc = markov.MarkovChain(random.random)
	START_OF_LINE = object()
	END_OF_LINE = object()

	with open('data.txt', 'r', encoding='utf-8') as f:
		for line in f.readlines():
			line = line.strip()

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

if __name__ == '__main__':
	main()
