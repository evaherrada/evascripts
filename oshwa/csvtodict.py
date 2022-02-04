import csv

with open('adafruit.csv', 'r', newline='\n') as F:
    csvreader = csv.reader(F, delimiter='|', quotechar='"')
    with open('test.txt', 'w') as f:
        for row in csvreader:
            f.write(f"{{'name': '{row[0]}', 'url': '{row[1]}', 'version': '{row[2]}', 'description': \"{row[3]}\", 'documentation': '{row[4]}'}},\n")
