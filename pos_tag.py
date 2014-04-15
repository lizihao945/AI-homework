'''
	Problem 5
	Homework 1
	Zihao Li 11061111
'''
import nltk

def read_from_file(path):
	file = open(path)
	all_text = []
	try:
		all_text = file.readlines()
	finally:
		file.close()
	return all_text

class WordTag:
	def count_word_with_tag(self, word, tag):
		rt = 0
		for key in self.d.keys():
			if (key[0] == word and key[1] == tag):
				rt += 1
		return rt

	# [XXX/a XXY/b]s ----> XXX/a XXY/b
	def remove_higher_tag(dataset):
		pass

	def __init__(self, filepath):
		lines = read_from_file(filepath)
		new_lines = []
		for line in lines:
			# skip empty lines
			if line == '\n':
				continue
			tmp = list(nltk.tag.str2tuple(str) for str in line.split())
			new_lines.append(tmp[1:])
		# build datasets
		total = len(new_lines)
		idx = int(total * 0.9)
		train_set = new_lines[:idx]
		test_set = new_lines[idx:]
		self.train_set = train_set
		self.test_set = test_set
		'''
		d = self.d
		for idx in xrange(10):
			print d.keys()[idx][0].encode('GBK')
			print d[d.keys()[idx]]
		'''
		
if __name__ == '__main__':
	data = WordTag('annotation.txt')
	word_pos_count = {}
	pos_count = {}
	words = {}
	adjoin_poss = {}
	# consider use reshape(numpy) and FreqDist(nltk)
	for line in data.train_set:
		prev = None
		for pair in line:
			word = pair[0]
			pos = pair[1]
			# count pos
			if pos_count.has_key(pos):
				pos_count[pos] += 1
			else:
				pos_count[pos] = 1
			# count the occurance of (word, pos)
			if word_pos_count.has_key(word):
				word_pos_count[word] += 1
			else:
				word_pos_count[word] = 1
			# words: {'word', {'pos', num}}
			if words.has_key(word):
				if words[word].has_key(pos):
					words[word][pos] += 1
				else:
					words[word][pos] = 1
			else:
				words[word] = {pos: 1}
			if prev == None:
				prev = pos
				continue
			# count the occurance of two adjoin words
			if adjoin_poss.has_key((prev, pos)):
				adjoin_poss[(prev, pos)] += 1
			else:
				adjoin_poss[(prev, pos)] = 1
			prev = pos

	# P(ti|ti-1)
	# the possibility of Ti after Ti-1
	for trans, count in adjoin_poss.items():
		adjoin_poss[trans] = count / float(pos_count[trans[0]])

	# the possibility of word as pos (pos known)
	# words: {'word', {'pos', (p1, p2)}}
	# p1 is P(t|w), p2 is P(w|t)
	for word, dic in words.items():
		tmp = sum(list(j for i, j in dic.items()))
		for pos, num in dic.items():
			dic[pos] = (num / float(tmp), num / float(pos_count[pos]))

	# number of all pairs
	total = sum(list(j for i, j in pos_count.items()))
	pos_count = pos_count.items()
	right_count = 0
	total_count = 0
	for line in data.test_set:
		# 1000 words per line
		v = [[0 for col in xrange(1000)] for row in xrange(len(pos_count))]
		# initialize v[i][0]
		for i in xrange(len(pos_count)):
			# frequency of pos[i]
			p = pos_count[i][1] / float(total)
			start_word = line[0][0]
			pos = pos_count[i][0]
			'''
			WHAT IS the RIGHT METHOD ?
			'''
			if not words.has_key(line[0][0]):
				words[line[0][0]] = {line[0][1]: (1.0, 1.0)}
			if not (words[start_word].has_key(pos)):
				v[i][0] = 0l
			else:
				# P(pos[i]) * P(w|t)
				v[i][0] = p * words[start_word][pos][1]
		re = list(0 for pair in xrange(len(line)))
		for t in xrange(1, len(line)):
			t_max = 0
			for i in xrange(len(pos_count)):
				# first judge whether it's a new word
				'''
				WHAT IS the RIGHT METHOD ?
				'''
				if not words.has_key(line[t][0]):
					words[line[t][0]] = {line[t][1]: (1.0, 1.0)}
				# the Tth word is Ith pos
				# calculate v[i][t]
				# skip impossible pos of a word
				if not words[line[t][0]].has_key(pos_count[i][0]):
					v[i][t] = 0
					continue
				# find the best way from previous pos
				for k in xrange(len(pos_count)):
					adj = (pos_count[k][0], pos_count[i][0])
					if not adjoin_poss.has_key(adj):
						continue
					if v[k][t - 1] * adjoin_poss[adj] > t_max:
						re[t - 1] = pos_count[k][0]
						t_max = v[k][t - 1] * adjoin_poss[adj]
				v[i][t] = t_max * words[line[t][0]][pos_count[i][0]][1]
			t_max = 0
		# choose last pos
		for k in xrange(len(pos_count)):
			if v[k][t] > t_max:
				re[t] = pos_count[k][0]
				t_max = v[k][t]
		# calculate test error
		tmp = list(t1 for t0, t1 in line)
		for result, answer in zip(re, tmp):
			total_count +=1
			if result == answer:
				right_count += 1
	print right_count / float(total_count)
