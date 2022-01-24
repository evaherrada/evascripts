import os
with open('libraries_not_in_bundle.txt', 'r') as F:
    for line in F:
        os.system(f'git clone https://github.com/adafruit/{line[:-1]} not_in_bundle/{line[:-1]}')
