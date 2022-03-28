import os
import time

os.system("python3 -m adabot.arduino_libraries -o ./arduino.txt")

time.sleep(5)

exit(1)

with open("arduino.txt", "r") as F:
    text = (
        F.read()
        .split("Libraries have commits since last release")[1]
        .split("\n\n")[0]
        .split("--------------")[-1]
        .split('\n')[1:]
    )
    print(text)
    for line in text:
        l = line.strip().split()
        os.system(f"google-chrome https://github.com/adafruit/{l[0]}/releases/new")
        os.system(f"google-chrome https://github.com/adafruit/{l[0]}/edit/master/library.properties")
        os.system(f"google-chrome https://github.com/adafruit/{l[0]}/compare/{l[1]}...master")
        input()
