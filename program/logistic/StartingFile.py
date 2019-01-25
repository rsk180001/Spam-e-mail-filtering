from Training import training , training_stop , stopWords
from Testing import test, test_stop
from LogisticRegression import measureAccuracy, gradientAscentApplication
import sys

trainHamFolderPath=sys.argv[1]
trainSpamFolderPath=sys.argv[2]
testHamFolderPath=sys.argv[3]
testSpamFolderPath=sys.argv[4]
learningRate=float(sys.argv[5])
lamda=float(sys.argv[6])


weightVector,ipVector,positive,negative,negAttrCount,posAttrCount,trainedWordList,wordcount,trainOutputList=training(trainHamFolderPath,trainSpamFolderPath)
wordlistTest,wordpositions,emailClass,testAttrList=test(trainedWordList,testHamFolderPath,testSpamFolderPath)
weight_matrix=gradientAscentApplication(ipVector, weightVector, trainOutputList,0,15,learningRate,lamda)
accuracy=measureAccuracy(weight_matrix,testAttrList,emailClass)
print("\nAccuracy of Logistic Regression including stop words:", accuracy*100)


stopWords=stopWords("StopWords.txt")
stopWeightVector,stopIpvector,stopPositive,stopNegative,stopNegAttrCount,stopPosAttrCount,stopWordlist,stopWordcount,stopTrainOutputList = training_stop(stopWords,trainHamFolderPath,trainSpamFolderPath)
testWordList,testWordPositions,stopOutputList,stopTestAttrList = test_stop(stopWords,stopWordlist,testHamFolderPath,testSpamFolderPath)
weightArrayStop = gradientAscentApplication(stopIpvector, stopWeightVector, stopTrainOutputList,0,15,learningRate,lamda)
accuracyStop = measureAccuracy(weightArrayStop,stopTestAttrList,stopOutputList)
print("\nAccuracy of Logistic Regression excluding stop words: ", accuracyStop*100)
