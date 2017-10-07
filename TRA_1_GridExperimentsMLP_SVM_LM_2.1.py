# ============================================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Grid Experiments MLP_SVM <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# AUTHOR : Larisa Morales Soto
# VERSION: 2.0
# CREATED: 05/10/17 7:39 pm
# DESCRIPTION: This program generates the grid of experiments by performing all the possible 
# combination of parameters to train each classifier.  
# REQUIREMENTS : Name of training classes and training sentences
# CATEGORY : Standalone
# INPUT FORMAT : Name of the training sentences files 
# USAGE : Each variable in the section input files and paths or Parameters dictionaries can be 
# modified by the user according to the combinatory needed and the specific files that will be used 
# LANGUAGE : Python 3.4
# PATH PROGRAM : /home/larisams/DataMin/Training/scripts
# OUTPUT FORMAT: Bash file with python calls followed by report-processing line  
# =============================================================================================

import re 
from random import randint

# Input files and paths

mainInPath = r'/home/larisams/DataMin/Training/inputData'
mainOutPath = r'/home/larisams/DataMin/Training/outputData'
trainS = [r'training_AC_LRK.txt',r'training_AC_LR.txt']
inTrainClass = r'training-classes.txt'


# Parameters dictionaries

vectorizer = {'TFIDF':'1','BINARY':'2','TFIDFBINARY':'3'}
remStopWds = {'T':'1','F':'0'} 
ngrams = {'1':['1'],'2':['2'],'3':['3'],'4':['1','2'],'5':['1','3']}
classweight = {'unbalanced':'0','balanced':'1'}
kernel = {'linear':'1','poly':'2','rbf':'3'}
script = 'Lmod_training-cross-validation-improving.py'
BasicParm = ' '.join(['python3',str(script),'--inputPath',str(mainInPath),'--inputTrainingClasses',str(inTrainClass),'--outputPath',str(mainOutPath),'--positiveClass','DISEASE'])
CP = ['--inputTrainingSentences','--outputFile','--classifier','--vectype','--classweight','--sngram','--fngram']
activationF = {'identity':'1','tanh':'2','relu':'3'}


# Grid MLP

cmline,outf ='',''
i=0
grid = open(r'/Users/larisams/Dropbox/Projects/BI/MineriaDatos/Training-CV/Grid_MLP.sh','w')
for ts in trainS:
    for vec in vectorizer:
        for ng in ngrams:
            for ac in activationF:
                for cw in classweight:
                    for sw in remStopWds:
                        outf,cmline,sgr,fgr = '','','',''
                        sgr= ngrams[ng][0]
                        fgr= ngrams[ng][0]
                        if len(ngrams[ng])>1:
                            fgr = ngrams[ng][1]
                        hl = str(randint(100,250))
                        outf = 'MLP'+'_'+re.search(r'_(.*).txt',ts).group(1)+'_'+vectorizer[vec]+ng+activationF[ac]+classweight[cw]+remStopWds[sw]+'_'+hl+'.txt'
                        cmline = ' '.join([BasicParm,CP[0],ts,CP[1],outf,CP[2],'MLP',CP[3],vec,CP[4],cw,CP[5],sgr,CP[6],fgr,"--hiddenlayer",hl+',','--activation',ac])
                        if remStopWds[sw] == '1':
                            cmline = ' '.join([cmline,"--removeStopWords"])
                        cat = 'cat {} {} > ed && mv ed {} | rm {}\n'.format('/'.join([mainOutPath,'FinalReport.txt']),'/'.join([mainOutPath,outf]),'/'.join([mainOutPath,'FinalReport.txt']),'/'.join([mainOutPath,outf]))
                        grid.write(cmline+'\n'+cat)
                        i+=1
grid.close()


# ### Grid SVM

cmline,outf ='',''
i=0
grid = open(r'/Users/larisams/Dropbox/Projects/BI/MineriaDatos/Training-CV/Grid_SVM.sh','w')
for ts in trainS:
    for vec in vectorizer:
        for ng in ngrams:
            for ker in kernel:
                for cw in classweight:
                        for sw in remStopWds:
                            outf,cmline = '',''
                            outf = 'SVM'+'_'+re.search(r'_(.*).txt',ts).group(1)+'_'+vectorizer[vec]+ng+classweight[cw]+kernel[ker]+remStopWds[sw]+'.txt'
                            cmline = ' '.join([BasicParm,CP[0],ts,CP[1],outf,CP[2],'SVM',CP[3],vec,CP[4],cw,CP[5],sgr,CP[6],fgr,'--kernel',ker])
                            if remStopWds[sw] == '1':
                                cmline = ' '.join([cmline,"--removeStopWords"])
                            cat = 'cat {} {} > ed && mv ed {} | rm {}\n'.format('/'.join([mainOutPath,'FinalReport.txt']),'/'.join([mainOutPath,outf]),'/'.join([mainOutPath,'FinalReport.txt']),'/'.join([mainOutPath,outf]))
                            grid.write(cmline+'\n'+cat)
                            i+=1
grid.close()




