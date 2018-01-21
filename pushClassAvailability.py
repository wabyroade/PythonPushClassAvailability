#!/usr/bin/env python3

import requests
import pprint
from bs4 import BeautifulSoup

# Values to properly populate the POST reqeust to registration server.
# Use browser developer tools when using the search page in Firefox or Chrome to find proper values.
#TODO: Add functionality to use session when required.
regCatalogURL = 'https://REGISTRATIONSERVER.COLLEGE.EDU/REGSERVERPAGE'
payload = {'Termcode': '201708', 'Sess': '', 'Campcode': '', 'CollegeCode': '', 'Deptcode': '',
        'Status': '', 'Level': '', 'CRN': '', 'Subjcode': 'ISM', 'CourseNumber': '3011',
        'CourseTitle': '', 'CreditHours': '', 'courseattribute': '', 'BeginTime': '',
        'Instructor': '', 'sortby': 'course', 'Button1': 'Search'}
idToScrape = 'Table4'

# I used SimplePush to facilitate the push messaging. Could be swapped out for other methods.
simplePushAcct = '96pjW4'
pushRequestURL = 'https://api.simplepush.io/send/' + simplePushAcct

courseResult = requests.post(regCatalogURL, data=payload)
courseMatrix = []

soup = BeautifulSoup(courseResult.text, 'html.parser')

table4 = soup.find(id=idToScrape)
index = 0
tableHeadings = []

for tableRow in table4.find_all("tr"):
    print("ROW: ")
    thisCourse = {}
    cellIndex = 0
    for tableCell in tableRow.find_all("td"):
#        print (tableCell.text)
        if(index == 0):
            tableHeadings.append(tableCell.text)
        else:
            thisCourse[tableHeadings[cellIndex]] = tableCell.text
#            print (tableCell.text)
        cellIndex = cellIndex + 1
#    print(thisCourse)
    if (index >> 0):
        courseMatrix.append(thisCourse)
    index = index + 1

#courseMatrix[5]['Seats Avail.'] = 1

for iterateCourse in courseMatrix:
    thisCRN = iterateCourse['CRN']
    thisCourseName = iterateCourse['Course']
    thisMaxSeats = iterateCourse['Max Seats']
    thisAvailSeats = iterateCourse['Seats Avail.']
    thisTimeLoc = iterateCourse['Meet Times Days -- Times -- Location         '].replace("\n","  ")

    print("CRN: " + thisCRN)
    print("Max Seats: " + thisMaxSeats)
    print("Avail. Seats: " + str(thisAvailSeats))
    print("Meet Times Days -- Times -- Location: " + thisTimeLoc)
    if (int(thisAvailSeats) >> 0):
        print("Seats Available!")
        availableClass = "CRN: " + thisCRN + "  Course: " + thisCourseName + "  Schedule: " + thisTimeLoc
        pushRequestFull = pushRequestURL + '/Class Available:' + thisCRN + '/' + thisTimeLoc
        pushRequest = requests.get(pushRequestFull)
        print(pushRequest.text)
