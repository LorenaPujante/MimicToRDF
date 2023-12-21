
from enum import Enum


######################
#  JERARQUIA LOGICA  #
######################

class ServiceType(Enum):
    Medical = 0
    Surgical = 1
    Neonatal = 2   # Newborns and maternity

class Service:
    def __init__(self, id, description, abrev, type):
        self.id = id
        self.description = description
        self.abrev = abrev
        self.type = type
        self.hospUnits = []  # IDs are saved
        self.rooms = []

class HospUnit:
    def __init__(self, id, description, abrev):
        self.id = id
        self.description = description
        self.abrev = abrev
        self.rooms = []         # IDs are saved
        self.beds = []          # IDs are saved
        self.service = None     # The object is saved


########################
#  JERARQUIA ESPACIAL  #
########################

class Bed:
    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.parent = None      # IDs are saved
        self.nextTo = []        # IDs are saved
        self.opposite = []      # IDs are saved
        self.hospUnit = None    # IDs are saved

class Room:
    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.parent = None          # IDs are saved
        self.nextTo = []            # IDs are saved
        self.opposite = []        # IDs are saved
        self.hospUnit = None        # IDs are saved     # All Rooms have this attribute
        self.service = None         # IDs are saved     # Only Rooms from Services S0-S7 have this attribute
        self.beds = []              # IDs are saved

class Corridor:
    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.nextTo = {0:None, 1:None, 2:None, 3:None, 4:None, 5:None}    # IDs are saved
        self.rooms = []         # The object is saved
        self.roomsBorder = {'leftTop':None, 'leftBottom':None, 'rightTop':None, 'rightBottom':None, 
                            'topLeft':None, 'topRight':None, 'bottomLeft':None, 'bottomRight':None}   # The objects are saved


#############
# PACIENTES #
#############

class Patient:
    def __init__(self, id, birth, sex, death):
        self.id = id
        self.sex = sex
        self.birth = birth
        self.death = death
        self.stepLocations = {}     # IDs are saved
        self.episodes = []  # The objects are saved
        self.seir = [None, None, None, None]     # To save in which step starts each stage


###########
# EVENTOS #
###########

class Episode:
    def __init__(self, id, description, start, end, patient):
        self.id = id
        self.description = description
        self.start = start
        self.end = end
        self.patient = patient  # IDs are saved
        self.events = []   # The objects are saved
        self.hospPerTM = []

class EventType(Enum):
    Hospitalization = 0     # (CIU and ER are included here)
    Radiology = 1
    Surgery = 2
    Death = 3
    TestMicro = 4

class Event:
    def __init__(self, id, description, start, end, location, service, episode, type):
        self.id = id
        self.description = description
        self.start = start
        self.end = end
        self.location = location    # IDs are saved
        self.hospUnit = None      # IDs are saved
        self.service = service      # IDs are saved
        self.type = type
        self.episode = episode      # IDs are saved
            # To save extra info
        self.extra1 = None  # For example, the Microorganism of a TestMicro (object)  
        self.extra2 = None  # For example, if the Microorganism is MDR

class Microorganism:
    def __init__(self, id, description):
        self.id = id
        self.description = description
        
class HospitalizationDummy:
    def __init__(self, id, description, episode):
        self.id = id
        self.description = description
        self.episode = episode  # IDs are saved