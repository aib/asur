import re

TR_UPPER = 'ĞÜŞİÖÇIÂ'
TR_LOWER = 'ğüşiöçıâ'
LETTERS = 'abcçdefgğhıijklmnoöpqrsştuüvwxyz' + 'ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜVWXYZ'
VOWELS = 'aeıioöuüAEIİOÖUÜ'
POSTPROCESS_ALLOWED = LETTERS + '0123456789' + 'âîû'

def lower(word):
	for pair in zip(TR_UPPER, TR_LOWER):
		word = word.replace(pair[0], pair[1])
	return word.lower()

def upper(word):
	for pair in zip(TR_LOWER, TR_UPPER):
		word = word.replace(pair[0], pair[1])
	return word.upper()

def count_syllables(word):
	return len(re.findall('[' + VOWELS + ']', word))

def last_n_letters(line, n):
	letters = ""
	for c in reversed(line):
		if c in LETTERS:
			letters = c + letters
			n -= 1
			if n <= 0:
				break
	return letters

def postprocess(line):
	line = lower(line)
	line = line.replace('\'', '')
	nline = ''
	for c in line:
		if c in POSTPROCESS_ALLOWED:
			nline += c
		else:
			nline += ' '
	return re.sub(r'\s+', ' ', nline).strip()
