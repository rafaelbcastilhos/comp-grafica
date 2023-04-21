# -*- coding: utf-8 -*-

import os
import gi
from sgi.displayfile import DisplayFile
from sgi.editor import Editor
from sgi.viewport import Viewport
from sgi.transform import Vector
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


@Gtk.Template(filename=os.path.join(os.getcwd(), "interface", "interface.ui"))
class MainWindow(Gtk.Window):
    __gtype_name__ = "MainWindow"  # Nome da janela principal

    viewport: Viewport
    display_file: DisplayFile
    editor: Editor
    viewport_drawing_area: Gtk.DrawingArea = Gtk.Template.Child()
    file_button: Gtk.MenuItem = Gtk.Template.Child()
    point_button: Gtk.ToggleButton = Gtk.Template.Child()
    line_button: Gtk.ToggleButton = Gtk.Template.Child()
    polygon_button: Gtk.ToggleButton = Gtk.Template.Child()
    bezier_curve_button: Gtk.ToggleButton = Gtk.Template.Child()
    spline_curve_button: Gtk.ToggleButton = Gtk.Template.Child()
    width_button: Gtk.SpinButton = Gtk.Template.Child()
    color_button: Gtk.ColorButton = Gtk.Template.Child()
    edges_button: Gtk.SpinButton = Gtk.Template.Child()
    fill_button: Gtk.CheckButton = Gtk.Template.Child()
    curve_point_count_button: Gtk.SpinButton = Gtk.Template.Child()
    curve_step_count_button: Gtk.SpinButton = Gtk.Template.Child()
    spline_point_count_button: Gtk.SpinButton = Gtk.Template.Child()
    spline_step_count_button: Gtk.SpinButton = Gtk.Template.Child()
    closed_spline_button: Gtk.CheckButton = Gtk.Template.Child()
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
    translate_x_button: Gtk.SpinButton = Gtk.Template.Child()
    translate_y_button: Gtk.SpinButton = Gtk.Template.Child()
    translate_z_button: Gtk.SpinButton = Gtk.Template.Child()
    apply_translation_button: Gtk.Button = Gtk.Template.Child()
    rescale_x_button: Gtk.SpinButton = Gtk.Template.Child()
    rescale_y_button: Gtk.SpinButton = Gtk.Template.Child()
    rescale_z_button: Gtk.SpinButton = Gtk.Template.Child()
    apply_scaling_button: Gtk.Button = Gtk.Template.Child()
    rotation_button: Gtk.SpinButton = Gtk.Template.Child()
    apply_rotation_button: Gtk.Button = Gtk.Template.Child()
    rotation_anchor_button: Gtk.Button = Gtk.Template.Child()
    rotation_anchor_button_x: Gtk.SpinButton = Gtk.Template.Child()
    rotation_anchor_button_y: Gtk.SpinButton = Gtk.Template.Child()
    rotation_anchor_button_z: Gtk.SpinButton = Gtk.Template.Child()
    clipping_method_button: Gtk.ToggleButton = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.maximize()

        self.display_file = DisplayFile(self.display_file_list)
        self.editor = Editor(self)
        self.viewport = Viewport(self, self.viewport_drawing_area, Vector(25.0, 25.0, 0.0))

        self.connect("key-press-event", self.on_input_key)
        self.connect("destroy", Gtk.main_quit)

    def on_input_key(self, widget, event):
        self.editor.input_key(event.string)
