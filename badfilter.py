import badwords

import sys

bwf = badwords.BadWordChecker('badwords.txt')

with open(sys.argv[1], 'r') as inf:
	with open(sys.argv[2], 'w') as outf:
		def _process_poem(pstr):
			if bwf.check_words(pstr.split()):
				print(pstr)
				return
			print(pstr, file=outf)

		pstr = ''
		for iline in inf:
			if len(iline) <= 1:
				_process_poem(pstr)
				pstr = ''
			else:
				pstr += iline
