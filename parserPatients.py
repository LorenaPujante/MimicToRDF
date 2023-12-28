from datetime import datetime
from classes import Patient
from variablesFiles import *


def parsePatients():
    
    dicPatients = {}

    nameFile = setFileInput(filesName["patient"])
    with open(nameFile) as file:
        for lineString in file:
            
            lineString = str(lineString)
            if lineString[0].isnumeric():
                line = lineString.split(',')
            
                id = int(line[0])
                birth_str = line[2]
                birth = datetime.strptime(birth_str, '%Y-%m-%d %H:%M:%S')

                sexLetter = line[1]
                if (sexLetter == 'M'):
                    sex = False
                else:
                    sex = True                
                death = line[len(line)-1].rstrip()
                if death=='1':
                    death = True
                elif death=='0':
                    death = False
            
                patient = Patient(id,birth,sex,death)
                dicPatients[id] = patient

    file.close()

    return dicPatients