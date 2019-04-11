# -*- coding: UTF-8 -*-
# ask_yes_no.py

from EmotionDetection import TrainOption
from EmotionDetection import TestOption
from EmotionDetection import WordFilter
from EmotionDetection import EvaluateText

from math import log10

from Tkinter import *
try:
    import Tkinter as tk
    import tkMessageBox, tkFileDialog, ttk
except ImportError:
    import tkinter as tk

import numpy as np
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
    
root=tk.Tk()
root.title("Emotion Detection Analysis")
root.state("zoomed")
root.configure(background="lightsteelblue")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

topFrame=Frame(root)
topFrame.configure(background="lightsteelblue")
topFrame.grid(row=0, column=0, sticky="nwe")

middleFrame=Frame(root)
middleFrame.configure(background="lightsteelblue")
middleFrame.grid(row=1, column=0, sticky="nw")

bottomFrame=Frame(root)
bottomFrame.configure(background="lightsteelblue")
bottomFrame.grid(row=2, columnspan=2, sticky="nsew")

trainBox=LabelFrame(middleFrame, relief=GROOVE, borderwidth=2, text="Training")
trainBox.configure(background="lightsteelblue")
trainBox.grid(row=0, sticky="nw")

testBox=LabelFrame(middleFrame, relief=GROOVE, borderwidth=2, text="Testing")
testBox.configure(background="lightsteelblue")
testBox.grid(row=0, sticky="nw")

guiBox=LabelFrame(middleFrame, relief=GROOVE, borderwidth=2, text="Evaluate Input")
guiBox.configure(background="lightsteelblue")

def runTrain():
    clearAll()
    answer = tkMessageBox.askyesno("Reset Data", "Reset training data?")
    
    if answer:
        trainBox.grid(row=0, column=1, rowspan=5, columnspan=5, padx=15, pady=15)

        btnTweetText=Button(trainBox, text='Tweet Text', command=selectTweetText, height=1, width=10, borderwidth=3)
        btnTweetText.configure(background="steelblue", fg="white")
        btnTweetText.grid(row=0, column=0, padx=15, pady=15)
        entryTweetText=Entry(trainBox, textvariable=varTweetText, width=80)
        entryTweetText.grid(row=0, column=2, padx=15, pady=15)

        btnTweetValues=Button(trainBox, text='Tweet Values', command=selectTweetValues, height=1, width=10, borderwidth=3)
        btnTweetValues.configure(background="steelblue", fg="white")
        btnTweetValues.grid(row=2, column=0, padx=15, pady=15)
        entryTweetValues=Entry(trainBox, textvariable=varTweetValues, width=80)
        entryTweetValues.grid(row=2, column=2, padx=15, pady=15)

        btnTrain=Button(trainBox, text='Train', command=lambda:TrainOption.startTraining(varStatusBar, varTweetText, varTweetValues), height=1, width=10, borderwidth=3)
        btnTrain.configure(background="steelblue", fg="white")
        btnTrain.grid(row=3, column=3, padx=15, pady=15)

def runTest():
    clearAll()
    
    testBox.grid(row=0, column=1, rowspan=5, columnspan=5, padx=15, pady=15)

    btnTestText=Button(testBox, text='Tweet Text', command=selectTestText, height=1, width=10, borderwidth=3)
    btnTestText.configure(background="steelblue", fg="white")
    btnTestText.grid(row=0, column=0, padx=15, pady=15)
    entryTestText=Entry(testBox, textvariable=varTestText, width=80)
    entryTestText.grid(row=0, column=2, padx=15, pady=15)

    btnTestValues=Button(testBox, text='Tweet Values', command=selectTestValues, height=1, width=10, borderwidth=3)
    btnTestValues.configure(background="steelblue", fg="white")
    btnTestValues.grid(row=2, column=0, padx=15, pady=15)
    entryTestValues=Entry(testBox, textvariable=varTestValues, width=80)
    entryTestValues.grid(row=2, column=2, padx=15, pady=15)

    btnTest=Button(testBox, text='Test', command=lambda:TestOption.startTesting(varStatusBar, varOutput, varCmOutput, varTestText, varTestValues), height=1, width=10, borderwidth=3)
    btnTest.configure(background="steelblue", fg="white")
    btnTest.grid(row=3, column=3, padx=15, pady=15)

    lblOutput=Label(testBox, textvariable=varOutput, font=('Consolas', 10), anchor="w")
    lblOutput.configure(background="lightsteelblue")
    lblOutput.grid(row=4, column=0, sticky='w')
    
    lblCmOutput=Label(testBox, textvariable=varCmOutput, font=('Consolas', 10), anchor="w")
    lblCmOutput.configure(background="lightsteelblue")
    lblCmOutput.grid(row=5, column=0, sticky='w')

def evaluateInput():
    clearAll()
    
    guiBox.grid(row=1, column=1, rowspan=5, columnspan=5, padx=15, pady=15)
    
    lblGuiInput=Label(guiBox, text="Input text:", font=(None, 15))
    lblGuiInput.configure(background="lightsteelblue")
    lblGuiInput.grid(row=0, sticky="nsew", pady=5)

    lblGuiPred=Label(guiBox, text="Predicted:", font=(None, 15))
    lblGuiPred.configure(background="lightsteelblue")
    lblGuiPred.grid(row=1)

    entryGuiInput = Entry(guiBox, textvariable=varGuiInput, font=(None, 15), width=50)
    entryGuiInput.grid(row=0, column=1, sticky="nsew", pady=10, padx=(0, 10))
    
    lblGuiOutput = Label(guiBox, textvariable=varGuiOutput, font=(None, 15))
    lblGuiOutput.configure(background="lightsteelblue")
    lblGuiOutput.grid(row=1, column=1, sticky="W")

    btnClear=Button(guiBox, text='Clear', command=clearEvaluateGUI, font=(None, 10))
    btnClear.configure(background="steelblue", fg="white")
    btnClear.grid(row=2, column=0, stick="nsew", pady=(8, 2), padx=10)
    
    btnPredict=Button(guiBox, text='Predict', command=predictEmotion, font=(None, 15))
    btnPredict.configure(background="steelblue", fg="white")
    btnPredict.grid(row=2, column=1, rowspan=2, sticky="nsew", pady=9, padx=20)

def selectTweetText():
    varTweetText.set(tkFileDialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select file [tweet text]'))

def selectTweetValues():
    varTweetValues.set(tkFileDialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select file [tweet values]'))

def selectTestText():
    varTestText.set(tkFileDialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select file [test text]'))

def selectTestValues():
    varTestValues.set(tkFileDialog.askopenfilename(filetypes=[('.csvfiles', '.csv')], title='Select file [test values]'))

def clearEvaluateGUI():
    varStatusBar.set("")
    varGuiInput.set("")
    varGuiOutput.set("")
    
def predictEmotion():
    varStatusBar.set("")
    
    with open("./data/Priors.csv", "r") as priorFile:
            priors = priorFile.readline().strip().split(',')[1:]
            priors = [log10(float(x)) for x in priors]
    predValues = []
    unfound = []

    wf = WordFilter.WordFilter()
    words = varGuiInput.get()
    #print "Input:", words
    words = wf.filterWords(words)

    #print "Tokens:", words
    for word in words:
        try:
            values = EvaluateText.evaluateWord(word)
        except IOError:
            varStatusBar.set("WordMap not found. Please train system first.")
            raise
        if values is not None:
            predValues.append(values)
        else:
            unfound.append(word)

    predValues = map(sum, zip(*predValues))
    predProb = map(sum, zip(priors, predValues))
    predEmotion = EvaluateText.guessEmotion(predProb)
    varGuiOutput.set(predEmotion)

    #print "Unfound:", unfound
    print "Prob:",', '.join([('%.2f') %x for x in predProb])
    
    max=10
    max=getBarScale(predProb)
            
    str="Input:", words, "Tokens:", words, "Unfound:", unfound, " ", "Prob:",', '.join([('%.2f') %abs(float("{0:.2f}".format(x))+max) for x in predProb])
    varStatusBar.set(str)
    
    iterable = ([abs(float("{0:.2f}".format(x))+max) for x in predProb])
    emotions=np.fromiter(iterable, float)
    
    objects = ("Empty", "Sadness", "Enthusiasm", "Neutral", "Worry", "Surprise", "Love", "Fun", "Hate", "Happiness", "Boredom", "Relief", "Anger")
    y_pos = np.arange(len(objects)) 

    fig = plt.figure(figsize=(13, 6))
    plt.bar(np.asarray(y_pos, dtype='float'), emotions, align='center', alpha=0.5, color="blue")
    plt.xticks(y_pos, objects)
    plt.yticks([])
    
    canvas = FigureCanvasTkAgg(fig, master=guiBox)
    canvas.get_tk_widget().grid(row=4, columnspan=2)
    canvas.draw()

def getBarScale(predProb):
    max=10
    for x in predProb:
        if abs(x)<80:
            max=80
        elif abs(x)<70:
            max=70
        elif abs(x)<60:
            max=60
        elif abs(x)<50:
            max=50
        elif abs(x)<40:
            max=40            
        elif abs(x)<30:
            max=30            
        elif abs(x)<20:
            max=20            
        elif abs(x)<10:
            max=10
    return max
            
def exitEmotionDetection():
    root.destroy()
        
def clearAll():
    varStatusBar.set("")

    trainBox.grid_forget()
    varTweetText.set("")
    varTweetValues.set("")

    testBox.grid_forget()
    varTestText.set("")
    varTestValues.set("")

    guiBox.grid_forget()
    varGuiInput.set("")
    varGuiOutput.set("")

    varCmOutput.set("")
    varOutput.set("")
    
trainButton=Button(topFrame, text='Train', command=runTrain, height=3, width=55, borderwidth=3)
trainButton.configure(background="steelblue", fg="white")
trainButton.grid(row=0, column=0)

testButton=Button(topFrame, text='Test', command=runTest, height=3, width=55, borderwidth=3)
testButton.configure(background="steelblue", fg="white")
testButton.grid(row=0, column=1)

evaluateUserInputButton=Button(topFrame, text='Evaluate User Input', command=evaluateInput, height=3, width=55, borderwidth=3, wraplength=80)
evaluateUserInputButton.configure(background="steelblue", fg="white")
evaluateUserInputButton.grid(row=0, column=2)

exitButton=Button(topFrame, text='Exit', command=exitEmotionDetection, height=3, width=55, borderwidth=3)
exitButton.configure(background="steelblue", fg="white")
exitButton.grid(row=0, column=3)

varStatusBar=StringVar()
varStatusBar.set("")
statusBar = Label(bottomFrame, textvariable=varStatusBar, relief=SUNKEN, anchor=W, background="lightsteelblue", foreground="navy", borderwidth=1)
statusBar.grid(row=0, sticky="new")

varTweetText=StringVar()
varTweetText.set("")

varTweetValues=StringVar()
varTweetValues.set("")

varTestText=StringVar()
varTestText.set("")

varTestValues=StringVar()
varTestValues.set("")

varGuiInput=StringVar()
varGuiInput.set("")

varGuiOutput=StringVar()
varGuiOutput.set("")

varCmOutput=StringVar()
varCmOutput.set("")

varOutput=StringVar()
varOutput.set("")

fig = plt.figure(figsize=(13, 6))   
canvas = FigureCanvasTkAgg(fig, master=guiBox)

root.mainloop()
