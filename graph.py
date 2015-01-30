from tkinter import *
from util import *
def graph(Canevas,match):
    for cell in match.cells.values():
        if cell.owner == match.me:
            color = 'blue'
        elif cell.owner == -1:
            color = 'grey'
        else:
            color = 'red'
        m=25
        d=80
        x = cell.x/m +d
        y = cell.y/m +d
        r = cell.radius/7
        for id_ in cell.links:
            Canevas.create_line(x,y,match.cells[id_].x/m+d,match.cells[id_].y/m+d,width = 2)

    for cell in match.cells.values():
        if cell.owner == match.me:
            color = 'blue'
        elif cell.owner == -1:
            color = 'grey'
        else:
            color = 'red'
        m=25
        d=80
        x = cell.x/m +d
        y = cell.y/m +d
        r = cell.radius/7
        Canevas.create_oval(x-r, y-r, x+r, y+r, outline='black', fill=color)
        Canevas.create_text(x,y-7,text=str(cell.nb_off))
        lo=[]
        
        for _id in cell.links.keys():
            if (match.cells[_id].owner == match.me and cell_value(match,match.cells[_id])>cell_value(match,cell)):
                lo.append(0)
        Canevas.create_text(x,y+7,text=str('I'*cell.speed_prod))
