import tkinter

def print_value(val):
    print(val)

root = tkinter.Tk()

scale = tkinter.Scale(orient='horizontal', from_=0, to=128, command=print_value)
scale.pack()

root.mainloop()
