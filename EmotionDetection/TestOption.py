from EvaluateText import evaluate

import csv

def test(text, values, varStatusBar, varCmOutput, varOutput):
    text=text.split('/')[-1]
    values=values.split('/')[-1]

    try:
        varStatusBar.set("Running text evaluation...")
        with open("./data/" + text, 'r+') as textFile:
            with open("./data/" + values, 'r+') as valueFile:
                print(valueFile)
                evaluate(textFile, valueFile, varStatusBar, varCmOutput, varOutput)

    except IOError:
        varStatusBar.set("File not found.")

def startTesting(varStatusBar, varOutput, varCmOutput, varTestText, varTestValues):    
    if varTestText.get()!="" and varTestValues.get()!="":
        testtextfile=varTestText.get()
        testvaluesfile=varTestValues.get()

        input_file = open(testvaluesfile,"r+")
        reader_file = csv.reader(input_file)
        
        test(testtextfile, testvaluesfile, varStatusBar, varCmOutput, varOutput)
