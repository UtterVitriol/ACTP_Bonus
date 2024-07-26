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


class MyDoor():
    def __init__(self) -> None:
        self.ajar = False
        self.locked = False

    def open(self) -> bool:
        if not self.ajar:
            self.ajar = True
            return True
        else:
            return False

    def close(self) -> bool:
        if self.ajar:
            self.ajar = False
            return True
        else:
            return False

    def lock(self) -> bool:
        if not self.locked:
            self.locked = True
            return True
        else:
            return False

    def unlock(self) -> bool:
        if self.locked:
            self.locked = False
            return True
        else:
            return False


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
        self.price = 2.00
        self.runTime = 0

        return

    def fill(self, mode):
        """
        cycles can range from light->normal->heavy with light receiving zero monetary discount, but heavy requiring an additional $0.50 to begin a run
        total run time changes include: light -=2min, regular == 5min, heavy +=3min
        """
        if mode == LoadType.LIGHT:
            self.runTime += 3
        elif mode == LoadType.REGULAR:
            self.runTime += 5
        elif mode == LoadType.HEAVY:
            self.runTime += 8
        else:
            return False

        return True

    def wash(self, mode):
        """
        cycles can range from light->normal->heavy with light receiving zero monetary discount, but heavy requiring an additional $1.50 to begin a run
        total run time changes include: light -=5min, regular == 10min, heavy +=7min
        """
        if mode == LoadType.LIGHT:
            self.runTime += 5
        elif mode == LoadType.REGULAR:
            self.runTime += 10
        elif mode == LoadType.HEAVY:
            self.runTime += 17
        else:
            return False

        return True

    def rinse(self, mode):
        """
        cycles can range from single->double with double requiring an additional $1.25 to begin a run
        total run time changes include: single == 10min, double +=5min
        """
        if mode == LoadType.SINGLE:
            self.runTime += 10
        elif mode == LoadType.DOUBLE:
            self.runTime += 15
        else:
            return False

        return True

    def spin(self, mode):
        """
        cycles can range from single->double with double requiring an additional $0.75 to begin run
        total run time changes include: single == 5min, double +=6min
        """
        if mode == LoadType.SINGLE:
            self.runTime += 5
        elif mode == LoadType.DOUBLE:
            self.runTime += 11
        else:
            return False

        return True


class MyWashingMachine():
    """
    must require a minimum of $2.00 to operate a standard 30-minute run (includes the regular fill, regular wash, single-rinse, and single-spin cycles)
    can take an additional $0.50-$4.00 in $0.25 intervals to increase cycles
    """

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
                choice
            elif choice == 'w':
                choice
            elif choice == 'r':
                choice
            elif choice == 's':
                choice
            elif choice == 'b':
                break
            else:
                print(f"{choice} is an invalid option")

    def _main(self):
        while (1):
            print(
                "--------------------",
                "Washing Washer",
                f"Money: {locale.currency(self.money, grouping=True)}",
                "--------------------",
                "Cycles: W",
                "Money: A",
                "Run: S",
                "Exit: H",
                sep='\n'
            )

            choice = input("Choice: ").lower()

            if choice == 'w':
                self._cycles()
            elif choice == 'a':
                self._money()
            elif choice == 's':
                print("Running")
            elif choice == 'h':
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
