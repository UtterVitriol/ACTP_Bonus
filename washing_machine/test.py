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


class Cycles(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Cycles")
        # self.grid(row=1, column=0, padx=20, pady=10)
        self.pack(fill=BOTH, padx=20, pady=10)

        # Fill
        self.cycle_fill_label = tk.Label(self, text="Fill")
        self.cycle_fill_label.grid(row=0, column=0, padx=10, pady=5)

        self.cycle_fill = tk.StringVar()
        self.cycle_fill.set("regular")

        self.cycle_fill_drop = tk.OptionMenu(
            self, self.cycle_fill, *["light", "regular", "heavy"])
        self.cycle_fill_drop.grid(row=1, column=0, padx=10, pady=5)

        # Wash
        self.cycle_wash_label = tk.Label(self, text="Wash")
        self.cycle_wash_label.grid(row=0, column=1, padx=10, pady=5)

        self.cycle_wash = tk.StringVar()
        self.cycle_wash.set("regular")

        self.cycle_wash_drop = tk.OptionMenu(
            self, self.cycle_wash, *["light", "regular", "heavy"])
        self.cycle_wash_drop.grid(row=1, column=1, padx=10, pady=5)

        # Rinse
        self.cycle_rinse_label = tk.Label(self, text="Rinse")
        self.cycle_rinse_label.grid(row=0, column=2, padx=10, pady=5)

        self.cycle_rinse = tk.StringVar()
        self.cycle_rinse.set("single")

        self.cycle_rinse_drop = tk.OptionMenu(
            self, self.cycle_rinse, *["single", "double"])
        self.cycle_rinse_drop.grid(row=1, column=2, padx=10, pady=5)

        # Spin
        self.cycle_spin_label = tk.Label(self, text="Spin")
        self.cycle_spin_label.grid(row=0, column=3, padx=10, pady=5)

        self.cycle_spin = tk.StringVar()
        self.cycle_spin.set("single")

        self.cycle_spin_drop = tk.OptionMenu(
            self, self.cycle_spin, *["single", "double"])
        self.cycle_spin_drop.grid(row=1, column=3, padx=10, pady=5)


class Money(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Money")
        # self.grid(row=row, column=0, padx=20, pady=10)
        self.pack(fill=BOTH, padx=20, pady=10)
        self.grid_columnconfigure((0, 3), weight=1)

        self.symbol = tk.Label(self, text="$")
        self.symbol.grid(row=0, column=1)

        self.money = tk.Spinbox(self, from_=0.00, to=4.00,
                                format="%.2f", increment=.25, state='readonly')
        # self.money.pack(padx=10, pady=5)
        self.money.grid(row=0, column=2, pady=5)


class StartButton(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Washing Machine")
        self.pack(fill=BOTH, padx=20, pady=10)
        self.isOn = False
        self.button = tk.Button(self, text="Off", command=self.switch)
        self.button.pack(padx=10, pady=5)

    def switch(self):
        if not self.isOn:
            self.button.config(text="On")
            self.isOn = True


class Dashboard(tk.Tk):

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.ree)
        # self.geometry("500x500")
        self.resizable(False, False)
        self.title("Washing Machine")
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.money = Money(self.frame)
        self.door = Door(self.frame)
        self.cycles = Cycles(self.frame)
        self.startb = StartButton(self.frame)

    def ree(self):
        print("no")
        self.destroy()


def main():
    d = Dashboard()
    # d.mainloop()
    input('reee')


if __name__ == "__main__":
    main()
