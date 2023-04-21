# -*- coding: utf-8 -*-

from math import degrees
import gi
from sgi.wireframe import Object, Window, BezierCurve
from sgi.transform import Vector
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DisplayFile():
    objects: list[Object]
    _all_objects_normalized: bool
    _display_file_list: Gtk.ListStore

    def __init__(self, display_file_list):
        self.objects = []
        self._all_objects_normalized = False
        self._display_file_list = display_file_list

    def add(self, obj):
        self.objects.append(obj)
        self._display_file_list.append([obj.name, str(obj.position)])
        self._all_objects_normalized = False

    def update(self, index):
        self._display_file_list[index][1] = str(self.objects[index].position)

    def remove_last(self):
        if len(self.objects) > 0:
            self.objects.pop()
            self._display_file_list.remove(self._display_file_list[-1].iter)
            self._all_objects_normalized = False

    def request_normalization(self):
        self._all_objects_normalized = False

    def normalize_objects(self, window):
        if not self._all_objects_normalized:
            self._all_objects_normalized = True

            window_up = window.calculate_up_vector()
            rotation = degrees(window_up * Vector(0.0, 1.0, 0.0))

            if window_up.x > 0.0:
                rotation = 360 - rotation

            for obj in self.objects + [window]:
                obj.normalize(window.position, window.scale, rotation)
