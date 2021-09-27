import tkinter as Tk
import serial
import time
import traceback
import numpy as np


class SmartPlant(object):
    def __init__(self):
        self.ser = serial.Serial(port='COM4',
                                 baudrate=57600,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS)

        self.tornado_state = False
        self.mist_state = False
        self.led1_state = False
        self.led2_state = False
        self.air_state = False

        self.label_air_temp = None
        self.label_water_temp = None
        self.label_ph = None
        self.root = None

    def send_message(self, msg, max_err=3, verbose=True):
        count_errors = 0
        time.sleep(0.04)
        while True:
            try:
                self.ser.write(msg)
                break
            except Exception:
                if verbose:
                    traceback.print_exc()
                if max_err and count_errors > max_err:
                    raise
                print ('error number', count_errors)
                count_errors += 1
                time.sleep(1)

    def read_message(self, max_err=3, verbose=True):
        count_errors = 0
        time.sleep(1)
        while True:
            try:
                response = self.ser.read_all()
                print ('ress', response)
                if response == '':
                    time.sleep(1)
                    continue
                return response
            except Exception:
                if verbose:
                    traceback.print_exc()
                if max_err and count_errors > max_err:
                    raise
                print ('error number', count_errors)
                count_errors += 1
                time.sleep(1)

    def get_temp_air(self):
        # return int(10*np.random.rand())
        self.send_message(msg=b'$30,0\r\n')
        res = self.read_message()
        print (res)
        try:
            return round(float(res.splitlines()[0].split(',')[1]), 1)
        except ValueError:
            return None

    def get_temp_water(self):
        # return int(10 * np.random.rand())
        self.send_message(msg=b'$20,0\r\n')
        res = self.read_message()
        print (res)
        try:
            return round(float(res.splitlines()[0].split(',')[1]),1)
        except ValueError:
            return None

    def get_ph(self):
        # return int(10 * np.random.rand())
        self.send_message(msg=b'$10,0\r\n')
        res = self.read_message()
        print (res)
        try:
            return round(float(res.splitlines()[0].split(',')[1]), 1)
        except ValueError:
            return None

    def switch_tornado(self):
        if self.tornado_state:
            self.tornado_state = False
        else:
            self.tornado_state = True
            self.send_message(msg=b'$200,0\r\n')
            print (self.read_message())
        print (self.tornado_state)

    def switch_mist(self):
        if self.mist_state:
            self.mist_state = False
        else:
            self.mist_state = True
            self.send_message(msg=b'$100,0\r\n')
            print (self.read_message())
        print (self.mist_state)

    def switch_led1(self):
        if self.led1_state:
            self.led1_state = False
        else:
            self.led1_state = True
            self.send_message(msg=b'$400,0\r\n')
            print (self.read_message())
        print (self.led1_state)

    def switch_led2(self):
        if self.led2_state:
            self.led2_state = False
        else:
            self.led2_state = True
            self.send_message(msg=b'$500,0\r\n')
            print (self.read_message())
        print (self.led2_state)

    def switch_air(self):
        if self.air_state:
            self.air_state = False
        else:
            self.air_state = True
            self.send_message(msg=b'$300,0\r\n')
            print (self.read_message())
        print (self.air_state)

    def update_data(self):
        self.label_air_temp.config(text=self.get_temp_air())
        self.label_water_temp.config(text=self.get_temp_water())
        self.label_ph.config(text=self.get_ph())
        self.root.geometry("")
        pass

    def aquarium_gui(self, message='hello, pugs!'):
        ret = [None]

        self.root = Tk.Tk()
        self.root.title("SmartPlant")

        # label
        label = Tk.Label(self.root, text="Welcome To SmartPlant")
        label.pack(side=Tk.constants.TOP)

        # buttons
        frame3 = Tk.Frame(self.root)
        frame3.pack(side=Tk.constants.TOP, padx=5, pady=3)

        labels3 = [
            {"text": "Air Temp", "fg": "blue", "bg": "White", "width": 16, "height": 3},
            {"text": "Water Temp", "fg": "blue", "bg": "White", "width": 16, "height": 3},
            {"text": "PH", "fg": "blue", "bg": "White", "width": 16, "height": 3}]
        for i, options in enumerate(labels3):
            Tk.Label(frame3, **options).grid(row=0, column=i, padx=2)

        frame4 = Tk.Frame(self.root)
        frame4.pack(side=Tk.constants.TOP, padx=5, pady=3)
        labels4 = [
            {"text": "None", "fg": "blue", "bg": "Grey", "width": 16, "height": 3},
            {"text": "None", "fg": "blue", "bg": "Grey", "width": 16, "height": 3},
            {"text": "None", "fg": "blue", "bg": "Grey", "width": 16, "height": 3}]
        # for i, options in enumerate(labels4):
        #     Tk.Label(frame4, **options).grid(row=0, column=i, padx=2)

        self.label_air_temp = Tk.Label(frame4, **labels4[0])
        self.label_air_temp.grid(row=0, column=0, padx=2)
        self.label_water_temp = Tk.Label(frame4, **labels4[1])
        self.label_water_temp.grid(row=0, column=1, padx=2)
        self.label_ph = Tk.Label(frame4, **labels4[2])
        self.label_ph.grid(row=0, column=2, padx=2)

        frame5 = Tk.Frame(self.root)
        frame5.pack(side=Tk.constants.TOP, padx=5, pady=3)
        button5 = {"text": "Update Data", "fg": "blue", "bg": "Grey", "width": 16, "height": 3,
                   "command": self.update_data}
        Tk.Button(frame5, **button5).grid(row=0, column=0, padx=2)

        frame1 = Tk.Frame(self.root)
        frame1.pack(side=Tk.constants.TOP, padx=5, pady=3)
        buttons1 = [
            {"text": "LED1", "fg": "blue", "bg": "Grey", "width": 16, "height": 3, "command": self.switch_led1},
            {"text": "LED2", "fg": "blue", "bg": "Grey", "width": 16, "height": 3, "command": self.switch_led2}]
        for i, options in enumerate(buttons1):
            Tk.Button(frame1, **options).grid(row=0, column=i, padx=2)

        frame2 = Tk.Frame(self.root)
        frame2.pack(side=Tk.constants.TOP, padx=5, pady=3)
        buttons2 = [
            {"text": "Mist", "fg": "black", "bg": "Grey", "width": 16, "height": 3, "command": self.switch_mist},
            {"text": "Tornado", "fg": "black", "bg": "Grey", "width": 16, "height": 3, "command": self.switch_tornado},
            {"text": "Air", "fg": "black", "bg": "Grey", "width": 16, "height": 3, "command": self.switch_air}]
        for i, options in enumerate(buttons2):
            Tk.Button(frame2, **options).grid(row=0, column=i, padx=2)

        self.root.protocol("WM_DELETE_WINDOW")

        self.root.mainloop()

        self.ser.close()

        return ret[0]


if __name__ == '__main__':
    g = SmartPlant()
    g.aquarium_gui()
