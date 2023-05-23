# -*- coding: utf-8 -*-

from math import degrees
from random import randrange
import gi
from sgi.object import Object, Window, Surface
from sgi.file_system import FileSystem
from sgi.transform import Vector
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# Nesta classe os objetos seriam armazenados e transferidos para o viewport quando necessário.
class DisplayFile():
    # Atributos públicos
    objects: list[Object]

    # Atributos privados
    _all_objects_normalized: bool
    _display_file_list: Gtk.ListStore
    _file_system: FileSystem

    def __init__(self, display_file_list: Gtk.ListStore):
        self.objects = []
        self._all_objects_normalized = False
        self._display_file_list = display_file_list
        self._file_system = FileSystem()

    def add(self, obj: Object):
        # Adiciona um objeto.
        self.objects.append(obj)
        self._display_file_list.append([obj.name, str(obj.position)])
        self._all_objects_normalized = False

    def update(self, index: int):
        # Atualiza as informações de um objeto.
        self._display_file_list[index][1] = str(self.objects[index].position)

    def remove_last(self):
        # Remove último objeto.
        if len(self.objects) > 0:
            self.objects.pop()
            self._display_file_list.remove(self._display_file_list[-1].iter)
            self._all_objects_normalized = False

    def normalize_objects(self, window: Window):
        # Normaliza todos os objetos.
        window_up = window.calculate_y_projected_vector()
        rotation = degrees(window_up * Vector(0.0, 1.0, 0.0))

        if window_up.x > 0.0:
            rotation = 360 - rotation

        for obj in self.objects + [window]:
            obj.normalize(window.position, window.scale, rotation)

    def load(self, file_name: str):
        # Carrega um arquivo.
        loaded = self._file_system.load_scene(file_name)

        for obj in loaded:
            self.add(obj)

    def save(self, file_name: str):
        # Carrega um arquivo.
        self._file_system.save_scene(file_name, self.objects)
