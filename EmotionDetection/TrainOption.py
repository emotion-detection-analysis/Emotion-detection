from WordMap import buildWordMap

import tkMessageBox, csv

# Training Program, builds map of words and emotion values from annotated corpus
def train(text, values, varStatusBar):
    text=text.split('/')[-1]
    values=values.split('/')[-1]
    
    try:
        varStatusBar.set("Loading input values into WordMap...")
        with open("./data/" + text, 'r') as textFile:
            with open("./data/" + values, 'r') as valueFile:
                buildWordMap(True, textFile, valueFile, varStatusBar)

    except IOError:
        varStatusBar.set("File not found.")

def startTraining(varStatusBar, varTweetText, varTweetValues):
    if varTweetText.get()!="" and varTweetValues.get()!="":
        tweettextfile=varTweetText.get()
        tweetvaluesfile=varTweetValues.get()

        input_file = open(tweetvaluesfile,"r+")
        reader_file = csv.reader(input_file)

        train(tweettextfile, tweetvaluesfile, varStatusBar)
