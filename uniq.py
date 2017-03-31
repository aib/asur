seen = set()
with open('asksozleri.txt', 'r') as f:
	with open('asksozleri_u.txt', 'w') as fo:
		for line in f:
			if line != "\n":
				if line in seen:
					continue
			fo.write(line)
			seen.add(line)
