from tkinter import *

window = Tk()
window.title("Mile to Km Converter")
window.minsize(width=200,height=100)

def convert_miles():
    miles = float(miles_input.get())
    km = round(miles * 1.60934)
    converted_label.config(text=f"{km}")

equal_label = Label(text="is equal to", font=("Arial",10))
equal_label.grid(column=0,row=1)

miles_input = Entry(width=10)
miles_input.grid(column=1, row=0)

miles_label = Label(text="Miles", font=("Arial",10))
miles_label.grid(column=2,row=0)

km_label = Label(text="Km",font=("Arial",10))
km_label.grid(column=2,row=1)

button = Button(text="Calculate", command=convert_miles)
button.grid(column=1,row=2)

converted_label = Label(text="0")
converted_label.grid(column=1,row=1)



window.mainloop()