import time
from gi.repository import Gtk, Gdk


# this script is used to build Dobot's programs you can later run (during calibration, for example).
# a program is a series of steps (movements/grips/sleep) for the Dobot.
# all the programs are saved in carchive.
# instructions: run the script -> choose a program from the list or a new one -> build the programs using the gui.
# in order to run the program use class "DobotController", method "execute_program".


class DobotProgramBuilder(DobotController):
    """
    this class is used to build/change Dobot's program.
    a program is a series of steps (movements/grips/sleep) for the Dobot.
    """
    def __init__(self, program=None, rnd=0):
        DobotController.__init__(self, dummy=False)
        self.program = program
        self.rnd = rnd
        self.selected_step = -1
        self.step_list_radio_buttons = []

        glade_path = 'lab/dobot/dobot_gui_glade2.glade'
        gladefile = config.jointo.svn_python(glade_path)
        builder = Gtk.Builder()
        builder.add_from_file(gladefile)
        self.window = builder.get_object("window1")
        self.window.connect("destroy", lambda x: Gtk.main_quit())

        self.go_home_button = builder.get_object("go_home_button")
        self.execute_all_button = builder.get_object("execute_all_button")
        self.execute_all_till_selected_step_button = builder.get_object("execute_all_till_selected_step_button")
        self.finish_program_button = builder.get_object("finish_program_button")

        self.delete_selected_step_button = builder.get_object("delete_selected_step_button")
        self.execute_selected_step_button = builder.get_object("execute_selected_step_button")
        self.selected_step_to_fetch_prog_button = builder.get_object("selected_step_to_fetch_prog_button")
        self.selected_step_to_return_prog_button = builder.get_object("selected_step_to_return_prog_button")

        self.list_title_label = builder.get_object("list_title_label")
        self.step_list_box = builder.get_object("step_list_box")

        self.warning_label = builder.get_object("warning_label")