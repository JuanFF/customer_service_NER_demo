import spacy
import json
import random


def get_formatted_ner_training ():

	formatted_ner_training = []

	with open('./datasets/ner.train.json', 'r', encoding = 'utf-8') as ner_training_file:
		ner_training = json.load(ner_training_file)
		for train in ner_training:
			formatted_train = (train['sequence'], {'entities': [tuple(ann_entity) for ann_entity in train['ann_entities']]})
			formatted_ner_training.append(formatted_train)

	return formatted_ner_training
			

def train_ner (data, iterations):
    TRAIN_DATA = data
    nlp = spacy.blank('es')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)

    return nlp


def get_ner_model (iterations):

    data = get_formatted_ner_training()
    nlp = train_ner(data, iterations)
    nlp.to_disk('customer_service_ner')


get_ner_model(30)