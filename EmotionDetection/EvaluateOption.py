from EvaluateText import evaluate

def evaluate():
    text = input("Text file: ")

    try:
        print("Running text evaluation...\n")
        with open("./data/" + text, 'r') as textFile:
            evaluate(textFile)

    except IOError:
        print("File not found. Returning to main menu...\n")
