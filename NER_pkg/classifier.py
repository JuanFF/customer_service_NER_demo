import fasttext


def save_classifier_model (training_file_path, vector_file_path):

	if vector_file_path:
		pretrain_vec_classifier_model = fasttext.train_supervised(input = training_file_path, lr=1.0, epoch=25, pretrainedVectors = vector_file_path)
		pretrain_vec_classifier_model.save_movel('pretrain_vec_classifier_model.bin')

	else:
		classifier_model = fasttext.train_supervised(input = training_file_path, lr=1.0, epoch=25)
		classifier_model.save_model('classifier_model.bin') 		


def classify (model_file_path, string):

	classifier_model = fasttext.load_model(model_file_path)
	label = classifier_model.predict(string)[0][0].split('__')[2]
	return label