from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import time
import random


def newQuestion():
    global questionPlace
    questionPlace = random.randint(0, len(test[2])-1)
    newQuestion = test[2][questionPlace][0]
    question.set(newQuestion)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def submitAnswer():
    global score
    if answerEntry.get().lower() in test[3] [questionPlace]:
        score += 1
        currentScore.set('Score: %s' % (score))
    else:
        score = 0
        currentScore.set('Score: %s' % (score))
    if score > int(test[4]):
        test[4] = score
        highScore.set('High score: %s' % (test[4]))
    answerEntry.delete(0, 'end')
    newQuestion()


def formatTest(filepath):
    global score
    with open(filepath) as file:
        file = file.readlines()

    nazev1 = file[0].split('/')[0]
    nazev2 = file[0].split('/')[1]

    sloupec1 = []
    sloupec2 = []

    highScore = file[1].strip('/n')
    score = 0

    for line in file[2:]:
        currentline = line.strip('\n')
        currentline = currentline.split('/')
        sloupec1.append(currentline[0].split(','))
        sloupec2.append(currentline[1].split(','))

    return nazev1, nazev2, sloupec1, sloupec2, highScore


def getExtension(filename):  # returns the last four characters in a filename as a string
    return filename[-4:None]


def openTest():
    global test
    gotfile = False
    filepath = None
    while not gotfile:
        filepath = filedialog.askopenfilename(title='Select test file')
        if getExtension(filepath) == '.tst':
            gotfile = True
        else:
            messagebox.showinfo("CHYBA: nerozeznany soubor", "Omlovame se ale soubory tupu '%s' nepodporujeme, podporujeme pouze soubory typu '.tst'" % (getExtension(filepath)))
    test = list(formatTest(filepath))
    newQuestion()


def makeMenu(root):
    menu = Menu(root)
    root.config(menu=menu)

    menu.add_command(label='Open', command=openTest)
    menu.add_command(label='Switch sides', command=None)

    return menu


def makeRoot():
    root = Tk()
    root.geometry('500x400')
    root.title('Vyzkousej me')
    root.configure(bg="gray")
    return root


root = makeRoot()
menu = makeMenu(root)
test = list(formatTest('programfiles/default.tst'))
questionPlace = 0
score = 0

currentScore = StringVar()
highScore = StringVar()
question = StringVar()
timeMultiplier = StringVar()

currentScoreLabel = Label(root, textvariable=currentScore, bg='gray')
highScoreLabel = Label(root, textvariable=highScore, bg='gray')
questionLabel = Label(root, textvariable=question)
answerEntry = Entry(root)
answerButton = Button(root, text='submit', command=submitAnswer)
timeMultiplierLabel = Label(root, textvariable=timeMultiplier, bg='gray')

currentScoreLabel.grid(row=0, column=0, columnspan=2, sticky=W)
highScoreLabel.grid(row=0, column=2, columnspan=2, sticky=E)
questionLabel.grid(row=1, column=1, sticky=W)
answerEntry.grid(row=1, column=2, sticky=E)
answerButton.grid(row=1, column=3, sticky=W)
timeMultiplierLabel.grid(row=2, column=0, columnspan=4)


currentScore.set('Score: %s' %(score))
highScore.set('High score: %s' %(test[4]))
question.set('question will appear here')
timeMultiplier.set('Time multiplier is: 0')

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
