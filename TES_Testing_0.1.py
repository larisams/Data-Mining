# ============================================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Testing <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Larisa Morales 
# VERSION: 1.0
# CREATED: 8/10/2017 4:27 pm
# DESCRIPTION: This program evaluates the model and vectorizer classifing the sentences and then 
# comparing this classes with their true classes.
# USAGE : python 3.4 classify.py --inputPath /home/larisams/storage --inputTestSentences  testing-sentences.txt 
# --inputTestClasses test-classes.txt --outputPath /home/larisams/storage --outputFile test-report.txt 
# --modelName SVM_AC_LR_23130 --modelPath /home/larisams/DataMin/Training/outputData 
# REQUIREMENTS : Text with sentences previously classified by the user,file with true testing classes model and vectorizer 
# CATEGORY : Standalone
# INPUT FORMAT : The file mist consist of one sentence per line, the true classes must be in the same order 
# as the sentences 
# OUTPUT FORMAT : The ouput consists of a test report with the performance metrics and the confussion matrix
# LANGUAGE : Python 3.4
# PATH PROGRAM : /home/larisams/DataMin/
# PARAMETERS
#   1) --inputPath Path to read test sentences 
#   2) --inputTestSentences File to read test sentences 
#   3) --inputTestClasses File to read true classes 
#   3) --outputPath Path to place classified TXT files.
#   4) --modelPath Parent path to read trained model and vectorizer.
#   5) --modelName Name of model and vectorizer to load.
#   6) --outputFile Name of output file 
# =============================================================================================

import os
from time import time
from optparse import OptionParser
from nltk import word_tokenize
import sys
from scipy.sparse import csr_matrix
from sklearn.externals import joblib
from sklearn.svm import SVC
import scipy.stats
from sklearn.feature_extraction import DictVectorizer
from sklearn import model_selection

###########################################################
#                       MAIN PROGRAM                      #
###########################################################

if __name__ == "__main__":
    # Parameter definition
    parser = OptionParser()
    parser.add_option("--inputPath", dest="inputPath",
                      help="Path to read file with features extracted to classify", metavar="PATH")
    parser.add_option("--inputTestSentences", dest="inputTestSentences",
                      help="File to read text to classify (one per line)", metavar="FILE")
    parser.add_option("--inputTestClasses", dest="inputTestClasses",
                      help="File to read training true classes", metavar="FILE")
    parser.add_option("--outputPath", dest="outputPath",
                      help="Path to place classified text", metavar="PATH")
    parser.add_option("--outputFile", dest="outputFile",
                      help="Output file name to write classified text", metavar="FILE")
    parser.add_option("--modelPath", dest="modelPath",
                      help="Path to read trained model", metavar="PATH")
    parser.add_option("--modelName", dest="modelName",
                      help="Name of model and vectorizer to load", metavar="NAME")
    # Clase positiva para clasificación
    parser.add_option("--clasePos", dest="clasePos",
                      help="Clase positiva del corpus", metavar="CLAS")
    # Clase negativa para clasificación
    parser.add_option("--claseNeg", dest="claseNeg",
                      help="Clase negativa del corpus", metavar="CLAS")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error("None parameters indicated.")
        sys.exit(1)

    # Printing parameter values
    print('-------------------------------- PARAMETERS --------------------------------')
    print("Path to read file with testing files: " + str(options.inputPath))
    print("File to read testing sentences : " + str(options.inputTestSentences))
    print("Path to place classified TXT file: " + str(options.outputPath))
    print("Output file name to write testing report: " + str(options.outputFile))
    print("Path to read trained model, vectorizer, and dimensionality reduction: " + str(options.modelPath))
    print("Name of model, vectorizer, and dimensionality reduction to load: " + str(options.modelName))
    print("Positive class: " + str(options.claseNeg))
    print("Negative class: " + str(options.clasePos))

    t1 = time()
    print("Reading test and true classes...")
    y_true = []
    with open(os.path.join(options.inputPath, options.inputTestClasses), encoding='utf8', mode='r') \
            as classFile:
        for line in classFile:
            line = line.strip('\n')
            y_true.append(line)

    testSentences = []
    with open(os.path.join(options.inputPath, options.inputTestSentences), encoding='utf8', mode='r') \
            as dataFile:
        for line in dataFile:
            line = line.strip('\n')
            testSentences.append(line)

    print("     Reading test and true classes done in {:.2} seg".format((time() - t1)))

    print("   Loading model and vectorizer: " + options.modelName)
    if options.modelName.find('.SVM.'):
        classifier = SVC()
    classifier = joblib.load(os.path.join(options.modelPath, 'models', options.modelName + '.mod'), mmap_mode=None)
    vectorizer = joblib.load(os.path.join(options.modelPath, 'vectorizers', options.modelName + '.vec'))

    matrixTesting = csr_matrix(vectorizer.transform(testSentences), dtype='double')
    print('     matrixTesting.shape: ', str(matrixTesting.shape))
    print("        Creating test vectorizer done in {:.2} seg".format((time() - t1)))

    print("    Testing... ")
    y_predicted = classifier_cv.predict(matrixTesting)
    pre = precision_score(y_true, y_predicted, average='weighted')
    rec = recall_score(y_true, y_predicted, average='weighted')
    f1 = f1_score(y_true, y_predicted, average='weighted')

    print("   Saving validation report...")
    with open(os.path.join(options.outputPath, options.outputFile), mode='w', encoding='utf8') as oFile:
        oFile.write('**********        TESTING REPORT     **********\n')
        oFile.write('Precision: {}\n'.format(pre))
        oFile.write('Recall: {}\n'.format(rec))
        oFile.write('F-score: {}\n'.format(f1))
        oFile.write('{}\n'.format((time() - t1)))
        oFile.write('Confusion matrix: \n')
        oFile.write(str(confusion_matrix(y_true, y_predicted)) + '\n')
        oFile.write('Classification report: \n')
        oFile.write(classification_report(y_true, y_predicted) + '\n')
    
    print('**********        TESTING REPORT     **********\n')
    print('Precision: {}'.format(pre))
    print('Recall: {}'.format(rec))
    print('F-score: {}'.format(f1))
    print('{}'.format((time() - t1)))
    print('Confusion matrix:')
    print(str(confusion_matrix(y_true, y_predicted)))
    print('Classification report:')
    print(classification_report(y_true, y_predicted))

    print("Training and cross validation done in: %fs" % (time() - t0))



               
