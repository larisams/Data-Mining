# ============================================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>> Diease Class Sentence Extraction <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Roberto Olayo Alarcon
# VERSION: 1.0
# CREATED: 9/10/2017 19:24 pm
# DESCRIPTION: This program extracts sentences classified as DISEASE and 
# writes a new document that only contains said sentences. Each line contains the respective
# PMID.
# USAGE : To extract sentences classified as DISEASE the input file path must be written in the
# "with open()" clause. Class tags must appear in the same line as the sentence
# REQUIREMENTS : flat text input file 
# CATEGORY : Pipeline to extract interactions
# INPUT FORMAT : the main input a file consisting of sentences that have been classified 
# by an automatic classifier. The class tag appears afeter the sentence
# OUTPUT FORMAT : Flat text file of DISEASE classified sentenceces along with PMID.
# LANGUAJE : Python 3.6
# PATH PROGRAM : /home/rolayo/mi_storage
# =============================================================================================
 
import re
newarch	= open("RsPhenDiseaseSentences.txt", 'w')
with open("/home/larisams/storage/RsPhenSentences_class.txt", 'r') as info:
        for line in info:
                line = line.rstrip()
                if re.search("^\d{7,8}\|\d+\s",line):
                        PMID = re.search("^(\d{7,8})\|\d+\s",line).group(1)
		if re.search("DISEASE",line):
			newarch.write(line)
			newarch.write('\t')
			newarch.write(PMID)
			newarch.write('\n')
newarch.close()

