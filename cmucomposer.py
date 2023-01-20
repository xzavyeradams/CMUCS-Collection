# Draft Link -> https://academy.cs.cmu.edu/sharing/ivorySheep7495
# Final Submitted Link -> https://academy.cs.cmu.edu/sharing/siennaBee6533
# This was my final project for CS 2. Unfortunately, I didn't actually get to finish it. And there were like, 3 or 4 versions that I haven't uploaded.
# It works, I found out you could make sound using a MIDI-like setup after CMU implemented their CS 2 stuff. It may not work, since they probably updated the CS 2 things.
# Check the commit history for any older versions, I believe this is the one I submitted.

# Xzavyer A

app.tutorialText = """
- To draw notes onto the track, select the button 
    on the far right labeled 'mode'.
    
- This will toggle the draw/delete drawing modes.

- To select new instruments, select any of the 
    buttons on the far left labeled 'instruments'.
    
- To clear out the entire track, select the button 
    labeled, 'clear all'.
    
- To play the music, press the spacebar once.

- To change the length of the note, press the button labeled '1/4' 
    to cycle through the lengths.

- To add rest notes, add the note to the track and then use the delete
    tool on that note to make it silent. You can re-enable notes by
    using the draw tool.
"""


### LOGIC
app.mainClr = rgb(84, 71, 204)
app.playing = False
app.draw = None # draw notes, false = delete notes, None = standby
app.validNoteLen = {
    1/8: 12.5,
    1/4: 25,
    1/2: 50,
    1: 100
}

def addNote(x, y, length):
    for marker in roll:
        if marker.contains(marker.centerX, y): # its in this section
            noteVal = marker
            actNote = noteVal.children[1].value
            instrument = app.activeInstrument
            color = instrument.activeFill

            shLength = app.validNoteLen[length]
            
            for i, note in enumerate(app.activeInstrument.visGroup): # checks if note already exists
                if note.contains(x, y): 
                    pushNotif(f"Made note #{i+1} active on {app.activeInstrument.name}.")
                    note.opacity = 100
                    app.activeInstrument.sequencer[i].pitch = noteVal
                    return app.activeInstrument.sequencer[i]
                    
            # draw note visually
            if instrument.visStartX + shLength >= 400:
                pushNotif("ERR: Cannot add any more notes to this track!", "red")
            else:
                instrument.visGroup.add(
                        Rect(instrument.visStartX, noteVal.top, shLength, 25, fill=color)
                    )
                instrument.visGroup.toFront()
                instrument.visStartX += shLength    
                instrument.sequencer.append(Note(actNote, 2, length))

def deleteNote(x, y):
    for i, note in enumerate(app.activeInstrument.visGroup):
        if note.contains(x, y):
            note.opacity = 10
            app.activeInstrument.sequencer[i].pitch = None
            pushNotif(f"Made note #{i+1} silent on {app.activeInstrument.name}.")
            return app.activeInstrument.sequencer[i]
        

class Notification:
    def __init__(self, value, fill, y=45):
        self.labelObject = Label(value, 200, y, fill=fill)
        self.lifetime = 60 # relation to steps
        self.dead = False
    
    def getNextPos(self):
        return self.labelObject.centerY + 15

notifications = []

def pushNotif(value, clr='white'):
    if len(notifications) == 0:
        notifications.append(Notification(value, clr))
    else:
        notifications.append(Notification(value, clr, notifications[-1].getNextPos()))

### objects mmm
# potentially use dataclasses instread
class InstrumentContainer:
    def __init__(self, name, activeFill):
        self.name = name
        self.activeFill = activeFill
        self.sequencer = [ ]
        self.visGroup = Group()
        self.visStartX = 25
        self.player = Sequencer((), instrument=name, volume=1)

app.piano = InstrumentContainer("piano", 'cornFlowerBlue')
app.violin = InstrumentContainer("violin", "coral")
app.organ = InstrumentContainer("organ", "gold")
app.bass = InstrumentContainer("bass", "fireBrick")

app.allInstrumentObjs = [app.piano, app.violin, app.organ, app.bass]

app.lengths = [1/8, 1/4, 1/2, 1]
app.lengthIndex = 1
app.length = 1/4
app.activeInstrument = app.piano
app.prevInstrument = app.piano
app.greatestLength = app.piano

### EVENTS
def onMousePress(x, y):
    if startButton.visible == True and startButton.contains(x, y):
        while True:
            understandPrompt = app.getTextInput("Do you want to read the tutorial? [Y/N]")
            if understandPrompt == "Y" or understandPrompt == "y":
                menuGroup.visible = False
                tutorialGroup.visible = True
                startButton.visible = True
                startButton.centerY = 320
                startButton.toFront()
                break
            elif understandPrompt == "N" or understandPrompt == "n":
                trackOneGroup.visible = True
                menuGroup.visible = False
                startButton.visible = False
                tutorialGroup.visible = False
                pushNotif("Welcome to CMU COMPOSER")
                break
        
    if tutorialButton.visible == True and tutorialButton.contains(x, y):
        menuGroup.visible = False
        tutorialGroup.visible = True
        startButton.visible = True
        startButton.centerY = 320
        startButton.toFront()
            
    if trackOneGroup.visible == True: # track stuff
        if toolbar.contains(x, y) and app.playing != True: # ensures that the user is attempting to click on something in the toolbar
            if clearBtn.contains(x, y):
                for instrument in app.allInstrumentObjs:
                    instrument.visStartX = 25
                    instrument.visGroup.clear()
                    instrument.sequencer = []
                    pushNotif("Cleared all instruments")
            if drawToggle.contains(x, y):
                app.draw = not app.draw
                if app.draw == True:
                    drawToggle.fill = 'green'
                    pushNotif("Tool mode: Draw")
                else:
                    drawToggle.fill = 'red'
                    pushNotif("Tool mode: Delete")
            if lengthButton.contains(x, y):
                if app.lengthIndex == 4:
                    app.lengthIndex = 0
                app.length = app.lengths[app.lengthIndex]
                app.lengthIndex += 1
                pushNotif(f"Changed length to {app.length}")
                lengthButtonLabel.value = app.length
            for instrument in instruments: # set default state for all instrument buttons, can be changed 
                if instrument.contains(x, y):
                    instrument.fill = instrument.value.activeFill
                    app.prevInstrument = app.activeInstrument
                    app.activeInstrument = instrument.value # sets the current instrument type
                    app.activeInstrument.visGroup.opacity = 100
                    pushNotif(f'Changed current instrument to "{instrument.value.name}"')
                    for instrument in instruments:
                        if instrument.value != app.activeInstrument:
                            instrument.fill = 'black'
                            instrument.value.visGroup.opacity = 0
                        if instrument.value == app.prevInstrument:
                            instrument.value.visGroup.opacity = 50
                    activeBar.left = 25
                    app.idx = 0
                            
        if app.draw == True:
            addNote(x, y, app.length)
        elif app.draw == False:
            deleteNote(x, y)

def onMouseMove(x, y):
    if menuGroup.visible == True or startButton.visible == True:
        if startButton.contains(x, y):
            startButton.children[0].fill = rgb(109, 91, 189)
            tutorialButton.children[0].fill = rgb(68, 57, 117)
        elif tutorialButton.contains(x, y):
            tutorialButton.children[0].fill = rgb(109, 91, 189)
            startButton.children[0].fill = rgb(68, 57, 117)
        else:
            startButton.children[0].fill = rgb(68, 57, 117)
            tutorialButton.children[0].fill = rgb(68, 57, 117)
            
def onKeyPress(k):
    if trackOneGroup.visible == True:
        if k == 'tab':
            ## debug stuff
            print(f"ACTIVE INSTRUMENT: {app.activeInstrument}")
        elif k == 'enter':
            app.greatestLength = app.piano
            for instrument in app.allInstrumentObjs:
                if len(app.greatestLength.sequencer) < len(instrument.sequencer):
                    app.greatestLength = instrument
            pushNotif(f"debug: playing {app.activeInstrument.name} ({len(app.activeInstrument.sequencer)})")
            pushNotif("Drawing disabled")
            app.playing = True
            for instrument in app.allInstrumentObjs:
                instrument.player.notes = tuple(instrument.sequencer)
                print(instrument.name, instrument.player.notes)
                instrument.player.play()
        elif k == 'p':
            print("\n\n\n\n\n\n\n\n\n\n\n\nCleared!\n\n")
        
def onStep():
    # notification system
    if len(notifications) != 0:
        for notif in notifications:
            notif.lifetime -= 1
            notif.labelObject.opacity -= 1.4
            if notif.lifetime <= 0:
                notif.labelObject.visible = False
                notifications.remove(notif)

activeBar = Rect(25, 25, 25, 275, fill='green', opacity=30)
app.idx = 0
def onSignal(notes):
    activeBar.toFront()
    drawToggle.fill = 'yellow'
    app.draw = None
    if app.idx < len(app.greatestLength.visGroup.children):
        note = app.activeInstrument.visGroup.children[app.idx]
        activeBar.left = note.left
        activeBar.width = note.width
        app.idx += 1
    else:
        activeBar.left = 25
        app.idx = 0
        app.draw = True
        drawToggle.fill = 'green'
        pushNotif("Drawing re-enabled")
        app.playing = False


### HOME MENU SCREEN (SCREEN 1)
buttonFill = rgb(68, 57, 117)
startButtonLabels = Group(Label("New Track", 215, 180, fill='white', size=18),
        Rect(145, 180, 4, 24, align='center', fill='white'),
        Rect(145, 180, 24, 4, align='center', fill='white')
    )
startButtonLabels.centerX = 200
startButton = Group(
        Rect(200, 180, 180, 55, fill=buttonFill, border='white', align='center'),
        startButtonLabels
    )

tutorialButtonLabels = Group(
        Label("Tutorial", 215, 240, fill='white', size=18),
        Label("?", 150, 240, fill='white', size=36)
    )

tutorialButton = Group(
        Rect(200, 240, 180, 55, fill=buttonFill, border='white', align='center'),
        tutorialButtonLabels
    )

buttons = Group(startButton, tutorialButton)

menuGroup = Group(
        Rect(0, 0, 400, 400, fill=app.mainClr),
        Label("CMU Composer", 200, 100, size=35, fill='white', font='montserrat', bold=True),
        Label("Xzavyer Adams", 10, 385, align='left', size=10, fill='white'),
        buttons
    )

### TRACK SCREEN (SCREEN 2)

# instrument buttons and properties
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
piano = Rect(10, 320, 40, 40, fill='cornFlowerBlue', border='white')
piano.value = app.piano

violin = Rect(55, 320, 40, 40, border='white')
violin.value = app.violin

organ = Rect(100, 320, 40, 40, border='white')
organ.value = app.organ

bass = Rect(145, 320, 40, 40, border='white')
bass.value = app.bass

drawToggle = Rect(350, 320, 40, 40, border='white')

instruments = [piano, violin, organ, bass]
toolbar = Group(
        Rect(0, 300, 400, 100, fill='grey'), piano, violin, organ, bass, drawToggle,
        otherGuiElements
    )
    
# piano roll thing
roll = Group()
lines = Group()
notes = ["C", "D", "E", "F", "G", "A", "B", "C", "D", "E", "F"]
notes.reverse()
y = 25
bin = 0
while y < 300:
    if bin == 0:     #
        f = 'silver' #
        bin = 1      #
    else:            #  lazy way, fix later
        f = 'white'  #
        bin = 0      #
    marker = Group(Rect(0, y, 25, 25, fill=f))
    try: # fix this try except clause
        next = y // 25 - 1
        marker.add(Label(notes[next], 12.5, y + 25 / 2, fill='black'))
    except:
        pass
    if y != 0:
        lines.add(Line(25, y, 400, y, fill=rgb(20,20,20)))
    roll.add(marker)
    y += 25    



# final group
trackOneGroup = Group(
        Rect(0, 0, 400, 400, fill=rgb(26,26,26)),
        Rect(0, 0, 400, 25, fill='grey'),
        Label("CMU COMPOSER v1.0", 10, 12, align='left', fill='white'),
        toolbar, roll, lines, activeBar
    )
trackOneGroup.visible = False

### tutorial area group
startX = 200
startY = 55
interval = 12
tutorialText = Group()
for i, string in enumerate(app.tutorialText.split("\n")): # splits by new lines
    tutorialText.add(Label(string, startX, startY+(interval*i), fill='white'))

tutorialGroup = Group(
        Rect(0, 0, 400, 400, fill=app.mainClr),
        Label("Tutorial", 200, 35, size=40, fill='white', font='montserrat', bold=True),
        tutorialText, startButton
    )
tutorialGroup.visible = False

startButton.visible = True
            
