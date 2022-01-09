from tkinter.font import *
from types import BuiltinFunctionType
import clipboard
import time
from tkinter import *
import math
from ctypes import windll
from numpy import linalg
from pynput import keyboard

# hide console
windll.user32.ShowWindow(windll.kernel32.GetConsoleWindow(), 0)

divineTable = [ [[251, 50],    [-169, 192],  [-82, -242]],
                [[213, 142],   [-230, 113],  [17, -255]],
                [[142, 213],   [-255, 17],   [113, -230]],
                [[50, 251],    [-242, -82],  [192, -169]],
                [[-50, 251],   [-192, -169], [242, -82]],
                [[-142, 213],  [-113, -230], [255, 17]],
                [[-213, 142],  [-17, -255],  [230, 113]],
                [[-251, 50],   [82, -242],   [169, 192]],
                [[-251, -50],  [169, -192],  [82, 242]],
                [[-213, -142], [230, -113],  [-17, 255]],
                [[-142, -213], [255, -17],   [-113, 230]],
                [[-50, -251],  [242, 82],    [-192, 169]],
                [[50, -251],   [192, 169],   [-242, 82]],
                [[142, -213],  [113, 230],   [-255, -17]],
                [[213, -142],  [17, 255],    [-230, -113]],
                [[251, -50],   [-82, 242],   [-169, -192]]]

eyeCount = 0
eye1 = []
eye2 = []

scheduleReset = False

# --- GUI SETUP ---

run = True

def test(*args):
    print(args)

# end program
def end_program():
    window.destroy()
    global run 
    run = False

# reset key listener
def on_press(key):
    global scheduleReset
    if key == keyboard.Key.f5:
        scheduleReset = True

listener = keyboard.Listener(on_press=on_press)
listener.start()


# default colors
bgcolor = "black"
fgcolor = "white"

divine = -1

# ceate window
window = Tk()
window.title("Speedrun Bot")
window.geometry("425x90")
window.configure(background=bgcolor)
window.protocol("WM_DELETE_WINDOW", end_program)

# frames
frameTriang = Frame(window, width=220, height=50, bg=bgcolor)
frameTriang.grid_propagate(0)

frameTriangResult = Frame(window, width=200, height=50, bg=bgcolor)
frameTriangResult.grid_propagate(0)

frameDivine = Frame(window, width=200, height=100, bg=bgcolor)
frameDivine.grid_propagate(0)

# labels for trinag
labelEye1 = Label(frameTriang, text="1. Eye: ", bg=bgcolor, fg=fgcolor)
labelEye1.grid(column=0, row=0, sticky="W")

labelEye2 = Label(frameTriang, text="2. Eye: ", bg=bgcolor, fg=fgcolor)
labelEye2.grid(column=0, row=1, sticky="W")

labelEye1Val = Label(frameTriang, text="-", bg=bgcolor, fg=fgcolor)
labelEye1Val.grid(column=1, row=0, sticky="W")

labelEye2Val = Label(frameTriang, text="-", bg=bgcolor, fg=fgcolor)
labelEye2Val.grid(column=1, row=1, sticky="W")

# labels for triang result
labelResultOverworld = Label(frameTriangResult, text="Overworld: ", bg=bgcolor, fg=fgcolor)
labelResultOverworld.grid(column=0, row=0, sticky="W")

lableResultNether = Label(frameTriangResult, text="Nether: ", bg=bgcolor, fg=fgcolor)
lableResultNether.grid(column=0, row=1, sticky="W")

labelResultOverworldVal = Label(frameTriangResult, text="-", bg=bgcolor, fg="#60db81")
labelResultOverworldVal.grid(column=1, row=0, sticky="W")

labelResultNetherVal = Label(frameTriangResult, text="-", bg=bgcolor, fg="#db6060")
labelResultNetherVal.grid(column=1, row=1, sticky="W")

labelResultOverworldDist = Label(frameTriangResult, text="", bg=bgcolor, fg=fgcolor)
labelResultOverworldDist.grid(column=2, row=0, sticky="W")

labelResultNetherDist = Label(frameTriangResult, text="", bg=bgcolor, fg=fgcolor)
labelResultNetherDist.grid(column=2, row=1, sticky="W")

#click events
labelResultOverworldVal.bind("<Button-1>", lambda e:clipboard.copy(labelResultOverworldVal.cget("text") + labelResultOverworldDist.cget("text")))
labelResultOverworldDist.bind("<Button-1>", lambda e:clipboard.copy(labelResultOverworldVal.cget("text") + labelResultOverworldDist.cget("text")))
labelResultNetherVal.bind("<Button-1>",  lambda e:clipboard.copy(labelResultNetherVal.cget("text") + labelResultNetherDist.cget("text")))
labelResultNetherDist.bind("<Button-1>",  lambda e:clipboard.copy(labelResultNetherVal.cget("text") + labelResultNetherDist.cget("text")))

def reset():
    print("reset")
    global eye1, eye2, eyeCount
    eye1 = []
    eye2 = []
    eyeCount = 0
    labelEye1Val.configure(text="-")
    labelEye2Val.configure(text="-")
    labelResultNetherDist.configure(text="")
    labelResultNetherVal.configure(text="-")
    labelResultOverworldDist.configure(text="")
    labelResultOverworldVal.configure(text="-")
    labelDivineVal.config(text="-")

    for label in labelDivineCords:
        label.configure(text="")

    for label in labelDivineDistance:
        label.configure(text="")

def deleteEye(label):
    global eyeCount, eye1, eye2
    if eyeCount == 1 and label == labelEye1Val:
        eye1 = []
        labelEye1Val.configure(text="-")
        eyeCount = 0

    elif eyeCount == 2 and label == labelEye2Val:
        eye2 = []
        labelEye2Val.configure(text="-")
        eyeCount = 1
    
    elif eyeCount == 2 and label == labelEye1Val:
        eye1 = eye2.copy()
        eye2 = []
        labelEye1Val.configure(text=labelEye2Val.cget("text"))
        labelEye2Val.configure(text="-")
        eyeCount = 1

for label in [labelEye1Val, labelEye2Val]:
    label.bind("<Enter>", lambda e,label=label:label.focus_set())
    label.bind("<Leave>", lambda e:window.focus_set())
    label.bind("<Delete>", lambda e,label=label:deleteEye(label))


# labels for divine
labelDivine = Label(frameDivine, text="Divine: ", bg=bgcolor, fg=fgcolor)
labelDivine.grid(column=0, row=0, sticky="W")

labelDivineVal = Label(frameDivine, text="-", bg=bgcolor, fg="#60db81")
labelDivineVal.grid(column=1, row=0, sticky="W")

labelDivineCords = []
labelDivineDistance = []

# crete 3 lables for divine blind cords
for i in range(3):
    lc = Label(frameDivine, text="", bg=bgcolor, fg=fgcolor)
    ld = Label(frameDivine, text="", bg=bgcolor, fg=fgcolor)
    lc.grid(column=3, row=i, sticky="W")
    ld.grid(column=4, row=i, sticky="W")

    lc.bind("<Button-1>", lambda e,lc=lc,ld=ld:clipboard.copy(lc.cget("text") + ld.cget("text")))
    ld.bind("<Button-1>", lambda e,lc=lc,ld=ld:clipboard.copy(lc.cget("text") + ld.cget("text")))

    labelDivineCords.append(lc)
    labelDivineDistance.append(ld)


buttonReset = Button(frameDivine, text="Reset", command = reset, bg="#222222", fg=fgcolor)
buttonReset.place(x=0, y=60)

# pack frames to window
frameTriang.place(x=5, y=0)
frameTriangResult.place(x=5, y=44)
frameDivine.place(x=225, y=0)

# --- CLIPBOARD CODE ---

cb = clipboard.paste()

while run:
    if scheduleReset:
        reset()
        scheduleReset = False

    # wait for clipboard to change
    if clipboard.paste() != cb:
        cb = clipboard.paste()
        # check if clipboard is text
        if len(cb) != 0:
            pars = cb.split()
            # F3 + C
            if pars[0] == "/execute":
                # triangualtion
                if pars[2] == "minecraft:overworld":

                    eyeCount += 1
                    if eyeCount == 1:
                        eye1 = pars[6:]
                        labelEye1Val.configure(text = "X: {0:<6} Z: {1:<6} | {2:.2f}°".format(int(float(eye1[0])), int(float(eye1[2])), ((float(eye1[3]) - 180) % 360 - 180)))

                    elif eyeCount == 2:
                        eye2 = pars[6:]
                        labelEye2Val.configure(text = "X: {0:<6} Z: {1:<6} | {2:.2f}°".format(int(float(eye2[0])), int(float(eye2[2])), ((float(eye2[3]) - 180) % 360 - 180)))

                    if(eyeCount == 2):
                        
                        
                        pos1 = [float(eye1[2]), float(eye1[0])]
                        ang1 = math.radians(float(eye1[3]))

                        #            z                  x
                        pos2 = [float(eye2[2]), float(eye2[0])]
                        ang2 = math.radians(float(eye2[3]))

                        #coefficient matrix
                        mat = [[math.sin(ang1), math.cos(ang1)],[math.sin(ang2), math.cos(ang2)]]

                        #vector
                        vec = [ pos1[0] * math.sin(ang1) + pos1[1] * math.cos(ang1),
                                pos2[0] * math.sin(ang2) + pos2[1] * math.cos(ang2)]

                        #solve linear equation
                        x = linalg.solve(mat, vec)
                        

                        labelResultOverworldVal.configure(text="X: {0:<6} Z: {1:<6}".format(int(x[1]), int(x[0])))
                        labelResultOverworldDist.configure(text="({0})".format(int(math.dist(pos1, x))))

                        labelResultNetherVal.configure(text="X: {0:<6} Z: {1:<6}".format(int(x[1] / 8), int(x[0] / 8)))
                        labelResultNetherDist.configure(text="({0})".format(int(math.dist(pos1, x) / 8)))

                        clipboard.copy("Nether X: {0} Z: {1} ({2})".format(int(x[1] / 8), int(x[0] / 8), int(math.dist(pos1, x) / 8)))



                # checkt divine distance
                if pars[2] == "minecraft:the_nether":
                    if divine != -1:
                        dist = []
                        for i in range(3):
                            dist.append(math.dist([float(pars[6]), float(pars[8])], divineTable[divine][i]))

                        for i in range(3):
                            labelDivineDistance[i].configure(text="({0})".format(int(dist[i])))
                            if dist[i] > dist[(i + 1) % 3] and dist[i] > dist[(i + 2) % 3]:
                                labelDivineDistance[i].configure(fg="#db6060")
                            elif dist[i] < dist[(i + 1) % 3] and dist[i] < dist[(i + 2) % 3]:
                                labelDivineDistance[i].configure(fg="#60db81")
                            else:
                                labelDivineDistance[i].configure(fg="#dbbc60")

            # F3 + I
            elif pars[0] == "/setblock":
                if not(int(pars[1]) > 15 or int(pars[1]) < 0 or int(pars[3]) > 15 or int(pars[3]) < 0):
                    divine = int(pars[1])
                    print(divine)
                    print(divineTable[divine])
                    labelDivineVal.configure(text=divine)

                    for i in range(3):
                        labelDivineCords[i].configure(text="  X: {0:<5} Z: {1:<5}".format(divineTable[divine][i][0], divineTable[divine][i][1]))


    window.update()

    time.sleep(0.01)

