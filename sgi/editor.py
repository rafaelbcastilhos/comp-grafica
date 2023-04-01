# -*- coding: utf-8 -*-

import gi
from sgi.transform import Vector
from sgi.object import ObjectType, Object, Point, Line, Rectangle, object
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Editor():
    _main_window: None
    _focus_object: Object
    _temp_coords: list[Vector]
    _mode: ObjectType
    _width: float
    _color: list[float]
    _edges: int
    _rotation_anchor: Vector
    _edges_button: Gtk.SpinButton
    _point_button: Gtk.ToggleButton
    _line_button: Gtk.ToggleButton
    _polygon_button: Gtk.ToggleButton
    _color_button: Gtk.ColorButton
    _position_x_button: Gtk.SpinButton
    _position_y_button: Gtk.SpinButton
    _position_z_button: Gtk.SpinButton
    _scale_x_button: Gtk.SpinButton
    _scale_y_button: Gtk.SpinButton
    _scale_z_button: Gtk.SpinButton
    _rotation_x_button: Gtk.SpinButton
    _rotation_y_button: Gtk.SpinButton
    _rotation_z_button: Gtk.SpinButton
    _translate_x_button: Gtk.SpinButton
    _translate_y_button: Gtk.SpinButton
    _translate_z_button: Gtk.SpinButton
    _rescale_x_button: Gtk.SpinButton
    _rescale_y_button: Gtk.SpinButton
    _rescale_z_button: Gtk.SpinButton
    _rotation_button: Gtk.SpinButton
    _rotation_anchor_button: Gtk.Button
    _rotation_anchor_button_x: Gtk.SpinButton
    _rotation_anchor_button_y: Gtk.SpinButton
    _rotation_anchor_button_z: Gtk.SpinButton
    _user_call_lock: bool

    def __init__(self, main_window):
        self._main_window = main_window
        self._focus_object = None
        self._temp_coords = []
        self._mode = ObjectType.NULL
        self._width = 1.0
        self._color = [1.0, 1.0, 1.0]
        self._edges = 3
        self._rotation_anchor = None
        self._color_button = self._main_window.color_button
        self._edges_button = self._main_window.edges_button
        self._point_button = self._main_window.point_button
        self._line_button = self._main_window.line_button
        self._polygon_button = self._main_window.polygon_button
        self._position_x_button = self._main_window.position_x_button
        self._position_y_button = self._main_window.position_y_button
        self._position_z_button = self._main_window.position_z_button
        self._scale_x_button = self._main_window.scale_x_button
        self._scale_y_button = self._main_window.scale_y_button
        self._scale_z_button = self._main_window.scale_z_button
        self._rotation_x_button = self._main_window.rotation_x_button
        self._rotation_y_button = self._main_window.rotation_y_button
        self._rotation_z_button = self._main_window.rotation_z_button
        self._translate_x_button = self._main_window.translate_x_button
        self._translate_y_button = self._main_window.translate_y_button
        self._translate_z_button = self._main_window.translate_z_button
        self._rescale_x_button = self._main_window.rescale_x_button
        self._rescale_y_button = self._main_window.rescale_y_button
        self._rescale_z_button = self._main_window.rescale_z_button
        self._rotation_button = self._main_window.rotation_button
        self._rotation_anchor_button = self._main_window.rotation_anchor_button
        self._rotation_anchor_button_x = self._main_window.rotation_anchor_button_x
        self._rotation_anchor_button_y = self._main_window.rotation_anchor_button_y
        self._rotation_anchor_button_z = self._main_window.rotation_anchor_button_z

        self._color_button.connect("color-set", self.set_color)
        self._edges_button.connect("value-changed", self.set_edges)
        self._point_button.connect("toggled", self.set_type, ObjectType.POINT)
        self._line_button.connect("toggled", self.set_type, ObjectType.LINE)
        self._polygon_button.connect("toggled", self.set_type, ObjectType.POLYGON)
        self._main_window.remove_button.connect("clicked", self.remove)
        self._main_window.apply_translation_button.connect("clicked", self.translate)
        self._main_window.apply_scaling_button.connect("clicked", self.rescale)
        self._main_window.apply_rotation_button.connect("clicked", self.rotate)
        self._rotation_anchor_button.connect("clicked", self.change_rotation_anchor)
        self._position_x_button.connect("value-changed", self.update_position)
        self._position_y_button.connect("value-changed", self.update_position)
        self._position_z_button.connect("value-changed", self.update_position)
        self._scale_x_button.connect("value-changed", self.update_scale)
        self._scale_y_button.connect("value-changed", self.update_scale)
        self._scale_z_button.connect("value-changed", self.update_scale)
        self._rotation_x_button.connect("value-changed", self.update_rotation)
        self._rotation_y_button.connect("value-changed", self.update_rotation)
        self._rotation_z_button.connect("value-changed", self.update_rotation)
        self._rotation_anchor_button_x.connect("value-changed", self.update_rotation_anchor)
        self._rotation_anchor_button_y.connect("value-changed", self.update_rotation_anchor)
        self._rotation_anchor_button_z.connect("value-changed", self.update_rotation_anchor)

        self._user_call_lock = True

    def update_spin_buttons(self):
        self._user_call_lock = False
        self._position_x_button.set_value(self._focus_object.position.x)
        self._position_y_button.set_value(self._focus_object.position.y)
        self._position_z_button.set_value(self._focus_object.position.z)
        self._scale_x_button.set_value(self._focus_object.scale.x)
        self._scale_y_button.set_value(self._focus_object.scale.y)
        self._scale_z_button.set_value(self._focus_object.scale.z)
        self._rotation_x_button.set_value(self._focus_object.rotation.x)
        self._rotation_y_button.set_value(self._focus_object.rotation.y)
        self._rotation_z_button.set_value(self._focus_object.rotation.z)
        self._rotation_anchor_button_x.set_value(self._rotation_anchor.x)
        self._rotation_anchor_button_y.set_value(self._rotation_anchor.y)
        self._rotation_anchor_button_z.set_value(self._rotation_anchor.z)
        self._user_call_lock = True

    def update_toggle_buttons(self, mode: ObjectType):
        self._user_call_lock = False
        match mode:
            case ObjectType.POINT:
                self._point_button.set_active(False)
            case ObjectType.LINE:
                self._line_button.set_active(False)
            case ObjectType.POLYGON:
                self._polygon_button.set_active(False)
        self._user_call_lock = True

    def click(self, position: Vector):
        if self._mode != ObjectType.NULL:

            self._temp_coords.append(position)
            object_completed = False

            if self._mode == ObjectType.POINT and len(self._temp_coords) >= 1:
                self._main_window.display_file.add_object(Point(self._temp_coords[0], "Point", self._color))
                object_completed = True
            elif self._mode == ObjectType.LINE and len(self._temp_coords) >= 2:
                self._main_window.display_file.add_object(
                    Line(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Line",
                        self._color,
                        self._width))
                object_completed = True
            elif self._mode == ObjectType.RECTANGLE and len(self._temp_coords) >= 2:
                self._main_window.display_file.add_object(
                    Rectangle(
                        self._temp_coords[0],
                        self._temp_coords[1],
                        "Rectangle",
                        self._color,
                        self._width,
                        True))
                object_completed = True
            elif self._mode == ObjectType.POLYGON and len(self._temp_coords) >= self._edges:
                self._main_window.display_file.add_object(
                    object(
                        self._temp_coords.copy(),
                        "object",
                        self._color,
                        self._width,
                        ObjectType.POLYGON,
                        True))
                object_completed = True

            if object_completed:
                self._focus_object = self._main_window.display_file.objects[-1]
                self._rotation_anchor = self._focus_object.position
                self.update_spin_buttons()
                self._temp_coords.clear()

    def set_type(self, user_data, mode: ObjectType):
        if not self._user_call_lock:
            return

        self._focus_object = None

        if self._mode != mode:

            self.update_toggle_buttons(self._mode)
            self._mode = mode
        else:
            self._mode = ObjectType.NULL

        if self._mode == ObjectType.POLYGON:
            self._edges_button.set_editable(True)
        else:
            self._edges_button.set_editable(False)

        self._temp_coords.clear()

    def set_color(self, user_data):
        rgba = self._color_button.get_rgba()
        self._color = (rgba.red, rgba.green, rgba.blue)

    def set_edges(self, user_data):
        self._edges = self._edges_button.get_value_as_int()

    def remove(self, user_data):
        self._main_window.display_file.remove_last()

    def translate(self, user_data):
        if self._focus_object is not None:
            translation_x = self._translate_x_button.get_value()
            translation_y = self._translate_y_button.get_value()
            translation_z = self._translate_z_button.get_value()

            self._focus_object.translate(Vector(translation_x, translation_y, translation_z))
            self.update_spin_buttons()

            object_index = self._main_window.display_file.objects.index(self._focus_object)
            self._main_window.display_file.update_object_info(object_index)
            self._main_window.display_file.request_normalization()

    def rescale(self, user_data):
        if self._focus_object is not None:
            scale_x = self._rescale_x_button.get_value()
            scale_y = self._rescale_y_button.get_value()
            scale_z = self._rescale_z_button.get_value()

            self._focus_object.rescale(Vector(scale_x, scale_y, scale_z))
            self.update_spin_buttons()
            self._main_window.display_file.request_normalization()

    def rotate(self, user_data):
        if self._focus_object is not None:
            angle = self._rotation_button.get_value()

            self._focus_object.rotate(angle, self._rotation_anchor)
            self.update_spin_buttons()
            self._main_window.display_file.request_normalization()

    def change_rotation_anchor(self, user_data):
        match self._rotation_anchor_button.get_label():
            case "Object":
                self._rotation_anchor = Vector(0.0, 0.0, 0.0)
                self.update_spin_buttons()
                self._rotation_anchor_button.set_label("World")
            case "World":
                self._rotation_anchor.x = self._rotation_anchor_button_x.get_value()
                self._rotation_anchor.y = self._rotation_anchor_button_y.get_value()
                self._rotation_anchor.z = self._rotation_anchor_button_z.get_value()
                self._rotation_anchor_button_x.set_editable(True)
                self._rotation_anchor_button_y.set_editable(True)
                self._rotation_anchor_button_z.set_editable(True)
                self._rotation_anchor_button.set_label("Specified")
            case "Specified":
                if self._focus_object is not None:
                    self._rotation_anchor = self._focus_object.position
                else:
                    self._rotation_anchor = Vector(0.0, 0.0, 0.0)

                self._rotation_anchor_button_x.set_editable(False)
                self._rotation_anchor_button_y.set_editable(False)
                self._rotation_anchor_button_z.set_editable(False)
                self.update_spin_buttons()
                self._rotation_anchor_button.set_label("Object")

    def update_position(self, user_data):
        if self._user_call_lock and self._focus_object is not None:
            diff_x = self._position_x_button.get_value() - self._focus_object.position.x
            diff_y = self._position_y_button.get_value() - self._focus_object.position.y
            diff_z = self._position_z_button.get_value() - self._focus_object.position.z

            self._focus_object.translate(Vector(diff_x, diff_y, diff_z))

            object_index = self._main_window.display_file.objects.index(self._focus_object)
            self._main_window.display_file.update_object_info(object_index)
            self._main_window.display_file.request_normalization()

    def update_scale(self, user_data):
        if self._user_call_lock and self._focus_object is not None:
            diff_x = self._scale_x_button.get_value() / self._focus_object.scale.x
            diff_y = self._scale_y_button.get_value() / self._focus_object.scale.y
            diff_z = self._scale_z_button.get_value() / self._focus_object.scale.z

            self._focus_object.rescale(Vector(diff_x, diff_y, diff_z))
            self._main_window.display_file.request_normalization()

    def update_rotation(self, user_data):
        if self._user_call_lock and self._focus_object is not None:
            diff_z = self._rotation_z_button.get_value() - self._focus_object.rotation.z

            self._focus_object.rotate(diff_z)
            self._main_window.display_file.request_normalization()

    def update_rotation_anchor(self, user_data):
        if self._user_call_lock:
            anchor_x = self._rotation_anchor_button_x.get_value()
            anchor_y = self._rotation_anchor_button_y.get_value()
            anchor_z = self._rotation_anchor_button_z.get_value()

            self._rotation_anchor = Vector(anchor_x, anchor_y, anchor_z)
