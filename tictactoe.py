# https://academy.cs.cmu.edu/sharing/crimsonChimpanzee4392
# Creative Task for Unit 8.5, may be bugged a bit I'm not sure nor can I remember. But! It works as intended.

###

# Tic-Tac-Toe v2
# Xzavyer Adams
# 2/18/22 - 2/23/22

# This is a Tic-Tac-Toe game with 2 gamemodes.


app.gameType = None # 1 = two plr. | 2 = you vs bot
app.last = 0 # turn counter

def makeGameBoard():
    """Generates a new game board"""
    g = Group()
    index = 0
    for top in range(20, 360, 120):
        for left in range(20, 360, 120):
            box = Rect(left, top, 120, 120, fill=None, border='black')
            box.gameIndex = index
            g.add(box)
            index += 1
    
    return Group(Rect(20, 20, 360, 360, fill=None, border='black', borderWidth=4), g)

board = makeGameBoard()
board.values = [
    0, 0, 0,
    0, 0, 0,  # 0 = none, 1 = x, 2 = 0
    0, 0, 0
    ]

# menu screen stuff    
board.visible = False

btn_twoPlayer = Group(Rect(200, 200, 120, 40, align='center', fill='paleGreen', border='white'),
                Label("2 Player", 200, 200, size=20, font='monospace'))
btn_bot = Group(Rect(200, 250, 120, 40, align='center', fill='lightBlue', border='white'),
                Label("vs. BOT", 200, 250, size=20, font='monospace'))
btn_info = Group(Rect(200, 300, 120, 40, align='center', fill='lightBlue', border='white'),
                Label("Tutorial", 200, 300, size=20, font='monospace'))
mm = Group(
        Label("Tic-Tac-Toe", 200, 120, size=34, font='monospace'),
        Label("Creative Task 8, Xzavyer A.", 200, 140, font='monospace'),
        btn_twoPlayer,
        btn_bot,
        btn_info
        )
        
tutorialMsg = Group(Rect(0, 0, 400, 400, opacity=70), 
        Label("2 Player: Take turns with the mouse to play.", 200, 25, fill='white'),
        Label("vs. Bot: 1 player plays against a bot that picks random empty spaces.", 200, 40, fill='white'),
        Label("Standard Tic-Tac-Toe rules, first to 3 in a row wins.", 200, 55, fill='white'),
        Label("Press any key to hide.", 200, 380, fill='white', size=20))
tutorialMsg.visible = False

def winnerScreen(text):
    Rect(0, 0, 400, 400, opacity=75)
    Label(text, 200, 200, fill='white', size=25, font='monospace')
    app.stop()

def genCheckWin():
    # horizontal
    yield [board.values[0+i:3+i] for i in range(0, 9, 3)]
    # vertical
    yield [[board.values[0+i] for i in range(ii, 9, 3)] for ii in range(0, 3)]
    # across
    yield [[board.values[0+i] for i in range(0, 12, 4)], [board.values[2+i] for i in range(0, 6, 2)]]

def checkWin():
    doubleCheck = False
    for win in genCheckWin():
        for spaces in win:
            for num in range(1,3):
                if all([True if space == num else False for space in spaces]):
                    if num == 1:
                        winnerScreen("X has won!")
                    elif num == 2:
                        winnerScreen("O has won!")
                    doubleCheck = True
                    
    if all([True if space != 0 else False for space in board.values]) and doubleCheck == False:
        winnerScreen("Nobody won.")
        
def startGame():
    board.visible = True

def drawO(x, y):
    Circle(x, y, 30, fill=None, border='cornflowerBlue', borderWidth=5)
    
def drawX(x, y):
    Line(x-30, y-30, x+30, y+30, fill='red', lineWidth=5)
    Line(x+30, y-30, x-30, y+30, fill='red', lineWidth=5)

    
def onMouseMove(x, y):
    if mm.visible == True:
        if btn_twoPlayer.contains(x, y):
            btn_twoPlayer.children[0].border = 'black'
        else:
            btn_twoPlayer.children[0].border = 'white'
    
        if btn_bot.contains(x, y):
            btn_bot.children[0].border = 'black'
        else:
            btn_bot.children[0].border = 'white'
            
        if btn_info.contains(x, y):
            btn_info.children[0].border = 'black'
        else:
            btn_info.children[0].border = 'white'
            
    elif mm.visible == False:
        for box in board.children[1]:
            if box.contains(x, y):
                if board.values[box.gameIndex] != 0:
                    box.fill = 'gainsboro'
                else:
                    box.fill = 'lightCyan'
            else:
                box.fill = None



def debug():
    for possible in genCheckWin():
        print(possible)

def onMousePress(x, y):
    if mm.visible == True:
        if btn_twoPlayer.contains(x, y):
            app.gameType = 1
            mm.visible = False
            startGame()
        elif btn_bot.contains(x, y):
            app.gameType = 2
            mm.visible = False
            startGame()
        elif btn_info.contains(x, y):
            tutorialMsg.visible = True
            app.paused = True
    elif mm.visible == False:
        for box in board.children[1]:
            if box.contains(x, y) and board.values[box.gameIndex] == 0:
                if app.gameType == 1:
                    if app.last % 2 != 0:
                        drawO(box.centerX, box.centerY)
                        board.values[box.gameIndex] = 2
                    else:
                        drawX(box.centerX, box.centerY)
                        board.values[box.gameIndex] = 1
                    
                    app.last += 1
                    checkWin()
                    
                elif app.gameType == 2:
                    if box.contains(x, y) and board.values[box.gameIndex] == 0:
                        drawX(box.centerX, box.centerY)
                        board.values[box.gameIndex] = 1
                        while True:
                            botSelection = randrange(0, 9)
                            if board.values[botSelection] == 0:
                                for box in board.children[1]:
                                    if box.gameIndex == botSelection:
                                        drawO(box.centerX, box.centerY)
                                        board.values[botSelection] = 2
                                break
                    checkWin()

def onKeyPress(k):
    if tutorialMsg.visible == True:
        app.paused = False
        tutorialMsg.visible = False
