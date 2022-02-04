lines = []
with open("repositories.txt", "r") as f:
    for line in f:
        lines.append(line.split('"')[1].split(" ")[0])

with open("repositories.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")
