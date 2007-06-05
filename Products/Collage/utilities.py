import re

isNumber = re.compile(r"^\d+$")

def findFirstAvailableInteger(ids):
    i = 1
    while True:
        if str(i) not in ids:
            return i
        i += 1
