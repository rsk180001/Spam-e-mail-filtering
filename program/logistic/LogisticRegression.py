
import math
def gradientAscentApplication(inputvec, weights, output, check, total, eta, regularize):
    summation = 0
    i = 0
    j = 0
    w0 = 0.5
    gradientAscent = []

    weightmatrix = weights[0]
    for row in inputvec:
        numberOfParamerts = row
        for parameters in row:
            summation = (inputvec[i][j] * weightmatrix[j]) + summation
            j = j + 1
        try:
            denominator = float(math.exp(w0 + summation))
        except:
            denominator = w0 + summation

        den = denominator + 1
        output_value = 1
        if output[i] == 'TRUE':
            output_value = 1
        else:
            output_value = 0
        gradientAscent.insert(i, output_value - (denominator / den))
        i = i + 1
        j = 0

    i = 0
    j = 0
    sum = 0

    for each_paramaters in numberOfParamerts:

        for eachrow in inputvec:
            sum = sum + ((inputvec[j][i]) * gradientAscent[j])
            j = j + 1
        weightmatrix[i] = weightmatrix[i] + (eta * sum) - (eta * regularize * weightmatrix[i])
        i = i + 1
        j = 0

    if check <= total:
        gradientAscentApplication(inputvec, weights, output, check + 1, total, eta, regularize)
    return weightmatrix


def measureAccuracy(weightMatrix, testInputvec, testOutput):
    i = 0
    j = 0
    classSpam = 0
    classHam = 0
    for row in testInputvec:
        sum = 0
        for each_col in row:
            sum = sum + (weightMatrix[j] * testInputvec[i][j])
            j = j + 1
        if (sum > 0.5):
            value = "TRUE"
        else:
            value = "FALSE"
        if (value == testOutput[i]):
            classSpam = classSpam + 1
        else:
            classHam = classHam + 1
        i = i + 1
        j = 0
    return classSpam / (classHam + classSpam)
