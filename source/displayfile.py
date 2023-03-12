# -*- coding: utf-8 -*-

import gi

from source.wireframe import Object
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DisplayFileHandler():
    objects: list[Object]
    _display_file_list: Gtk.ListStore

    def __init__(self, display_file_list: Gtk.ListStore) -> None:
        self.objects = []
        self._display_file_list = display_file_list

    def add_object(self, obj: Object) -> None:
        self.objects.append(obj)
        self._display_file_list.append([obj.name, str(obj.position)])

    def update_object_info(self, index: int) -> None:
        self._display_file_list[index][1] = str(self.objects[index].position)

    def clear_all(self) -> None:
        self.objects.clear()
        self._display_file_list.clear()