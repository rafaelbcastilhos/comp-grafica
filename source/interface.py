# -*- coding: utf-8 -*-

import os
import gi
from source.displayfile import DisplayFileHandler
from source.editor import EditorHandler
from source.viewport import ViewportHandler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename=os.path.join(os.getcwd(), "interface", "interface.ui"))
class MainWindow(Gtk.Window):
    __gtype_name__ = "MainWindow"  # Nome da janela principal

    viewport_handler: ViewportHandler
    display_file_handler: DisplayFileHandler
    editor_handler: EditorHandler

    viewport_drawing_area: Gtk.DrawingArea = Gtk.Template.Child()
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

    def __init__(self) -> None:
        super().__init__()
        self.display_file_handler = DisplayFileHandler(self.display_file_list)
        self.editor_handler = EditorHandler(self,
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
        self.viewport_handler = ViewportHandler(self, self.viewport_drawing_area)

        self.connect("destroy", Gtk.main_quit)