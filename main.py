# -*- coding: utf-8 -*-

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from source.interface import MainWindow

main_window = MainWindow()
main_window.show()

Gtk.main()