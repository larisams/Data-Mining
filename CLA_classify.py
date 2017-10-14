# ============================================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Classify <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Carlos Mendez
# MODIFIED BY : Larisa Morales 
# VERSION: 1.0
# CREATED: 10/10/2017 7:32 pm
# DESCRIPTION: This program classifies text files by using trained SVM model and vectorizer
# USAGE : python 3.4 classify.py --inputPath /home/larisams/storage --inputFile  RsPhenSentences.txt \
# --outputPath /home/larisams/storage --outputFile RsPhenSentences_class.txt --modelName SVM_AC_LR_23130 \
# --modelPath /home/larisams/DataMin/Training/outputData --clasePos DISEASE --claseNeg OTHER 
# REQUIREMENTS : Text file to classify, model and vectorizer 
# CATEGORY : Standalone
# INPUT FORMAT : The file mist consist of one sentence per line 
# OUTPUT FORMAT : The ouput consists of classified sentences in the format sentence <tab> class
# LANGUAGE : Python 3.4
# PATH PROGRAM : /home/larisams/DataMin/Final
# PARAMETERS
#   1) --inputPath Path to read TXT files to classify.
#   2) --inputFile File to read text to classify (one per line).
#   3) --outputPath Path to place classified TXT files.
#   4) --modelPath Parent path to read trained model and vectorizer.
#   5) --modelName Name of model and vectorizer to load.
#   6) --outputFile File to write the classified sentences 
#   7) --clasePos Clase positiva para clasificación
#   8) --claseNeg Clase negativa para clasificación
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
    parser.add_option("--inputFile", dest="inputFile",
                      help="File to read text to classify (one per line)", metavar="FILE")
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
    print("Path to read file with features extracted to classify: " + str(options.inputPath))
    print("File to read text to classify (one per line): " + str(options.inputFile))
    print("Path to place classified TXT file: " + str(options.outputPath))
    print("Output file name to write classified text: " + str(options.outputFile))
    print("Path to read trained model, vectorizer, and dimensionality reduction: " + str(options.modelPath))
    print("Name of model, vectorizer, and dimensionality reduction to load: " + str(options.modelName))
    print("Positive class: " + str(options.claseNeg))
    print("Negative class: " + str(options.clasePos))

    t0 = time()

    listSentences = []

    with open(os.path.join(options.inputPath, options.inputFile), 'r', encoding='utf8', errors='replace') as iFile:
        for line in iFile.readlines():
            line = line.strip('\n')
            listSentences.append(line)

    print("Classifying texts...")
    print("   Loading model and vectorizer: " + options.modelName)
    if options.modelName.find('.SVM.'):
        classifier = SVC()
    classifier = joblib.load(os.path.join(options.modelPath, 'models', options.modelName + '.mod'), mmap_mode=None)
    vectorizer = joblib.load(os.path.join(options.modelPath, 'vectorizers', options.modelName + '.vec'))

    matrix = csr_matrix(vectorizer.transform(listSentences), dtype='double')
    print("   matrix.shape " + str(matrix.shape))

    # Classify corpus list
    y_predicted = classifier.predict(matrix)

    print("   Predicted class list length: " + str(len(y_predicted)))

    with open(os.path.join(options.outputPath, options.outputFile), "w", encoding="utf-8") as oFile:
        oFile.write('SENTENCE\tPREDICTED_CLASS\n')
        for s, pc in zip(listSentences, y_predicted):
            oFile.write(s + '\t' + pc + '\n')

    print("Texts classified in : %fs" % (time() - t0))
