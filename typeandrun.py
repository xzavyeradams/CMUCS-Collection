# https://academy.cs.cmu.edu/sharing/whiteSmokeCamel6177
# This was one of the first things I made. It's not efficient at all, but essentially you could run code that you type onto the canvas with it.


# HOW TO:
# Write code as your normally would inside the canvas.
# Backspace & Enter work normally (sometimes not in the most graceful way)
# Once you have written your code, press ESCAPE and it will run the code using
# python's eval() built-in.


# config
break_point = 380 # break point to begin a new line (x coordinate)
spacing = 8.5 # between characters
font = "monospace" # 'arial' || 'monospace'

# set steps per second so the cursor doesn't blink too fast
app.stepsPerSecond = 5 
current_pos = [20, 30]
curs_pos = [21.5, 26]
characters = []
translate = {
    "space": " ",
    "tab": "    ",
    "right": ">",
    "left": "<",
    "up": "^",
    "down": "v"
}
placeholder = Label("Start typing...", 55, 15, fill='grey')
cursor = Rect(*curs_pos, 2, 15)

def set_pos(x, y):
    current_pos[0] = x
    current_pos[1] = y
    return current_pos

def set_curs_pos(x, y):
    curs_pos[0] = cursor.centerX = x
    curs_pos[1] = cursor.centerY = y
    return cursor.centerX, cursor.centerY
    
# have to do this due to unboundlocalerrors
def get_pos():
    return current_pos

def get_curs_pos():
    return curs_pos

def get_font():
    return font

def run_code():
    eval_list = []
    for c in characters:
        try:
            eval_list.append(c.value)
        except AttributeError:
            eval_list.append(c)
    eval_statement = "".join(l for l in eval_list)
    eval(eval_statement)

# typing
def onKeyPress(key):
    placeholder.visible = False
    x, y = get_pos()
    cx, cy = get_curs_pos()
    kwargs = {}
    
    # logic stuff
    if x >= break_point:
        set_pos(20, y+20)
        set_curs_pos(21.5, cy+20)
    
    # if key needs to be translated, translate, or else use the key provided.
    key = translate[key] if key in translate else key
    
    # font check
    font = get_font()
    if font != "":
        kwargs.update({"font": font})
    
    # special keys
    if key == "enter":
        set_pos(20, y+20)
        set_curs_pos(21.5, cy+20)
        characters.append("\n")
        return None
    elif key == "backspace":
        try:
            dl = characters[-1]
            if dl == "\n":
                set_pos(20, y-20)
                set_curs_pos(21.5, cy-20)
            else:
                dl.visible = False
                set_pos(dl.centerX, dl.centerY)
                set_curs_pos(dl.centerX, cy)
            characters.pop()
        except IndexError:
            print("ERR: Cannot backspace. (there are no characters.)")
        return None
    elif key == "escape":
        run_code()
        return None
        
    # write character to canvas
    x,y = get_pos()
    l = Label(key, x, y, **kwargs)
    characters.append(l)
    set_pos(x+spacing, y)
    cx, cy = get_curs_pos()
    set_curs_pos(cx+spacing, cy)
    
    # log what happened
    print(f"LOG: '{key}' @ pos. {get_pos()} (count: {len(characters)})")
    
def onStep():
    # cursor blink
    if cursor.visible == True:
        cursor.visible = False
    else:
        cursor.visible = True
