import cv2
from collections import Counter
import collections
import os
import time
import subprocess


def screens():
    output = [l for l in subprocess.check_output(["xrandr"]).decode("utf-8").splitlines()]
    return [l.split()[0] for l in output if " connected " in l]

sources = screens()
print("choose your source to change brightness:")
for i, source in enumerate(sources):
    print("\t", i, "-",source)
getfromuser = int(input("\nwhich one (default is 0): "))
choosed = sources[getfromuser]

cap = cv2.VideoCapture(0)

while True:
    dark = 0
    medium = 0
    bright = 0
    values = []
    screen = []
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_gray = cv2.resize(gray, (100,100))

    for i in resized_gray:
        for j in i:
            screen.append(j)

    dic = dict(Counter(screen))
    for i in range(0,256):
        if dic.get(i):
            if 0 < i < 40:
                dark = dark + dic.get(i)

            if 30 < i < 100:
                medium = medium + dic.get(i)

            if 100 < i < 255:
                bright = bright + dic.get(i)

    values.append([dark, medium, bright])
    max_val_screen = max(values[0])
    val_dict = {"dark": values[0][0], "medium": values[0][1], "bright": values[0][2]}

    # print(val_dict)
    for key, value in val_dict.items():
        # print(val_dict.get(key))
        if val_dict.get(key) == max_val_screen:
            # print(key)
            if key == "dark":
                os.system("xrandr --output {} --brightness 0.5".format(choosed))

            if key == "medium":
                os.system("xrandr --output {} --brightness 0.7".format(choosed))

            if key == "bright":
                os.system("xrandr --output {} --brightness 1".format(choosed))

    # cv2.imshow("frame", resized_gray)
    key = cv2.waitKey(100)
    if key == 27:
        break

cv2.destroyAllWindows()
cap.release()
