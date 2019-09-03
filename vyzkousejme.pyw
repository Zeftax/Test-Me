from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import random
import time


def swapSides(): # prohodi sloupce v souboru testu (a tim i zmeni co je otazka a co odpoved)
    global test
    global score

    temp = test[0]
    test[0] = test[1]
    test[1] = temp

    score = 0
    currentScore.set('Score: %s' % score)
    newQuestion()


def saveTest(): # ulozi soubor testu
    print(test)
    print(filepath)
    with open(filepath, mode='w', encoding = "UTF-8") as file:
        file.write(str(test[2])+'\n')
        for i in range(len(test[0])):
            for j in range(len(test[0][i])):
                file.write(test[0][i][j])
                if j < len(test[0][i])-1:
                    file.write(',')
            file.write('/')
            for j in range(len(test[1][i])):
                file.write(test[1][i][j])
                if j < len(test[1][i])-1:
                    file.write(',')
            file.write('\n')


def newQuestion(): # nastavi novou otazku
    global questionPlace
    global timeAsked
    questionPlace = random.randint(0, len(test[0])-1)
    newQuestion = test[0][questionPlace][0]
    question.set(newQuestion)
    timeAsked = time.time()-1


def on_closing(): #zobrazi se pri zavirani programu, pokud se uzivatel rozhodne program zavrit, tak prvne ulozi highscore
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        saveTest()
        root.destroy()


def submitAnswer(uselessArgument): # precte pole pro zadani odpovedi, zhodnoti ji, a vhodnym zpusobem zmeni score a highscore 
    global score
    if answerEntry.get().lower() in test[1] [questionPlace]:
        score += timeMultiplier
        currentScore.set('Score: %s' % (score))
    else:
        score = 0
        currentScore.set('Score: %s' % (score))
    if score > test[2]:
        test[2] = score
        highScore.set('High score: %s' % (test[2]))
    answerEntry.delete(0, 'end')
    newQuestion()
    currentScore.set('Score: %s' % round(score, 2))
    highScore.set('High score: %s' % round(test[2], 2))


def formatTest(filepath): # precte soubor a formatuje jej do listu test
    global score
    with open(filepath, encoding = "UTF-8") as file:
        file = file.readlines()

    sloupec1 = []
    sloupec2 = []

    highScore = float(file[0].strip('\n'))
    score = 0

    for line in file[1:]:
        currentline = line.strip('\n')
        currentline = currentline.split('/')
        sloupec1.append(currentline[0].split(','))
        sloupec2.append(currentline[1].split(','))

    return sloupec1, sloupec2, highScore


def getExtension(filename):  # vrati posledni ctyry znaky jmena souboru 
    return filename[-4:None]


def openTest(): # ziska adresu testu a nastavi seznam test aby byl novy test, pote reqestuje novou otazku
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
    #newQuestion()
    submitAnswer(0)


def makeMenu(root): # vytvori menu
    menu = Menu(root)
    root.config(menu=menu)

    menu.add_command(label='Open', command=openTest)
    menu.add_command(label='Switch sides', command=swapSides)

    return menu


def makeRoot(): # vytvori hlavni okno
    root = Tk()
    root.geometry('500x400')
    root.title('Test Me')
    root.configure(bg="gray")
    root.iconbitmap('programfiles/icon.ico')
    return root


root = makeRoot()

filepath = 'programfiles/default.tst'
test = list(formatTest('programfiles/default.tst'))
questionPlace = 0
score = 0.0

currentScore = StringVar()
highScore = StringVar()
question = StringVar()
timeMultiplier = 1

anotherSpacingLabel = Label(bg='gray', padx=5)
currentScoreLabel = Label(root, textvariable=currentScore, bg='gray')
highScoreLabel = Label(root, textvariable=highScore, bg='gray')
questionLabel = Label(root, textvariable=question, width=30)
spacingLabel = Label(bg='gray', padx=10)
answerEntry = Entry(root, width=30)
answerButton = Button(root, text='submit', command=lambda: submitAnswer(0))
timeMultiplierLabel = Label(root, text='Your time bonus is: %s' %timeMultiplier, bg='gray')

anotherSpacingLabel.grid(row=0, column=0)
currentScoreLabel.grid(row=0, column=1, columnspan=2, sticky=W)
highScoreLabel.grid(row=0, column=4, columnspan=2, sticky=E)
questionLabel.grid(row=1, column=2, sticky=W)
spacingLabel.grid(row=1, column=3)
answerEntry.grid(row=1, column=4, sticky=E)
answerButton.grid(row=1, column=5, sticky=W)
timeMultiplierLabel.grid(row=2, column=1, columnspan=5)

currentScore.set('Score: %s' %(score))
highScore.set('High score is: %s' %(test[2]))
question.set('question will appear here')

root.protocol("WM_DELETE_WINDOW", on_closing)
answerEntry.bind('<Return>', submitAnswer)

menu = makeMenu(root)

running = True

while(running):
    try:
        if time.time() - timeAsked >=100:
            timeMultiplier = 1
        else:
            timeMultiplier = (1/(time.time()-timeAsked)*100)
        timeMultiplierLabel.configure(text='Your time bonus is: %s' %round(timeMultiplier, 2))
    except:
        None
    root.update()