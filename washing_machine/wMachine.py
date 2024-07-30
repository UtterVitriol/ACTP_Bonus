import time
import locale
import threading
from enum import Enum
from wMachineGui import MainMoney, Door, Cycles, StartButton, Error, Progress, Button
import tkinter as tk

locale.setlocale(locale.LC_ALL, '')
# TODO: Make gui only responsible for gui state


class LoadType(Enum):
    LIGHT = 1
    REGULAR = 2
    HEAVY = 3
    SINGLE = 4
    DOUBLE = 5


class MyLoad():
    def __init__(self):
        self.price = 2.0
        self.addonPrice = 0

        self.fillStartType = LoadType.REGULAR
        self.washStartType = LoadType.REGULAR
        self.rinseStartType = LoadType.SINGLE
        self.spinStartType = LoadType.SINGLE

        self.fillHasCapped = False
        self.washHasCapped = False
        self.rinseHasCapped = False
        self.spinHasCapped = False

        self.fillUpdated = False
        self.washUpdated = False
        self.rinseUpdate = False
        self.spinUpdated = False

        self.fillTime = 5
        self.washTime = 10
        self.rinseTime = 10
        self.spinTime = 5

    def runFill(self):
        now = int(time.time())
        cur = now
        while cur < now + self.fillTime:
            time.sleep(1)
            cur = int(time.time())
            yield cur

    def runWash(self):
        now = int(time.time())
        cur = now
        while cur < now + self.washTime:
            time.sleep(1)
            cur = int(time.time())
            yield cur

    def runRinse(self):
        now = int(time.time())
        cur = now
        while cur < now + self.rinseTime:
            time.sleep(1)
            cur = int(time.time())
            yield cur

    def runSpin(self):
        now = int(time.time())
        cur = now
        while cur < now + self.spinTime:
            time.sleep(1)
            cur = int(time.time())
            yield cur

    def calcFill(self, mode: LoadType) -> None:
        self.fill = mode
        if mode == LoadType.LIGHT:
            self.fillStartType = LoadType.LIGHT
            self.fillTime = 3 * 60
        elif mode == LoadType.REGULAR:
            self.fillStartType = LoadType.REGULAR
            self.fillTime = 5 * 60
        elif mode == LoadType.HEAVY:
            self.fillStartType = LoadType.HEAVY
            self.fillTime = 8 * 60
            self.price += .5

    def calcWash(self, mode: LoadType) -> None:
        self.wash = mode
        if mode == LoadType.LIGHT:
            self.washStartType = LoadType.LIGHT
            self.washTime = 5 * 60
        elif mode == LoadType.REGULAR:
            self.washStartType = LoadType.REGULAR
            self.washTime = 10 * 60
        elif mode == LoadType.HEAVY:
            self.washStartType = LoadType.HEAVY
            self.washTime = 17 * 60
            self.price += 1.5

    def calcRinse(self, mode: LoadType) -> None:
        self.rinse = mode
        if mode == LoadType.SINGLE:
            self.rinseTime = 10 * 60
        elif mode == LoadType.DOUBLE:
            self.rinseTime = 15 * 60
            self.price += 1.25

    def calcSpin(self, mode: LoadType) -> None:
        self.spin = mode
        if mode == LoadType.SINGLE:
            self.rinseStartType = LoadType.SINGLE
            self.spinTime = 5 * 60
        elif mode == LoadType.DOUBLE:
            self.rinseStartType = LoadType.DOUBLE
            self.spinTime = 11 * 60
            self.price += .75

    def calcCostStart(self, fill: str, wash: str, rinse: str, spin: str) -> None:
        self.price = 2.0
        self.calcFill(LoadType[fill.upper()])
        self.calcWash(LoadType[wash.upper()])
        self.calcRinse(LoadType[rinse.upper()])
        self.calcSpin(LoadType[spin.upper()])

    def calcCostRunning(self, fill: str, wash: str, rinse: str, spin: str) -> None:
        self.addonPrice = 0
        if fill == "heavy" and not self.fillHasCapped:
            self.addonPrice += .5
        if wash == "heavy" and not self.washHasCapped:
            self.addonPrice += 1.5
        if rinse == "double" and not self.rinseHasCapped:
            self.addonPrice += 1.25
        if spin == "double" and not self.spinHasCapped:
            self.addonPrice += .75


class MyMainMenu(tk.Frame):
    def __init__(self, load: MyLoad, startFunc):
        super().__init__()
        # self = tk.Frame(self)
        self.startFunc = startFunc
        self.load = load
        self.money = MainMoney(self)
        self.door = Door(self)
        self.cycles = Cycles(self, self.updateCostStart)
        self.startb = StartButton(self, self.start)
        self.err = Error(self)

    def updateCostStart(self, cycles: list):
        self.load.calcCostStart(*cycles)
        self.money.update_cost(self.load.price)

    def start(self):
        self.err.update("")
        if self.door.door_open.get() == "opened":
            self.err.update("Door open")
            return
        if self.door.door_lock.get() == "unlocked":
            self.err.update("Door unlocked")
            return
        if float(self.money.moneyStr.get()) < self.load.price:
            self.err.update("Not enough money")
            return

        if self.load.fillStartType == LoadType.HEAVY:
            self.load.fillHasCapped = True
        if self.load.washStartType == LoadType.HEAVY:
            self.load.washHasCapped = True
        if self.load.rinseStartType == LoadType.DOUBLE:
            self.load.rinseHasCapped = True
        if self.load.spinStartType == LoadType.DOUBLE:
            self.load.spinHasCapped = True

        self.money.update_money(0.0)
        self.money.update_cost(0)

        # self.door.disable()
        self.startFunc()

    def stop(self):
        self.cycles.update()
        self.door.enable()


class MyRunningMenu(tk.Frame):
    def __init__(self, load: MyLoad):
        super().__init__()
        self.load = load
        self.money = MainMoney(self)
        self.cycles = Cycles(self, self.updateCostStart)
        self.button = Button(self, self.changeCycle)
        self.err = Error(self)

    def addProgress(self, title):
        self.progress = Progress(self, title)

    def updateCostStart(self, cycles: list):
        self.load.calcCostRunning(*cycles)
        self.money.update_cost(self.load.addonPrice)

    def changeCycle(self):
        self.err.update("")
        money = float(self.money.moneyStr.get())
        if money < self.load.addonPrice:
            self.err.update("Not enough money")
            return

        state = self.cycles.get_state()

        fill = LoadType[state[0].upper()]
        if fill == LoadType.HEAVY and not self.load.fillHasCapped:
            self.load.fillHasCapped = True
        self.load.fillStartType = fill

        wash = LoadType[state[1].upper()]
        if wash == LoadType.HEAVY and not self.load.washHasCapped:
            self.load.washHasCapped = True
        self.load.washStartType = wash

        rinse = LoadType[state[2].upper()]
        if rinse == LoadType.DOUBLE and not self.load.rinseHasCapped:
            self.load.rinseHasCapped = True
        self.load.rinseStartType = rinse

        spin = LoadType[state[3].upper()]
        if spin == LoadType.DOUBLE and not self.load.spinHasCapped:
            self.load.spinHasCapped = True
        self.load.spinStartType = spin

        print(self.load.fillTime)
        self.load.calcCostStart(*state)
        print(self.load.fillTime)

        self.money.update_money(money - self.load.addonPrice)
        self.money.update_cost(0)


class MyWashingMachine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.ree)
        # self.geometry("1000x1000")
        self.resizable(False, False)
        self.title("Washing Machine")

        self.load = MyLoad()
        self.main = MyMainMenu(self.load, self.start_load)
        self.main.pack()

    def run(self):
        self.mainloop()

    def start_load(self):
        self.main.pack_forget()
        self.running = MyRunningMenu(self.load)
        self.running.pack()
        self.thr = threading.Thread(target=self.run_load, daemon=True)
        self.thr.start()

    def run_load(self):
        self.running.addProgress("Fill")
        for second in self.load.runFill():
            self.running.progress.bar.config(max=self.load.fillTime)
            self.running.progress.bar.step(1)
        self.running.progress.destroy()

        self.running.cycles.disable_cycle(0)

        self.running.addProgress("Wash")
        for second in self.load.runWash():
            self.running.progress.bar.config(max=self.load.washTime)
            self.running.progress.bar.step(1)
        self.running.progress.destroy()

        self.running.cycles.disable_cycle(1)

        self.running.addProgress("Rinse")
        for second in self.load.runRinse():
            self.running.progress.bar.config(max=self.load.rinseTime)
            self.running.progress.bar.step(1)
        self.running.progress.destroy()

        self.running.cycles.disable_cycle(2)

        self.running.addProgress("Spin")
        for second in self.load.runSpin():
            self.running.progress.bar.config(max=self.load.spinTime)
            self.running.progress.bar.step(1)
        self.running.progress.destroy()

        self.running.cycles.disable_cycle(3)

        self.running.destroy()
        self.main.pack()
        self.main.stop()

    def ree(self):
        self.destroy()


def main():
    wm = MyWashingMachine()
    wm.run()
    # wm.getMoney()
    # a = threading.Timer(1, print("fuck"))
    # a.start()

    return


if __name__ == "__main__":
    main()
