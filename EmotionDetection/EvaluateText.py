# EvaluateText.py
#
# Maps words in input file based on wordList values
# and averages to find a value for the whole input line.
#
# emotion order: anger disgust fear joy sadness surprise

from pandas_ml import ConfusionMatrix
from WordFilter import WordFilter
from time import strftime
from math import log10
from tqdm import tqdm
import matplotlib.pyplot as plt
import tkMessageBox
import csv

def evaluate(textFile, valueFile=None, varStatusBar=None, varCmOutput=None, varOutput=None):
    timestamp = strftime("%Y-%m-%d:%H-%M-%S")
    reportFile = "./reports/" + timestamp + ".txt"
    outputFile = "./evaluations/" + timestamp + ".csv"
    statsFile = "./statistics/" + timestamp + ".txt"
    wf = WordFilter()
    totalReal = []
    totalPred = []
    with open("./data/Priors.csv", "r") as priorFile:
        print(priorFile)
        priors = priorFile.readline().strip().split(',')[1:]
        priors = [log10(float(x)) for x in priors]

    testSize=0
    lst = []
    lst.append(("Real Emotion", "Predicted Emotion", "Tweet"))
    for line in tqdm(textFile):
        testSize+=1

        lineID = line.split(',')[0]
        words = wf.filterWords(line)

        predValues = []
        unfound = []

        for word in words:
            try:
                values = evaluateWord(word)
            except IOError:
                varStatusBar.set("WordMap not found. Please train system first.")
                raise
            if values is not None:
                predValues.append(values)
            else:
                unfound.append(word)
        predValues = map(sum, zip(*predValues))
        predProb = map(sum, zip(priors, predValues))
        predEmotion = guessEmotion(predProb)
        valueFormat = ",".join("%.2f" % n for n in predValues)

        if valueFile:
            realValues = [float(i) for i in valueFile.readline().strip().split(',')[1:]]
            realEmotion = guessEmotion(realValues)
            if predEmotion != "No Words Found":
                totalReal.append(realEmotion)
                totalPred.append(predEmotion)

                if realEmotion!=predEmotion:
                    lst.append((realEmotion, predEmotion, line))
                    
        with open(outputFile, "a+") as output:
            output.write("{},{},{}\n".format(lineID, predEmotion, valueFormat))

        with open(reportFile, "a+") as report:
            report.write("{}\n".format(line))
            report.write("Filtered: {}\n".format(words))
            report.write("Words not found:{}\n".format(unfound))
            report.write("Emotion probabilities: {}\n".format(valueFormat))
            report.write("Predicted emotion: {}\n".format(predEmotion))
            if valueFile:
                report.write("Correct emotion: {}\n".format(realEmotion))
            report.write("-" * 70)
            report.write("\n")

    if valueFile:
        varStatusBar.set("Evaluation Complete.")
    
        with open('./data/RealPred.csv', 'w') as realpredFile:
            writer = csv.writer(realpredFile, delimiter=',')
            writer.writerows(lst)
            
        cm = ConfusionMatrix(totalReal, totalPred)        
        viewPlot = tkMessageBox.askyesno("Confusion Matrix", "View confusion matrix plot?")
        if viewPlot:
            normaliseData = tkMessageBox.askyesno("Confusion Matrix", "Normalise plot?")

            varOutput.set("Accuracy: " + str(cm.stats()['overall']['Accuracy']))
            varCmOutput.set("Confusion Matrix: \n" + str(cm.stats()['cm']))

            data=cm.stats()
            for key, value in data.items():
                print(key, value)
                
            cm.plot(normalized=normaliseData)
            plt.show()
            
        with open(statsFile, "w+") as report:
            report.seek(0)
            report.write(str(cm))
            report.write("\n")

def evaluateWord(word):
    values = None
    with open('./data/WordMap.csv', 'r') as wordList:
        for line in wordList:
            data = line.strip().split(',')
            if data[0] == word:
                values = [log10(float(i)) for i in data[1:]]

    return values


def checkAcc(predicted, actual):
    return [abs(pair[0] - pair[1]) for pair in zip(predicted, actual)]


def averageValue(array):
    transposed = zip(*array)
    averages = map(avg, transposed)
    return averages


def avg(array):
    if len(array) > 0:
        result = float(sum(array)) / len(array)
    else:
        result = None
    return result


def guessEmotion(array):
    array = zip(array, ["Empty", "Sadness", "Enthusiasm", "Neutral", "Worry", "Surprise", "Love", "Fun", "Hate", "Happiness", "Boredom", "Relief", "Anger"])
    output = "No Words Found"

    try:
        maxIndex = array.index(max(array))
    except ValueError:
        maxIndex = None

    if maxIndex is not None:
        output = array[maxIndex][1]
    return output


def buildReport(filename, data):
    filename = "./reports/" + strftime("%Y-%m-%d:%H%-M%-S") + ".csv"
    with open(filename, "w") as report:
        report.write(data)
