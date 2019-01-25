
import os

spamOrHamClass = [];
attrList = [[]];
spamAttrCnt = []
hamAttrCnt = []
bagOfWords = [];
wordFrequency = [];
position = 0;
rows = 0;
row_values = [[]]


def Getfilesinfolder(path):
    fileNames = []
    for dirEntries in os.listdir(path):
        dirEntryPath = os.path.join(path,dirEntries)
        if os.path.isfile(dirEntryPath):
            fileNames.append(dirEntryPath)
    return fileNames;

def getDataFromFiles(list):
    data = []
    for files in list:
        with open(files, 'r') as myFile:
            try:
                content = myFile.read()
            except:
                pass
            data.append(content);
    return data;

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

def training(trainHamFolder, trainSpamFolder):

    spamFiles = Getfilesinfolder(trainSpamFolder)
    hamFiles = Getfilesinfolder(trainHamFolder)

    spamArray = getDataFromFiles(spamFiles)
    hamArray = getDataFromFiles(hamFiles)

    rows, position = trainSpamClassData(spamArray, 0)
    spamAttrList = len(attrList)
    trainHamClassData(hamArray, rows, position)
    total = len(attrList)
    hamAttrList = total - spamAttrList
    weights, wordFrequency = rephraseTrainingData()

    return weights, wordFrequency, hamAttrList, spamAttrList, spamAttrCnt, hamAttrCnt, bagOfWords, wordFrequency, spamOrHamClass

def trainHamClassData(allHamFiles, rows, position):
    tempValues = []
    for eachMail in allHamFiles:
        words = eachMail.split()
        tempValues = []
        iterator = 0;
        row_values.insert(rows - 1, tempValues)

        attrTempValue = []
        if rows > 1:
            attrList.insert(rows - 1, attrTempValue)
        
        for word in words:

            if (len(word) <= 1) or (word == 'Subject:'):
                continue

            try:
                index_location = bagOfWords.index(word)
                hamAttrCnt[index_location] = hamAttrCnt[index_location] + 1
                wordFrequency[index_location] = wordFrequency[index_location] + 1
                try:
                    index = row_values[rows - 1].index(word)
                    attrList[rows - 1][index] = attrList[rows - 1][index] + 1
                except:
                    row_values[rows - 1].insert(iterator, word)
                    attrList[rows - 1].insert(iterator, 1);
                    iterator = iterator + 1
            except:
                spamAttrCnt.insert(position, 0);
                row_values[rows - 1].insert(iterator, word)
                attrList[rows - 1].insert(iterator, 1);
                bagOfWords.insert(position, word)
                wordFrequency.insert(position, 1);
                hamAttrCnt.insert(position, 1);
                position = position + 1;
                iterator = iterator + 1

        spamOrHamClass.insert(rows, "TRUE")
        rows = rows + 1;


def rephraseTrainingData():

    feature = [[]]
    weights = [[]]
    i = 0
    j = 0
    for row in attrList:
        if i >= 1:
            samplematrix = []
            weights.insert(i, samplematrix)
            samplevector = []
            feature.insert(i, samplevector)
        for word in bagOfWords:
            weights[i].insert(j, 0)
            try:
                index = row_values[i].index(word)
                value = attrList[i][index];
                feature[i].insert(j, value);
            except:
                feature[i].insert(j, 0)
            j = j + 1;
        i = i + 1;
        j = 0;
    return weights, feature


def trainSpamClassData(allSpamFiles, position):
    
    rows = 1;					
    tempValues = []
    for mail in allSpamFiles:
        words = mail.split()
        tempValues = []
        row_values.insert(rows - 1, tempValues)
        attrTempValue = []
        if rows > 1:
            attrList.insert(rows - 1, attrTempValue)
        iterator = 0;		
        for word in words:

            if (len(word) <= 1) or (word == 'Subject:'):
                continue

            try:
                index_location = bagOfWords.index(word)
                spamAttrCnt[index_location] = spamAttrCnt[index_location] + 1  
                wordFrequency[index_location] = wordFrequency[index_location] + 1
                try:
                    index = row_values[rows - 1].index(word)
                    attrList[rows - 1][index] = attrList[rows - 1][index] + 1
                except:
                    row_values[rows - 1].insert(iterator, word)
                    attrList[rows - 1].insert(iterator, 1);
                    iterator = iterator + 1
            except:
                spamAttrCnt.insert(position, 1);			
                row_values[rows - 1].insert(iterator, word)	
                attrList[rows - 1].insert(iterator, 1);	
                bagOfWords.insert(position, word)
                wordFrequency.insert(position, 1);
                hamAttrCnt.insert(position, 0);		
                position = position + 1;									
                iterator = iterator + 1
        spamOrHamClass.insert(rows, "FALSE")
        rows = rows + 1;						

    return len(allSpamFiles) + 1, position


output_list=[];
Attribute_list=[[]];
negative_attribute_count=[]
positive_attribute_count=[]
wordlist=[];
wordcount=[];
place=0;
row_count=0;
arrayOfWords=[[]]

    

def trainSpamClassDataExcludingStopWords(list,place,stop_words):
    
    row_count=1;
    row_value_temp=[]
    for each_data in list:
        words_inlist=each_data.split()
        row_value_temp=[]
        arrayOfWords.insert(row_count-1,row_value_temp)
        attribute_temp_value=[]
        if row_count>1:
           Attribute_list.insert(row_count-1, attribute_temp_value)
        row_itteration=0;
        for words in words_inlist:
           
            try:
                stop_index=stop_words.index(words)
                continue
            except:
                pass
            if(len(words)<=1)or(words=='Subject:'):
                continue
                
            try:
            
                index_location=wordlist.index(words)
                negative_attribute_count[index_location]=negative_attribute_count[index_location]+1
                wordcount[index_location]=wordcount[index_location]+1
                try:
                    row_index=arrayOfWords[row_count-1].index(words)
                    Attribute_list[row_count-1][row_index]=Attribute_list[row_count-1][row_index]+1
                except:
                    arrayOfWords[row_count-1].insert(row_itteration, words)
                    Attribute_list[row_count-1].insert(row_itteration,1);
                    row_itteration=row_itteration+1
            except:
               
                wordlist.insert(place, words)
                wordcount.insert(place, 1);
                positive_attribute_count.insert(place, 0);
                negative_attribute_count.insert(place, 1);
                arrayOfWords[row_count-1].insert(row_itteration, words)
                Attribute_list[row_count-1].insert(row_itteration,1);
                place=place+1;
                row_itteration=row_itteration+1
                
        
        output_list.insert(row_count, "FALSE")
        row_count=row_count+1;
        
    return len(list)+1,place  
  
def trainHamClassDataExcludingStopWords(list,row_count,place,stop_words):
       
    row_value_temp=[]
    for each_data in list:
        words_inlist=each_data.split()
        row_value_temp=[]
        arrayOfWords.insert(row_count-1,row_value_temp)
        attribute_temp_value=[]
        if row_count>1:
           Attribute_list.insert(row_count-1, attribute_temp_value)
        row_itteration=0;
        for words in words_inlist:
            try:
                stop_index=stop_words.index(words)
                continue
            except:
                pass
            if(len(words)<=1)or(words=='Subject:'):
                continue
                
            try:
                index_location=wordlist.index(words)
                positive_attribute_count[index_location]=positive_attribute_count[index_location]+1
                wordcount[index_location]=wordcount[index_location]+1
                try:
                    row_index=arrayOfWords[row_count-1].index(words)
                    Attribute_list[row_count-1][row_index]=Attribute_list[row_count-1][row_index]+1
                except:
                    arrayOfWords[row_count-1].insert(row_itteration, words)
                    Attribute_list[row_count-1].insert(row_itteration,1);
                    row_itteration=row_itteration+1
            except:
               
                wordlist.insert(place, words)
                wordcount.insert(place, 1);
                positive_attribute_count.insert(place, 1);
                negative_attribute_count.insert(place, 0);
                arrayOfWords[row_count-1].insert(row_itteration, words)
                Attribute_list[row_count-1].insert(row_itteration,1);
                place=place+1;
                row_itteration=row_itteration+1
                
        
        output_list.insert(row_count, "TRUE")
        row_count=row_count+1;
        
            
def rephraseTrainingDataForStop():
    
    inputvector=[[]]
    weightvector=[[]]
    i=0
    j=0
    for row in Attribute_list:
        if i>=1:
            samplematrix=[]
            weightvector.insert(i,samplematrix)
            samplevector=[]
            inputvector.insert(i,samplevector)
        for word in wordlist:
            weightvector[i].insert(j,0)
            try:
                index=arrayOfWords[i].index(word)
                value=Attribute_list[i][index];
                inputvector[i].insert(j,value);
            except:
                inputvector[i].insert(j,0)
            j=j+1;
        i=i+1;
        j=0;
    return weightvector,inputvector
	
def training_stop(stop_words,training_ham_folder,training_spam_folder):
    spam_list = Getfilesinfolder(training_spam_folder);
    ham_list = Getfilesinfolder(training_ham_folder);
	
    spam_array = getDataFromFiles(spam_list);
    ham_array = getDataFromFiles(ham_list);
	
    row_count,place = trainSpamClassDataExcludingStopWords(spam_array,0,stop_words);
    negative = len(Attribute_list)
    trainHamClassDataExcludingStopWords(ham_array,row_count,place,stop_words);
    total = len(Attribute_list)
    positive = total-negative
    weightmatrix,inputmatrix = rephraseTrainingDataForStop()
	
    return weightmatrix,inputmatrix,positive,negative,negative_attribute_count,positive_attribute_count,wordlist,wordcount,output_list


