'''
	Problem 4
	Homework 1
	Zihao Li 11061111
'''
import nltk

# the grammar is a modified version
# based on the grammar in the ppt
def build_grammar():
	return nltk.parse_cfg('''
		S -> NP VP
		S -> S Conj S
		NP -> Pronoun
		NP -> Name
		NP -> Article Noun
		NP -> Number
		NP -> NP PP
		NP -> NP RelClause
		VP -> Verb
		VP -> Verb NP
		VP -> Verb Adj
		VP -> VP PP
		PP -> Prep NP
		RelClause -> 'that' VP
		Article -> 'the' | 'a' | 'an' | 'this' | 'that'
		Prep -> 'to' | 'in' | 'on' | 'near'
		Conj -> 'and' | 'or' | 'but'
		Pronoun -> 'I' | 'you' | 'he' | 'me' | 'him'
		Verb -> 'book' | 'include' | 'prefer' | 'walk'
		None -> 'book' | 'flight' | 'meal'
		Name -> 'John' | 'Mary' | 'Boston'
		Adj -> 'first' | 'earliest' | 'cheap'
		''')

if __name__ == '__main__':
	print '... building grammar'
	grammar = build_grammar()
	sentence = 'John walk to Boston'
	parser = nltk.ChartParser(grammar)
	trees = parser.nbest_parse(sentence.split())
	print '... printing trees'
	for tree in trees:
		print tree
