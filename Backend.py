#import dom so i can parse xml
from xml.dom.minidom import parse
import xml.dom.minidom


#declaring Variables for the tree and screen

global file_handle
file_handle = open("/config/workspace/Dbd-Perk-Tracker/Template.prk", "r+")
dokument = xml.dom.minidom.parse(file_handle)

perklist = dokument.documentElement


#dicts for characters
global survivors
global killer
global dict


class character:

    def __init__(self, name, chartype):

        self.name = name
        self.chartype = chartype


    def perks(self, possessed, unlocked, locked):

        self.possessed = possessed
        self.unlocked = unlocked
        self.locked = locked


class perk:

    def __init__(self, name, status):

        self.name = name
        self.status = status

    def save(self,char, perklist):
        print(self.name)
        perks = perklist.getElementsByTagName("perk")

        for prk in perks:

            if prk.getAttribute("name") == name_depare(self.name):

                perks = prk
                perks = perks.getElementsByTagName(char)
                perks = perks.item(0).childNodes[0]
                perks.data = "Test"
                perks.writexml(file_handle)
                break

        else:

            pass




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

#########################################

def name_depare(character):
    
    character = character.split(' ')
    name = character[0].lower()

    for char in character:

        if char == character[0]:

            continue 

        else:

            name = name + '_' +char.lower()

    return(name)



########################
#Character objekte erstellen
dict = create_objects(perklist)

#character objekten perks zuweisen
for char in dict:

    dict[char].possessed, dict[char].unlocked, dict[char].locked = sortperks(perklist, dict[char].name, dict[char].chartype)

#character objecte in survivor/killer aufteilen
survivors, killer, error = split_characters(dict)

survivors['dwight_fairfield'].possessed['Bond'].save(survivors['dwight_fairfield'].name,perklist)
