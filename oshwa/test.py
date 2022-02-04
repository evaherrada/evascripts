max_num = 0
with open('adafruit.txt', 'r') as F:
    for line in F:
        num = int(line[:-1].split('/')[-1])
        print(num)
        if num > max_num:
            max_num = num

print(max_num)

