#Due to the company's database requiring every JSON packet for a 24 hour period to be downloaded individually, this script was designed to merge datapackets from a like branch together to make loading them into Power BI easier
#It was also designed to make organization of files more streamlined
import json
import os

inputFolder = r"<input_folder>"
outputFolder = r"<output_folder>"
fileNameOutput = "Odontología Torres_Merged.json" #Current Branch being worked on

os.makedirs(outputFolder, exist_ok=True)
#Makes a new directory but checks if one already exists

outputFile = os.path.join(outputFolder, fileNameOutput)
count = 0
mergedData = []

#Iterate through all JSON data packets
for filename in os.listdir(inputFolder):
    filePath = os.path.join(inputFolder, filename)
    with open(filePath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            mergedData.extend(data)
            count += 1
            print(f"Extended {count} items")
        else:
            mergedData.append(data)
            count += 1
            print(f"Appended {count} items")

completeData = {
    "ticketsBatch":{
        "BatchId": "Odontología Torres", 
        "tickets": mergedData
    }
}

with open(outputFile, 'w', encoding='utf-8') as out_file:
    print ("Saving to file")
    json.dump(completeData, out_file, ensure_ascii=False, indent=4)
    
print(f"Merged {len(mergedData)} items into {outputFile}") #Informs user of successful output
    
