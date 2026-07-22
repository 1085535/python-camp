import tkinter as tk

window = tk.Tk()
window.title("Canvas Practice")

canvas = tk.Canvas(window, width=200, height=200, bg="black")
canvas.pack()

canvas.create_oval(50, 50, 150, 150, outline="gray", width=8)

canvas.create_arc(50, 50, 150, 150, start=90, extent=120, outline="lime", width=8, style=tk.ARC)

window.mainloop()