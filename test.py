from UI import UI

from tkinter import Canvas, Tk


root = Tk()

canvas = Canvas(root, width=500, height=500)
canvas.pack(expand=1)

UI(canvas).draw_grafic()

root.mainloop()