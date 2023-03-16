# -*- coding: utf-8 -*-

import gi

from sgi.object import Object
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DisplayFile():
    objects: list[Object]
    _display_file_list: Gtk.ListStore

    def __init__(self, display_file_list: Gtk.ListStore):
        self.objects = []
        self._display_file_list = display_file_list

    def clear_all(self):
        self.objects.clear()
        self._display_file_list.clear()

    def add(self, obj: Object):
        self.objects.append(obj)
        self._display_file_list.append([obj.name, str(obj.position)])

    def update(self, index: int):
        self._display_file_list[index][1] = str(self.objects[index].position)

