# >>>>>>>>>>>>>>>>>>>>>>>>>>>>Sentence Extraction With Tags<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Roberto Olayo Alarcon
# VERSION: 1.0
# CREATED: 30/09/2017 11:47
# DESCRIPTION: This line calls Stanford CoreNLP to separate sentences and annotate lemmas and Part of Speech 
# USAGE : Call of script. To change name of input files, code must be changed
# REQUIREMENTS : tab seperated values in conll format.
# CATEGORY : Part of Pipline to train a classifier
# INPUT FORMAT : a tsv file in conll format
# OUTPUT FORMAT : flat text file
# LANGUAJE : Python 3.4
# PATH PROGRAM : /home/rolayo/Downloads/TaggingTraining.py
# =============================================================================================

# coding: utf-8

# In[26]:

#Esta seccion extrae oraciones con lemma y postag de un archivo con taggeado de rs y en enfermedad
#de manera que queda palabra|lemma|postag

newarch = open("training_RLP.txt", 'w')
tagged_lines = []
with open("training-sentences.PhenTAG_rsTAG.txt.conll", 'r') as info:
    for line in info:
        #Cada nueva oracion empieza con el indice 1. Se se encuentra con el inicio de una linea la oracion anterior
        #se escribe en el archivo
        if line.startswith('1\t'):
            tagged_lines = ' '.join(tagged_lines)
            if len(tagged_lines) > 0:
                newarch.write(tagged_lines)
                newarch.write('\n')
            tagged_lines = []
        #Se hace un split sobre la linea y se guarda la palabra, lemma, y postag   
        line = line.split('\t')
        if len(line) > 1:
            line = line[1] + '|' + line[2] + '|' + line[3]
            tagged_lines.append(line)
    #Se escribe la ultima oracion        
    tagged_lines = ' '.join(tagged_lines)
    newarch.write(tagged_lines)
    
newarch.close()        


# In[27]:

#Esta seccion extrae oraciones con lemma de un archivo con taggeado de rs y en enfermedad
#de manera que queda palabra|lemma

newarch = open("training_RL.txt", 'w')
tagged_lines = []
with open("training-sentences.PhenTAG_rsTAG.txt.conll", 'r') as info:
    for line in info:
        #Cada nueva oracion empieza con el indice 1. Se se encuentra con el inicio de una linea la oracion anterior
        #se escribe en el archivo
        if line.startswith('1\t'):
            tagged_lines = ' '.join(tagged_lines)
            if len(tagged_lines) > 0:
                newarch.write(tagged_lines)
                newarch.write('\n')
            tagged_lines = []
        #Se hace un split sobre la linea y se guarda la palabra y lemma
        line = line.split('\t')
        if len(line) > 1:
            line = line[1] + '|' + line[2]
            tagged_lines.append(line)
    #Se escribe la ultima oracion                    
    tagged_lines = ' '.join(tagged_lines)
    newarch.write(tagged_lines)
    
newarch.close()        


# In[28]:

#Esta seccion extrae oraciones con lemma de un archivo sin taggeado de rs y en enfermedad
#de manera que queda palabra|lemma
newarch = open("training_L.txt", 'w')
tagged_lines = []
with open("training-sentences.rs.word.txt.conll", 'r') as info:
    for line in info:
        #Cada nueva oracion empieza con el indice 1. Se se encuentra con el inicio de una linea la oracion anterior
        #se escribe en el archivo        
        if line.startswith('1\t'):
            tagged_lines = ' '.join(tagged_lines)
            if len(tagged_lines) > 0:
                newarch.write(tagged_lines)
                newarch.write('\n')
            tagged_lines = []
        #Se hace un split sobre la linea y se guarda la palabra y lemma
        line = line.split('\t')
        if len(line) > 1:
            line = line[1] + '|' + line[2]
            tagged_lines.append(line)
    #Se escribe la ultima oracion            
    tagged_lines = ' '.join(tagged_lines)
    newarch.write(tagged_lines)
    
newarch.close()  

