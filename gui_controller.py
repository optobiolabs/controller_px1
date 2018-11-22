#!/usr/local/bin/python2

from tkinter import *
from tkinter import ttk
import serial_connect as sc
from datetime import *
import os

class App:

    def __init__(self, master):

        self.master = master

        #self.ser  = ser

        self.state = False
        self.hours = 1
        self.minutes = 0
        self.seconds = 0


        COLOR_1 = 'black'
        COLOR_2 = 'grey'
        COLOR_3 = 'blue'
        COLOR_4 = 'blue'
        COLOR_5 = 'blue'
        COLOR_6 = 'yellow'

        #Notebook Style
        self.noteStyler = ttk.Style()
        # Import the Notebook.tab element from the default theme
        self.noteStyler.element_create('Plain.Notebook.tab', "from", 'default')
        # Redefine the TNotebook Tab layout to use the new element
        self.noteStyler.layout("TNotebook.Tab",
            [('Plain.Notebook.tab', {'children':
                [('Notebook.padding', {'side': 'top', 'children':
                    [('Notebook.focus', {'side': 'top', 'children':
                        [('Notebook.label', {'side': 'top', 'sticky': ''})],
                    'sticky': 'nswe'})],
                'sticky': 'nswe'})],
            'sticky': 'nswe'})])
        self.noteStyler.configure("TNotebook", background=COLOR_1, borderwidth=0, foreground="white")
        self.noteStyler.configure("TNotebook.Tab", background=COLOR_2, foreground=COLOR_3,
                                              lightcolor=COLOR_6, borderwidth=0)
        self.noteStyler.configure("TFrame", background=COLOR_1, foreground=COLOR_2, borderwidth=0)


        self.n = ttk.Notebook(master, style='TNotebook') #, style="LayoutNB")
        self.n.grid(column=0, row=0, padx=20, pady=0, ipadx=20, ipady=20, sticky=EW)

        self.f1 = ttk.Frame(self.n, style='TFrame')
        self.f2 = ttk.Frame(self.n, style='TFrame')
        self.f3 = ttk.Frame(self.n, style='TFrame')

        self.n.add(self.f1, text='Quick Start')
        self.n.add(self.f2, text='enter Profile')
        self.n.add(self.f3, text='Settings')

        self.manual  = LabelFrame(self.f1)
        self.manual.grid(row=0, column=0, padx=50,ipadx=20, ipady=20, pady=20)

        ch1 = StringVar(value = "off")
        ch2 = StringVar(value = "off")

        # slider 1
        Label(self.manual, text="CH1").grid(row=0, column=0,ipadx=20, ipady=20, sticky=SW)
        self.ch1_scale = Scale(self.manual, from_=0, to=100, orient=HORIZONTAL, width=15, length=300, variable = ch1, showvalue = 0,troughcolor='white')
        self.ch1_scale.grid(row=0, column=1, sticky=W, columnspan=3)
        self.ch1_scale.bind("<ButtonRelease-1>", self.readScale)
        self.ch1_scale_entry = Entry(self.manual, width=3, textvariable=ch1)
        self.ch1_scale_entry.grid(row=0, column = 4)
        self.ch1_scale_apply = Button(self.manual, text = "on", command = self.toggle1)
        self.ch1_scale_apply.grid(row=0, column = 5, sticky=W)

        # slider 2
        Label(self.manual, text="CH2").grid(row=1, column=0,ipadx=20, ipady=20, sticky=SW)
        self.ch2_scale = Scale(self.manual, from_=0, to=100, orient=HORIZONTAL, width=15, length=300, variable = ch2, showvalue = 0,troughcolor='white')
        self.ch2_scale.grid(row=1, column=1, sticky=W, columnspan=3)
        self.ch2_scale.bind("<ButtonRelease-1>", self.readScale)
        self.ch2_scale_entry = Entry(self.manual, width=3, textvariable=ch2)
        self.ch2_scale_entry.grid(row=1, column = 4)
        self.ch2_scale_apply = Button(self.manual, text = "on", command = self.toggle2)
        self.ch2_scale_apply.grid(row=1, column = 5, sticky=W)

        # separator
        s = ttk.Separator(self.manual, orient=HORIZONTAL)
        s.grid(row=3, column= 0, columnspan= 7, sticky= EW, pady=20, padx=10)

        # profile 1
        Label(self.manual, text="CH1 start").grid(row=4, column=0,  sticky=W,ipadx=20)
        self.ch1_start = Entry(self.manual, width = 8)
        self.ch1_start.grid(row=4, column=1, sticky=W)
        Label(self.manual, text="intensity").grid(row=4, column=2,  sticky=W)
        self.ch1_int = Entry(self.manual, width = 6)
        self.ch1_int.grid(row=4, column=3, sticky=W)
        Label(self.manual, text="duration").grid(row=4, column=4,  sticky=W)
        self.ch1_dur = Entry(self.manual, width = 8)
        self.ch1_dur.grid(row=4, column=5, sticky=W)

        # profile 2
        Label(self.manual, text="CH2 start").grid(row=5, column=0,  sticky=W,ipadx=20)
        self.ch2_start = Entry(self.manual, width = 8)
        self.ch2_start.grid(row=5, column=1, sticky=W)
        Label(self.manual, text="intensity").grid(row=5, column=2,  sticky=W)
        self.ch2_int = Entry(self.manual, width = 6)
        self.ch2_int.grid(row=5, column=3, sticky=W)
        Label(self.manual, text="duration").grid(row=5, column=4,  sticky=W)
        self.ch2_dur = Entry(self.manual, width = 8)
        self.ch2_dur.grid(row=5, column=5, sticky=W)

        self.submit = Button(self.manual, text = "upload profile")
        self.submit.grid(row=6, column=3, sticky=N, ipady=20, columnspan=2)
        self.submit = Button(self.manual, text = "start")
        self.submit.grid(row=6, column=5, sticky=N, ipady=20)

        # separator
        s = ttk.Separator(self.manual, orient=HORIZONTAL)
        s.grid(row=7, column= 0, columnspan= 7, sticky= EW, pady=20, padx=10)

        # status USB
        self.device = Label(self.manual, text="searching device",)
        self.device.grid(row=8, column=0,ipadx=20, ipady=20, sticky=W)
        self.status = Canvas(self.manual, width=30, height=30)
        self.status.grid(row=8, column=1, sticky=W)
        self.oval_red = self.status.create_oval(10, 10, 30, 30, fill="red", outline="white")
        self.status_usb()

        # start measurement
        time_start = datetime.now()
        self.measure = Button(self.manual, text = "start measurement", command = self.measure)
        self.measure.grid(row=8, column=2, sticky=W, columnspan=2)
        self.time = Label(self.manual, text = '--:--:--') #.strftime('%H:%M:%S')
        self.time.grid(row=8, column=4, sticky=W)


        self.code_input = LabelFrame(self.f2)
        self.code_input.grid(row=0, column=0, padx=50, pady=20)
        self.code_input.grid_columnconfigure(0, minsize=245)
        self.code_submit = Button(self.f2, text='submit')
        self.code_submit.grid(row=1, column=0, sticky=W+E, padx=50)

        self.channel1 = LabelFrame(self.code_input)
        self.channel1.grid(row=0, column=0, padx=20, pady=10, ipadx=10, ipady=10)
        self.channel1.grid_columnconfigure(0, minsize=100)
        Label(self.channel1, text="channel 1", padx = 10, pady= 10, font='Helvetica 16 bold').grid(row=0,column=0, sticky=W)

        self.channel2 = LabelFrame(self.code_input)
        self.channel2.grid(row=0, column=1, padx=20, pady=10, ipadx=10, ipady=10)
        self.channel2.grid_columnconfigure(0, minsize=100)
        Label(self.channel2, text="channel 2", padx = 10, pady= 10, font='Helvetica 16 bold').grid(row=0,column=0, sticky=W)

        #master.steps=illuminate

        self.entry1 = add_entry(self.channel1)
        self.entry2 = add_entry(self.channel2)

        Label(self.f3, text="channel 1").grid(row=0, column=0)
        self.channel1_wl = Entry(self.f3, width=10)
        self.channel1_wl.grid(row=0, column=1)
        Label(self.f3, text="nm").grid(row=0, column=2, sticky=W)
        Label(self.f3, text="channel 2").grid(row=1, column=0)
        self.channel2_wl = Entry(self.f3, width=10)
        self.channel2_wl.grid(row=1, column=1)
        Label(self.f3, text="nm").grid(row=1, column=2, sticky=W)

        # separator
        s = ttk.Separator(self.f3, orient=HORIZONTAL)
        s.grid(row=2, column= 0, columnspan= 7, sticky= EW, pady=20, padx=10)

        Label(self.f3, text="filename").grid(row=3, column=0)
        self.channel1_wl = Entry(self.f3, width=13)
        self.channel1_wl.grid(row=3, column=1)

        # separator
        s = ttk.Separator(self.f3, orient=HORIZONTAL)
        s.grid(row=4, column= 0, columnspan= 7, sticky= EW, pady=20, padx=10)

        Label(self.f3, text="device").grid(row=5, column=0)
        self.channel1_wl = Entry(self.f3, width=13)
        self.channel1_wl.grid(row=5, column=1)


    def readScale(self, event):

        intensity1 = '0'
        intensity2 = '0'

        if self.ch1_scale_apply.configure('text')[-1] == "off":
            intensity1 = self.ch1_scale_entry.get()
        if self.ch2_scale_apply.configure('text')[-1] == "off":
            intensity2 = self.ch2_scale_entry.get()

        self.controll_ch(intensity1,intensity2)

    def toggle1(self):

        intensity2 = self.ch2_scale_entry.get()
        if self.ch1_scale_apply.configure('text')[-1] == "on":
            intensity1 = self.ch1_scale_entry.get()
            self.ch1_scale_apply.configure(text = 'off')
            self.controll_ch(intensity1, intensity2)
            self.ch1_scale.configure(troughcolor='blue')
        else:
            self.ch1_scale_apply.configure(text = 'on')
            self.controll_ch('0', intensity2)
            self.ch1_scale.configure(troughcolor='white')


    def toggle2(self):

        intensity1 = self.ch1_scale_entry.get()
        if self.ch2_scale_apply.configure('text')[-1] == "on":
            intensity2 = self.ch2_scale_entry.get()
            self.ch2_scale_apply.configure(text = 'off')
            self.controll_ch(intensity1, intensity2)
            self.ch2_scale.configure(troughcolor='green')
        else:
            self.ch2_scale_apply.configure(text = 'on')
            self.controll_ch(intensity1, '0')
            self.ch2_scale.configure(troughcolor='white')

    def controll_ch(self, intensity1, intensity2):

        profile = "0,"+ intensity1 + ",0:0," + intensity2 + ",0"
        print (profile)
        if not sc.arduino.name == 'no device found':
            print (sc.arduino.readline())
            sc.arduino.write((str(profile) + '\r\n').encode())
            print (sc.arduino.readline())
            self.status.itemconfig(self.oval_red, fill="green")

    def status_usb(self):
        if not sc.arduino.name == 'no device found':
            self.status.itemconfig(self.oval_red, fill="green")
            self.device.configure(text="device ready")
        else:
            self.status.itemconfig(self.oval_red, fill="red")
            self.device.configure(text="no device")

    def measure(self):

        self.time_start = datetime.now()
        self.protocoll("start measurement")
        self.state = True
        self.counter()
        # Timer(self.f1) XXX

    def counter(self):

        if self.state == True:
            self.time.configure(text="%02d:%02d:%02d" % (self.hours, self.minutes,self.seconds))

            self.master.after(1000, self.counter)
        else:
            self.master.after(100, self.counter)

    def protocoll(self, text):

        fh = open("protocoll.txt", "a")
        fh.write(str(datetime.now()) + " " + text + "\n")
        fh.close


class add_entry:
    def __init__(self, master):
        self.master = master
        self.entries = []

        self.canvas = Canvas(master, width=200, height=342)
        self.add_button = Button(master, text=" add entry ", command=self.add)
        self.container = Frame()

        self.canvas.create_window(0, 0, anchor="nw", window=self.container)
        self.add_button.grid(row=0, column=0, sticky= E)
        self.canvas.grid(row=1, column=0)

        self.add()

    def add(self):
        step = LabelFrame(self.container, padx = 20, pady= 4, bg='lightgrey', bd = 0)
        step.grid(in_=self.container)

        Label(step, text="time", bg='lightgrey').grid(row = 0, column = 0, sticky=W)
        time = Entry(step, width=12)
        time.grid(row = 0, column = 1)
        Label(step, text="intensity", bg='lightgrey').grid(row = 1, column = 0, sticky=W)
        intensity = Entry(step, width=12)
        intensity.grid(row = 1, column = 1)
        Label(step, text="duration", bg='lightgrey').grid(row = 2, column = 0, sticky=W)
        duration = Entry(step, width=12)
        duration.grid(row = 2, column = 1)

        self.entries.append(time)


def main():

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    root = Tk()
    root.title("Opto Control")
    root.geometry("850x750+20+50")
    app = App(root)

    canvas = Canvas(root, width =700, height = 130)
    canvas.grid(column=0, row=9, columnspan= 3, sticky=W)
    img = PhotoImage(master = root, file = resource_path("logoOB.gif"))
    canvas.create_image(420,60, image=img)

    root.mainloop()

if __name__ == '__main__':
  main()
