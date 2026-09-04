import json
import os

inputFolder = "D:\Quanty\Queries\Comfandi\Data Batches\Odontología Torres\Raw"
outputFolder = "D:\Quanty\Queries\Comfandi\Data Batches\Odontología Torres\Merged"
fileNameOutput = "Odontología Torres_Merged.json"

os.makedirs(outputFolder, exist_ok=True)
#Makes a new directory but checks if one already exists

outputFile = os.path.join(outputFolder, fileNameOutput)
count = 0
mergedData = []

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
        "BatchId": "Clínica Cartago Ambulatorio",
        "tickets": mergedData
    }
}

with open(outputFile, 'w', encoding='utf-8') as out_file:
    print ("Saving to file")
    json.dump(completeData, out_file, ensure_ascii=False, indent=4)
    
print(f"Merged{len(mergedData)} items into {outputFile}")
    
