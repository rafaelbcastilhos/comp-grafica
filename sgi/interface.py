# -*- coding: utf-8 -*-

import os
import gi
from sgi.displayfile import DisplayFile
from sgi.editor import Editor
from sgi.viewport import Viewport

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename=os.path.join(os.getcwd(), "interface", "interface.ui"))
class MainWindow(Gtk.Window):
    __gtype_name__ = "MainWindow"  # Nome da janela principal

    viewport: Viewport
    display_file: DisplayFile
    editor: Editor

    drawing_area: Gtk.DrawingArea = Gtk.Template.Child()
    point_button: Gtk.ToggleButton = Gtk.Template.Child()
    line_button: Gtk.ToggleButton = Gtk.Template.Child()
    polygon_button: Gtk.ToggleButton = Gtk.Template.Child()
    edges_button: Gtk.SpinButton = Gtk.Template.Child()
    display_file_list: Gtk.ListStore = Gtk.Template.Child()
    remove_button: Gtk.Button = Gtk.Template.Child()
    position_x_button: Gtk.SpinButton = Gtk.Template.Child()
    position_y_button: Gtk.SpinButton = Gtk.Template.Child()
    position_z_button: Gtk.SpinButton = Gtk.Template.Child()
    scale_x_button: Gtk.SpinButton = Gtk.Template.Child()
    scale_y_button: Gtk.SpinButton = Gtk.Template.Child()
    scale_z_button: Gtk.SpinButton = Gtk.Template.Child()
    rotation_x_button: Gtk.SpinButton = Gtk.Template.Child()
    rotation_y_button: Gtk.SpinButton = Gtk.Template.Child()
    rotation_z_button: Gtk.SpinButton = Gtk.Template.Child()

    def __init__(self):
        super().__init__()
        self.display_file = DisplayFile(self.display_file_list)
        self.editor = Editor(self,
                                            self.point_button,
                                            self.line_button,
                                            self.polygon_button,
                                            self.edges_button,
                                            self.remove_button,
                                            self.position_x_button,
                                            self.position_y_button,
                                            self.position_z_button,
                                            self.scale_x_button,
                                            self.scale_y_button,
                                            self.scale_z_button,
                                            self.rotation_x_button,
                                            self.rotation_y_button,
                                            self.rotation_z_button)
        self.viewport = Viewport(self, self.drawing_area)

        self.connect("destroy", Gtk.main_quit)