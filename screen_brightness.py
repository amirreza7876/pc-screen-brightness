import collections
import os
import subprocess
import time
from collections import Counter

import cv2


def screens():
    """
    Return displays outputs
    """
    output = [
        l for l in subprocess.check_output(["xrandr"]).decode("utf-8").splitlines()
    ]
    return [l.split()[0] for l in output if " connected " in l]


def revert(output):
    """
    Revert display settings if user disapproves
    """
    os.system("xrandr --output {} --brightness 1".format(output))


def main():
    sources = screens()
    print("Choose your display:")
    for i, source in enumerate(sources):
        print("\t", i, "-", source)
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
                        "xrandr --output {} --brightness 0.7".format(selected_display)
                    )

                if key == "bright":
                    os.system(
                        "xrandr --output {} --brightness 1".format(selected_display)
                    )

        while True:
            confirm = input("Apply changes? (y/n): ")
            if confirm == "n":
                revert(selected_display)
                print("Changes dscarded; Quitting now")
                exit(0)
            elif confirm == "y":
                print("Changes applied; Quitting now")
                exit(0)
            else:
                print("Invalid input, retry")

        """key = cv2.waitKey(100)
        if key == 27:
            break"""
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()