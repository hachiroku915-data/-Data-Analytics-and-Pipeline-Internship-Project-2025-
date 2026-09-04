import json
import requests
import pytz
from pytz import timezone
from datetime import datetime
import time
import os
from playsound import playsound

targ_timezone = pytz.timezone("Iceland")

#start with number 9

day = 1
numOfDays = 0

branch_name = ""
branch = ""


month = 1
year = 2023
monthName = ""

count = int(input("Please enter a number for the branch to be selected: "))


if count == 0:
    branch_name = "Odontología Torres"
    branch = "oU4v5nt77uYfiaQn3cZQ"
elif count == 1:
    branch_name = "Odontología Alameda"
    branch = "8bNXhoGfGKceVo9Nke1k"
elif count == 2:
    branch_name = "IPS Yumbo"
    branch = "WRnpf0mRDVPePtsnzkz2"
elif count == 3:
    branch_name = "IPS Tuluá"
    branch = "IzhIz4rNSclmALbX3bp7"
elif count == 4:
    branch_name = "IPS Torres"
    branch = "juhBKQAUfukPcNpv3Crf"
elif count == 5:
    branch_name = "IPS Tequendama"
    branch = "3X6VRYkJy4NQrBPkHXT6"
elif count == 6:
    branch_name = "IPS SIA Sur"
    branch = "dzbkwGsOGHxE1YgDcO41"
elif count == 7:
    branch_name = "IPS SIA Norte"
    branch = "BHZy2g4sEcbkYaaIr8qk"
elif count == 8:
    branch_name = "IPS San Nicolás"
    branch = "33sZlGOD9jz3dd1lhkJP"
elif count == 9:
    branch_name = "IPS Prado"
    branch = "XsEZLZwWPPEIEuVTBGTY"
elif count == 10:
    branch_name = "IPS Palmira"
    branch = "Q16lIZ660RUwNkpPQD4a"
elif count == 11:
    branch_name = "IPS Morichal"
    branch = "d1G2sZQ6H3xgPQKYxTta"
elif count == 12:
    branch_name = "IPS Cartago"
    branch = "ax0GGBWvdHcmSLuCfrlk"
elif count == 13:
    branch_name = "IPS Buga"
    branch = "GQxoTDvc0QNWRCU0tXSU"
elif count == 14:
    branch_name = "IPS Alameda"
    branch = "5EZJywAysVflvI1u9A2o"
elif count == 15:
    branch_name = "Clínica Cartago Hospitalario"
    branch = "5tWVAeM0IRPN3AJSnXa2"
elif count == 16:
    branch_name = "Clínica Cartago Ambulatorio"
    branch = "6evy2NDnWmAI6WSOx0Cc"
else:
    branch = "" 
    branch_name = ""

while (year <= 2025):

    while (month <= 12):
        
        if month == 1:
            numOfDays = 31
            monthName = "January"
        elif month == 2:
            if (year % 4 == 0):
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

        output_location = f'D:\Quanty\Queries\Comfandi\Complete List'



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



            url = "https://qanty.com/api/tickets_detailed"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'fBUURJZ94p3Q14YV80Vp9D9Mt4ZQhbr5'
            }

            body = {
                "company_id": "qWBRkJQkaSBOc0d52c8E",  
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
                    "Fecha del Turno": datetime.utcfromtimestamp(ticket.get("issueDate", 0) / 1000).isoformat(),
                    "CustomerName": customer.get("name"),
                    "CustomerLastName": customer.get("lastName"),
                    "CustomerDocId": customer.get("docId"),
                    "CustomerDocType": customer.get("docType")
                }
                records.append(ticket_flat)

            

            fileName = f"{branch_name}_{month} {day} {year}.json"

            output_file = os.path.join(output_location, fileName) if output_location else fileName

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=4)
            print(f"Saved{len(records)} tickets to '{output_file}'")
            day = day + 1 
        month = month + 1
        day = 1
    year = year + 1
    month = 1

completeSound = "D:\Quanty\Auto Downloader\complete.wav"
playsound (completeSound)










