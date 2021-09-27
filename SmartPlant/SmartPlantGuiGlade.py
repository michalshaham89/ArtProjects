import time
#from gi.repository import Gtk, Gdk
import gi
gi.require_version("Gtk", "2.0")
from gi.repository import Gtk


class SmartPlantGui(object):
    """
    this class is used to build/change Dobot's program.
    a program is a series of steps (movements/grips/sleep) for the Dobot.
    """

    def __init__(self, program=None, rnd=0):
        glade_path = 'C:\Users\Michal\Documents\michuli\hackatau\SmartPlantGui.glade'
        builder = Gtk.Builder()
        builder.add_from_file(glade_path)
        self.window = builder.get_object("window1")
        self.window.connect("destroy", lambda x: Gtk.main_quit())

        self.button_led1 = builder.get_object("button_led1")
        self.button_led2 = builder.get_object("button_led2")
        self.button_led3 = builder.get_object("button_led3")
        self.button_mist = builder.get_object("button_mist")
        self.hscale_tornado = builder.get_object("hscale_tornado")
        self.button_bubbles = builder.get_object("button_bubbles")

        self.label_graph1 = builder.get_object("label_graph1")
        self.label_graph2 = builder.get_object("label_graph2")
        self.label_graph3 = builder.get_object("label_graph3")
        self.label_graph4 = builder.get_object("label_graph4")
        self.label_graph5 = builder.get_object("label_graph5")

        self.gui()

    def gui(self):
        self.label_graph4.set_text('hayush')
        self.window.show_all()
        Gtk.main()
