import os
from classes import *
from weightsLocsHierarchy import weights
from variablesFiles import getTwoLastDigitsNumber
from writerNT import *


##################
# INITIALIZATION #
##################

def setFolderOutputNT_star(folder, minYearN, maxYearN, minYear, maxYear, maxEvents):
    global folderOutput_NT_star
    folderOutput_NT_star = folder
    if (not os.path.exists(folderOutput_NT_star)):
        os.makedirs(folderOutput_NT_star)
    
    minYearN_2digits = getTwoLastDigitsNumber(minYearN)
    maxYearN_2digits = getTwoLastDigitsNumber(maxYearN)
    minYear_2digits = getTwoLastDigitsNumber(minYear)
    maxYear_2digits = getTwoLastDigitsNumber(maxYear)
    if maxEvents == 0:
        maxEvents_div1000 = "all"
    else:
        maxEvents_div1000 = int(maxEvents/1000)

    global folderOutput_Classes_NT_star
    folderOutput_Classes_NT_star = folderOutput_NT_star + "\\Classes_{}-{}__{}-{}__{}".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    if (not os.path.exists(folderOutput_Classes_NT_star)):
        os.makedirs(folderOutput_Classes_NT_star)

    global folderOutput_Relations_NT_star
    folderOutput_Relations_NT_star = folderOutput_NT_star + "\\Relations_{}-{}__{}-{}__{}".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    if (not os.path.exists(folderOutput_Relations_NT_star)):
        os.makedirs(folderOutput_Relations_NT_star)

    return folderOutput_Classes_NT_star, folderOutput_Relations_NT_star, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000


''''''''''''''
'''  MAIN  '''
''''''''''''''

def printNT_star(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms):
    printClassesNT_star(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms)
    printRelsNT_star(dicServices, dicCorridors, dicRooms, dicBeds, dicPatients)


def printClassesNT_star(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms):
    # Hospital
    printClassesHospitalNT_star(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds)

    # Patients
    printPatientsNT_star(dicPatients)

    # Microorganismos
    printMicroorganismsNT_star(dicMicroorganisms)

    # Episodes y Events
    printClassesEpisodesEventsNT_star(dicPatients)


def printRelsNT_star(dicServices, dicCorridors, dicRooms, dicBeds, dicPatients):
    # Hospital
    printRelationsHospitalNT_star(dicServices, dicCorridors, dicRooms, dicBeds)

    # Patients, Episodes y Events
    printRelationsEpisodesEventsNT_star(dicPatients)



''''''''''''''''''
'''  HOSPITAL  '''
''''''''''''''''''

###########
# CLASSES #
###########

# MAIN
def printClassesHospitalNT_star(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds):
    
    printServicesNT_star(dicServices)
    printHospUnitsNT_star(dicHospUnits)
    
    printCorridorsNT_star(dicCorridors)
    printRoomsNT_star(dicRooms)
    printBedsNT_star(dicBeds)


# Services
def printServicesNT_star(dicServices):
    file = open("{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['service'], '.nt'), 'w')
    toWrite = getToWriteServicesNT(dicServices)
    file.write(toWrite)
    file.close()

# HospUnits
def printHospUnitsNT_star(dicHospUnits):
    file = open("{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['uh'], '.nt'), 'w')
    toWrite = getToWriteHospUnitsNT(dicHospUnits)   
    file.write(toWrite)
    file.close()


# Corridors
def printCorridorsNT_star(dicCorridors):
    file = open("{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['corridor'], '.nt'), 'w')
    toWrite = getToWriteCorridorsNT(dicCorridors)
    file.write(toWrite)
    file.close()

# Rooms
def printRoomsNT_star(dicRooms):
    file = open("{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['room'], '.nt'), 'w')
    toWrite = getToWriteRoomsNT(dicRooms)
    file.write(toWrite)
    file.close()
    
# Bed ->  Same as with NT
def printBedsNT_star(dicBeds):
    file = open("{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['bed'], '.nt'), 'w')
    writeBedsNT(dicBeds, file)
    file.close()



#############
# RELATIONS #
#############

# MAIN
def printRelationsHospitalNT_star(dicServices, dicCorridors, dicRooms, dicBeds):
    
    printRel_ServiceHospUnitNT_star(dicServices)
    
    printRel_CorridorRoomNT_star(dicCorridors)
    printRel_RoomBedNT_star(dicRooms)

    printRel_Bed_NextToOppositeNT_star(dicBeds, "{}{}".format(nameFiles_Rels['bed_nt'], '.ttl'), "nextTo")
    printRel_Bed_NextToOppositeNT_star(dicBeds, "{}{}".format(nameFiles_Rels['bed_ot'], '.ttl'), "opposite")
    printRel_Room_NextToOppositeNT_star(dicRooms, "{}{}".format(nameFiles_Rels['room_nt'], '.ttl'), "nextTo")
    printRel_Room_NextToOppositeNT_star(dicRooms, "{}{}".format(nameFiles_Rels['room_ot'], '.ttl'), "opposite")
    printRel_Corridor_NextToNT_star(dicCorridors)
    

# Relation Service - HospUnit
def printRel_ServiceHospUnitNT_star(dicServices):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['serv_uh'], '.ttl'), 'w')
    toWrite = ""
    for s in dicServices.values():
        for hu in s.hospUnits:
            toWrite += "<{}#HospitalizationUnit/{}> <{}#hospUnitFromService> <{}#Service/{}>.\n".format(prefixes_nt["hospOnt"],hu, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],s.id)
            toWrite += "<< <{}#HospitalizationUnit/{}> <{}#hospUnitFromService> <{}#Service/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],hu, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],s.id, prefixes_nt["hospOnt"], weights["hospUnitFromService"],prefixes_nt["xmlSchema"])
    file.write(toWrite)
    file.close()

# Relation Corridor - Room
def printRel_CorridorRoomNT_star(dicCorridors):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['room_corridor'], '.ttl'), 'w')
    toWrite = ""
    for c in dicCorridors.values():
        for r in c.rooms:
            toWrite += "<{}#Room/{}> <{}#placedIn> <{}#Corridor/{}>.\n".format(prefixes_nt["hospOnt"],r.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],c.id)
            toWrite += "<< <{}#Room/{}> <{}#placedIn> <{}#Corridor/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],r.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],c.id, prefixes_nt["hospOnt"], weights["placedIn_RoomCorridor"],prefixes_nt["xmlSchema"])
    file.write(toWrite)
    file.close()

# Relation Room - Bed
def printRel_RoomBedNT_star(dicRooms):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['bed_room'], '.ttl'), 'w')
    toWrite = ""
    for ward in dicRooms.values():
        for r in ward.values():
            for b in r.beds:
                toWrite += "<{}#Bed/{}> <{}#placedIn> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],b, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],r.id)
                toWrite += "<< <{}#Bed/{}> <{}#placedIn> <{}#Room/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],b, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],r.id, prefixes_nt["hospOnt"], weights["placedIn_SeatRoom"],prefixes_nt["xmlSchema"])
    file.write(toWrite)
    file.close()


# Relation Room - Room    (nextTo  //  opposite)
def printRel_Room_NextToOppositeNT_star(room, nameFile, nextOrOpposite):
    file = open(folderOutput_Relations_NT_star + nameFile, 'w')
    toWrite = ""
    
    writtenPairs = {}
    for ward in room.values():
        for room in ward.values():
            # NextTo neighbors or Opposite neighbours are selected
            listNeighbours = None
            if nextOrOpposite == "nextTo":
                listNeighbours = room.nextTo
            elif nextOrOpposite == "opposite":
                listNeighbours = room.opposite

            # Pairs (Room, Neighbour) are added to write
            for neighbours in listNeighbours:
                keyPair1 = "{}-{}".format(neighbours,room.id)
                if keyPair1 not in writtenPairs:

                    if nextOrOpposite == "nextTo":
                        toWrite += "<{}#Room/{}> <{}#nextTo> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],room.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbours)
                        toWrite += "<< <{}#Room/{}> <{}#nextTo> <{}#Room/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],room.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbours, prefixes_nt["hospOnt"], weights["nextTo_Room"],prefixes_nt["xmlSchema"])

                    elif nextOrOpposite == "opposite":
                        toWrite += "<{}#Room/{}> <{}#opposite> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],room.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbours)
                        toWrite += "<< <{}#Room/{}> <{}#opposite> <{}#Room/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],room.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbours, prefixes_nt["hospOnt"], weights["opposite_Room"],prefixes_nt["xmlSchema"])

                    # The pairs (Neighbor, Room) are also written in writtenPairs so as not to repeat it later   
                    keyPair2 = "{}-{}".format(room.id,neighbours)
                    writtenPairs[keyPair2] = 1

    file.write(toWrite)
    file.close()

# Relation Bed - Bed    (nextTo  //  opposite)
def printRel_Bed_NextToOppositeNT_star(dicBeds, nameFile, nextOrOpposite):
    file = open(folderOutput_Relations_NT_star + nameFile, 'w')
    toWrite = ""
    
    writtenPairs = {}
    for bed in dicBeds.values():
        # NextTo neighbors or Opposite neighbours are selected
        listNeighbours = None
        if nextOrOpposite == "nextTo":
            listNeighbours = bed.nextTo
        elif nextOrOpposite == "opposite":
            listNeighbours = bed.opposite
        
        # Pairs (Bed, Neighbour) are added to write
        for neighbour in listNeighbours:
            keyPair1 = "{}-{}".format(neighbour,bed.id)
            if keyPair1 not in writtenPairs:

                if nextOrOpposite == "nextTo":
                    toWrite += "<{}#Bed/{}> <{}#nextTo> <{}#Bed/{}>.\n".format(prefixes_nt["hospOnt"],bed.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbour)
                    toWrite += "<< <{}#Bed/{}> <{}#nextTo> <{}#Bed/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],bed.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbour, prefixes_nt["hospOnt"], weights["nextTo_Seat"],prefixes_nt["xmlSchema"])

                elif nextOrOpposite == "opposite":
                    toWrite += "<{}#Bed/{}> <{}#opposite> <{}#Bed/{}>.\n".format(prefixes_nt["hospOnt"],bed.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbour)
                    toWrite += "<< <{}#Bed/{}> <{}#opposite> <{}#Bed/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],bed.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbour, prefixes_nt["hospOnt"], weights["opposite_Seat"],prefixes_nt["xmlSchema"])
                
                # The pairs (Neighbor, Bed) are also written in writtenPairs so as not to repeat it later       
                keyPair2 = "{}-{}".format(bed.id,neighbour)
                writtenPairs[keyPair2] = 1

    file.write(toWrite)
    file.close()

# Relation Corridor - Corridor  (nextTo)
def printRel_Corridor_NextToNT_star(dicCorridors):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['corridor_nt'], '.ttl'), 'w')
    
    writtenPairs = []
    for corr in dicCorridors.values():
        # Neighbour 0
        if corr.nextTo[0] is not None:
            neighbours = corr.nextTo[0]
            keyPair1 = "{}-{}".format(neighbours,corr.id)
            if keyPair1 not in writtenPairs:
                file.write("<{}#Corridor/{}> <{}#nextTo> <{}#Corridor/{}>.\n".format(prefixes_nt["hospOnt"],corr.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbours))
                file.write("<< <{}#Corridor/{}> <{}#nextTo> <{}#Corridor/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],corr.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbours, prefixes_nt["hospOnt"], weights["nextTo_Corridor"],prefixes_nt["xmlSchema"]))

                keyPair2 = "{}-{}".format(corr.id,neighbours)
                writtenPairs.append(keyPair2)
        
        # Neighbour 1
        if corr.nextTo[1] is not None:
            neighbours = corr.nextTo[1]
            keyPair1 = "{}-{}".format(neighbours,corr.id)
            if keyPair1 not in writtenPairs:
                file.write("<{}#Corridor/{}> <{}#nextTo> <{}#Corridor/{}>.\n".format(prefixes_nt["hospOnt"],corr.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbours))
                file.write("<< <{}#Corridor/{}> <{}#nextTo> <{}#Corridor/{}> >> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],corr.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],neighbours, prefixes_nt["hospOnt"], weights["nextTo_Corridor"],prefixes_nt["xmlSchema"]))

                keyPair2 = "{}-{}".format(corr.id,neighbours)
                writtenPairs.append(keyPair2)
        
    file.close()  



''''''''''''''''''
'''  PATIENTS  '''
''''''''''''''''''

def printPatientsNT_star(dicPatients):
    file = open("{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['patient'], '.nt'), 'w')
    writePatientsNT(file, dicPatients)
    file.close()



''''''''''''''''''''''''
'''  MICROORGANISM   '''
''''''''''''''''''''''''

def printMicroorganismsNT_star(dicMicroorganisms):
    file = open("{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['microorganism'], '.nt'), 'w')
    toWrite = getToWriteMicroorganismsNT(dicMicroorganisms)
    file.write(toWrite)
    file.close()



''''''''''''''''''''''''''''''
'''  EPISODES AND EVENTS   '''
''''''''''''''''''''''''''''''

##########
# CLASSES #
##########

# MAIN
def printClassesEpisodesEventsNT_star(dicPatients):
    printEpisodesNT_star(dicPatients)

    printEventsNT_star(dicPatients, EventType.Hospitalization, "{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['hospitalization'], '.nt'))
    printEventsNT_star(dicPatients, EventType.Death, "{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['death'], '.nt'))
    printEventsNT_star(dicPatients, EventType.TestMicro, "{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['testMicro'], '.nt'))



# Episodes
def printEpisodesNT_star(dicPatients):
    file = open("{}{}{}".format(folderOutput_Classes_NT_star, nameFiles_Classes['episode'], '.nt'), 'w')
    writeEpisodesNT(dicPatients, file)
    file.close()

# Events
def printEventsNT_star(dicPatients, tipo, nameFile):
    file = open(nameFile, 'w')
    writeEventsNT(dicPatients, tipo, file)
    file.close()



##############
# RELATIONS #
##############

# MAIN
def printRelationsEpisodesEventsNT_star(dicPatients):
    printRel_EpisodePatientNT_star(dicPatients)
    printRel_EventEpisodeNT_star(dicPatients)
    printRel_EventBedNT_star(dicPatients)
    printRel_EventHospUnitNT_star(dicPatients)
    printRel_TestMicroorgNT_star(dicPatients)


# Relacion Episode-Patient    ->  Same as with NT    
def printRel_EpisodePatientNT_star(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['ep_pat'], '.nt'), 'w')
    writeRel_EpisodePatientNT(dicPatients, file)
    file.close()

# Relacion Event-Episode  ->  Same as with NT
def printRel_EventEpisodeNT_star(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['ev_ep'], '.nt'), 'w')
    writeRel_EventEpisodeNT(dicPatients, file)
    file.close()    
    
# Relacion Event-Bed   ->  Same as with NT  
def printRel_EventBedNT_star(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['ev_bed'], '.nt'), 'w')
    writeRel_EventBedNT(dicPatients, file)
    file.close() 
    
# Relacion Event-HospUnit    ->  Same as with NT
def printRel_EventHospUnitNT_star(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['ev_uh'], '.nt'), 'w')
    writeRel_EventoUnidadHospNT(dicPatients, file)
    file.close() 
    
# Relacion TestMicro-Microorganism
def printRel_TestMicroorgNT_star(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT_star, nameFiles_Rels['test_micro'], '.ttl'), 'w')
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.type is EventType.TestMicro:
                    microorg = ev.extra1
                    if ev.extra2:
                        mdr = 1
                    else:
                        mdr = 0
                    
                    file.write("<{}#TestMicro/{}> <{}#hasFound> <{}#Microorganism/{}>.\n".format(prefixes_nt["hospOnt"],ev.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],microorg.id))
                    file.write("<< <{}#TestMicro/{}> <{}#hasFound> <{}#Microorganism/{}> >> <{}#mdr> \"{}\"^^<{}/boolean>.\n".format(prefixes_nt["hospOnt"],ev.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],microorg.id, prefixes_nt["hospOnt"], mdr,prefixes_nt["xmlSchema"]))
    file.close() 


