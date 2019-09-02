from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import random


def swapSides():
    global test

    temp = test[2]
    test[2] = test[3]
    test[3] = temp

    newQuestion()


def saveTest():
    print(test)
    with open(filepath, mode='w') as file:
        file.write(test[0]+'/'+test[1])
        file.write(str(test[4])+'\n')
        for i in range(len(test[2])):
            for j in range(len(test[2][i])):
                file.write(test[2][i][j])
                if j < len(test[2][i])-1:
                    file.write(',')
            file.write('/')
            for j in range(len(test[3][i])):
                file.write(test[3][i][j])
                if j < len(test[3][i])-1:
                    file.write(',')
            file.write('\n')


def newQuestion():
    global questionPlace
    questionPlace = random.randint(0, len(test[2])-1)
    newQuestion = test[2][questionPlace][0]
    question.set(newQuestion)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        saveTest()
        root.destroy()


def submitAnswer(uselessArgument):
    global score
    if answerEntry.get().lower() in test[3] [questionPlace]:
        score += 1
        currentScore.set('Score: %s' % (score))
    else:
        score = 0
        currentScore.set('Score: %s' % (score))
    if score > test[4]:
        test[4] = score
        highScore.set('High score: %d' % (test[4]))
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

    highScore = int(file[1].strip('\n'))
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
    global filepath
    saveTest()
    gotfile = False
    filepath = None
    while not gotfile:
        filepath = filedialog.askopenfilename(title='Select test file')
        if getExtension(filepath) == '.tst':
            gotfile = True
        else:
            messagebox.showinfo("ERROR: unrecognized file", "We are sorry but files with the '%s' appendix are not supported, we support only '.tst' files." % (getExtension(filepath)))
    test = list(formatTest(filepath))
    newQuestion()
    currentScore.set('Score: %s' % score)
    highScore.set('High score: %d' % test[4])


def makeMenu(root):
    menu = Menu(root)
    root.config(menu=menu)

    menu.add_command(label='Open', command=openTest)
    menu.add_command(label='Switch sides', command=swapSides)

    return menu


def makeRoot():
    root = Tk()
    root.geometry('500x400')
    root.title('Test Me')
    root.configure(bg="gray")
    return root


root = makeRoot()
filepath = 'programfiles/default.tst'
test = list(formatTest('programfiles/default.tst'))
questionPlace = 0
score = 0

currentScore = StringVar()
highScore = StringVar()
question = StringVar()
timeMultiplier = StringVar()

anotherSpacingLabel = Label(bg='gray', padx=5)
currentScoreLabel = Label(root, textvariable=currentScore, bg='gray')
highScoreLabel = Label(root, textvariable=highScore, bg='gray')
questionLabel = Label(root, textvariable=question, width=30)
spacingLabel = Label(bg='gray', padx=10)
answerEntry = Entry(root, width=30)
answerButton = Button(root, text='submit', command=submitAnswer)
timeMultiplierLabel = Label(root, textvariable=timeMultiplier, bg='gray')

anotherSpacingLabel.grid(row=0, column=0)
currentScoreLabel.grid(row=0, column=1, columnspan=2, sticky=W)
highScoreLabel.grid(row=0, column=4, columnspan=2, sticky=E)
questionLabel.grid(row=1, column=2, sticky=W)
spacingLabel.grid(row=1, column=3)
answerEntry.grid(row=1, column=4, sticky=E)
answerButton.grid(row=1, column=5, sticky=W)
timeMultiplierLabel.grid(row=2, column=1, columnspan=5)

currentScore.set('Score: %s' %(score))
highScore.set('High score: %d' %(test[4]))
question.set('question will appear here')
timeMultiplier.set('Time multiplier is: 0')

root.protocol("WM_DELETE_WINDOW", on_closing)
answerEntry.bind('<Return>', submitAnswer)

menu = makeMenu(root)

root.mainloop()