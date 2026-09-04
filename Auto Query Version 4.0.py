#Please note that some information contained within the original version of this script was sensitive company information as it was designed to work specifically with thier system.
#Due to this issue, I have REDACTED sensitive information and made note of so below. The structure of the script remains the same.
#This program was originally constructed and refined between Aug. and Jun. of 2025
import json
import requests
import pytz
from pytz import timezone
from datetime import datetime
import time
import os
from playsound import playsound

targ_timezone = pytz.timezone("Iceland") #Allows us to get the correct timezone within this library. This is due to the company location and the way their internal system operates.

day = 1
numOfDays = 0

branch_name = "" #This is the name of the specific medical office we are pulling data for
branch = "" #This is where the specific token for the branch's data is held


month = 1
year = 2023
monthName = ""

count = int(input("Please enter a number for the branch to be selected: "))


if count == 0:
    branch_name = "Odontología Torres"
    branch = "REDACTED" #All of these branch variables would normally hold the specific token for the branch but have been removed for security reasons. 
elif count == 1:
    branch_name = "Odontología Alameda"
    branch = "REDACTED"
elif count == 2:
    branch_name = "IPS Yumbo"
    branch = "REDACTED"
elif count == 3:
    branch_name = "IPS Tuluá"
    branch = "REDACTED"
elif count == 4:
    branch_name = "IPS Torres"
    branch = "REDACTED"
elif count == 5:
    branch_name = "IPS Tequendama"
    branch = "REDACTED"
elif count == 6:
    branch_name = "IPS SIA Sur"
    branch = "REDACTED"
elif count == 7:
    branch_name = "IPS SIA Norte"
    branch = "REDACTED"
elif count == 8:
    branch_name = "IPS San Nicolás"
    branch = "REDACTED"
elif count == 9:
    branch_name = "IPS Prado"
    branch = "REDACTED"
elif count == 10:
    branch_name = "IPS Palmira"
    branch = "REDACTED"
elif count == 11:
    branch_name = "IPS Morichal"
    branch = "REDACTED"
elif count == 12:
    branch_name = "IPS Cartago"
    branch = "REDACTED"
elif count == 13:
    branch_name = "IPS Buga"
    branch = "REDACTED"
elif count == 14:
    branch_name = "IPS Alameda"
    branch = "REDACTED"
elif count == 15:
    branch_name = "Clínica Cartago Hospitalario"
    branch = "REDACTED"
elif count == 16:
    branch_name = "Clínica Cartago Ambulatorio"
    branch = "REDACTED"
else:
    branch = "" 
    branch_name = ""

while (year <= 2025):

    while (month <= 12):
        
        if month == 1:
            numOfDays = 31
            monthName = "January"
        elif month == 2: 
            if (year % 4 == 0): #Automatically calculates if the current year we are pulling data from is a leap year and accounts for the extra day. 
                if (year % 100 != 0):
                    numOfDays = 29
                else:
                    if (year % 400 == 0):
                        numOfDays = 29
                    else:
                        numOfDays = 28
            else:
                numOfDays = 28
            monthName = "February"
        elif month == 3:
            monthName = "March"
            numOfDays = 31
        elif month == 4:
            monthName = "April"
            numOfDays = 30
        elif month == 5:
            monthName = "May"
            numOfDays = 31
        elif month == 6:
            monthName = "June"
            numOfDays = 30
        elif month == 7:
            monthName = "July"
            numOfDays = 31
        elif month == 8:
            monthName = "August"
            numOfDays = 31
        elif month == 9:
            monthName = "September"
            numOfDays = 30
        elif month == 10:
            monthName = "October"
            numOfDays = 31
        elif month == 11:
            monthName = "November"
            numOfDays = 30
        elif month == 12:
            monthName = "December"
            numOfDays = 31
        else:
            print ("This is an invalid month, please enter a valid month: \n" )

        output_location = f'<output_location>' #Specified file path for this specific dataset, would be changed based on the needs of the company. This version is hardcoded due to the fact that the location of the data I was downloading was constant.



        while (day <= numOfDays):
            startHour = 00
            startMinute = 00
            startSecond = 00
            endHour = 23
            endMinute = 59
            endSecond = 59

            start_date = datetime(year, month, day, startHour, startMinute, startSecond)
            startTimezone = targ_timezone.localize(start_date, is_dst=None)
            startEpoch = int(startTimezone.timestamp())
            end_date = datetime(year, month, day, endHour, endMinute, endSecond)
            endTimezone = targ_timezone.localize(end_date, is_dst=None)
            endEpoch = int(endTimezone.timestamp())



            url = "REDACTED" #Holds specific api URL for data extraction.
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'REDACTED' #Holds the authorization token for the company's database. 
            }

            body = {
                "company_id": "REDACTED",  
                "branch_id": branch,
                "start_date": startEpoch,
                "end_date": endEpoch
            }

            response = requests.post(url, json=body, headers=headers)
            response.raise_for_status()
            data = response.json()

            tickets_obj = data.get("tickets",{})

            records = []
            for key, ticket in tickets_obj.items():
                customer = ticket.get("customer",{})
                ticket_flat = {
                    "Turno": ticket.get("name"),
                    "Estado": ticket.get("status"),
                    "Sede": ticket.get("branchName"),
                    "Línea actual": ticket.get("currentLineName"),
                    "Línea inicial": ticket.get("startLineName"),
                    "Fecha del Turno": datetime.utcfromtimestamp(ticket.get("issueDate", 0) / 1000).isoformat(), #Deprecated format has been left unchanged to preserve originality. The modern equivalent of this line would be: "Fecha del Turno": datetime.fromtimestamp(ticket.get("issueDate", 0) / 1000, tz=UTC)
                    "CustomerName": customer.get("name"),
                    "CustomerLastName": customer.get("lastName"),
                    "CustomerDocId": customer.get("docId"),
                    "CustomerDocType": customer.get("docType")
                }
                records.append(ticket_flat)

            

            fileName = f"{branch_name}_{month} {day} {year}.json" #Automatically names the file, files had to be downloaded individually due to the constraints of the company database. A seperate merging program was created to resolve this.

            output_file = os.path.join(output_location, fileName) if output_location else fileName

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=4)
            print(f"Saved {len(records)} tickets to '{output_file}'")
            day = day + 1 
        month = month + 1
        day = 1
    year = year + 1
    month = 1

completeSound = "<completeSound Folder>"
playsound (completeSound) #Optional addition. This allowed me to focus on other aspects of the project while this worked in the background.










