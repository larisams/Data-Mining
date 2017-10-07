# ============================================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>>> Training and cross validation <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Larisa Morales Soto
# VERSION: 1.0
# CREATED: 05/10/17 3:28 pm
# DESCRIPTION: This program perform the training and cross-validation steps for SVM and MLP
# classifiers with the same training sentences for each one and reports it's scores along with 
# the model and vectorizer 
# REQUIREMENTS : command line parameters, training classes and training sentences files 
# CATEGORY : Standalone
# INPUT FORMAT : the main input are two flat files. One must include a single-column file 
# with the treining classes, the other one must contain the training sentences in the same order 
# Command line Parameters:
# 1) --inputPath Path to read input files.
# 2) --inputTrainingSentences File to read training data.
# 3) --inputTrainingClasses File to read training true classes.
# 4) --outputPath Path for output files.
# 5) --outputFile File for validation report.
# 6) --classifier Classifier: SVM.
# 7) --removeStopWords  Remove stop words
# 8) --vectype Vectorizer type: TFIDF or BINARY
# 9) --positiveClass Positive class
# 10) --kernel SVM Kernel
# 11) --classweight balanced or unbalanced
# 12) --activation Activation formula for MLP 
# 13) --sngram minimun ngram
# 14) --fngram maximum ngram 
# 15) --hiddenlayers Hidden layer for MLP
# LANGUAGE : Python 3.4
# PATH PROGRAM : /home/larisams/DataMin/Training/scripts
# OUTPUT FORMAT:
# 1) Evaluation report.
# 2) Vectorizer and model. 
# USAGE:
# python3 Lmod_training-cross-validation-improving.py --inputPath /home/larisams/DataMin/Training/inputData --inputTrainingClasses training-classes.txt --outputPath /home/larisams/DataMin/Training/outputData --positiveClass DISEASE --inputTrainingSentences training_AC_LRK.txt --outputFile SVM_AC_LRK_11011.txt --classifier SVM --vectype TFIDF --classweight unbalanced --sngram 1 --fngram 3 --kernel linear --removeStopWords
# =============================================================================================
import os
from time import time
from optparse import OptionParser
from sklearn.svm import SVC
from sklearn.metrics import f1_score, confusion_matrix, \
    classification_report, make_scorer, precision_score, recall_score
import sys
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import csr_matrix
from sklearn.model_selection import cross_val_score
from sklearn import model_selection
import scipy.stats
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier

###########################################################
#                       MAIN PROGRAM                      #
###########################################################

if __name__ == "__main__":
    # Parameter definition
    parser = OptionParser()
    parser.add_option("--inputPath", dest="inputPath",
                      help="Path to read input files", metavar="PATH")
    parser.add_option("--inputTrainingSentences", dest="inputTrainingSentences",
                      help="File to read training data", metavar="FILE")
    parser.add_option("--inputTrainingClasses", dest="inputTrainingClasses",
                      help="File to read training true classes", metavar="FILE")
    parser.add_option("--outputPath", dest="outputPath",
                          help="Path for output files", metavar="PATH")
    parser.add_option("--outputFile", dest="outputFile",
                      help="File for validation report", metavar="FILE")
    parser.add_option("--classifier", dest="classifier",
                      help="Classifier", metavar="CLASSIFIER")
    parser.add_option("--vectype", dest="vectype",
                      help="Vectorizer type: TFIDF, TFIDFBINARY, BINARY", metavar="TEXT")
    parser.add_option("--positiveClass", dest="positiveClass",
                      help="Positive class", metavar="TEXT")
    parser.add_option("--removeStopWords", default=False,
                      action="store_true", dest="removeStopWords",
                      help="Remove stop words")
    parser.add_option("--kernel", dest="kernel", default='linear',
                      choices=('rbf', 'linear', 'poly'),
                      help="Kernel", metavar="TEXT")
    parser.add_option("--sngram", type="int",
                      dest="sngram", default=1,
                      help="Start n-gram", metavar="N")
    parser.add_option("--fngram", type="int",
                      dest="fngram", default=1,
                      help="Final n-gram", metavar="N")
    parser.add_option("--classweight", dest="clweight",
                      choices=('unbalanced', 'balanced',),
                      help="ClassWeight", metavar="TEXT")
    parser.add_option("--hiddenlayers", dest="hiddenlayers", help="Hidden layer size", default=(100, ), metavar="tuple")
    parser.add_option("--activation", dest="activation", help="Activation function", default='identity', choices=('identity', 'tanh', 'relu'), metavar="TEXT")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error("None parameters indicated.")
        sys.exit(1)

    # Printing parameter values
    print('-------------------------------- PARAMETERS --------------------------------')
    print("Path to read input files: " + str(options.inputPath))
    print("File to read training data: " + str(options.inputTrainingSentences))
    print("File to read training true classes: " + str(options.inputTrainingClasses))
    print("Path for output files: " + str(options.outputPath))
    print("File to write report: " + str(options.outputFile))
    print("Classifier: " + str(options.outputFile))
    print("Vectorizer type: " + str(options.vectype))
    print("Positive class: " + str(options.positiveClass))
    print("Remove stop words: " + str(options.removeStopWords))
    print("Kernel: " + str(options.kernel))
    print("Start ngram: " + str(options.sngram))
    print("Final ngram: " + str(options.fngram))
    print("Class weight: " + str(options.clweight))

    # Start time
    t0 = time()

    t1 = time()
    print("Reading training and true classes...")
    trueTrainingClasses = []
    with open(os.path.join(options.inputPath, options.inputTrainingClasses), encoding='utf8', mode='r') \
            as classFile:
        for line in classFile:
            line = line.strip('\n')
            trueTrainingClasses.append(line)

    trainingSentences = []
    with open(os.path.join(options.inputPath, options.inputTrainingSentences), encoding='utf8', mode='r') \
            as dataFile:
        for line in dataFile:
            line = line.strip('\n')
            trainingSentences.append(line)
    # print(trainingSentences)

    print("     Reading training and true classes done in {:.2} seg".format((time() - t1)))

    if options.removeStopWords:
        print("   Removing stop words")
        pf = stopwords.words('english')
    else:
        pf = None

    t1 = time()
    print('     Creating training vectorizers...')
    if options.vectype == "TFIDF":
        vectorizer = TfidfVectorizer(ngram_range=(options.sngram, options.fngram), stop_words=pf)
    elif options.vectype == "TFIDFBINARY":
        vectorizer = TfidfVectorizer(ngram_range=(options.sngram, options.fngram), stop_words=pf, binary=True)
    elif options.vectype == "BINARY":
        vectorizer = CountVectorizer(ngram_range=(options.sngram, options.fngram), stop_words=pf, binary=True)

    matrixTraining = csr_matrix(vectorizer.fit_transform(trainingSentences), dtype='double')
    print('     matrixTraining.shape: ', matrixTraining.shape)
    print("        Creating training vectorizer done in {:.2} seg".format((time() - t1)))

    scoring = make_scorer(f1_score, pos_label=options.positiveClass)

    if options.classifier == "SVM":
        classifier = SVC()
        if options.kernel == 'rbf':
            paramGrid = {'C': scipy.stats.expon(scale=10), 'gamma': scipy.stats.expon(scale=.1),
                         'kernel': ['rbf'], 'class_weight': [None, str(options.clweight)]}
        elif options.kernel == 'linear':
            paramGrid = {'C': scipy.stats.expon(scale=10), 'kernel': ['linear'],
                         'class_weight': [None, 'balanced']}
        elif options.kernel == 'poly':
            paramGrid = {'C': scipy.stats.expon(scale=10), 'gamma': scipy.stats.expon(scale=.1),
                         'degree': [2, 3],
                         'kernel': ['poly'], 'class_weight': [None, str(options.clweight)]}
        classifier_cv = model_selection.RandomizedSearchCV(classifier, paramGrid,
                                                          cv=10, n_jobs=1, verbose=3,
                                                          scoring=scoring, random_state=42)
        t1 = time()
        print("   Training and cross validation...")
        classifier_cv.fit(matrixTraining, trueTrainingClasses)
        best_score = classifier_cv.best_score_
        best_parameters = classifier_cv.best_estimator_.get_params()
        print("     Training and cross validation done in {:.2} seg".format((time() - t1)))
        t1 = time()
        joblib.dump(classifier_cv.best_estimator_,os.path.join(options.outputPath, 'models', options.outputFile.replace(".txt", ".mod")))
        joblib.dump(vectorizer,os.path.join(options.outputPath, 'vectorizers', options.outputFile.replace(".txt", ".vec")))
        print("        Saving training model and vectorizer done in: %fs" % (time() - t1))
       
    if options.classifier == "MLP":       
        h = [int(x) for x in options.hiddenlayers.split(',') if x]
        lay = tuple(h)
        classifier_mlp = MLPClassifier(hidden_layer_sizes=lay, activation=options.activation)
        t1 = time()
        print("   Training and cross validation...")
        classifier_mlp.fit(matrixTraining,trueTrainingClasses)
        scores = cross_val_score(classifier_mlp,matrixTraining,trueTrainingClasses,cv=10,scoring=scoring,n_jobs=-1)
        best_score = scores.mean()
        joblib.dump(classifier_mlp,os.path.join(options.outputPath, 'models', options.outputFile.replace(".txt", ".mod")))
        joblib.dump(vectorizer,os.path.join(options.outputPath, 'vectorizers', options.outputFile.replace(".txt", ".vec")))
        print("        Saving training model and vectorizer done in: %fs" % (time() - t1))
        best_parameters = classifier_mlp.get_params()
        print("     Training and cross validation done in {:.2} seg".format((time() - t1)))
	
    print("   Saving validation report...")
    with open(os.path.join(options.outputPath, options.outputFile), mode='w', encoding='utf8') as oFile:
        oFile.write('{}\t'.format(options.outputFile))
        oFile.write('{}\t'.format(options.classifier))
        oFile.write('{}\t'.format(best_score))
        for param in sorted(best_parameters.keys()):
            oFile.write("%s: %r | " % (param, best_parameters[param]))
        oFile.write('\n')
    print("     Saving validation report done!")

    print('**********        VALIDATION REPORT     **********')
    print('Classifier: {}'.format(options.classifier))
    print('Kernel: {}'.format(options.kernel))
    print('Best score{}: {}'.format(scoring, best_score))
    print('Best parameters:')
    for param in sorted(best_parameters.keys()):
        print("\t%s: %r" % (param, best_parameters[param]))

    print("Training and cross validation done in: %fs" % (time() - t0))
