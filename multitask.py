from multiprocessing import Process
from tkinter import*
def slider_1(slider1):
    global R1
    R1=slider1
def slider_2(slider2):
    global R2
    R2=slider2
def loop_a():
    master=Tk()
    while True:
        print(R1)
        master.update()
        slider1=Scale(master,from_=0,to=255,orient=HORIZONTAL,command=slider_1)
        slider1.grid(row=0,column=0)
        slider1.set(R1)
def loop_b():
    coba=Tk()
    while True:
        print(R2)
        coba.update()
        slider2=Scale(coba,from_=0,to=100,orient=HORIZONTAL,command=slider_2)
        slider2.grid(row=0,column=1)
        slider2.set(R2)
R1=0
R2=0

if __name__ == '__main__':
    Process(target=loop_a).start()
    Process(target=loop_b).start()