import dupfinder

import collections

df = dupfinder.Dupfinder('asksozleri.txt')

poems = []
count = 0
with open('all.txt', 'r') as f:
	plines = 0
	poem = {}
	for line in f:
		if plines == 0:
			scores = line.split()
			ss = [ float(scores[0]), float(scores[1]), scores[3] ]
			poem = { 'score': ss, 'text': "" }
		elif plines == 4:
			pl = poem['text'].split('\n')[0:3]
			poem['is_dup'] = df.is_dup(pl)
			if poem['is_dup']:
				print(poem['text'])
			poems.append(poem)
			plines = 0
			poem = {}
			count += 1
			print(count)
			continue
		else:
			poem['text'] += line
	
		plines += 1

good = []
with open('good.txt', 'r') as f:
	for line in f:
		good.append(int(line))

bad = []
with open('bad.txt', 'r') as f:
	for line in f:
		bad.append(int(line))

s0g = 0
s1g = 0
gtypes = []
count = 0
for g in good:
	s0g += poems[g]['score'][0]
	s1g += poems[g]['score'][1]
	gtypes.append(poems[g]['score'][2])
	count += 1
s0g /= count
s1g /= count

s0b = 0
s1b = 0
btypes = []
count = 0
for b in bad:
	s0b += poems[b]['score'][0]
	s1b += poems[b]['score'][1]
	btypes.append(poems[b]['score'][2])
	count += 1
s0b /= count
s1b /= count

print(s0g, s1g, collections.Counter(gtypes))
print(s0b, s1b, collections.Counter(btypes))

s0 = 0
s1 = 0
atypes = []
count = 0
for p in poems:
	s0 += p['score'][0]
	s1 += p['score'][1]
	atypes.append(p['score'][2])
	count += 1
s0 /= count
s1 /= count

print(s0, s1, collections.Counter(atypes))
