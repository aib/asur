import markovs
import strutil

class TookTooLong(Exception):
	pass

def get_word_line(markovs, c):
	while True:
		word = markovs.mc1.get(markovs.MC1_ALL)
		line = word
		while strutil.count_syllables(line) < c:
			word = markovs.mc2.get(word)
			if word is None or word == markovs.MC2_END:
				break
			line = line + " " + word
		if strutil.count_syllables(line) == c:
			return line

def get_begin_line(markovs, c):
	while True:
		word = markovs.MC2_BEGIN
		line = ""
		while strutil.count_syllables(line) < c:
			word = markovs.mc2.get(word)
			if word is None or word == markovs.MC2_END:
				break
			line = line + " " + word
		if strutil.count_syllables(line) == c:
			return line

def get_end_line(markovs, c):
	while True:
		word = markovs.mc1.get(markovs.MC1_ALL)
		line = word
		while True:
			word = markovs.mc2.get(word)
			if word is None:
				line = ""
				break
			if word == markovs.MC2_END:
				break
			line = line + " " + word
		if strutil.count_syllables(line) == c:
			return line

def get_begin_end_line(markovs, c):
	while True:
		word = markovs.MC2_BEGIN
		line = ""
		while True:
			word = markovs.mc2.get(word)
			if word is None:
				line = ""
				break
			if word == markovs.MC2_END:
				break
			line = line + " " + word
		if strutil.count_syllables(line) == c:
			return line

def get_end_reverse_line(markovs, c):
	while True:
		word = markovs.MC2R_END
		line = ""
		while strutil.count_syllables(line) < c:
			word = markovs.mc2r.get(word)
			if word is None or word == markovs.MC2R_BEGIN:
				break
			line = word + " " + line
		if strutil.count_syllables(line) == c:
			return line

def get_end_reverse_with_rhyme(markovs, c, rhyme):
	while True:
		lwtries = 0
		while True:
			endword = markovs.mc2r.get(markovs.MC2R_END)
			if strutil.last_n_letters(endword, len(rhyme)) == rhyme:
				break
			lwtries += 1
			if lwtries >= 1000:
				raise TookTooLong()

		word = endword
		line = endword
		while strutil.count_syllables(line) < c:
			word = markovs.mc2r.get(word)
			if word is None or word == markovs.MC2R_BEGIN:
				break
			line = word + " " + line
		if strutil.count_syllables(line) == c:
			return line
