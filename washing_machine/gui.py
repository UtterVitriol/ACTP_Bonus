import tkinter as tk

def toggle():

    if toggle_btn.config('relief')[-1] == 'sunken':
        toggle_btn.config(relief="raised")
    else:
        toggle_btn.config(relief="sunken")

def main():
    root = tk.Tk()
    toggle_btn = tk.Button(text="Toggle", width=12, relief="raised", command=toggle)
    toggle_btn.pack(pady=5)
    root.mainloop()

if __name__ == "__main__":
    main()