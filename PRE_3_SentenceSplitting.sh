# >>>>>>>>>>>>>>>>>>>>>>>>>>>> Phenotype Association extraction<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Roberto Olayo Alarcon
# VERSION: 1.0
# CREATED: 17/09/2017 20:00
# DESCRIPTION: This line calls Stanford CoreNLP to separate sentences
# USAGE : This program needs an input file to work with
# REQUIREMENTS : flat text input file. Must be executed from the directory where the CoreNLP files are. Input file must also be in the same directory
# CATEGORY : Standalone
# INPUT FORMAT : the main input is a plain text document, from Stanford CoreNLP
# OUTPUT FORMAT : Plain text file
# LANGUAJE : Python 2.7
# PATH PROGRAM : /home/rolayo/stanford-corenlp-full-2017-06-09
# =============================================================================================

java -cp "*" -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit -file All_Abstract_DisGeNet_Completo.txt -outputFormat text

