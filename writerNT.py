import os
from classes import *
from weightsLocsHierarchy import weights
from variablesFiles import getTwoLastDigitsNumber
from variablesWriter import prefixes_nt, nameFiles_Classes, nameFiles_Rels



##################
# INICIALIZACION #
##################

def setFolderOutputNT(folder, minYearN, maxYearN, minYear, maxYear, maxEvents):
    global folderOutput_NT
    folderOutput_NT = folder
    if (not os.path.exists(folderOutput_NT)):
        os.makedirs(folderOutput_NT)
    
    minYearN_2digits = getTwoLastDigitsNumber(minYearN)
    maxYearN_2digits = getTwoLastDigitsNumber(maxYearN)
    minYear_2digits = getTwoLastDigitsNumber(minYear)
    maxYear_2digits = getTwoLastDigitsNumber(maxYear)
    if maxEvents == 0:
        maxEvents_div1000 = "all"
    else:
        maxEvents_div1000 = int(maxEvents/1000)

    global folderOutput_Classes_NT
    folderOutput_Classes_NT = folderOutput_NT + "\\Classes_{}-{}__{}-{}__{}".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    if (not os.path.exists(folderOutput_Classes_NT)):
        os.makedirs(folderOutput_Classes_NT)

    global folderOutput_Relations_NT
    folderOutput_Relations_NT = folderOutput_NT + "\\Relations_{}-{}__{}-{}__{}".format(minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000)
    if (not os.path.exists(folderOutput_Relations_NT)):
        os.makedirs(folderOutput_Relations_NT)

    return folderOutput_Classes_NT, folderOutput_Relations_NT, minYearN_2digits, maxYearN_2digits, minYear_2digits, maxYear_2digits, maxEvents_div1000



''''''''''''''
'''  MAIN  '''
''''''''''''''

def printNT(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms):
    printClassesNT(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms)
    printRelsNT(dicServices, dicCorridors, dicRooms, dicBeds, dicPatients)


def printClassesNT(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds, dicPatients, dicMicroorganisms):
    # Hospital
    printClassesHospitalNT(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds)

    # Patients
    printPatientsNT(dicPatients)

    # Microorganisms
    printMicroorganismsNT(dicMicroorganisms)

    # Episodes y Events
    printClassesEpisodesEventsNT(dicPatients)


def printRelsNT(dicServicios, dicPasillos, dicRooms, dicBeds, dicPatients):
    # Hospital
    printRelationsHospitalNT(dicServicios, dicPasillos, dicRooms, dicBeds)

    # Patients, Episodes y Events
    printRelationsEpisodesEventsNT(dicPatients)



''''''''''''''''''
'''  HOSPITAL  '''
''''''''''''''''''

##########
# CLASES #
##########

# MAIN
def printClassesHospitalNT(dicServices, dicHospUnits, dicCorridors, dicRooms, dicBeds):
    
    printServicesNT(dicServices)
    printHospUnitsNT(dicHospUnits)
    
    printCorridorsNT(dicCorridors)
    printRoomsNT(dicRooms)
    printBedsNT(dicBeds)



# Services
def printServicesNT(dicServices):
    file = open("{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['service'], '.nt'), 'w')
    toWrite = getToWriteServicesNT(dicServices)
    file.write(toWrite)
    file.close()

def getToWriteServicesNT(dicServices):
    toWrite = ""
    for s in dicServices.values():
        toWrite += "<{}#Service/{}> <{}#type> <{}#Service>.\n".format(prefixes_nt['hospOnt'],s.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"])
        toWrite += "<{}#Service/{}> <{}#id> \"{}\"^^<{}#integer>.\n".format(prefixes_nt["hospOnt"],s.id, prefixes_nt["hospOnt"], s.id,prefixes_nt['xmlSchema'])
        toWrite += "<{}#Service/{}> <{}#description> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],s.id, prefixes_nt["hospOnt"], s.description,prefixes_nt['xmlSchema'])
        toWrite += "<{}#Service/{}> <{}#abbreviation> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],s.id, prefixes_nt["hospOnt"], s.abrev,prefixes_nt['xmlSchema'])

    return toWrite
    

# Hospitalization Units
def printHospUnitsNT(dicHospUnits):
    file = open("{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['uh'], '.nt'), 'w')
    toWrite = getToWriteHospUnitsNT(dicHospUnits)
    file.write(toWrite)
    file.close()

def getToWriteHospUnitsNT(dicHospUnits):
    toWrite = ""
    for hu in dicHospUnits.values():
        toWrite += "<{}#HospitalizationUnit/{}> <{}#type> <{}#HospitalizationUnit>.\n".format(prefixes_nt['hospOnt'],hu.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"])
        toWrite += "<{}#HospitalizationUnit/{}> <{}#id> \"{}\"^^<{}#integer>.\n".format(prefixes_nt["hospOnt"],hu.id, prefixes_nt["hospOnt"], hu.id,prefixes_nt['xmlSchema'])
        toWrite += "<{}#HospitalizationUnit/{}> <{}#description> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],hu.id, prefixes_nt["hospOnt"], hu.description,prefixes_nt['xmlSchema'])
        toWrite += "<{}#HospitalizationUnit/{}> <{}#abbreviation> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],hu.id, prefixes_nt["hospOnt"], hu.abrev,prefixes_nt['xmlSchema'])   

    return toWrite


# Corridors
def printCorridorsNT(dicCorridors):
    file = open("{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['corridor'], '.nt'), 'w')
    toWrite = getToWriteCorridorsNT(dicCorridors)
    file.write(toWrite)
    file.close()

def getToWriteCorridorsNT(dicCorridors):
    toWrite = ""
    for c in dicCorridors.values():
        toWrite += "<{}#Corridor/{}> <{}#type> <{}#Location>.\n".format(prefixes_nt['hospOnt'],c.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"])
        toWrite += "<{}#Corridor/{}> <{}#type> <{}#Corridor>.\n".format(prefixes_nt['hospOnt'],c.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"])
        toWrite += "<{}#Corridor/{}> <{}#id> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],c.id, prefixes_nt["hospOnt"], c.id,prefixes_nt['xmlSchema'])
        toWrite += "<{}#Corridor/{}> <{}#description> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],c.id, prefixes_nt["hospOnt"], c.description,prefixes_nt['xmlSchema'])

    return toWrite


# Rooms
def printRoomsNT(dicRooms):
    file = open("{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['room'], '.nt'), 'w')
    toWrite = getToWriteRoomsNT(dicRooms)
    file.write(toWrite)
    file.close()

def getToWriteRoomsNT(dicRooms):
    toWrite = ""
    for ward in dicRooms.values():
        for r in ward.values():
            toWrite += "<{}#Room/{}> <{}#type> <{}#Location>.\n".format(prefixes_nt['hospOnt'],r.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"])
            toWrite += "<{}#Room/{}> <{}#type> <{}#Room>.\n".format(prefixes_nt['hospOnt'],r.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"])
            toWrite += "<{}#Room/{}> <{}#id> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],r.id, prefixes_nt["hospOnt"], r.id,prefixes_nt['xmlSchema'])
            toWrite += "<{}#Room/{}> <{}#description> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],r.id, prefixes_nt["hospOnt"], r.description,prefixes_nt['xmlSchema'])

    return toWrite


# Beds
def printBedsNT(dicBeds):
    file = open("{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['bed'], '.nt'), 'w')
    writeBedsNT(dicBeds, file)
    file.close()

def writeBedsNT(dicBeds, file):
    for b in dicBeds.values():
        file.write("<{}#Bed/{}> <{}#type> <{}#Location>.\n".format(prefixes_nt['hospOnt'],b.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"]))
        file.write("<{}#Bed/{}> <{}#type> <{}#Seat>.\n".format(prefixes_nt['hospOnt'],b.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"]))
        file.write("<{}#Bed/{}> <{}#type> <{}#Bed>.\n".format(prefixes_nt['hospOnt'],b.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"]))
        file.write("<{}#Bed/{}> <{}#id> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],b.id, prefixes_nt["hospOnt"], b.id,prefixes_nt['xmlSchema']))
        file.write("<{}#Bed/{}> <{}#description> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],b.id, prefixes_nt["hospOnt"], b.description,prefixes_nt['xmlSchema']))

    

##############
# RELATIONS #
##############

# MAIN
def printRelationsHospitalNT(dicServices, dicCorridors, dicRooms, dicBeds):
    
    printRel_ServiceHospUnitNT(dicServices)
    
    printRel_CorridorRoomNT(dicCorridors)
    printRel_RoomBedNT(dicRooms)

    printRel_Bed_NextToOppositeNT(dicBeds, "{}{}".format(nameFiles_Rels['bed_nt'], '.nt'), "nextTo")
    printRel_Bed_NextToOppositeNT(dicBeds, "{}{}".format(nameFiles_Rels['bed_ot'], '.nt'), "opposite")
    printRel_Room_NextToOppositeNT(dicRooms, "{}{}".format(nameFiles_Rels['room_nt'], '.nt'), "nextTo")
    printRel_Room_NextToOppositeNT(dicRooms, "{}{}".format(nameFiles_Rels['room_ot'], '.nt'), "opposite")
    printRel_Corridor_NextToNT(dicCorridors)
    

# Relation Service - HospUnit
def printRel_ServiceHospUnitNT(dicServices):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['serv_uh'], '.nt'), 'w')
    toWrite = ""
    for s in dicServices.values():
        for uh in s.hospUnits:
            toWrite += "<{}#HospUnitFromService/{}_{}> <{}#type> <{}#HospUnitFromService>.\n".format(prefixes_nt["hospOnt"],uh,s.id, prefixes_nt["rdf"], prefixes_nt["hospOnt"])
            toWrite += "<{}#HospUnitFromService/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],uh,s.id, prefixes_nt["hospOnt"], weights['hospUnitFromService'],prefixes_nt['xmlSchema'])
            toWrite += "<{}#HospUnitFromService/{}_{}> <{}#hospUnitFromService1> <{}#HospitalizationUnit/{}>.\n".format(prefixes_nt["hospOnt"],uh,s.id, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],uh)
            toWrite += "<{}#HospUnitFromService/{}_{}> <{}#hospUnitFromService2> <{}#Service/{}>.\n".format(prefixes_nt["hospOnt"],uh,s.id, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],s.id)
    file.write(toWrite)
    file.close()


# Relation Corridor - Room
def printRel_CorridorRoomNT(diccorridors):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['room_corridor'], '.nt'), 'w')
    toWrite = ""
    for c in diccorridors.values():
        for r in c.rooms:
            toWrite += "<{}#PlacedIn/{}_{}> <{}#type> <{}#PlacedIn>.\n".format(prefixes_nt["hospOnt"],r.id,c.id, prefixes_nt["rdf"], prefixes_nt["hospOnt"])
            toWrite += "<{}#PlacedIn/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],r.id,c.id, prefixes_nt["hospOnt"], weights['placedIn_RoomCorridor'],prefixes_nt['xmlSchema'])
            toWrite += "<{}#PlacedIn/{}_{}> <{}#placedIn1> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],r.id,c.id, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],r.id)
            toWrite += "<{}#PlacedIn/{}_{}> <{}#placedIn2> <{}#Corridor/{}>.\n".format(prefixes_nt["hospOnt"],r.id,c.id, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],c.id)
    file.write(toWrite)
    file.close()

# Relation Room - Bed
def printRel_RoomBedNT(dicRooms):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['bed_room'], '.nt'), 'w')
    for ward in dicRooms.values():
        for r in ward.values():
            for b in r.beds:
                file.write("<{}#PlacedIn/{}_{}> <{}#type> <{}#PlacedIn>.\n".format(prefixes_nt["hospOnt"],b,r.id, prefixes_nt["rdf"], prefixes_nt["hospOnt"]))
                file.write("<{}#PlacedIn/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],b,r.id, prefixes_nt["hospOnt"], weights['placedIn_SeatRoom'],prefixes_nt['xmlSchema']))
                file.write("<{}#PlacedIn/{}_{}> <{}#placedIn1> <{}#Bed/{}>.\n".format(prefixes_nt["hospOnt"],b,r.id, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],b))
                file.write("<{}#PlacedIn/{}_{}> <{}#placedIn2> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],b,r.id, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],r.id))
    file.close()


# Relation Room - Room    (nextTo  //  opposite)
def printRel_Room_NextToOppositeNT(dicRooms, nameFile, nextOrOpposite):
    file = open(folderOutput_Relations_NT + nameFile, 'w')
    
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
                    if nextOrOpposite == "nextTo":
                        file.write("<{}#NextTo/{}_{}> <{}#type> <{}#NextTo>.\n".format(prefixes_nt["hospOnt"],room.id,neighbour, prefixes_nt["rdf"], prefixes_nt["hospOnt"]))
                        file.write("<{}#NextTo/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],room.id,neighbour, prefixes_nt["hospOnt"], weights['nextTo_Room'],prefixes_nt['xmlSchema']))
                        file.write("<{}#NextTo/{}_{}> <{}#nextTo1> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],room.id,neighbour, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],room.id))
                        file.write("<{}#NextTo/{}_{}> <{}#nextTo2> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],room.id,neighbour, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],neighbour))

                    elif nextOrOpposite == "opposite":
                        file.write("<{}#Opposite/{}_{}> <{}#type> <{}#Opposite>.\n".format(prefixes_nt["hospOnt"],room.id,neighbour, prefixes_nt["rdf"], prefixes_nt["hospOnt"]))
                        file.write("<{}#Opposite/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],room.id,neighbour, prefixes_nt["hospOnt"], weights['opposite_Room'],prefixes_nt['xmlSchema']))
                        file.write("<{}#Opposite/{}_{}> <{}#opposite1> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],room.id,neighbour, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],room.id))
                        file.write("<{}#Opposite/{}_{}> <{}#opposite2> <{}#Room/{}>.\n".format(prefixes_nt["hospOnt"],room.id,neighbour, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],neighbour))

                    # The pairs (Neighbor, Room) are also written in writtenPairs so as not to repeat it later   
                    keyPair2 = "{}-{}".format(room.id,neighbour)
                    writtenPairs[keyPair2] = 1
                
    file.close() 

# Relation Bed - Bed    (nextTo  //  opposite)
def printRel_Bed_NextToOppositeNT(dicBeds, nameFile, nextOrOpposite):
    file = open(folderOutput_Relations_NT + nameFile, 'w')
    
    writtenPairs = {}
    for bed in dicBeds.values():
        # NextTo neighbors or Opposite neighbours are selected
        listNeighbours = None
        if nextOrOpposite == "nextTo":
            listNeighbours = bed.nextTo
        elif nextOrOpposite == "opposite":
            listNeighbours = bed.opposite
        
        # Pairs (Bed, Neighbour) are added to write
        for neighbours in listNeighbours:
            keyPair1 = "{}-{}".format(neighbours,bed.id)
            if keyPair1 not in writtenPairs:
                if nextOrOpposite == "nextTo":
                    file.write("<{}#NextTo/{}_{}> <{}#type> <{}#NextTo>.\n".format(prefixes_nt["hospOnt"],bed.id,neighbours, prefixes_nt["rdf"], prefixes_nt["hospOnt"]))
                    file.write("<{}#NextTo/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],bed.id,neighbours, prefixes_nt["hospOnt"], weights['nextTo_Seat'],prefixes_nt['xmlSchema']))
                    file.write("<{}#NextTo/{}_{}> <{}#nextTo1> <{}#Bed/{}>.\n".format(prefixes_nt["hospOnt"],bed.id,neighbours, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],bed.id))
                    file.write("<{}#NextTo/{}_{}> <{}#nextTo2> <{}#Bed/{}>.\n".format(prefixes_nt["hospOnt"],bed.id,neighbours, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],neighbours))

                elif nextOrOpposite == "opposite":
                    file.write("<{}#Opposite/{}_{}> <{}#type> <{}#Opposite>.\n".format(prefixes_nt["hospOnt"],bed.id,neighbours, prefixes_nt["rdf"], prefixes_nt["hospOnt"]))
                    file.write("<{}#Opposite/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],bed.id,neighbours, prefixes_nt["hospOnt"], weights['opposite_Seat'],prefixes_nt['xmlSchema']))
                    file.write("<{}#Opposite/{}_{}> <{}#opposite1> <{}#Bed/{}>.\n".format(prefixes_nt["hospOnt"],bed.id,neighbours, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],bed.id))
                    file.write("<{}#Opposite/{}_{}> <{}#opposite2> <{}#Bed/{}>.\n".format(prefixes_nt["hospOnt"],bed.id,neighbours, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],neighbours))
                        
                # The pairs (Neighbor, Bed) are also written in writtenPairs so as not to repeat it later    
                keyPair2 = "{}-{}".format(bed.id,neighbours)
                writtenPairs[keyPair2] = 1

    file.close() 

# Relation Corridor - Corridor  (nextTo)
def printRel_Corridor_NextToNT(dicCorridors):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['corridor_nt'], '.nt'), 'w')
    
    writtenPairs = []
    for corr in dicCorridors.values():
        # Neighbour 0
        if corr.nextTo[0] is not None:
            neighbour = corr.nextTo[0]
            keyPair1 = "{}-{}".format(neighbour,corr.id)
            if keyPair1 not in writtenPairs:
                file.write("<{}#NextTo/{}_{}> <{}#type> <{}#NextTo>.\n".format(prefixes_nt["hospOnt"],corr.id,neighbour, prefixes_nt["rdf"], prefixes_nt["hospOnt"]))
                file.write("<{}#NextTo/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],corr.id,neighbour, prefixes_nt["hospOnt"], weights['nextTo_Corridor'],prefixes_nt['xmlSchema']))
                file.write("<{}#NextTo/{}_{}> <{}#nextTo1> <{}#Corridor/{}>.\n".format(prefixes_nt["hospOnt"],corr.id,neighbour, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],corr.id))
                file.write("<{}#NextTo/{}_{}> <{}#nextTo2> <{}#Corridor/{}>.\n".format(prefixes_nt["hospOnt"],corr.id,neighbour, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],neighbour))

                keyPair2 = "{}-{}".format(corr.id,neighbour)
                writtenPairs.append(keyPair2)
        
        # Neighbour 1
        if corr.nextTo[1] is not None:
            neighbour = corr.nextTo[1]
            keyPair1 = "{}-{}".format(neighbour,corr.id)
            if keyPair1 not in writtenPairs:
                file.write("<{}#NextTo/{}_{}> <{}#type> <{}#NextTo>.\n".format(prefixes_nt["hospOnt"],corr.id,neighbour, prefixes_nt["rdf"], prefixes_nt["hospOnt"]))
                file.write("<{}#NextTo/{}_{}> <{}#cost> \"{}\"^^<{}#float>.\n".format(prefixes_nt["hospOnt"],corr.id,neighbour, prefixes_nt["hospOnt"], weights['nextTo_Corridor'],prefixes_nt['xmlSchema']))
                file.write("<{}#NextTo/{}_{}> <{}#nextTo1> <{}#Corridor/{}>.\n".format(prefixes_nt["hospOnt"],corr.id,neighbour, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],corr.id))
                file.write("<{}#NextTo/{}_{}> <{}#nextTo2> <{}#Corridor/{}>.\n".format(prefixes_nt["hospOnt"],corr.id,neighbour, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],neighbour))

                keyPair2 = "{}-{}".format(corr.id,neighbour)
                writtenPairs.append(keyPair2)
        
    file.close()  



''''''''''''''''''
'''  PATIENTS  '''
''''''''''''''''''

def printPatientsNT(dicPatients):
    file = open("{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['patient'], '.nt'), 'w')
    writePatientsNT(file, dicPatients)
    file.close()

def writePatientsNT(file, dicPatients):
    for p in dicPatients.values():
        file.write("<{}#Patient/{}> <{}#type> <{}#Patient>.\n".format(prefixes_nt['hospOnt'],p.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"]))
        file.write("<{}#Patient/{}> <{}#id> \"{}\"^^<{}#integer>.\n".format(prefixes_nt["hospOnt"],p.id, prefixes_nt["hospOnt"], p.id,prefixes_nt['xmlSchema']))
        file.write("<{}#Patient/{}> <{}#dateBirth> \"{}\"^^<{}#dateTime>.\n".format(prefixes_nt["hospOnt"],p.id, prefixes_nt["hospOnt"], p.birth.strftime("%Y-%m-%dT%H:%M:%S"),prefixes_nt['xmlSchema']))
        if p.sex:
            sex = 'M'
        else:
            sex = 'F'
        file.write("<{}#Patient/{}> <{}#sex> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],p.id, prefixes_nt["hospOnt"], sex,prefixes_nt['xmlSchema']))
    


''''''''''''''''''''''''
'''  MICROORGANISM   '''
''''''''''''''''''''''''

def printMicroorganismsNT(dicMicroorganisms):
    file = open("{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['microorganism'], '.nt'), 'w')
    toWrite = getToWriteMicroorganismsNT(dicMicroorganisms)
    file.write(toWrite)
    file.close()

def getToWriteMicroorganismsNT(dicMicroorganisms):
    toWrite = ""
    for m in dicMicroorganisms.values():
        toWrite += "<{}#Microorganism/{}> <{}#type> <{}#Microorganism>.\n".format(prefixes_nt['hospOnt'],m.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"])
        toWrite += "<{}#Microorganism/{}> <{}#id> \"{}\"^^<{}#integer>.\n".format(prefixes_nt["hospOnt"],m.id, prefixes_nt["hospOnt"], m.id,prefixes_nt['xmlSchema'])
        toWrite += "<{}#Microorganism/{}> <{}#description> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],m.id, prefixes_nt["hospOnt"], m.description,prefixes_nt['xmlSchema'])
    
    return toWrite



''''''''''''''''''''''''''''''
'''  EPISODES AND EVENTS   '''
''''''''''''''''''''''''''''''

###########
# CLASSES #
###########

# MAIN
def printClassesEpisodesEventsNT(dicPatients):
    printEpisodesNT(dicPatients)

    printEventsNT(dicPatients, EventType.Hospitalization, "{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['hospitalization'], '.nt'))
    printEventsNT(dicPatients, EventType.Death, "{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['death'], '.nt'))
    printEventsNT(dicPatients, EventType.TestMicro, "{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['testMicro'], '.nt'))


# Episodes
def printEpisodesNT(dicPatients):    
    file = open("{}{}{}".format(folderOutput_Classes_NT, nameFiles_Classes['episode'], '.nt'), 'w')
    writeEpisodesNT(dicPatients, file)
    file.close()

def writeEpisodesNT(dicPatients, file):
    for patient in dicPatients.values():
        for ep in patient.episodes:
            file.write("<{}#Episode/{}> <{}#type> <{}#Episode>.\n".format(prefixes_nt['hospOnt'],ep.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"]))
            file.write("<{}#Episode/{}> <{}#id> \"{}\"^^<{}#integer>.\n".format(prefixes_nt["hospOnt"],ep.id, prefixes_nt["hospOnt"], ep.id,prefixes_nt['xmlSchema']))
            file.write("<{}#Episode/{}> <{}#description> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],ep.id, prefixes_nt["hospOnt"], ep.description,prefixes_nt['xmlSchema']))
            file.write("<{}#Episode/{}> <{}#start> \"{}\"^^<{}#dateTime>.\n".format(prefixes_nt["hospOnt"],ep.id, prefixes_nt["hospOnt"], ep.start.strftime("%Y-%m-%dT%H:%M:%S"),prefixes_nt['xmlSchema']))   # Formato: %Y-%m-%d %H:%M:%S  ->  2022-01-01 00:00:00
            file.write("<{}#Episode/{}> <{}#end> \"{}\"^^<{}#dateTime>.\n".format(prefixes_nt["hospOnt"],ep.id, prefixes_nt["hospOnt"], ep.end.strftime("%Y-%m-%dT%H:%M:%S"),prefixes_nt['xmlSchema']))


# Events
def printEventsNT(dicPatients, type, nameFile):    
    file = open(nameFile, 'w')
    writeEventsNT(dicPatients, type, file)
    file.close()

def writeEventsNT(dicPatients, type, file):
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.type is type:
                    file.write("<{}#{}/{}> <{}#type> <{}#Event>.\n".format(prefixes_nt['hospOnt'],ev.type.name,ev.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"]))
                    file.write("<{}#{}/{}> <{}#type> <{}#{}>.\n".format(prefixes_nt['hospOnt'],ev.type.name,ev.id, prefixes_nt['rdf'], prefixes_nt["hospOnt"],ev.type.name))
                    file.write("<{}#{}/{}> <{}#id> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],ev.type.name,ev.id, prefixes_nt["hospOnt"], ev.id,prefixes_nt['xmlSchema']))
                    file.write("<{}#{}/{}> <{}#description> \"{}\"^^<{}#string>.\n".format(prefixes_nt["hospOnt"],ev.type.name,ev.id, prefixes_nt["hospOnt"], ev.description,prefixes_nt['xmlSchema']))
                    file.write("<{}#{}/{}> <{}#start> \"{}\"^^<{}#dateTime>.\n".format(prefixes_nt["hospOnt"],ev.type.name,ev.id, prefixes_nt["hospOnt"], ev.start.strftime("%Y-%m-%dT%H:%M:%S"),prefixes_nt['xmlSchema']))   # Formato: %Y-%m-%d %H:%M:%S  ->  2022-01-01 00:00:00
                    file.write("<{}#{}/{}> <{}#end> \"{}\"^^<{}#dateTime>.\n".format(prefixes_nt["hospOnt"],ev.type.name,ev.id, prefixes_nt["hospOnt"], ev.end.strftime("%Y-%m-%dT%H:%M:%S"),prefixes_nt['xmlSchema']))


#############
# RELATIONS #
#############

# MAIN
def printRelationsEpisodesEventsNT(dicPatients):
    printRel_EpisodePatientNT(dicPatients)
    printRel_EventEpisodeNT(dicPatients)
    printRel_EventBedNT(dicPatients)
    printRel_EventHospUnitNT(dicPatients)
    printRel_TestMicroorgNT(dicPatients)


# Relation Episode-Patient
def printRel_EpisodePatientNT(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['ep_pat'], '.nt'), 'w')
    writeRel_EpisodePatientNT(dicPatients, file)
    file.close()

def writeRel_EpisodePatientNT(dicPatients, file):
    for patient in dicPatients.values():
        for ep in patient.episodes:
            file.write("<{}#Episode/{}> <{}#episodeFromPatient> <{}#Patient/{}>.\n".format(prefixes_nt["hospOnt"],ep.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],patient.id))


# Relation Event-Episode
def printRel_EventEpisodeNT(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['ev_ep'], '.nt'), 'w')
    writeRel_EventEpisodeNT(dicPatients, file)
    file.close() 

def writeRel_EventEpisodeNT(dicPatients, file):
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                file.write("<{}#{}/{}> <{}#eventFromEpisode> <{}#Episode/{}>.\n".format(prefixes_nt["hospOnt"],ev.type.name,ev.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],ep.id))


# Relation Event-Bed
def printRel_EventBedNT(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['ev_bed'], '.nt'), 'w')
    writeRel_EventBedNT(dicPatients, file)
    file.close()    

def writeRel_EventBedNT(dicPatients, file):
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.location is not None:
                    file.write("<{}#{}/{}> <{}#hasLocation> <{}#Bed/{}>.\n".format(prefixes_nt["hospOnt"],ev.type.name,ev.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],ev.location))
    

# Relation Event-HospUnit
def printRel_EventHospUnitNT(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['ev_uh'], '.nt'), 'w')
    writeRel_EventoUnidadHospNT(dicPatients, file)
    file.close()    

def writeRel_EventoUnidadHospNT(dicPatients, file):
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.hospUnit is not None:
                    file.write("<{}#{}/{}> <{}#hasHospUnit> <{}#HospitalizationUnit/{}>.\n".format(prefixes_nt["hospOnt"],ev.type.name,ev.id, prefixes_nt["hospOnt"], prefixes_nt["hospOnt"],ev.hospUnit))


# Relation TestMicro-Microorganism
def printRel_TestMicroorgNT(dicPatients):
    file = open("{}{}{}".format(folderOutput_Relations_NT, nameFiles_Rels['test_micro'], '.nt'), 'w')
    for patient in dicPatients.values():
        for ep in patient.episodes:
            for ev in ep.events:
                if ev.type is EventType.TestMicro:
                    microorg = ev.extra1
                    file.write("<{}#TestFoundMicroorg/{}_{}> <{}#type> <{}#TestFoundMicroorg>.\n".format(prefixes_nt["hospOnt"],ev.id,microorg.id, prefixes_nt["rdf"], prefixes_nt["hospOnt"]))
                    if ev.extra2:
                        mdr = 1
                    else:
                        mdr = 0
                    file.write("<{}#TestFoundMicroorg/{}_{}> <{}#mdr> \"{}\"^^<{}#boolean>.\n".format(prefixes_nt["hospOnt"],ev.id,microorg.id, prefixes_nt["hospOnt"], mdr,prefixes_nt['xmlSchema']))
                    file.write("<{}#TestFoundMicroorg/{}_{}> <{}#hasFound1> <{}#TestMicro/{}>.\n".format(prefixes_nt["hospOnt"],ev.id,microorg.id, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],ev.id))
                    file.write("<{}#TestFoundMicroorg/{}_{}> <{}#hasFound2> <{}#Microorganism/{}>.\n".format(prefixes_nt["hospOnt"],ev.id,microorg.id, prefixes_nt["hospOnt"], prefixes_nt['hospOnt'],microorg.id))
    file.close() 




