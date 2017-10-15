# ============================================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>> Diease Class Sentence Extraction <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Roberto Olayo Alarcon
# VERSION: 1.0
# CREATED: 9/10/2017 19:24 pm
# DESCRIPTION: This program extracts interactions between RS numbers and diseases that are in the
# same sentence. Sentences must be of DISEASE class and contain RS and PHEN tags
# USAGE : Interactions are extracted from a file consisting of sentences that have been classified
# as DISEASE. File path must be writte into the "with open()" clause. 
# REQUIREMENTS : flat text input file of DISEASE classified sentences
# CATEGORY : Pipeline to extract interactions
# INPUT FORMAT : the main input a file consisting of sentences that have been classified as 
# DISEASE and are tagged with their respective PMID 
# by an automatic classifier. The class tag appears afeter the sentence
# OUTPUT FORMAT : Tabule separated values file. 1) RS numbers 2) Associated Disease 
# 3) PMID of the abstract from where the interaction is extracted
# LANGUAJE : Python 3.6
# PATH PROGRAM : /home/rolayo/mi_storage
# =============================================================================================
import re
newarch = open("RsPhenInteractions.txt",'w')
with open("RsPhenDiseaseSentences.txt",'r') as info:
	for line in info:
		if re.search('<RS>rs\d+?</RS>',line):
			RSNUMS = list(set(re.findall("<RS>rs\d+?</RS>",line)))
			r = 1
		if re.search('<PHE>.+?</PHE>',line):
			PHENS = list(set(re.findall('<PHE>.+?</PHE>',line)))
			p = 1
		if r and p:
			for rs in RSNUMS:
				rs = re.search('<RS>(rs\d+?)</RS>',rs).group(1)
			for dis in PHENS:
				dis = re.search('<PHE>(.+?)</PHE>',dis).group(1)
				interaction = rs + '\t' + dis + '\t' + line.split('\t')[1] + '\n'
				newarch.write(interaction)
newarch.close()
