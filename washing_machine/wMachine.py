import time
import locale
import threading
from enum import Enum
from wMachineGui import MainMoney, Money, Door, Cycles, Cycle, StartButton, Error, Progress
import tkinter as tk

locale.setlocale(locale.LC_ALL, '')
# TODO: Make gui only responsible for gui state


class LoadType(Enum):
    LIGHT = 1
    REGULAR = 2
    HEAVY = 3
    SINGLE = 4
    DOUBLE = 5


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
    def __init__(self):
        self.price = 2.0

        self.fill = LoadType.REGULAR
        self.wash = LoadType.REGULAR
        self.rinse = LoadType.SINGLE
        self.spin = LoadType.SINGLE

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
        while cur != now + self.fillTime:
            time.sleep(1)
            cur = int(time.time())
            yield cur

    def runWash(self):
        now = int(time.time())
        cur = now
        while cur != now + self.washTime:
            time.sleep(1)
            cur = int(time.time())
            yield cur

    def runRinse(self):
        now = int(time.time())
        cur = now
        while cur != now + self.rinseTime:
            time.sleep(1)
            cur = int(time.time())
            yield cur

    def runSpin(self):
        now = int(time.time())
        cur = now
        while cur != now + self.spinTime:
            time.sleep(1)
            cur = int(time.time())
            yield cur

    def calcFill(self, mode: LoadType) -> None:
        self.fill = mode
        if mode == LoadType.LIGHT:
            self.fillTime = 3
        elif mode == LoadType.REGULAR:
            self.fillTime = 5
        elif mode == LoadType.HEAVY:
            self.fillTime = 8
            self.price += .5

    def calcWash(self, mode: LoadType) -> None:
        self.wash = mode
        if mode == LoadType.LIGHT:
            self.washTime = 5
        elif mode == LoadType.REGULAR:
            self.washTime = 10
        elif mode == LoadType.HEAVY:
            self.washTime = 17
            self.price += 1.5

    def calcRinse(self, mode: LoadType) -> None:
        self.rinse = mode
        if mode == LoadType.SINGLE:
            self.rinseTime = 10
        elif mode == LoadType.DOUBLE:
            self.rinseTime = 15
            self.price += 1.25

    def calcSpin(self, mode: LoadType) -> None:
        self.spin = mode
        if mode == LoadType.SINGLE:
            self.spinTime = 5
        elif mode == LoadType.DOUBLE:
            self.spinTime = 11
            self.price += .75

    # def reset_time(self) -> None:
    #     self.fillTime = 5
    #     self.washTime = 10
    #     self.rinseTime = 10
    #     self.spinTime = 5

    def calc_cost_start(self, fill: str, wash: str, rinse: str, spin: str) -> None:
        self.price = 2.0
        self.calcFill(LoadType[fill.upper()])
        self.calcWash(LoadType[wash.upper()])
        self.calcRinse(LoadType[rinse.upper()])
        self.calcSpin(LoadType[spin.upper()])

    def calc_cost_running(self, fill: str, wash: str, rinse: str, spin: str) -> None:
        self.price = 0.0
        self.calcFill(LoadType[fill.upper()])
        self.calcWash(LoadType[wash.upper()])
        self.calcRinse(LoadType[rinse.upper()])
        self.calcSpin(LoadType[spin.upper()])


class MyMainMenu(tk.Frame):
    def __init__(self, load: MyLoad, startFunc):
        super().__init__()
        # self = tk.Frame(self)
        self.startFunc = startFunc
        self.load = load
        self.money = MainMoney(self)
        self.door = Door(self)
        self.cycles = Cycles(self, self.updateCostStart)
        self.startb = StartButton(self, self.start, self.update_cycle)
        self.err = Error(self)

    def updateCostStart(self, cycles: list):
        self.load.calc_cost_start(*cycles)
        self.money.update_cost(self.load.price)

    def update_cycle(self):
        self
        # state = self.cycles.get_state()
        # if self.cycles.cycle_fill_drop["state"] == "normal":
        #     self.load.calcFill(LoadType[state[0].upper()])
        # if self.cycles.cycle_wash_drop["state"] == "normal":
        #     self.load.calcWash(LoadType[state[1].upper()])
        # if self.cycles.cycle_rinse_drop["state"] == "normal":
        #     self.load.calcRinse(LoadType[state[2].upper()])
        # if self.cycles.cycle_spin_drop["state"] == "normal":
        #     self.load.calcSpin(LoadType[state[3].upper()])

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
        self.money = Money(self)

        self.fill = Cycle(
            self, "Fill", load.fill.name.lower(), [
                "light", "regular", "heavy"])

        self.wash = Cycle(
            self, "Wash", load.wash.name.lower(), [
                "light", "regular", "heavy"])

        self.rinse = Cycle(
            self, "Rinse", load.rinse.name.lower(), [
                "single", "double"])

        self.spin = Cycle(
            self, "Spin", load.spin.name.lower(), [
                "single", "double"])

        # self.progress = Progress(self)

    def fillCostRunning(self, cycles: list):
        self.load.calc_cost_running(*cycles)
        self.fill.update_cost(self.load.price)

    def washCostRunning(self, cycles: list):
        self.load.calc_cost_running(*cycles)
        self.wash.update_cost(self.load.price)

    def fillCostRunning(self, cycles: list):
        self.load.calc_cost_running(*cycles)
        self.fill.update_cost(self.load.price)

    def fillCostRunning(self, cycles: list):
        self.load.calc_cost_running(*cycles)
        self.fill.update_cost(self.load.price)

    def addProgress(self, title):
        self.progress = Progress(self, title)

    def updateFill(self):
        self

    def updateWash(self):
        self

    def updateRinse(self):
        self

    def updateSpin(self):
        self


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
        for minute in self.load.runFill():
            self.running.progress.bar.step(100/self.load.fillTime)
        self.running.progress.destroy()

        self.running.fill.disable()

        self.running.addProgress("Wash")
        for minute in self.load.runWash():
            self.running.progress.bar.step(100/self.load.washTime)
        self.running.progress.destroy()

        self.running.wash.disable()

        self.running.addProgress("Rinse")
        for minute in self.load.runRinse():
            self.running.progress.bar.step(100/self.load.washTime)
        self.running.progress.destroy()

        self.running.rinse.disable()

        self.running.addProgress("Spin")
        for minute in self.load.runSpin():
            self.running.progress.bar.step(100/self.load.spinTime)
        self.running.progress.destroy()

        self.running.spin.disable()

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
