import re


cleanse_rules = [

	# RT
	('^RT @\S+\: ', ''),
	
	# @account
	('^(@\S+ )+', ''),
	('( @\S+)+$', ''),
	('( @\S+)+', ' @usuario'),

	# #hastag
	('^(#\S+ )+', ''),
	('( #\S+)+$', ''),
	('#(\S+) ', r'\1 '),

	# http
	('\s+v.a… ?http.+', ''),
	('(… )?https\S+$', ''),
	('\s+v.a http.+', ''),
	('http\S+ v.a .+', ''),
	
	# …
	('…$', ''),

	# \s
	('\s{2,}', ' '),

	# \¡!¿?
	('\¡{2,}', '¡'),
	('\!{2,}', '!'),
	('\¿{2,}', '¿'),
	('\?{2,}', '?'),

	# |
	('\|', ':')

]

tokenization_rules = [

	# symbol to the right
	('(\w{2,})(\,|\.|\?|\!|\:|\;)', r'\1' + ' ' + r'\2'),

	# symbol to the left
	( '(\¡|\¿)(\w{2,})', r'\1' + ' ' + r'\2'),

	# () "“
	(' (\(|\"|\'|\“|‘)(\w)', r' \2'),
	('(\w)(\)|\"|\'|\”|’) ', r'\1 ')

]

split_rules = [

	' \. ',
	' \: ',
	' \.\.\.+ ',
	'\.{4,}',
	'\!+',
	'\?+'

]


def cleanse_tweet (tweet):

	for cleanse_rule in cleanse_rules:
		tweet = re.sub(cleanse_rule[0], cleanse_rule[1], tweet)
	
	for tokenization_rule in tokenization_rules:
		tweet = re.sub(tokenization_rule[0], tokenization_rule[1], tweet)

	tweet = tweet.strip().lower()
	cleansed_tweet = tweet

	return cleansed_tweet


def splitter (tweet):

	regex = '|'.join(split_rules)

	sequences = re.split(regex ,tweet)

	return sequences


def preprocess_tweet (tweet):

	cleansed_tweet = cleanse_tweet(tweet)

	if len(cleansed_tweet) == 0:
		return None

	sequences = splitter(cleansed_tweet)

	sequences = [sequence for sequence in sequences if len(sequence) > 5 and len(sequence.split()) > 1 ]

	return sequences



