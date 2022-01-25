import json
import os

with open("repos1.txt", "r") as f:
    os.chdir("./repos/")
    for line in f:
        os.system(f"git clone https://github.com/adafruit/{line[:-1]}.git")
