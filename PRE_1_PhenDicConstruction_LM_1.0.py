
# ============================================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>> Phenotype Dictionary construction <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Larisa Morales Soto
# VERSION: 1.0
# CREATED: 14/09/2017 10:55 pm
# DESCRIPTION: This program generates a phenotypes dictionery
# USAGE : This program needs the paths of the input and output format, this must be modified
# directly on the source code in the variables inputfile and dicOUT
# REQUIREMENTS : flat text input file
# CATEGORY : Standalone
# INPUT FORMAT : the main input is the file genemap2.txt, this files has 13 columns, the ones 
# used in this script are columns 8 an 13
# OUTPUT FORMAT : The ouput file name can be modified by changing the variable dicOUT
# LANGUAJE : Python 3.6
# PATH PROGRAM : /home/larisams/storage/BEI_project/bin/PhenotypeAssoc.py
# =============================================================================================

import re as re
from collections import defaultdict as df

inputfile = r'/home/larisams/storage/BEI_project/data_source/genemap2_ed.txt'
dicOUT = r'/home/larisams/storage/BEI_project/data_source/Dic_Phens.txt'

with open(inputfile) as f:
    GeneDic,MIMdict = df(str),df(str)
    for line in f:
        gene,all_phens = line.split('\t')[7],line.split('\t')[12]
        for p in all_phens.split(';'):
            fields = re.search(r'(.*),\s+([0-9]{6}).*',p)
            if fields:
                GeneDic[gene] += fields.group(1).lstrip('{|?|[').rstrip('}|]')+';'
                MIMdict[fields.group(2)] += fields.group(1).lstrip('{|?|[').rstrip('}|]')+';'
            else:
                GeneDic[gene] = 'No phenotype associated'

# Writing phenotypes dictionary
 
with open(dicOUT,'w') as f:
    for key in GeneDic.keys():
        line = GeneDic[key].rstrip(';')+'\n'
        f.write(line)

        

