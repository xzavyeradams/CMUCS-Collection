# xzavyer.dev/notagame.html or (if that doesn't work for whatever reason) https://academy.cs.cmu.edu/sharing/orangeRedCow4497
# This was submitted for the 2022 Fall Creative Task competition for Unit 12
# Xzavyer A - Fall 22' Submission Unit 12
### zombie game v2 (big map)

app.debug = False
app.reload = False
app.stepCount = 0
app.secondaryStepCount = 0
app.isPaused = True
app.spawnTimer = 150
app.notifications = [ ]

### level object & attributes
level = Group()
mapsize = 1000
f = 'red'
misc = Group(Rect(200, 200, 100, mapsize, align="center"), Rect(200, 200, mapsize, 100, align="center"))
bounds = Rect(200, 200, mapsize, mapsize, fill=rgb(80, 90, 80), align='center')
border = Rect(200, 200, mapsize + 400, mapsize + 400, opacity=50, align='center', border='red', fill=None, borderWidth=200)
level.add(bounds, border, misc)

### player object & attributes
playerArms = Group(
    Line(191, 200, 198, 220),
    Line(209, 200, 204, 220),
    Rect(201, 220, 6, 11, fill='grey', align='center')
    )
zombies = []
player = Group(Circle(200, 200, 10, fill='white', border='black', borderWidth=3), playerArms)
player.speed = 1.5
player.defaultSpeed = player.speed
player.spushNotifSpeed = player.speed + (player.speed * 0.5)
player.maxHp = 6
player.hp = player.maxHp
player.fakeX = 200
player.fakeY = 200
player.projectiles = []
player.score = 0
player.maxAmmo = 11
player.ammo = player.maxAmmo
player.reloadInterval = 8
player.maxPossibleHp = 16
player.maxPossibleAmmo = 55
player.maxPossibleSpeed = 6
player.constantFire = False
player.firingInterval = 10

### debug ui stuff
debughp = Label("Player HP: 3", 200, 20, fill='red', size=14)
playerspeed = Label("Player Spd.: 3", 200, 34, fill='blue', size=14) # change to stamina
levelpos = Label("Level Center Pos.: (x, y)", 200, 390, size=14)
debugscore = Label("Player Score: 0", 200, 58, fill='magenta', size=14)
enemycount = Label(f"Enemies: 0", 200, 46, fill='green', size=14)
ammocount = Label(f"Ammunition Count: 6", 200, 70, fill='yellow', size=14)
debug = Group(Rect(200, 44, 150, 70, opacity=25, align='center'), debughp, levelpos, playerspeed, enemycount, debugscore, ammocount)
debug.visible = False

### GUI
health = Group()
roundCountdown = Label(f"New Round Starts in: {app.spawnTimer}", 200, 350, fill="red")
roundLabel = Label("Round", 390, 15, font="montserrat", size=15, bold=True, align='right')
roundCount = Label(1, 390, 30, font="montserrat", size=15, align="right")
ammoLabel = Label("Ammo", 8, 365, font='montserrat', size=15, bold=True, align='left')
score = Label("Score", 390, 365, font='montserrat', size=15, bold=True, align='right')
scoreLabel = Label(f"{player.score:010d}", 390, 385, align='right', size=15, font='montserrat')
ammo = Group()
gui = Group(ammo, scoreLabel, ammoLabel, score, health, roundLabel)


def updateHealthGui():
    health.clear()
    for l in range(10, 20*player.maxHp, 20):
        health.add(Rect(l, 10, 20, 20, fill='green'))
    health.add(Rect(10, 10, 20*player.maxHp, 20, fill=None, border='black', borderWidth=2))
updateHealthGui()

def updateAmmoGui():
    ammo.clear()
    for x in range(0, 5*player.maxAmmo, 5):
        ammo.add(Rect(x+10, 385, 4, 15, fill='yellow', border='black', borderWidth=1, align='center'))
updateAmmoGui()


def end():
    Rect(0, 0, 400, 400, opacity=85)
    Label("Game Over", 200, 120, fill='white', font='montserrat', size=25)
    Label(f"Score: {player.score:010d} pts.", 200, 150, font='montserrat', size=20, fill='white')
    Label("Press the refresh button at the top left to play again!", 200, 290, size=13, fill='white', font='montserrat')
    app.isPaused = True
    app.paused = True
    app.stop()
    
def hit(damage):
    if player.hp - damage <= 0:
        end()
    else:
        player.hp -= 1
        health.children[player.hp].fill='red'
        
### pause/ss menu

pauseMenu = Group(
    Rect(0, 0, 400, 400, opacity=85),
    Label("Xzavyer A.", 20, 20, align="left", fill="grey"),
    Label("Launch projectiles at the zombies that spawn in each round.", 20, 45, fill="white", align="left"),
    Label("Every zombie has a differing speed, health point value, and color.", 20, 65, fill="white", align="left"),
    Label("RIGHT CLICK launches a projectile in the direction of your mouse.", 20, 85, fill="white", align="left"),
    Label("Hold SPACE to sprint slightly faster, press R to reload.", 20, 105, fill="white", align="left"),
    Label("You cannot fire while you are reloading, press R to stop reloading.", 20, 125, fill="white", align="left"),
    Label("Press TAB to enable debug/cheat menu. (may be unstable!)", 20, 145, fill="white", align="left"),
    Label("WASD to move, it is recommended that you play with a mouse.", 20, 165, fill="white", align="left"),
    Label("DEBUG/CHEAT CONTROLS", 20, 200, fill="red", align="left", bold=True),
    Label("Q = Spawn a zombie in a random location", 20, 220, fill="white", align="left"),
    Label("T = Hit yourself.", 20, 240, fill="white", align="left"),
    Label("Z = +1 HP", 120, 240, fill="white", align="left"),
    Label("X = +1 Ammo Slot", 190, 240, fill="white", align="left"),
    Label("C = -1 Reload Interval (faster reloading.)", 20, 260, fill="white", align="left"),
    Label("Tab, Escape, hold Z + X + C at the same time for max settings.", 20, 280, fill="white", align="left"),
    Label("E or Q launches projectiles at an increased rate towards the mouse.", 20, 300, fill="white", align="left"),
    Label("Press ESCAPE to pause/unpause.", 200, 380, fill="red"),
    Label("Controls / How-to-play", 200, 20, fill="red", bold=True)
)


# pauseMenu = Group(Rect(0, 0, 400, 400, opacity=50), Label("Game Paused", 200, 100, size=20, fill='white', font='montserrat'))
# pauseMenu.visible = False

### objects
class Projectile:
    def __init__(self, spawnX, spawnY, angle):
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.angle = angle
        self.speed = 30
        self.shape = Rect(spawnX, spawnY, 4, 10, fill='yellow', border='black', borderWidth=1, align='center', 
                        rotateAngle=angle)
        
    def randSpread(self):
        """As the projectile travels, it will get more unstable."""
        modifier = 30
        dist = distance(self.spawnX, self.spawnY, self.shape.centerX, self.shape.centerY)/modifier
        
        if dist != 0:
            spread = (random() * (dist*-1)) + dist
        else:
            spread = 0
    
        return spread
            
    def step(self):
        """Called on onStep"""
        delThreshold = 450 # distance required before projectile is deleted
        spread = self.randSpread()
        x, y = getPointInDir(self.shape.centerX, self.shape.centerY, self.angle, self.speed)
        x += spread
        self.shape.centerX = x 
        self.shape.centerY = y
        
        if distance(self.spawnX, self.spawnY, self.shape.centerX, self.shape.centerY) >= delThreshold:
            self.shape.visible = False
            player.projectiles.remove(self)

    def remove(self):
        """Removes the projectile"""
        try:
            self.shape.visible = False
            player.projectiles.remove(self)
        except ValueError:
            self.shape.visible = False

class Notification:
    def __init__(self, value, fill, y):
        self.label = Label(value, 10, y, fill=fill, align="left") # Actual label object
        self.lifetime = 60                           # Lifetime of notification, relation to steps
    
    def getNextPos(self):
        return self.label.centerY + 15

def pushNotif(value, color='white'):
    y = 45
    if len(app.notifications) != 0:
        y = app.notifications[-1].getNextPos()
    app.notifications.append(Notification(value, color, y))

class Zombie:
    def __init__(self, spawnX, spawnY):
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.speed = randrange(1, 4)
        self.hp = randrange(1, 4)
        self.shape = Circle(spawnX, spawnY, 10, fill=rgb(0, randrange(100, 256), 0),
                        border='black', borderWidth=3)
        self.score = pythonRound(10 + self.hp // 2 + self.speed // 2)
        gui.toFront()
        
    def hit(self, amount):
        """Called when a zombie is hit with a projectile"""
        self.hp -= amount
        if self.hp <= 0:
            self.shape.visible = False
            zombies.remove(self)
            player.score += self.score
            scoreLabel.value = f"{player.score:010d}"
    
    def step(self):
        """Called on onStep to move the zombie"""
        angle = angleTo(self.shape.centerX, self.shape.centerY, player.centerX, player.centerY)
        x, y = getPointInDir(self.shape.centerX, self.shape.centerY, angle, self.speed)
        self.shape.centerX, self.shape.centerY = x, y

def startRound():
    roundCountdown.visible = False
    zombCount = roundCount.value * 3 + (roundCount.value // 2)
    roundCount.value += 1
    if roundCount.value % 5 == 0:
        pushNotif("Restoring HP! (Every 5 rounds)")
        player.hp = player.maxHp
        updateHealthGui()
    for i in range(zombCount):
        zombies.append(Zombie(randrange(mapsize*-1, mapsize), randrange(mapsize*-1, mapsize)))
        
def onKeyPress(key):
    if key == "escape":
        pauseMenu.visible = not pauseMenu.visible
        app.isPaused = not app.isPaused
        pushNotif("Game unpaused")
        pauseMenu.toFront()
        
    if app.isPaused == False:
        if key == 'tab':
            app.debug = not app.debug
            debug.visible = not debug.visible
            pushNotif(f"Debug: {app.debug}")
        
        if app.debug == True:
            if key == 'q':
                zombies.append(Zombie(randrange(mapsize*-1, mapsize), randrange(mapsize*-1, mapsize)))
            elif key == 't':
                hit(1)
            elif key == 'z':
                player.maxHp += 1
                player.hp = player.maxHp
                updateHealthGui()
                pushNotif(f"Debug: maxHP: {player.maxHp}") # replace with CMU Composer notif system
            elif key == 'x':
                player.maxAmmo += 1
                player.ammo = player.maxAmmo
                updateAmmoGui()
                pushNotif(f"Debug: maxAmmo: {player.maxAmmo}")
            elif key == 'c':
                player.reloadInterval -= 1
                pushNotif(f"Debug: reloadInterval: {player.reloadInterval}")
                
        if key == 'r' and player.ammo != player.maxAmmo:
            app.reload = not app.reload
            
def onKeyHold(keys):
    ### movementds
    if app.debug == True and app.isPaused == True:
        if 'c' in keys and 'z' in keys and 'x' in keys:
            player.maxHp = player.maxPossibleHp
            player.hp = player.maxHp
            updateHealthGui()
            player.maxAmmo = player.maxPossibleAmmo
            player.ammo = player.maxAmmo
            updateAmmoGui()
            player.speed = player.maxPossibleSpeed
            player.defaultSpeed = player.speed
            player.spushNotifSpeed = player.speed + (player.speed * 0.5)
            player.reloadInterval = 1
            pushNotif("Debug (cheat): Max Settings Given!")
            
    if app.isPaused == False:
        
        if "e" in keys or "q" in keys:
            if player.ammo != 0 and app.reload != True:
                angle = player.rotateAngle + 180
                player.projectiles.append(Projectile(200, 200, angle))
                player.ammo -= 1
                ammo.children[player.ammo].fill = 'black'
                
        if 'w' in keys:
            if player.hits(player.centerX, bounds.top) != True:
                level.centerY += player.speed
                player.fakeY += player.speed
                if len(zombies) != 0:
                    for zombie in zombies:
                        zombie.shape.centerY += player.speed
        if 's' in keys:
            if player.hits(player.centerX, bounds.bottom) != True:
                level.centerY -= player.speed
                player.fakeY -= player.speed
                if len(zombies) != 0:
                    for zombie in zombies:
                        zombie.shape.centerY -= player.speed
        if 'a' in keys:
            if player.hits(bounds.left, player.centerY) != True:
                level.centerX += player.speed
                player.fakeX += player.speed
                if len(zombies) != 0:
                    for zombie in zombies:
                        zombie.shape.centerX += player.speed
        if 'd' in keys:
            if player.hits(bounds.right, player.centerY) != True:
                level.centerX -= player.speed
                player.fakeX -= player.speed
                if len(zombies) != 0:
                    for zombie in zombies:
                        zombie.shape.centerX -= player.speed
                        
        if 'space' in keys:
            player.speed = player.spushNotifSpeed
        if 'space' not in keys:
            player.speed = player.defaultSpeed
        
        
        border.opacity = distance(player.centerX, player.centerY, level.centerX, level.centerY) / (mapsize / 100)



def onStep():
    ### everything runs off of this essentially
    if app.isPaused == False:
        if len(app.notifications) != 0:
            for notification in app.notifications:
                notification.lifetime -= 1
                notification.label.opacity -= 1.4
                if notification.lifetime <= 0:
                    notification.label.visible = False
                    app.notifications.remove(notification)
        if len(zombies) == 0:
            if roundCountdown.visible == False:
                app.spawnTimer = 250
            roundCountdown.visible = True
            if app.spawnTimer == 0:
                startRound()

            app.spawnTimer -= 1
            roundCountdown.value = f"New Round Starts in: {app.spawnTimer}"
            
        if app.debug == True:
            debughp.value = f"Player HP: {player.hp}"
            levelpos.value = f"Level Center Pos.: ({level.centerX}, {level.centerY})"
            playerspeed.value = f"Player Spd.: {player.speed}"
            enemycount.value = f"Enemies: {len(zombies)}"
            debugscore.value = f"Player Score: {player.score}"
            ammocount.value = f"Ammunition Count: {player.ammo}"
            
        for proj in player.projectiles:
            proj.step()
            for zombie in zombies:
                if proj.shape.hitsShape(zombie.shape):
                    zombie.hit(1)
                    proj.remove()
        
        for zombie in zombies:
            if zombie.shape.hitsShape(player):
                angle = angleTo(zombie.shape.centerX, zombie.shape.centerY, player.centerX, player.centerY)
                zombie.shape.centerX, zombie.shape.centerY = getPointInDir(zombie.shape.centerX, zombie.shape.centerY, 
                                                angleTo(zombie.shape.centerX, zombie.shape.centerY, player.centerX, player.centerY), 
                                                randrange(zombie.speed * 4, zombie.speed * 7) * -1)
                hit(1)
            zombie.step()
        
        if app.reload == True and player.ammo != player.maxAmmo:
            app.stepCount += 1
            if app.stepCount == player.reloadInterval:
                try:
                    ammo.children[player.ammo].fill='yellow'
                    player.ammo += 1
                    app.stepCount = 0
                    if player.maxAmmo == player.ammo:
                        app.reload = False
                except IndexError:
                    app.stepCount = 0
            
def onMouseMove(x, y):
    if app.isPaused == False:
        ang = angleTo(x, y, 200, 200)
        player.rotateAngle = ang
    
def onMousePress(x, y):
    ### fires a projectile
    if app.isPaused == False:
        if player.ammo != 0 and app.reload != True:
            angle = angleTo(200, 200, x, y)
            player.projectiles.append(Projectile(200, 200, angle))
            player.ammo -= 1
            ammo.children[player.ammo].fill = 'black'
