from tkinter import *
def graph(Canevas,match):
    for cell in match.cells.values():
        if cell.owner == match.me:
            color = 'blue'
        elif cell.owner == -1:
            color = 'black'
        else:
            color = 'red'
        x = cell.x/50 +40
        y = cell.y/50 +40
        r = cell.radius/15
        Canevas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)
        Canevas.create_text(x, y, text=str(cell.id))
        for id_ in cell.links:
            Canevas.create_line(x,y,match.cells[id_].x/50+40,match.cells[id_].y/50+40)
            
