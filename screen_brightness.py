import collections
import os
import subprocess
import time
from collections import Counter
from signal import signal, SIGINT
import cv2
import sys


def screens():
    """
    Return displays outputs
    """
    global output
    output = [
        l for l in subprocess.check_output(["xrandr"]).decode("utf-8").splitlines()
    ]
    return [l.split()[0] for l in output if " connected " in l]


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Reset brightness to 1')
    os.system("xrandr --output {} --brightness 1".format(selected_display))
    exit(0)


def main():
    global selected_display
    sources = screens()
    print("Choose your display:")
    for i, source in enumerate(sources):
        if sys.version_info[0] > 3:
            print("\t", i, "-", source)
        else:
            print("\t"+ str(i)+ "-"+ source)
    try:
        selected_display = int(input("\nSelect output (default is 0): "))
    except ValueError:
        selected_display = 0

    selected_display = sources[selected_display]

    cap = cv2.VideoCapture(0)

    while True:
        dark, medium, bright = 0, 0, 0
        values, screen = [], []
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_gray = cv2.resize(gray, (100, 100))

        # rename i, j
        for i in resized_gray:
            for j in i:
                screen.append(j)

        screens_dic = dict(Counter(screen))
        for i in range(0, 256):
            if screens_dic.get(i):
                if 0 < i < 40:
                    dark = dark + screens_dic.get(i)

                if 30 < i < 100:
                    medium = medium + screens_dic.get(i)

                if 100 < i < 255:
                    bright = bright + screens_dic.get(i)

        values.append([dark, medium, bright])
        max_val_screen = max(values[0])
        val_dict = {
            "dark": values[0][0],
            "medium": values[0][1],
            "bright": values[0][2],
        }

        for key, value in val_dict.items():
            if val_dict.get(key) == max_val_screen:
                if key == "dark":
                    os.system(
                        "xrandr --output {} --brightness 0.5".format(selected_display)
                    )

                if key == "medium":
                    os.system(
                        "xrandr --output {} --brightness 0.8".format(selected_display)
                    )

                if key == "bright":
                    os.system(
                        "xrandr --output {} --brightness 1".format(selected_display)
                    )

        key = cv2.waitKey(100)
        """
        if key == 27:
            break"""
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    signal(SIGINT, handler)
    main()
