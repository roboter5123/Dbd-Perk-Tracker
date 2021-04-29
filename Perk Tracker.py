############################################################################################################################################################################

#import dom so i can parse xml
from xml.dom.minidom import parse
import xml.dom.minidom

#for UI
from tkinter import *
import tkinter as tk

#for math.ceil
import math

############################################################################################################################################################################

#declaring Variables for the tree and screen
dokument = xml.dom.minidom.parse("H:\Dropbox\Perk Tracker\Template.prk")
perklist = dokument.documentElement

########################################################################################################

#erschafft fenster
global window
window = tk.Tk()

#setzt standard größe
window.geometry('1550x872')

#setzt fenster name
window.title("Perk Tracker")

########################################################################################################

#dicts für charactere

global survivors
global killer
global dict

############################################################################################################################################################################
#Klassen definieren
############################################################################################################################################################################


class character:

    def __init__(self, name, chartype):

        self.name = name
        self.chartype = chartype


    def perks(self, possessed, unlocked, locked):

        self.possessed = possessed
        self.unlocked = unlocked
        self.locked = locked


    def detBackground(self):

        if self.chartype == 'killer':

            self.bg = 'red2'

        elif self.chartype == 'survivor':

            self.bg = 'powder blue'

        else:

            self.bg = 'deep pink'


    def btnCreate(self, frm_master):

        self.detBackground()
        self.frm_master = frm_master
        self.btn = tk.Button(master = self.frm_master, text = name_prepare(self.name), bg = self.bg, command = lambda : make_btn_perk(self))


    def btnDraw(self, coords):

        self.frm_master.rowconfigure(coords['y'], weight = 1)
        self.frm_master.columnconfigure(coords['x'], weight = 1)
        self.btn.grid(row = coords['y'], column = coords['x'], sticky = 'nsew')

############################################

class perk:

    def __init__(self, name, status):

        self.name = name
        self.status = status


    def detBackground(self):

        if self.status == 'possessed':

            self.bg = 'green'

        elif self.status == 'unlocked':

             self.bg = 'yellow'

        elif self.status == 'locked':

            self.bg = 'red'

        else:

            self.bg = 'deep pink'


    def frmCreate(self, frm_master, coords):

        self.detBackground()
        self.frm_master = frm_master

        self.frm = tk.Frame(master = frm_master, background = self.bg)

        self.btn_possessed = tk.Button(master = self.frm, bg = self.bg, width = 2, height = 1)
        self.btn_unlocked = tk.Button(master = self.frm, bg = self.bg, width = 2, height = 1)

        self.load = PhotoImage(file = fr"H:\Dropbox\Perk Tracker\img\{self.name}.png")
        self.img = tk.Label(self.frm, image = self.load, background = self.bg)

        self.text = tk.Label(master = self.frm, text = self.name, background=self.bg)


    def frm_draw(self, coords):
    
        self.frm_master.columnconfigure(coords['y'], weight = 1)
        self.frm_master.rowconfigure(coords['x'], weight = 1)

        self.frm.grid(row = coords['y'], column = coords['x'], padx=5, pady=5, sticky = 'nsew')

        self.frm.columnconfigure(1, weight = 1)
        self.frm.rowconfigure([0,1], weight = 1)

        self.btn_possessed.grid(row = 1, column = 0,padx=5)
        self.btn_unlocked.grid(row = 1, column = 2,padx=5)

        self.img.grid(row = 0, column =1, padx=2, pady=0)

        self.text.grid(row = 1, column = 1,padx=5, pady=2)


############################################################################################################################################################################
#funktionen fürs backend
############################################################################################################################################################################

#creates character objects
def create_objects(perklist):

    dict = {}
    last = perklist.getElementsByTagName("killer")[1]
    last = last.parentNode
    perks = [perklist.getElementsByTagName("perk")[0], last]

    for perk in perks:

        characters = []
        children = perk.childNodes

        for child in children:

            if child.nodeType == 3:

                continue 

            elif child.tagName == "name" or child.tagName == "unlocked" or child.tagName == "description":

                continue
     
            elif child.tagName == "survivor" or child.tagName == "killer":

                char_type = child.tagName

            else:

                characters.append(child.tagName)

        for char in characters:
	
            name = char
            char = character(char, char_type)
            dict[name] = char

    return(dict)

########################################################################################################

#sort Perks into lists
def sortperks(perklist, character_name, char_type):


    #Im Baum in den tag perks navigieren
    perks = perklist.getElementsByTagName("perk")

    #listen um die ergebnise zu speichern
    possessed = {}
    unlocked = {}
    locked = {}

    for prk in perks:

        #Wenn ein Perk nicht dem type des characters entspricht (killer/survivor) wird er übersprungen. 
        #Dies bewirkt das alle killer/ survivor nur perks in den listen haben die sie im spiel auch haben können
        try:

            perk_type = prk.getElementsByTagName(char_type)[0].nodeName

        except:

            continue

        perk_character = False

        #sucht den xml tag mit dem character name und speichert den inhalt in variable
        try:

            perk_character = prk.getElementsByTagName(character_name)[0].childNodes[0].nodeValue

        except:

            pass

        #needed because i didn't put a None tag in for All_surv perks
        #sucht den xml tag mit unlocked und speichert den inhalt in variable
        try:

            perkunlocked = prk.getElementsByTagName("unlocked")[0].childNodes[0].nodeValue
        
        except:

            perkunlocked = None

        #sucht den xml tag mit name und speichert den inhalt in variable
        perkname = prk.getElementsByTagName("name")[0].childNodes[0].nodeValue

        
        #sortiert die perks in listen ein. Possessed is der char hat den perk
        if perk_character == 'True':
            
            possessed[perkname] = perk(perkname,'possessed')

        elif perk_character == 'False' and (perkunlocked == 'True' or perkunlocked == None):

            unlocked[perkname] = perk(perkname,'unlocked')

        else:

            locked[perkname] = perk(perkname,'locked')
    
    return(possessed, unlocked, locked)

########################################################################################################

#splitet killer und survivor in verschiedene dicts
def split_characters(dict):
    
    survivors = {}
    killers = {}
    error = {}

    for char in dict:

        if dict[char].chartype == 'killer':

            killers[char] = dict[char]
        
        elif dict[char].chartype == 'survivor':

            survivors[char] = dict[char]

        else:

            error[char] = dict[char]

    return(survivors, killers, error)

########################################################################################################


########################################################################################################

#bereitet die namen for um sie dem user zu zeigen zb 'dwight_fairfield > Dwight Fairdield '
def name_prepare(character):
    
    character = character.split('_')
    name = character[0].capitalize()

    for char in character:

        if char == character[0]:

            continue 

        else:

            name = name + ' ' + char.capitalize()

    return(name)

########################################################################################################

#bereitet die namen for um sie im programm zu benutzen zb 'Dwight Fairdield > dwight_fairfield'
def name_depare(character):
    
    character = character.split(' ')
    name = character[0].lower()

    for char in character:

        if char == character[0]:

            continue 

        else:

            name = name + '_' +char.lower()

    return(name)


############################################################################################################################################################################
#funktionen fürs UI
############################################################################################################################################################################

#Created alle Widgets die im prigramm benutzt werden. Damit ich sie nich immer wieder neu machen muss
def initialize_ui():

    global frm_left
    frm_left = tk.Frame(master = window, bg = "powder blue")

    global frm_right
    frm_right = tk.Frame(master=window, bg="red2")

    global btn_survivor
    btn_survivor = tk.Button(master = frm_left, width = 40 ,height = 6, text = "Survivor", bg="powder blue",command = lambda: character_screen(survivors,"powder blue"))

    global btn_killer
    btn_killer = tk.Button(master = frm_right, width = 40,height = 6, text = "Killer", bg = "red3", command = lambda: character_screen(killer, "red2"))

    for char in dict:

        dict[char].btnCreate(frm_left)

    global btn_back
    btn_back = tk.Button(master = frm_left, text = 'Back', bg = "white", command = lambda : first_screen())


def first_screen():

    for row_num in range(frm_left.grid_size()[1]):

        frm_left.rowconfigure(row_num, weight = 0)

    for char in dict:

        dict[char].btn.grid_remove()

    btn_back.grid_forget()

    #configed den grid des fensters für die 2 frames
    window.rowconfigure(0, weight = 1, uniform = 'group 1')
    window.columnconfigure([0,1], weight = 1, minsize = 0, uniform = 'group 1')

    #zeichnet die frames für Links
    frm_left.config(bg =  'powder blue')
    frm_left.grid(row = 0, column = 0, sticky = 'nsew')
    frm_left.rowconfigure([0,1], weight = 1)
    frm_left.columnconfigure(0, weight = 1)

    #zeichnet die frames für rechts
    frm_right.config(bg = "red2")
    frm_right.grid(row = 0, column = 1, sticky = 'nsew')
    frm_right.rowconfigure(0, weight = 1)
    frm_right.columnconfigure(0, weight = 1)

    #zeichnet knopf survivor
    btn_survivor.pack(fill = "none", expand = 'true')

    #zeichnet knopf killer
    btn_killer.pack(fill = "none", expand = 'true')

    window.mainloop()


########################################################################################################

#create frames for character and perks
def character_screen(characters, backgr):

    btn_killer.pack_forget()
    btn_survivor.pack_forget()

    frm_left.config(bg =  backgr)
    frm_right.config(bg = "bisque2")
    #frm_chars.pack(fill = BOTH, expand = 'True')
    window.rowconfigure(0, weight = 1)
    window.columnconfigure(0, weight = 1, minsize = 230, uniform = 'group 1')
    window.columnconfigure(1, weight = 8, minsize = 1300, uniform = 'group 1')

    coord = {'x' : 0, 'y' : 0}
    global charlen
    charlen = len(characters)

#draws characterbuttons
    for char in characters:

        characters[char].btnDraw(coord)


        if coord['y'] >= (charlen/2) - 1:

            coord['y'] = 0
            coord['x'] += 1

        else:

            coord['y'] += 1
            
    if (charlen - 1) % 2 == 1:

        frm_left.rowconfigure(math.floor(charlen/2 +1), weight = 1, uniform = 'group 2')
        btn_back.grid(column = 0 , row = math.floor( charlen/2 + 1 ),columnspan = 2, sticky = 'nsew')

    else:

        btn_back.grid(column = 1 , row = math.floor( charlen/2 ), sticky = 'nsew')
        
    
    window.mainloop()

########################################################################################################

def make_btn_perk(char):
    
    coord = {'y' : 0, 'x' : 0}
    max_x = 6

    for prk in char.possessed:


        char.possessed[prk].frmCreate(frm_right, coord)
        char.possessed[prk].frm_draw(coord)

        if coord['x'] == max_x:

            coord['x'] = 0
            coord['y'] = coord['y'] + 1

        else:

            coord['x'] = coord['x'] +1

    for prk in char.unlocked:


        char.unlocked[prk].frmCreate(frm_right, coord)
        char.unlocked[prk].frm_draw(coord)

        if coord['x'] == max_x:

            coord['x'] = 0
            coord['y'] = coord['y'] + 1

        else:

            coord['x'] = coord['x'] +1

    for prk in char.locked:


        char.locked[prk].frmCreate(frm_right, coord)
        char.locked[prk].frm_draw(coord)

        if coord['x'] == max_x:

            coord['x'] = 0
            coord['y'] = coord['y'] + 1

        else:

            coord['x'] = coord['x'] +1

############################################################################################################################################################################
#Main Code
############################################################################################################################################################################

#Character objekte erstellen
dict = create_objects(perklist)

#character objekten perks zuweisen
for char in dict:

    dict[char].possessed, dict[char].unlocked, dict[char].locked = sortperks(perklist, dict[char].name, dict[char].chartype)

#character objecte in survivor/killer aufteilen
survivors, killer, error = split_characters(dict)

initialize_ui()

first_screen()