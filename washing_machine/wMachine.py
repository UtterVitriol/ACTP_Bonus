import time
import locale
import threading
from enum import Enum

locale.setlocale(locale.LC_ALL, '')
# TODO: Exceptions


class LoadType(Enum):
    LIGHT = 1
    REGULAR = 2
    HEAVY = 3
    SINGLE = 4
    DOUBLE = 5


class DoorState(Enum):
    OPEN = 1
    CLOSED = 2
    UNLOCKED = 3
    LOCKED = 4


class MyDoor():
    def __init__(self) -> None:
        self.ajar = DoorState.CLOSED
        self.locked = DoorState.UNLOCKED

    def open(self) -> bool:
        if self.ajar is DoorState.CLOSED:
            self.ajar = DoorState.OPEN

    def close(self) -> bool:
        if self.ajar is DoorState.OPEN:
            self.ajar = DoorState.CLOSED

    def lock(self) -> bool:
        if self.locked is DoorState.UNLOCKED:
            self.locked = DoorState.LOCKED

    def unlock(self) -> bool:
        if self.locked is DoorState.LOCKED:
            self.locked = DoorState.UNLOCKED


class WashCycle():
    def __init__(self):
        print("I'm circle")

    def light(self):
        return

    def normal(self):
        return

    def heavy(self):
        return


class MyTimer():
    def __init__(self):
        self.length = 0
        return

    def start(self, length: int):
        self.length = length
        now = int(time.time())
        cur = now
        while cur != now + self.length:
            cur = int(time.time())
            time.sleep(1)

    def increase(self, length: int):
        self.length += length


class MyLoad():
    def __init__(self, fill, wash, rinse, spin):
        self.price = 2.0
        self.runTime = 0
        self._calcFill(fill)
        self._calcWash(wash)
        self._calcRinse(rinse)
        self._calcSpin(spin)

        return

    def _calcFill(self, mode):
        if mode == LoadType.LIGHT:
            self.runTime += 3
        elif mode == LoadType.REGULAR:
            self.runTime += 5
        elif mode == LoadType.HEAVY:
            self.runTime += 8
            self.price += .5
        else:
            return False

        return True

    def _calcWash(self, mode):
        if mode == LoadType.LIGHT:
            self.runTime += 5
        elif mode == LoadType.REGULAR:
            self.runTime += 10
        elif mode == LoadType.HEAVY:
            self.runTime += 17
            self.price += 1.5
        else:
            return False

        return True

    def _calcRinse(self, mode):
        if mode == LoadType.SINGLE:
            self.runTime += 10
        elif mode == LoadType.DOUBLE:
            self.runTime += 15
            self.price += 1.25
        else:
            return False

        return True

    def _calcSpin(self, mode):
        if mode == LoadType.SINGLE:
            self.runTime += 5
        elif mode == LoadType.DOUBLE:
            self.runTime += 11
            self.price += .75
        else:
            return False

        return True


class MyWashingMachine():
    CycleTypes = {
        "Light": LoadType.LIGHT,
        "Regular": LoadType.REGULAR,
        "Heavy": LoadType.HEAVY,
        "Single": LoadType.SINGLE,
        "Double": LoadType.DOUBLE
    }

    def __init__(self):
        self.door = MyDoor()
        self.timer = MyTimer()
        self.on = False
        self.money = 0
        self.cycles = {
            "fill": LoadType.REGULAR,
            "wash": LoadType.REGULAR,
            "rinse": LoadType.SINGLE,
            "spin": LoadType.SINGLE,
        }

    def _money(self):
        while (1):
            print(
                "--------------------",
                f"Money: {locale.currency(self.money, grouping=True)}",
                "--------------------",
                "Insert Quarter: I",
                "Refund: R",
                "Back: B",
                sep="\n"
            )

            choice = input("Choice: ").lower()

            if choice == 'i':
                if self.money == 4.0:
                    print("Max monies")
                    continue
                self.money += .25
            elif choice == 'r':
                self.money = 0
            elif choice == 'b':
                break
            else:
                print(f"{choice} is an invalid option")
                continue

    def _lrh(self):
        while (1):
            print(
                "Light: L",
                "Regular: R",
                "Heavy: H",
                sep="\n"
            )

            choice = input("Choice: ").lower()
            if choice == 'l':
                return LoadType.LIGHT
            elif choice == 'r':
                return LoadType.REGULAR
            elif choice == 'h':
                return LoadType.HEAVY
            else:
                print(f"{choice} is an invalid option")

    def _sd(self):
        while (1):
            print(
                "Single: S",
                "Double: D",
                sep="\n"
            )

            choice = input("Choice: ").lower()

            if choice == 's':
                return LoadType.SINGLE
            elif choice == 'd':
                return LoadType.DOUBLE
            else:
                print(f"{choice} is an invalid option")

    def _cycles(self):
        while (1):
            print(
                "--------------------",
                f"Fill: {self.cycles['fill'].name} | Wash: {self.cycles['wash'].name} ",
                f"Rinse: {self.cycles['rinse'].name} | Spin: {self.cycles['spin'].name}",
                "--------------------",
                "Fill: F",
                "Wash: W",
                "Rinse: R",
                "Spin: S",
                "Back: B",
                sep="\n"
            )

            choice = input("Choice: ").lower()

            if choice == 'f':
                self.cycles['fill'] = self._lrh()
            elif choice == 'w':
                self.cycles['wash'] = self._lrh()
            elif choice == 'r':
                self.cycles['rinse'] = self._sd()
            elif choice == 's':
                self.cycles['spin'] = self._sd()
            elif choice == 'b':
                break
            else:
                print(f"{choice} is an invalid option")

    def _run(self):
        load = MyLoad(*self.cycles.values())
        if self.money < load.price:
            print("Not enough monies")
            return

    def _main(self):
        while (1):
            print(
                "--------------------",
                "Washing Washer",
                f"Door: {self.door.ajar.name} | {self.door.locked.name}",
                f"Money: {locale.currency(self.money, grouping=True)}",
                "--------------------",
                "Door: D",
                "Cycles: C",
                "Money: M",
                "Run: r",
                "Exit: E",
                sep='\n'
            )

            choice = input("Choice: ").lower()

            if choice == 'd':
                print("door")
            elif choice == 'c':
                self._cycles()
            elif choice == 'm':
                self._money()
            elif choice == 'r':
                print("Running")
            elif choice == 'e':
                break
            else:
                print(f"{choice} is an invalid option")

    def start(self):
        self._main()


def main():
    wm = MyWashingMachine()
    wm.start()
    # wm.getMoney()
    # a = threading.Timer(1, print("fuck"))
    # a.start()

    return


if __name__ == "__main__":
    main()
