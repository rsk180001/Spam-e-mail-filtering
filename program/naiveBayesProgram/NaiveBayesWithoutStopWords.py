import os
import math 
import sys

#Sample command line input. Should not contain any spaces in path name
#Python NaiveBayesWithoutStopWords.py E:\machinelearning\Assignment2\train\spam 
#E:\machinelearning\Assignment2\train\ham E:\machinelearning\Assignment2\test\spam 
#E:\machinelearning\Assignment2\test\ham

# path hardcoded.
#pathToSpamFiles = "E:\\machinelearning\\Assignment2\\train\\spam"
#pathToHamFiles = "E:\\machinelearning\\Assignment2\\train\\ham"
#pathToTestSpamFiles = "E:\\machinelearning\\Assignment2\\test\\spam"
#pathToTestHamFiles = "E:\\machinelearning\\Assignment2\\test\\ham"

pathToSpamFiles = sys.argv[1]
pathToHamFiles = sys.argv[2]
pathToTestSpamFiles = sys.argv[3]
pathToTestHamFiles = sys.argv[4]

# Make array of words for given list of files.
def getDataFromFiles(l):
    mailArray = []
    for fileName in l:
        with open(fileName, 'r') as readableFile:
            try:
                contents = readableFile.read()
            except:
                pass
            mailArray.append(contents);
    return mailArray;

#get the full path of data 
def Getfilesinfolder(path):
    fileNames = []
    for filenames in os.listdir(path):
        fullFilePath = os.path.join(path,filenames)
        if os.path.isfile(fullFilePath):
            fileNames.append(fullFilePath)
    return fileNames;

# Read stop words file and make array of words
def stopWords(stop_wrords_file):
    words_list=[]
    with open(stop_wrords_file,'r') as my_file:
                try:
                    s=my_file.read()
                    words_list=s.split()
                except:
                    pass
    return words_list

# Train data: Prepare bag of words for given class.
def trainClassData(mailList , stopWordsArray):
    total_words = 0;					
    bag_of_words = {}
    for mail in mailList:
        wordsInMail = mail.split()
        for word in wordsInMail:
            if (word == 'Subject:'):
                continue
            elif word in stopWordsArray:
                continue
            elif word in bag_of_words.keys():
                bag_of_words[word] += 1
                total_words += 1
            else:
                bag_of_words[word] = 1
                total_words += 1
    return bag_of_words, total_words


# Calculate conditional probabilities for all words in a bag of word of given class.
def calculateConditionalProbabilities(bagOfWords , totalWords,vocabularyLength):
    conditionalProb = {}
    for word in bagOfWords.keys():
        count = bagOfWords[word] + 1
        conditionalProb[word] = count / (totalWords+vocabularyLength)
    return conditionalProb

# Determine Class of new mail.
def classifyMails(mailsArray, spamPrior, conProbSpam, conProbHam, totSpamWords, totHamWords, vocabularyLength, stopWordArray):
    priorOfSpam = math.log(spamPrior)
    priorOfHam = math.log(1-spamPrior) 
    finalClassification = {"Spam": 0 , "Ham":0}
    for mail in mailsArray:
        words = mail.split();
        for word in words:
            if word in conProbSpam.keys():
                priorOfSpam += math.log(conProbSpam[word])
            elif word in stopWordArray:
                continue
            else:
                priorOfSpam += math.log(1/(totSpamWords+vocabularyLength))             
            if word in conProbHam.keys():
                priorOfHam += math.log(conProbHam[word])   
            elif word in stopWordArray:
                continue
            else:
                priorOfHam += math.log(1/(totHamWords + vocabularyLength))     
        if priorOfSpam >= priorOfHam:
            finalClassification["Spam"] +=  1
        else:
            finalClassification["Ham"] +=  1
        priorOfSpam = math.log(spamPrior)
        priorOfHam = math.log(1-spamPrior) 
    return finalClassification

# Make array of stop words. The file stopwords.txt must be in the same folder as that of program file.
stopWordArray = stopWords("StopWords.txt")

# Training data
allSpamFileNames = Getfilesinfolder(pathToSpamFiles)
allSpamMailArray = getDataFromFiles(allSpamFileNames)
spamMailsLen = len(allSpamMailArray)
bagOfSpamWords, totalSpamWords = trainClassData(allSpamMailArray , stopWordArray)

allHamFileNames = Getfilesinfolder(pathToHamFiles)
allHamMailArray = getDataFromFiles(allHamFileNames)
hamMailsLen = len(allHamMailArray)
bagOfHamWords, totalHamWords = trainClassData(allHamMailArray , stopWordArray)

v = len(set(list(bagOfSpamWords.keys()) + list(bagOfHamWords.keys())))

probabilitySpamWords = calculateConditionalProbabilities(bagOfSpamWords,totalSpamWords,v)
probabilityHamWords = calculateConditionalProbabilities(bagOfHamWords,totalHamWords,v)

pOfSpamClass = spamMailsLen / (spamMailsLen + hamMailsLen)
pOfHamClass =  hamMailsLen / (spamMailsLen + hamMailsLen)


# Testing -----------------------------------------
testSpamFileNames = Getfilesinfolder(pathToTestSpamFiles)
testSpamMailArray = getDataFromFiles(testSpamFileNames)
output = classifyMails(testSpamMailArray, pOfSpamClass, probabilitySpamWords, probabilityHamWords, totalSpamWords, totalHamWords, v, stopWordArray)

testHamFileNames = Getfilesinfolder(pathToTestHamFiles)
testHamMailArray = getDataFromFiles(testHamFileNames)
output1 = classifyMails(testHamMailArray, pOfSpamClass, probabilitySpamWords, probabilityHamWords, totalSpamWords, totalHamWords, v, stopWordArray)

print("Spam accuracy without stopwords" , (output["Spam"]/len(testSpamMailArray)) * 100)
print("Ham accuracy without stopwords" , (output1["Ham"]/len(testHamMailArray)) * 100)





