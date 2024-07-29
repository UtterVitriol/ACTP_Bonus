"""dashboard.py - contains the Dashboard class."""
import tkinter as tk
from tkinter import Frame, LEFT, RIGHT, Toplevel, Text, BOTH, ttk


class Door(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Door")
        # self.grid(row=0, column=0, padx=20, pady=10)
        self.pack(fill=BOTH, padx=20, pady=10)
        self.grid_columnconfigure((0, 3), weight=1)

        self.door_open = tk.StringVar()
        self.door_open.set("opened")
        self.door_lock = tk.StringVar()
        self.door_lock.set("unlocked")

        self.door_open_drop = tk.OptionMenu(
            self, self.door_open, *["opened", "closed"], command=self.validate_door)
        self.door_open_drop.grid(row=0, column=1, padx=10, pady=5)

        self.door_lock_drop = tk.OptionMenu(
            self, self.door_lock, *["unlocked", "locked"], command=self.validate_door)
        self.door_lock_drop.grid(row=0, column=2, padx=10, pady=5)

    def validate_door(self, choice):
        if choice == "locked" and self.door_open.get() == "opened":
            self.door_lock.set("unlocked")
        elif choice == "opened" and self.door_lock.get() == "locked":
            self.door_open.set("closed")

    def disable(self):
        self.door_lock_drop.config(state=tk.DISABLED)
        self.door_open_drop.config(state=tk.DISABLED)

    def enable(self):
        self.door_lock_drop.config(state=tk.NORMAL)
        self.door_open_drop.config(state=tk.NORMAL)


class Cycles(tk.LabelFrame):
    def __init__(self, master, updateFunc):
        super().__init__(master, text="Cycles")
        # self.grid(row=1, column=0, padx=20, pady=10)
        self.pack(fill=BOTH, padx=20, pady=10)
        self.updateFunc = updateFunc

        # Fill
        self.cycle_fill_label = tk.Label(self, text="Fill")
        self.cycle_fill_label.grid(row=0, column=0, padx=10, pady=5)

        self.cycle_fill = tk.StringVar()
        self.cycle_fill.set("regular")

        self.cycle_fill_drop = tk.OptionMenu(
            self, self.cycle_fill, *["light", "regular", "heavy"], command=lambda func: self.update())
        self.cycle_fill_drop.grid(row=1, column=0, padx=10, pady=5)

        # Wash
        self.cycle_wash_label = tk.Label(self, text="Wash")
        self.cycle_wash_label.grid(row=0, column=1, padx=10, pady=5)

        self.cycle_wash = tk.StringVar()
        self.cycle_wash.set("regular")

        self.cycle_wash_drop = tk.OptionMenu(
            self, self.cycle_wash, *["light", "regular", "heavy"], command=lambda func: self.update())
        self.cycle_wash_drop.grid(row=1, column=1, padx=10, pady=5)

        # Rinse
        self.cycle_rinse_label = tk.Label(self, text="Rinse")
        self.cycle_rinse_label.grid(row=0, column=2, padx=10, pady=5)

        self.cycle_rinse = tk.StringVar()
        self.cycle_rinse.set("single")

        self.cycle_rinse_drop = tk.OptionMenu(
            self, self.cycle_rinse, *["single", "double"], command=lambda func: self.update())
        self.cycle_rinse_drop.grid(row=1, column=2, padx=10, pady=5)

        # Spin
        self.cycle_spin_label = tk.Label(self, text="Spin")
        self.cycle_spin_label.grid(row=0, column=3, padx=10, pady=5)

        self.cycle_spin = tk.StringVar()
        self.cycle_spin.set("single")

        self.cycle_spin_drop = tk.OptionMenu(
            self, self.cycle_spin, *["single", "double"], command=lambda func: self.update())
        self.cycle_spin_drop.grid(row=1, column=3, padx=10, pady=5)

        self.update()

    def update(self):
        state = [
            self.cycle_fill.get(),
            self.cycle_wash.get(),
            self.cycle_rinse.get(),
            self.cycle_spin.get()
        ]

        self.updateFunc(state)

    def get_state(self):
        state = [
            self.cycle_fill.get(),
            self.cycle_wash.get(),
            self.cycle_rinse.get(),
            self.cycle_spin.get()
        ]
        return state

    def disable_cycle(self, cycle: int):
        if cycle == 0:
            self.cycle_fill_drop.config(state=tk.DISABLED)
        elif cycle == 1:
            self.cycle_wash_drop.config(state=tk.DISABLED)
        elif cycle == 2:
            self.cycle_rinse_drop.config(state=tk.DISABLED)
        elif cycle == 3:
            self.cycle_spin_drop.config(state=tk.DISABLED)

    def enable_cycles(self):
        self.cycle_fill_drop.config(state=tk.NORMAL)
        self.cycle_wash_drop.config(state=tk.NORMAL)
        self.cycle_rinse_drop.config(state=tk.NORMAL)
        self.cycle_spin_drop.config(state=tk.NORMAL)


class MainMoney(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Money")
        # self.grid(row=row, column=0, padx=20, pady=10)
        self.pack(fill=BOTH, padx=20, pady=10)
        self.grid_columnconfigure((0, 5), weight=1)

        self.costLabel = tk.Label(self, text="Price: $")
        self.costLabel.grid(row=0, column=1)

        self.costEntry = tk.Entry(self, state=tk.DISABLED)
        self.costEntry.grid(row=0, column=2, pady=5)

        self.moneyLabel = tk.Label(self, text="Inserted: $")
        self.moneyLabel.grid(row=0, column=3)

        self.moneyStr = tk.StringVar(self)
        self.moneyStr.set("0.00")

        self.moneySBox = tk.Spinbox(self, from_=0.00, to=6.00,
                                    format="%.2f", increment=.25, state='readonly', textvariable=self.moneyStr)
        self.moneySBox.grid(row=0, column=4, pady=5)

    def update_cost(self, cost: float):
        self.costEntry.config(state=tk.NORMAL)
        self.costEntry.delete(0, tk.END)
        self.costEntry.insert(0, f"{cost:.2f}")
        self.costEntry.config(state=tk.DISABLED)

    def update_money(self, money: float):
        self.moneyStr.set(
            f"{money:.2f}"
        )


class StartButton(tk.LabelFrame):
    def __init__(self, master, startFunc, updateFunc):
        super().__init__(master, text="Start")
        self.startFunc = startFunc
        self.updateFunc = updateFunc
        self.pack(fill=BOTH, padx=20, pady=10)
        self.grid_columnconfigure((0, 4), weight=1)

        self.isOn = False
        self.startButton = tk.Button(
            self, text="Start", command=self.startFunc)
        self.startButton.grid(row=0, column=1, padx=10, pady=5)

        self.stateEntry = tk.Entry(self, state=tk.DISABLED)
        self.stateEntry.grid(row=0, column=3, pady=5)
        self.update("Press start to wash")

    def switch(self):
        if self.isOn:
            self.startButton.config(text="Start")
            self.isOn = False
        else:
            self.startButton.config(text="On")
            self.isOn = True

    def update(self, text: str):
        self.stateEntry.config(state=tk.NORMAL)
        self.stateEntry.delete(0, tk.END)
        self.stateEntry.insert(0, text)
        self.stateEntry.config(state=tk.DISABLED)

    def disable(self):
        self.startButton.config(state=tk.DISABLED)

    def enable(self):
        self.startButton.config(state=tk.NORMAL)


class Error(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Error")
        self.pack(fill=BOTH, padx=20, pady=10)
        self.grid_columnconfigure((0, 2), weight=1)
        self.errorEntry = tk.Entry(self, state=tk.DISABLED)
        self.errorEntry.grid(row=0, column=1, pady=5)

    def update(self, text: str):
        self.errorEntry.config(state=tk.NORMAL)
        self.errorEntry.delete(0, tk.END)
        self.errorEntry.insert(0, text)
        self.errorEntry.config(state=tk.DISABLED)


class Money(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Money")
        self.pack(fill=BOTH, padx=20, pady=10)
        self.grid_columnconfigure((0, 3), weight=1)

        self.moneyLabel = tk.Label(self, text="Inserted: $")
        self.moneyLabel.grid(row=0, column=1)

        self.moneyStr = tk.StringVar(self)
        self.moneyStr.set("0.00")
        self.moneySBox = tk.Spinbox(self, from_=0.00, to=6.00,
                                    format="%.2f", increment=.25, state='readonly', textvariable=self.moneyStr)
        self.moneySBox.grid(row=0, column=2, pady=5)

    def update_money(self, price: float):
        self.moneyStr.set(
            f"{float(self.moneyStr.get()) - price:.2f}"
        )

    def set(self, val: float):
        self.moneyStr.set(f"{val:.2f}")


class Cycle(tk.LabelFrame):
    def __init__(self, master, title: str, start: str, options: list):
        super().__init__(master, text=title)
        self.pack(fill=BOTH, padx=20, pady=10)
        self.grid_columnconfigure((0, 5), weight=1)

        self.cycle = tk.StringVar()
        self.cycle.set(start)

        self.costLabel = tk.Label(self, text="Price: $")
        self.costLabel.grid(row=0, column=1)

        self.costEntry = tk.Entry(self, state=tk.DISABLED)
        self.costEntry.grid(row=0, column=2, pady=5)

        self.cycle_fill_drop = tk.OptionMenu(
            self, self.cycle, *options, command=lambda func: self.update())
        self.cycle_fill_drop.grid(row=0, column=3, padx=10, pady=5)

        self.cycleButton = tk.Button(self, text="Update")
        self.cycleButton.grid(row=0, column=4, padx=10, pady=5)

    def update_cost(self, cost: float):
        self.costEntry.config(state=tk.NORMAL)
        self.costEntry.delete(0, tk.END)
        self.costEntry.insert(0, f"{cost:.2f}")
        self.costEntry.config(state=tk.DISABLED)

    def disable(self):
        self.cycle_fill_drop.config(state=tk.DISABLED)
        self.cycleButton.config(state=tk.DISABLED)


class Progress(tk.LabelFrame):
    def __init__(self, master, title):
        super().__init__(master, text=title)
        self.pack(fill=BOTH, padx=20, pady=10)
        self.bar = ttk.Progressbar(self)
        self.bar.pack(fill=BOTH, padx=10, pady=5)


class Dashboard(tk.Tk):

    def __init__(self, startFunc):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.ree)
        # self.geometry("500x500")
        self.resizable(False, False)
        self.title("Washing Machine")
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.money = MainMoney(self.frame)
        self.door = Door(self.frame)
        self.cycles = Cycles(self.frame)
        self.startb = StartButton(self.frame, startFunc)

    def ree(self):
        print("no")
        self.destroy()


def main():
    d = Dashboard()
    # d.mainloop()
    input('reee')


if __name__ == "__main__":
    main()
