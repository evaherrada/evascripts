import ast
import csv
with open('adafruit.csv', 'w', newline='') as csvfile:
    adafruitwriter = csv.writer(csvfile, delimiter='|',
                            quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    adafruitwriter.writerow(['name', 'url', 'version', 'description', 'documentation'])
    with open('adafruit.txt', 'r') as F:
        for line in F:
            row = ast.literal_eval(line)
            adafruitwriter.writerow(row.values())
