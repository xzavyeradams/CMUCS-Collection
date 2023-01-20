# https://academy.cs.cmu.edu/sharing/silverKitten3669
# This was my final project for CS 2. Unfortunately, I didn't actually get to finish it. And there were like, 3 or 4 versions that I haven't uploaded.
# It works, I found out you could make sound using a MIDI-like setup after CMU implemented their CS 2 stuff. It may not work, since they probably updated the CS 2 things.

# Final Project, Xzavyer A
# CMU COMPOSER is a simplified music production app.

### app variables (manjority)

app.mainColor = rgb(84, 71, 204)                         # Color for UI elements
app.background = app.mainColor                           # Background
app.playing = False                                      # Variable that defines whether or not music is being played
app.mode = False                                         # Variable that defines what mode the user is using
app.length = 1/4                                         # Current length of the notes
app.notifications = [ ]                                  # List of notifications, for the notification system
app.activeInstrument = None                              # Variable that defines the instrument being used
app.previousInstrument = None                            # Variable that defines the previous instrument selected
app.lengths = {1/8: 12.5, 1/4: 25, 1/2: 50, 1: 100}      # List of note lengths and the note sizes
app.tutorialRead = False                                 # Variable that defines whether or not the user read the tutorial
app.lengthIndex = 1                                      # Keeps track of lengths

###

### Classes
class Instrument:
    def __init__(self, name, uiElement, color):
        self.name = name                                          # Name, used for showing the user the instrument name
        self.uiElement = uiElement                                # Button to select the instrument
        self.color = color                                        # UI element color
        self.notes = [ ]                                          # The actual list of notes, for the sequencer
        self.visual = Group()                                     # The actual representation of notes on the app
        self.visualX = 25                                         # The start position for the notes on the app
        self.sequencer = Sequencer((), instrument=name, volume=1) # The sequencer, plays the notes, CS2

class Notification:
    def __init__(self, value, fill, y):
        self.label = Label(value, 200, y, fill=fill) # Actual label object
        self.lifetime = 60                           # Lifetime of notification, relation to steps
    
    def getNextPos(self):
        return self.label.centerY + 15
###


### General UI Elements
## Main Menu
startButton = Group(
        Rect(200, 180, 180, 55, fill=rgb(68, 57, 117), border='white', align='center'),
        Label("+ NEW TRACK", 200, 180, fill='white', size=18)
    )
    
tutorialButton = Group(
        Rect(200, 240, 180, 55, fill=rgb(68, 57, 117), border='white', align='center'),
        Label("? TUTORIAL", 200, 240, fill='white', size=18)
    )
    
mainMenu = Group(
        startButton, tutorialButton, Label("CMU Composer", 200, 100, size=35, fill='white', bold=True),
        Label("Xzavyer Adams", 200, 385, size=10, fill='white')
    )

## Track Screen
app.pointer = Rect(25, 25, 25, 275, fill='green', opacity=30)


clearBtn = Group(
        Rect(10, 365, 85, 30, border='white'),
        Label("CLEAR ALL", 52, 380, fill='white')
    )
lengthButtonLabel = Label("1/4", 120, 380, fill='white')
lengthButton = Group(
        Rect(100, 365, 40, 30, border='white'),
        lengthButtonLabel
    )
otherGuiElements = Group(
        Label("Instruments", 97, 310, fill='white', bold=True),
        Label("Mode", 355, 310, fill='white', bold=True, align='left'),
        clearBtn, lengthButton
    )

# app variables for instrument management
app.piano = Instrument("piano", Rect(10, 320, 40, 40, border='white'), 'cornFlowerBlue')
app.violin = Instrument("violin", Rect(55, 320, 40, 40, border='white'), 'coral')
app.organ = Instrument("organ", Rect(100, 320, 40, 40, border='white'), 'gold')
app.bass = Instrument("bass", Rect(145, 320, 40, 40, border='white'), 'fireBrick')
app.instrumentObjs = [app.piano, app.violin, app.organ, app.bass]

drawToggle = Rect(350, 320, 40, 40, border='white')

toolbar = Group(
        Rect(0, 300, 400, 100, fill='grey'), drawToggle,
        otherGuiElements, app.piano.uiElement, app.violin.uiElement,
        app.organ.uiElement, app.bass.uiElement, app.pointer
    )

notes = ["C", "D", "E", "F", "G", "A", "B", "C", "D", "E", "F"]
notes.reverse()
markers = Group()
lines = Group()
my = 25 # start of the markers
while my < 300:
    if str(my)[-1] == '0':
        fill = 'silver'
    else: 
        fill = 'white'
    marker = Group(
            Rect(0, my, 25, 25, fill=fill), 
            Label(notes[my//25-1], 12.5, my + 12.5, fill='black')
        )
    if my != 0:
        lines.add(Line(25, my, 400, my, fill=rgb(20,20,20)))
    markers.add(marker)
    my += 25
    
trackScreen = Group(
        Rect(0, 0, 400, 400, fill=rgb(26,26,26)),
        Rect(0, 0, 400, 25, fill='grey'),
        Label("CMU COMPOSER v2", 10, 12, align='left', fill='white'),
        markers, lines, toolbar
        
    )
trackScreen.visible = False

## Tutorial Stuff
tutorialGroup = Group()
###

### Helper Functions

def pushNotif(value, color='white'):
    y = 45
    if len(app.notifications) != 0:
        y = app.notifications[-1].getNextPos()
    app.notifications.append(Notification(value, color, y))

def changeInstrument(instrument: Instrument):
    if app.activeInstrument != None:
        app.activeInstrument.uiElement.fill = "black"
    app.activeInstrument = instrument
    instrument.uiElement.fill = instrument.color
    pushNotif(f"Changed Instrument to '{instrument.name}'.")

def toggleMode():
    if app.mode == True:
        app.mode = False
        drawToggle.fill = "red"
        pushNotif("Mode: Delete")
    elif app.mode == False:
        app.mode = True
        drawToggle.fill = "green"
        pushNotif("Mode: Draw")

def clear():
    for instrument in app.instrumentObjs:
        instrument.notes = []
        instrument.visual.clear()
        instrument.visualX = 25
    pushNotif("Cleared all tracks.")

def cycleLength():
    if app.lengthIndex == 4:
        app.lengthIndex = 0
    app.length = app.lengths[list(app.lengths)[app.lengthIndex]]
    app.lengthIndex += 1
    pushNotif(f"Changed length to {app.length}.")


###

### Events

def onMouseMove(x, y):
    if mainMenu.visible == True or startButton.visible == True:
        if startButton.contains(x, y):
            startButton.children[0].fill = rgb(109, 91, 189)
            tutorialButton.children[0].fill = rgb(68, 57, 117)
        elif tutorialButton.contains(x, y):
            tutorialButton.children[0].fill = rgb(109, 91, 189)
            startButton.children[0].fill = rgb(68, 57, 117)
        else:
            startButton.children[0].fill = rgb(68, 57, 117)
            tutorialButton.children[0].fill = rgb(68, 57, 117)

def onMousePress(x, y):
    if startButton.visible == True and startButton.contains(x, y):
        if app.tutorialRead != True:
            while True:
                understandPrompt = app.getTextInput("Do you want to read the tutorial? [Y/N]")
                if understandPrompt == "Y" or understandPrompt == "y":
                    mainMenu.visible = False
                    tutorialGroup.visible = True
                    startButton.visible = True
                    startButton.centerY = 320
                    startButton.toFront()
                    break
                elif understandPrompt == "N" or understandPrompt == "n":
                    trackScreen.visible = True
                    mainMenu.visible = False
                    startButton.visible = False
                    tutorialGroup.visible = False
                    pushNotif("Welcome to CMU COMPOSER")
                    changeInstrument(app.piano)
                    break
        else:
            changeInstrument(app.piano)
            trackOneGroup.visible = True
            mainMenu.visible = False
            startButton.visible = False
            tutorialGroup.visible = False
            pushNotif("Welcome to CMU COMPOSER")
    
    # track stuff
    if trackScreen.visible == True:
        if toolbar.contains(x, y): 
            for instrument in app.instrumentObjs:
                if instrument.uiElement.contains(x, y):
                    changeInstrument(instrument)
            if drawToggle.contains(x, y):
                toggleMode()
            if clearBtn.contains(x, y):
                clear()
            if lengthButton.contains(x, y):
                cycleLength()
                lengthButtonLabel.value = app.length

def onStep():
    if len(app.notifications) != 0:
        for notification in app.notifications:
            notification.lifetime -= 1
            notification.label.opacity -= 1.4
            if notification.lifetime <= 0:
                notification.label.visible = False
                app.notifications.remove(notification)
            
