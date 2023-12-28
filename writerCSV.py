import os
from classes import *
from weightsLocsHierarchy import weights
from variablesFiles import getTwoLastDigitsNumber
from variablesWriter import nameFiles_Classes, nameFiles_Rels


##################
# INITIALIZATION #
##################

def setFolderOutputCSV(folder, minYearN, maxYearN, minYear, maxYear, maxEvents):
    global folderOutput_CSV
    folderOutput_CSV = folder
    if (not os.path.exists(folderOutput_CSV)):
        os.makedirs(folderOutput_CSV)
    
    minYearN_2digits = getTwoLastDigitsNumber(minYearN)
    maxYearN_2digits = getTwoLastDigitsNumber(maxYearN)
    minYear_2digits = getTwoLastDigitsNumber(minYear)
    maxYear_2digits = getTwoLastDigitsNumber(maxYear)
    if maxEvents == 0:
        maxEvents_div1000 = "all"
    else:
        maxEvents_div1000 = int(maxEvents/1000)
    
    global folderOutput_Classes_CSV
    folderOutput_Classes_CSV = folderOutput_CSV + "\\Classes_{}-{}__{}-{}__{}".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    if (not os.path.exists(folderOutput_Classes_CSV)):
        os.makedirs(folderOutput_Classes_CSV)

    global folderOutput_Relations_CSV
    folderOutput_Relations_CSV = folderOutput_CSV + "\\Relations_{}-{}__{}-{}__{}".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    if (not os.path.exists(folderOutput_Relations_CSV)):
        os.makedirs(folderOutput_Relations_CSV)



''''''''''''''
'''  MAIN  '''
''''''''''''''

def printCSV(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms):
    printClassesCSV(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms)
    printRelsCSV(dicServices, dicCorridors, dicRooms, dicBeds, dicPatients)


def printClassesCSV(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms):
    # Logical Hospital
    printServicesCSV(dicServices)
    printHospUnitsCSV(dicHospUnits)
    
    # Physical Hospital
    printCorridorsCSV(dicCorridors)
    printRoomsCSV(dicRooms)
    printBedsCSV(dicBeds)

    # Patients
    printPatientsCSV(dicPatients)

    # Microorganisms
    printMicroorganismsCSV(dicMicroorganisms)

    # Episodes y Events
    printClassesEpisodesEventsCSV(dicPatients)


def printRelsCSV(dicServicios, dicPasillos, dicRooms, dicBeds, dicPatients):
    # Hospital
    printRelationsHospitalCSV(dicServicios, dicPasillos, dicRooms, dicBeds)

    # Patients, Episodes and Events
    printRelationsEpisodesEventsCSV(dicPatients)



''''''''''''''''''
'''  HOSPITAL  '''
''''''''''''''''''

###############
# CSV CLASSES #
###############

# MAIN
def printClassesHospitalCSV(dicServices, dicHospUnits, dicRooms, dicBeds):
    
    printServicesCSV(dicServices)
    printHospUnitsCSV(dicHospUnits)
    
    printRoomsCSV(dicRooms)
    printBedsCSV(dicBeds)


# Services
def printServicesCSV(dicServices):
    file = open("{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['service'], '.csv'), 'w')
    toWrite = "id,description,abbreviation\n"
    for id in dicServices:
        toWrite = toWrite + "{},{},{}\n".format(id,dicServices[id].description,dicServices[id].abrev)
    file.write(toWrite)
    file.close()

# Hospitalization Units
def printHospUnitsCSV(dicHospUnits):
    file = open("{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['uh'], '.csv'), 'w')
    toWrite = "id,description,abbreviation\n"
    for id, value in dicHospUnits.items():
        toWrite = toWrite + "{},{},{}\n".format(id,value.description,value.abrev)    
    file.write(toWrite)
    file.close()


# Corridors
def printCorridorsCSV(dicCorridors):
    file = open("{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['corridor'], '.csv'), 'w')
    toWrite = "id,description\n"
    for id, value in dicCorridors.items():
        toWrite = toWrite + "{},{}\n".format(id,value.description)
    file.write(toWrite)
    file.close()

# Rooms
def printRoomsCSV(dicRooms):
    file = open("{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['room'], '.csv'), 'w')
    toWrite = "id,description\n"
    for ward in dicRooms.values():
        for room in ward.values():
            toWrite = toWrite + "{},{}\n".format(room.id,room.description)
    file.write(toWrite)
    file.close()

# Beds
def printBedsCSV(dicBeds):
    file = open("{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['bed'], '.csv'), 'w')
    toWrite = "id,description\n"
    for id, value in dicBeds.items():
        toWrite = toWrite + "{},{}\n".format(id,value.description)
    file.write(toWrite)
    file.close()



##################
# CSV RELACIONES #
##################

# MAIN
def printRelationsHospitalCSV(dicServices, dicCorridors, dicRooms, dicBeds):
    
    printRel_ServiceHospUnitCSV(dicServices)
    
    printRel_CorridorRoomCSV(dicCorridors)
    printRel_RoomBedCSV(dicRooms)

    printRel_Bed_NextToOppositeCSV(dicBeds, "{}{}".format(nameFiles_Rels['bed_nt'], '.csv'), "nextTo")
    printRel_Bed_NextToOppositeCSV(dicBeds, "{}{}".format(nameFiles_Rels['bed_ot'], '.csv'), "opposite")
    printRel_Room_NextToOppositeCSV(dicRooms, "{}{}".format(nameFiles_Rels['room_nt'], '.csv'), "nextTo")
    printRel_Room_NextToOppositeCSV(dicRooms, "{}{}".format(nameFiles_Rels['room_ot'], '.csv'), "opposite")
    printRel_Corridor_NextToCSV(dicCorridors)
    

# Relation Service - HospUnit
def printRel_ServiceHospUnitCSV(dicServices):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['serv_uh'], '.csv'), 'w')
    toWrite = "idService,idHospUnit,cost\n"
    for s in dicServices.values():
        for uh in s.hospUnits:
            toWrite = toWrite + "{},{},{}\n".format(s.id,uh,weights['hospUnitFromService'])
    file.write(toWrite)
    file.close()


# Relation Corridor - Room
def printRel_CorridorRoomCSV(dicCorridors):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['room_corridor'], '.csv'), 'w')
    toWrite = "idCorridor,idRoom,cost\n"
    for p in dicCorridors.values():
        for r in p.rooms:
            toWrite = toWrite + "{},{},{}\n".format(p.id,r.id,weights["placedIn_RoomCorridor"])
    file.write(toWrite)
    file.close()

# Relation Room - Bed
def printRel_RoomBedCSV(dicRooms):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['bed_room'], '.csv'), 'w')
    toWrite = "idRoom,idBed,cost\n"
    for ward in dicRooms.values():
        for r in ward.values():
            for b in r.beds:
                toWrite = toWrite + "{},{},{}\n".format(r.id,b,weights["placedIn_SeatRoom"])
    file.write(toWrite)
    file.close()
  

# Relation Room - Room    (nextTo  //  opposite)
def printRel_Room_NextToOppositeCSV(dicRooms, nameFile, nextOrOpposite):
    file = open(folderOutput_Relations_CSV + nameFile, 'w')
    toWrite = "idRoom1,idRoom2,cost\n"
    
    writtenPairs = {}

    for ward in dicRooms.values():
        for room in ward.values():
            # NextTo neighbors or Opposite neighbours are selected
            listNeighbours = None
            if nextOrOpposite == "nextTo":
                listNeighbours = room.nextTo
            elif nextOrOpposite == "opposite":
                listNeighbours = room.opposite
            
            # Pairs (Room, Neighbour) are added to write
            for neighbour in listNeighbours:
                keyPair1 = "{}-{}".format(neighbour,room.id)
                if keyPair1 not in writtenPairs:
                    toWrite = toWrite + "{},{}".format(room.id,neighbour)
                    if nextOrOpposite == "nextTo":
                        toWrite += ",{}\n".format(weights["nextTo_Room"])
                    elif nextOrOpposite == "opposite":
                        toWrite += ",{}\n".format(weights["opposite_Room"])

                    # The pairs (Neighbor, Room) are also written in writtenPairs so as not to repeat it later
                    keyPair2 = "{}-{}".format(room.id,neighbour)
                    writtenPairs[keyPair2] = 1
    file.write(toWrite)
    file.close()

# Relation Cama - Cama    (nextTo  //  opposite)
def printRel_Bed_NextToOppositeCSV(dicBeds, nameFile, nextOrOpposite):
    file = open(folderOutput_Relations_CSV + nameFile, 'w')
    toWrite = "idBed1,idBed2,cost\n"

    writtenPairs = []
    for bed in dicBeds.values():
        # NextTo neighbors or Opposite neighbours are selected
        listNeighbours = None
        if nextOrOpposite == "nextTo":
            listNeighbours = bed.nextTo
        elif nextOrOpposite == "opposite":
            listNeighbours = bed.opposite

        # Pairs (Bed, Neighbour) are added to write
        for neigbour in listNeighbours:
            keyPair1 = "{}-{}".format(neigbour,bed.id)
            if keyPair1 not in writtenPairs:
                toWrite = toWrite + "{},{}".format(bed.id,neigbour)
                if nextOrOpposite == "nextTo":
                    toWrite += ",{}\n".format(weights["nextTo_Seat"])    
                elif nextOrOpposite == "opposite":
                    toWrite += ",{}\n".format(weights["opposite_Seat"])

                # The pairs (Neighbor, Room) are also written in writtenPairs so as not to repeat it later
                keyPair2 = "{}-{}".format(bed.id,neigbour)
                writtenPairs.append(keyPair2)

    file.write(toWrite)
    file.close()

# Relation Corridor - Corridor  (nextTo)
def printRel_Corridor_NextToCSV(dicCorridors):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['corridor_nt'], '.csv'), 'w')
    toWrite = "idCorr1,idCorr2,cost\n"

    writtenPairs = []
    for corr in dicCorridors.values():
        # Neighbour 0
        if corr.nextTo[0] is not None:
            neighbour = corr.nextTo[0]
            keyPair1 = "{}-{}".format(neighbour,corr.id)
            if keyPair1 not in writtenPairs:
                toWrite = toWrite + "{},{},{}\n".format(corr.id,neighbour,weights["nextTo_Corridor"])

                keypAIR2 = "{}-{}".format(corr.id,neighbour)
                writtenPairs.append(keypAIR2)
        
        # Neighbour 1
        if corr.nextTo[1] is not None:
            neighbour = corr.nextTo[1]
            keyPair1 = "{}-{}".format(neighbour,corr.id)
            if keyPair1 not in writtenPairs:
                toWrite = toWrite + "{},{},{}\n".format(corr.id,neighbour,weights["nextTo_Corridor"])

                keypAIR2 = "{}-{}".format(corr.id,neighbour)
                writtenPairs.append(keypAIR2)
        
    file.write(toWrite)
    file.close()  



''''''''''''''''''
'''  PATIENTS  '''
''''''''''''''''''

def printPatientsCSV(dicPatients):
    file = open("{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['patient'], '.csv'), 'w')
    toWrite = "id,dateBirth,sex\n"
    for p in dicPatients.values():
        toWrite = toWrite + "{},{},{}\n".format(p.id,p.birth.strftime("%Y-%m-%dT%H:%M:%SZ"),p.sex)
    file.write(toWrite)
    file.close()



''''''''''''''''''''''''
'''  MICROORGANISM   '''
''''''''''''''''''''''''

def printMicroorganismsCSV(dicMicroorganisms):
    file = open("{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['microorganism'], '.csv'), 'w')
    toWrite = "id,description\n"
    for m in dicMicroorganisms.values():
        toWrite = toWrite + "{},{}\n".format(m.id,m.description)
    file.write(toWrite)
    file.close()



''''''''''''''''''''''''''''''
'''  EPISODES AND EVENTS   '''
''''''''''''''''''''''''''''''

##############
# CSV CLASSES #
##############

# MAIN
def printClassesEpisodesEventsCSV(dicPatients):
    printEpisodesCSV(dicPatients)

    printEventsCSV(dicPatients, EventType.Hospitalization, "{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['hospitalization'], '.csv'))
    printEventsCSV(dicPatients, EventType.Death, "{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['death'], '.csv'))
    printEventsCSV(dicPatients, EventType.TestMicro, "{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['testMicro'], '.csv'))


# Episodes
def printEpisodesCSV(dicPatients):    
    file = open("{}{}{}".format(folderOutput_Classes_CSV, nameFiles_Classes['episode'], '.csv'), 'w')
    toWrite = "id,description,start,end\n"  # Format: %Y-%m-%dT%H:%M:%SZ  ->  2022-01-01T00:00:00Z
    for patient in dicPatients.values():
        for ep in patient.episodes:
            toWrite += "{},{},{},{}\n".format(ep.id,ep.description,ep.start.strftime("%Y-%m-%dT%H:%M:%SZ"),ep.end.strftime("%Y-%m-%dT%H:%M:%SZ"))
    file.write(toWrite)
    file.close()

# Eventes
def printEventsCSV(dicPatients, type, nameFile):    
    file = open(nameFile, 'w')
    toWrite = "id,description,start,end\n"  # Format: %Y-%m-%dT%H:%M:%SZ  ->  2022-01-01T00:00:00Z
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.type is type:
                    toWrite += "{},{},{},{}\n".format(ev.id,ev.description,ev.start.strftime("%Y-%m-%dT%H:%M:%SZ"),ev.end.strftime("%Y-%m-%dT%H:%M:%SZ"))
    file.write(toWrite)
    file.close()



##################
# CSV RELATIONS #
##################

# MAIN
def printRelationsEpisodesEventsCSV(dicPatients):
    printRel_EpisodePatientCSV(dicPatients)
    printRel_EventEpisodeCSV(dicPatients)
    printRel_EventBedCSV(dicPatients)
    printRel_EventHospUnitCSV(dicPatients)
    printRel_TestMicroorgCSV(dicPatients)


# Relation Episode-Patient
def printRel_EpisodePatientCSV(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['ep_pat'], '.csv'), 'w')
    toWrite = "idEpisode,idPatient\n"
    for patient in dicPatients.values():
        for ep in patient.episodes:
            toWrite += "{},{}\n".format(ep.id, patient.id)
    file.write(toWrite)
    file.close()

# Relation Event-Episode
def printRel_EventEpisodeCSV(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['ev_ep'], '.csv'), 'w')
    toWrite = "idEvent,idEpisode\n"
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                toWrite += "{},{}\n".format(ev.id, ep.id)
    file.write(toWrite)
    file.close() 

# Relation Event-Bed
def printRel_EventBedCSV(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['ev_bed'], '.csv'), 'w')
    toWrite = "idEvent,idBed\n"
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.location is not None:
                    toWrite += "{},{}\n".format(ev.id, ev.location)
    file.write(toWrite)
    file.close()    

# Relation Event-HospUnit
def printRel_EventHospUnitCSV(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['ev_uh'], '.csv'), 'w')
    toWrite = "idEvent,idHospUnit\n"
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.hospUnit is not None:
                    toWrite += "{},{}\n".format(ev.id, ev.hospUnit)
    file.write(toWrite)
    file.close()    

# Relation TestMicro-Microorganism
def printRel_TestMicroorgCSV(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_CSV, nameFiles_Rels['test_micro'], '.csv'), 'w')
    toWrite = "idEvent,idMicroorg,mdr\n"
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.type is EventType.TestMicro:
                    microorg = ev.extra1
                    toWrite += "{},{},{}\n".format(ev.id, microorg.id, ev.extra2)
    file.write(toWrite)
    file.close() 


