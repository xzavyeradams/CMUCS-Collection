# https://academy.cs.cmu.edu/sharing/antiqueWhiteHorse6130
# This is some sort of physics simulation I made. The ball can move, gain velocity, and move based upon the momentum of the object. Friction then slows it down.

# dynamic velocity demo

dbg = Label("accelX: 0, accelY: 0, speed: 0", 200, 10)

object = Circle(200, 200, 10, fill='white', border='black')
object.velocityX = 0
object.velocityY = 0
object.accelerationRate = 0.25
object.maxSpeed = 10
object.frictionRate = 0.1

def onKeyHold(keys):
    if 'w' in keys:
        if abs(object.velocityX) + abs(object.velocityY) <= object.maxSpeed:
            object.velocityY -= object.accelerationRate
    if 's' in keys:
        if abs(object.velocityX) + abs(object.velocityY) <= object.maxSpeed:
            object.velocityY += object.accelerationRate
    if 'a' in keys:
        if abs(object.velocityX) + abs(object.velocityY) <= object.maxSpeed:
            object.velocityX -= object.accelerationRate
    if 'd' in keys:
        if abs(object.velocityX) + abs(object.velocityY) <= object.maxSpeed:
            object.velocityX += object.accelerationRate

def onStep():
    dbg.value = f"accelX: {object.velocityX}, accelY: {object.velocityY}, speed: {object.velocityX + object.velocityY}"
    object.centerX += object.velocityX
    object.centerY += object.velocityY
    
    if object.velocityX < 0 and object.velocityX != 0:
        object.velocityX += object.frictionRate
    elif object.velocityX > 0 and object.velocityX != 0:
        object.velocityX -= object.frictionRate

    if object.velocityY < 0 and object.velocityY != 0:
        object.velocityY += object.frictionRate
    elif object.velocityY > 0 and object.velocityY != 0:
        object.velocityY -= object.frictionRate
