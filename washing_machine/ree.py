import msvcrt
import time


def Countdown():
    p = 3.00
    alarm = time.time() + p
    text = []
    while True:
        n = time.time()
        if msvcrt.kbhit():
            text.append(msvcrt.getche())
        if n < alarm:
            print(round(alarm - n))
        else:
            print("Time's up!")
            break
    print(text)


Countdown()
