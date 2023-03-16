# -*- coding: utf-8 -*-

import gi
from sgi.transform import Vector
from sgi.object import ObjectType, Object, Point, Line, Wireframe

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Editor():
    # Botões de edição.
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
    _user_call_lock: bool

    def __init__(self,
                 main_window,
                 point_button: Gtk.ToggleButton,
                 line_button: Gtk.ToggleButton,
                 polygon_button: Gtk.ToggleButton,
                 edges_button: Gtk.SpinButton,
                 remove_button: Gtk.Button,
                 position_x_button: Gtk.SpinButton,
                 position_y_button: Gtk.SpinButton,
                 position_z_button: Gtk.SpinButton,
                 scale_x_button: Gtk.SpinButton,
                 scale_y_button: Gtk.SpinButton,
                 scale_z_button: Gtk.SpinButton,
                 rotation_x_button: Gtk.SpinButton,
                 rotation_y_button: Gtk.SpinButton,
                 rotation_z_button: Gtk.SpinButton):

        self._main_window = main_window
        self._focus_object = None
        self._temp_coords = []
        self._mode = ObjectType.NULL
        self._width = 1.0
        self._color = [1.0, 1.0, 1.0]
        self._edges = 3
        self._rotation_anchor = None

        self._color_button = [1.0, 1.0, 1.0]
        self._edges_button = edges_button
        self._edges_button.connect("value-changed", self.set_edges)

        self._point_button = point_button
        self._line_button = line_button
        self._polygon_button = polygon_button

        self._point_button.connect("toggled", self.set_type, ObjectType.POINT)
        self._line_button.connect("toggled", self.set_type, ObjectType.LINE)
        self._polygon_button.connect("toggled", self.set_type, ObjectType.POLYGON)

        self._position_x_button = position_x_button
        self._position_y_button = position_y_button
        self._position_z_button = position_z_button
        self._scale_x_button = scale_x_button
        self._scale_y_button = scale_y_button
        self._scale_z_button = scale_z_button
        self._rotation_x_button = rotation_x_button
        self._rotation_y_button = rotation_y_button
        self._rotation_z_button = rotation_z_button

        remove_button.connect("clicked", self.clear)

        self._position_x_button.connect("value-changed", self.update_position)
        self._position_y_button.connect("value-changed", self.update_position)
        self._position_z_button.connect("value-changed", self.update_position)
        self._scale_x_button.connect("value-changed", self.update_scale)
        self._scale_y_button.connect("value-changed", self.update_scale)
        self._scale_z_button.connect("value-changed", self.update_scale)
        self._rotation_x_button.connect("value-changed", self.update_rotation)
        self._rotation_y_button.connect("value-changed", self.update_rotation)
        self._rotation_z_button.connect("value-changed", self.update_rotation)

        self._user_call_lock = True

    def update_toggle_buttons(self, mode: ObjectType):
        # Atualiza marcação
        self._user_call_lock = False
        match mode:
            case ObjectType.POINT:
                self._point_button.set_active(False)
            case ObjectType.LINE:
                self._line_button.set_active(False)
            case ObjectType.POLYGON:
                self._polygon_button.set_active(False)
        self._user_call_lock = True

    def update_spin_buttons(self):
        # Atualiza input numéricos.
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
        self._user_call_lock = True

    def click(self, position: Vector):
        # Processa input de clique no viewport.
        if self._mode != ObjectType.NULL:
            self._temp_coords.append(position)
            completed = False
            if self._mode == ObjectType.POINT and len(self._temp_coords) >= 1:
                self._main_window.display_file.add(Point(self._temp_coords[0], "Point", self._color))
                completed = True
            elif self._mode == ObjectType.LINE and len(self._temp_coords) >= 2:
                self._main_window.display_file.add(
                    Line(self._temp_coords[0], self._temp_coords[1], "Line", self._color, self._width))
                completed = True
            elif self._mode == ObjectType.POLYGON and len(self._temp_coords) >= self._edges:
                self._main_window.display_file.add(
                    Wireframe(self._temp_coords.copy(), "Wireframe", self._color, self._width))
                completed = True

            if completed:
                self._focus_object = self._main_window.display_file.objects[-1]
                self._rotation_anchor = self._focus_object.position
                self.update_spin_buttons()
                self._temp_coords.clear()

    def set_type(self, user_data, mode: ObjectType):
        # Define o tipo.
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

    def set_width(self, user_data):
        self._width = self._width_button.get_value()

    def set_color(self, user_data):
        rgba = Gdk.RGBA(red=1.000000, green=1.000000, blue=1.000000, alpha=1.000000)
        self._color = (rgba.red, rgba.green, rgba.blue)

    def set_edges(self, user_data):
        self._edges = self._edges_button.get_value_as_int()

    def clear(self, user_data):
        self._main_window.display_file.clear_all()

    def update_scale(self, user_data):
        # Atualiza a escala
        if self._user_call_lock and self._focus_object is not None:
            diff_x = self._scale_x_button.get_value() / self._focus_object.scale.x
            diff_y = self._scale_y_button.get_value() / self._focus_object.scale.y
            diff_z = self._scale_z_button.get_value() / self._focus_object.scale.z

            self._focus_object.rescale(Vector(diff_x, diff_y, diff_z))

    def update_position(self, user_data):
        # Atualiza a posição
        if self._user_call_lock and self._focus_object is not None:
            diff_x = self._position_x_button.get_value() - self._focus_object.position.x
            diff_y = self._position_y_button.get_value() - self._focus_object.position.y
            diff_z = self._position_z_button.get_value() - self._focus_object.position.z

            self._focus_object.translate(Vector(diff_x, diff_y, diff_z))

            object_index = self._main_window.display_file.objects.index(self._focus_object)
            self._main_window.display_file.update(object_index)

    def update_rotation_anchor(self, user_data):
        # Atualiza o ponto de ancoragem da rotação.
        if self._user_call_lock:
            anchor_x = self._rotation_anchor_button_x.get_value()
            anchor_y = self._rotation_anchor_button_y.get_value()
            anchor_z = self._rotation_anchor_button_z.get_value()

            self._rotation_anchor = Vector(anchor_x, anchor_y, anchor_z)

    def update_rotation(self, user_data):
        # Atualiza a rotação
        if self._user_call_lock and self._focus_object is not None:
            diff_x = self._rotation_x_button.get_value() - self._focus_object.rotation.x
            diff_y = self._rotation_y_button.get_value() - self._focus_object.rotation.y
            diff_z = self._rotation_z_button.get_value() - self._focus_object.rotation.z

            self._focus_object.rotate(diff_z)