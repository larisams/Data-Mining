# >>>>>>>>>>>>>>>>>>>>>>>>>>>>Stanford Core Sentence Annotation<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Roberto Olayo Alarcon
# VERSION: 1.0
# CREATED: 30/09/2017 11:00
# DESCRIPTION: This line calls Stanford CoreNLP to separate sentences and annotate lemmas and Part of Speech 
# USAGE : This program uses two input files. The fist line uses a file without disease or rs tagging. The second line uses a file with disease an rs tagging
# REQUIREMENTS : flat text input file. Must be executed from the directory where the CoreNLP files are.
# CATEGORY : Standalone
# INPUT FORMAT : the main input is a plain text document
# OUTPUT FORMAT : a tsv file.
# LANGUAJE : bash
# PATH PROGRAM : /home/rolayo/stanford-corenlp-full-2017-06-09
# =============================================================================================

java -cp "*" -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma -file Documentos/training-sentences.rs.word.txt -outputFormat conll -outputDirectory Results/

java -cp "*" -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma -file Documentos/training-sentences.PhenTAG_rsTAG.txt -outputFormat conll -outputDirectory Results/
