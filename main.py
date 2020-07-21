from NER_pkg import tweet_processing, classifier
import fasttext
import spacy


'''
This a demo script of a NER algorithm that
labels issue-related entities mentioned in social
media customer service channels.

"Hable por teléfono con su compañera porque estoy
sin [teléfono] ni [wifi] desde ayer"
'''

classifier_model_path = 'NER_pkg/classifier_model.bin'
nlp = spacy.load('./NER_pkg/customer_service_ner')


def get_entities (text_source):

	entities = []

	# text source like tweets are splited into text sequences
	sequences = tweet_processing.preprocess_tweet(text_source)

	if sequences is not None:

		for sequence in sequences:

			# classify sequences into frames (delay, fail, supply, blank)
			frame = classifier.classify(classifier_model_path, sequence)

			# if 'blank', sequence meaning is irrelevant and NER won't be applied
			if frame is not 'blank':
				doc = nlp(sequence)
				# only frame-related entities are considered
				entities += [ent.text for ent in doc.ents if frame == ent.label_.split('_')[0]]

	return entities


def annotate_test_corpus ():

	test_corpus_file_name = input('Test corpus file name > ')

	with open(test_corpus_file_name, 'r', encoding = 'utf-8') as test_corpus_file:
		test_corpus = [line.rstrip() for line in test_corpus_file.readlines()]
	
	generated_file_name = test_corpus_file_name.split('.')[-2] + '.annotated.tsv'

	with open(generated_file_name, 'w', encoding = 'utf-8') as ann_test_corpus_file:
		ann_test_corpus_file.write('text_source' + '\t' + 'entities_output' + '\n')
		for i in range(len(test_corpus)):
			print(' Processing ' + str(i+1) + '/' + str(len(test_corpus)), "  \r", end='')
			entities = get_entities(test_corpus[i])
			if len(entities) == 0:
				entities = '0'
			else:
				entities = ', '.join(entities)
			ann_test_corpus_file.write(test_corpus[i] + '\t' + entities + '\n')

	print(generated_file_name + ' has been written')


def main ():
	annotate_test_corpus()


main()