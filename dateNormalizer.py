import os
import math
from datetime import datetime, timedelta

from variablesFiles import *
from auxFunctionsNormDate import *


#                           A                        B
# Normalize years:      2100 - 2210      a       2001 - 2012

# V' = ((V-minA)/(maxA-minA)) * (maxB-minB) + minB
# V' = ((V-2100)/(2210-2100)) * (2012-2001) + 2001 = ((V-2100)/110) * 11 + 2001
def normalizeYear(v):
    vv =  ((v-2100)/110) * 11 + 2001
    vv = math.trunc(vv)

    return vv

def normalizeYear_params(v, minB, maxB):
    vv = ((v-2100)/110) * (maxB - minB) + minB
    vv = math.trunc(vv)

    return vv


#########################
# Leap years management #
#########################

def isLeapyear(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def changeFebruaryLeapYear(date, year, yearNorm):

    change = False
    if isLeapyear(year) and not isLeapyear(yearNorm):
        if date.day==29 and date.month==2:
            date = date.replace(day=1)
            date = date.replace(month=3)
            change = True
        
    return date, change

def normYearDate(date_str, minYearNorm, maxYearNorm):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    dateYear = date.year
    dateYearNorm = normalizeYear_params(dateYear, minYearNorm, maxYearNorm)
    date, changeLeap = changeFebruaryLeapYear(date, dateYear, dateYearNorm)
    dateNorm = date.replace(year=dateYearNorm)
    dateNorm = dateNorm.replace(second=00)

    return dateNorm, changeLeap



##############################################
# Read and Write Files with Normalized Years #
##############################################

def normalizeDates_Episodes(minYear, maxYear):
    
    nameFile = setFileInput(filesName["episode"])
    with open(nameFile) as file:

        nameFile2 = setFileOutput(filesName["episode"], minYear, maxYear)
        if not os.path.isfile(nameFile2):
            file2 = open(nameFile2, 'w')

            for lineString in file:
                lineString = str(lineString)
            
                if lineString[0].isnumeric():
                    
                    line = lineString.split(',')
                    
                    subjectid = line[0]
                    hadmid = line[1]
                    admissionType = line[4]
                    admissionType = admissionType[:-1]
                    
                    startNorm, addDay = normYearDate(line[2], minYear, maxYear)

                    endNorm, addDay = normYearDate(line[3], minYear, maxYear)
                    if addDay:
                        endNorm += timedelta(days=1)

                    file2.write("{},{},{},{},{}\n".format(subjectid,hadmid,startNorm.strftime("%Y-%m-%d %H:%M:%S"),endNorm.strftime("%Y-%m-%d %H:%M:%S"),admissionType))

                else:
                    file2.write(lineString)

            file2.close()
    
    file.close()


def normaliznormalizeDates_Transfers_Loc(minYear, maxYear):

    nameFile = setFileInput(filesName["ev_hosp_loc"])
    with open(nameFile) as file:

        nameFile2 = setFileOutput(filesName["ev_hosp_loc"], minYear, maxYear)
        if not os.path.isfile(nameFile2):
            file2 = open(nameFile2, 'w')

            hadmidBefore = None
            addDay = False

            for lineString in file:
                lineString = str(lineString)
            
                if lineString[0].isnumeric():
                    
                    line = lineString.split(',')
                    
                    rowid = line[0]
                    subjectid = line[1]
                    hadmid = line[2]
                    icustayid = line[3]
                    careunit = line[4]
                    wardid = line[5]

                    if hadmidBefore is not None:
                        if hadmid != hadmidBefore:
                            addDay = False
                    else:
                        addDay = False
                        
                    startNorm, addDayAux = normYearDate(line[6], minYear, maxYear)

                    if addDay:
                        startNorm += timedelta(days=1)
                    else:
                        addDay = addDayAux 
                    
                    end_str = line[7]
                    end_str = end_str[:-1]
                    endNorm, addDayAux = normYearDate(end_str, minYear, maxYear)

                    if addDay:
                        endNorm += timedelta(days=1)
                    else:
                        addDay = addDayAux 

                    file2.write("{},{},{},{},{},{},{},{}\n".format(rowid,subjectid,hadmid,icustayid,careunit,wardid,startNorm.strftime("%Y-%m-%d %H:%M:%S"),endNorm.strftime("%Y-%m-%d %H:%M:%S")))

                    hadmidBefore = hadmid

                else:
                    file2.write(lineString)

            file2.close()
    
    file.close()


def normaliznormalizeDates_Services(minYear, maxYear):        

    nameFile = setFileInput(filesName["ev_hosp_serv"])
    with open(nameFile) as file:

        nameFile2 = setFileOutput(filesName["ev_hosp_serv"], minYear, maxYear)
        if not os.path.isfile(nameFile2):
            file2 = open(nameFile2, 'w')

            hadmidAnt = None
            addDay = False

            for lineString in file:
                lineString = str(lineString)
            
                if lineString[0].isnumeric():
                    
                    line = lineString.split(',')
                    
                    rowid = line[0]
                    subjectid = line[1]
                    hadmid = line[2]
                    currservice = line[4]
                    currservice = currservice[:-1]

                    if hadmidAnt is not None:
                        if hadmid != hadmidAnt:
                            addDay = False
                    else:
                        addDay = False

                    startNorm, addDayAux = normYearDate(line[3], minYear, maxYear)
                    
                    if addDay:
                        startNorm += timedelta(days=1)
                    else:
                        addDay = addDayAux  

                    file2.write("{},{},{},{},{}\n".format(rowid,subjectid,hadmid,startNorm.strftime("%Y-%m-%d %H:%M:%S"),currservice))

                else:
                    file2.write(lineString)

            file2.close()
    
    file.close()


def normaliznormalizeDates_Deaths(minYear, maxYear):
    
    nameFile = setFileInput(filesName["ev_death"])
    with open(nameFile) as file:

        nameFile2 = setFileOutput(filesName["ev_death"], minYear, maxYear)
        if not os.path.isfile(nameFile2):
            file2 = open(nameFile2, 'w')

            for lineString in file:
                lineString = str(lineString)
            
                if lineString[0].isnumeric():
                    
                    line = lineString.split(',')
                    
                    rowid = line[0]
                    subjectid = line[1]
                    hadmid = line[2]
                    
                    death_str = line[3]
                    death_str = death_str[:-1]
                    deathNorm, addDayAux = normYearDate(death_str, minYear, maxYear)

                    file2.write("{},{},{},{}\n".format(rowid,subjectid,hadmid,deathNorm.strftime("%Y-%m-%d %H:%M:%S")))

                else:
                    file2.write(lineString)

            file2.close()
    
    file.close()


def normaliznormalizeDates_TestMicro(minYear, maxYear):
    
    nameFile = setFileInput(filesName["ev_tm"])
    with open(nameFile) as file:

        nameFile2 = setFileOutput(filesName["ev_tm"], minYear, maxYear)
        if not os.path.isfile(nameFile2):
            file2 = open(nameFile2, 'w')

            for lineString in file:
                lineString = str(lineString)
            
                if lineString[0].isnumeric():
                    
                    line = lineString.split(',')
                    
                    rowid = line[0]
                    hadmid = line[1]
                    orgid = line[2]
                    interpretation = line[4]
                    interpretation = interpretation[:-1]

                    dateNorm, addDayAux = normYearDate(line[3], minYear, maxYear)

                    file2.write("{},{},{},{},{}\n".format(rowid,hadmid,orgid,dateNorm.strftime("%Y-%m-%d %H:%M:%S"),interpretation))

                else:
                    file2.write(lineString)

            file2.close()
    
    file.close()



#####################
# FUNCION PRINCIPAL #
#####################

def normalizeDates(minYear, maxYear):
    normalizeDates_Episodes(minYear, maxYear)
    normaliznormalizeDates_Transfers_Loc(minYear, maxYear)   
    normaliznormalizeDates_Services(minYear, maxYear)
    normaliznormalizeDates_Deaths(minYear, maxYear)
    normaliznormalizeDates_TestMicro(minYear, maxYear)





if __name__ == "__main__":
    normalizeDates(None, None)
