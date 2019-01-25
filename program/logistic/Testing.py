        
import os

output = [];
attrList = [[]];
spamAttrCnt = []
hamAttrCnt = []
bagOfWords = [];
frequency = [];
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


def test(testList, hamTest, spamTest):    
    spamFiles = Getfilesinfolder(spamTest)
    hamFiles = Getfilesinfolder(hamTest)
    spamArray = getDataFromFiles(spamFiles)
    hamArray = getDataFromFiles(hamFiles)
    rows, position = getSpamClassData(spamArray, 0)
    getHamClassData(hamArray, rows, position)
    weightvector, inputvector = rephraseTestData(testList)
    return row_values, attrList, output, inputvector

def getSpamClassData(allSpamFiles, position):
    rows = 1;
    tempValues = []
    for mail in allSpamFiles:
        words = mail.split()
        tempValues = []

        attrTempValue = []
        if rows > 1:
            attrList.insert(rows - 1, attrTempValue)
            row_values.insert(rows - 1, tempValues)
        iterator = 0;
        for word in words:

            if (len(word) <= 1) or (word == 'Subject:'):
                continue

            try:

                index_location = bagOfWords.index(word)
                spamAttrCnt[index_location] = spamAttrCnt[index_location] + 1
                frequency[index_location] = frequency[index_location] + 1
                try:
                    index = row_values[rows - 1].index(word)
                    attrList[rows - 1][index] = attrList[rows - 1][index] + 1
                except:
                    iterator = iterator + 1
                    row_values[rows - 1].insert(iterator, word)
                    attrList[rows - 1].insert(iterator, 1);
                    
            except:
                spamAttrCnt.insert(position, 1);
                row_values[rows - 1].insert(iterator, word)
                attrList[rows - 1].insert(iterator, 1);
                bagOfWords.insert(position, word)
                frequency.insert(position, 1);
                hamAttrCnt.insert(position, 0);
                position = position + 1;
                iterator = iterator + 1

        output.insert(rows, "FALSE")
        rows = rows + 1;

    return len(allSpamFiles) + 1, position


def getHamClassData(allHamFiles, rows, position):
    tempValues = []
    for mail in allHamFiles:
        a = mail.split()
        tempValues = []

        attrTempValue = []
        if rows > 1:
            attrList.insert(rows - 1, attrTempValue)
            row_values.insert(rows - 1, tempValues)
        iterator = 0;
        for word in a:

            if (len(word) <= 1) or (word == 'Subject:'):
                continue

            try:
                index_location = bagOfWords.index(word)
                hamAttrCnt[index_location] = hamAttrCnt[index_location] + 1
                frequency[index_location] = frequency[index_location] + 1
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
                frequency.insert(position, 1);
                hamAttrCnt.insert(position, 1);
                position = position + 1;
                iterator = iterator + 1

        output.insert(rows, "TRUE")
        rows = rows + 1;



def rephraseTestData(testList):
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
        for word in testList:
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


output_list = [];
Attribute_list = [[]];
negative_attribute_count = []
positive_attribute_count = []
wordlist = [];
wordcount = [];
position = 0;
row_count = 0;
row_values = [[]]

def getSpamClassDataExcludingStopWords(list, position, stop_words):
    row_count = 1;
    row_value_temp = []
    for each_data in list:
        words_inlist = each_data.split()
        row_value_temp = []

        attribute_temp_value = []
        if row_count > 1:
            Attribute_list.insert(row_count - 1, attribute_temp_value)
            row_values.insert(row_count - 1, row_value_temp)
        row_itteration = 0;
        for words in words_inlist:
            '''To exclude stop words'''
            try:
                stop_index = stop_words.index(words)
                continue
            except:
                pass
            if (len(words) <= 1) or (words == 'Subject:'):
                continue

            try:

                index_location = wordlist.index(words)
                negative_attribute_count[index_location] = negative_attribute_count[index_location] + 1
                wordcount[index_location] = wordcount[index_location] + 1
                try:
                    row_index = row_values[row_count - 1].index(words)
                    Attribute_list[row_count - 1][row_index] = Attribute_list[row_count - 1][row_index] + 1
                except:
                    row_values[row_count - 1].insert(row_itteration, words)
                    Attribute_list[row_count - 1].insert(row_itteration, 1);
                    row_itteration = row_itteration + 1
            except:

                wordlist.insert(position, words)
                wordcount.insert(position, 1);
                positive_attribute_count.insert(position, 0);
                negative_attribute_count.insert(position, 1);
                row_values[row_count - 1].insert(row_itteration, words)
                Attribute_list[row_count - 1].insert(row_itteration, 1);
                position = position + 1;
                row_itteration = row_itteration + 1

        output_list.insert(row_count, "FALSE")
        row_count = row_count + 1;

    return len(list) + 1, position


def getHamClassDataExcludingStopWords(list, row_count, position, stop_words):
    row_value_temp = []
    for each_data in list:
        words_inlist = each_data.split()
        row_value_temp = []

        attribute_temp_value = []
        if row_count > 1:
            Attribute_list.insert(row_count - 1, attribute_temp_value)
            row_values.insert(row_count - 1, row_value_temp)
        row_itteration = 0;
        for words in words_inlist:
            '''To exclude stop words'''
            try:
                stop_index = stop_words.index(words)
                continue
            except:
                pass
            if (len(words) <= 1) or (words == 'Subject:'):
                continue

            try:
                index_location = wordlist.index(words)
                positive_attribute_count[index_location] = positive_attribute_count[index_location] + 1
                wordcount[index_location] = wordcount[index_location] + 1
                try:
                    row_index = row_values[row_count - 1].index(words)
                    Attribute_list[row_count - 1][row_index] = Attribute_list[row_count - 1][row_index] + 1
                except:
                    row_values[row_count - 1].insert(row_itteration, words)
                    Attribute_list[row_count - 1].insert(row_itteration, 1);
                    row_itteration = row_itteration + 1
            except:

                wordlist.insert(position, words)
                wordcount.insert(position, 1);
                positive_attribute_count.insert(position, 1);
                negative_attribute_count.insert(position, 0);
                row_values[row_count - 1].insert(row_itteration, words)
                Attribute_list[row_count - 1].insert(row_itteration, 1);
                position = position + 1;
                row_itteration = row_itteration + 1

        output_list.insert(row_count, "TRUE")
        row_count = row_count + 1;


def rephraseTestDataForStop(wordlist_test):
    inputvector = [[]]
    weightvector = [[]]
    i = 0
    j = 0
    for row in Attribute_list:
        if i >= 1:
            samplematrix = []
            weightvector.insert(i, samplematrix)
            samplevector = []
            inputvector.insert(i, samplevector)
        for word in wordlist_test:
            weightvector[i].insert(j, 0)
            try:
                index = row_values[i].index(word)
                value = Attribute_list[i][index];
                inputvector[i].insert(j, value);
            except:
                inputvector[i].insert(j, 0)
            j = j + 1;
        i = i + 1;
        j = 0;
    return weightvector, inputvector


def test_stop(stop_word, stop_wordlist, test_ham_folder, test_spam_folder):

    spam_list = Getfilesinfolder(test_spam_folder)
    ham_list = Getfilesinfolder(test_ham_folder)
	
    spam_array = getDataFromFiles(spam_list)
    ham_array = getDataFromFiles(ham_list)
	
    row_count, position = getSpamClassDataExcludingStopWords(spam_array, 0, stop_word)
	
    getHamClassDataExcludingStopWords(ham_array, row_count, position, stop_word)
	
    weightvector, inputvector = rephraseTestDataForStop(stop_wordlist)
	
    return row_values, Attribute_list, output_list, inputvector
    

