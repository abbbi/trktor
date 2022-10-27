#!/bin/bash
set -e
pip install pygame pygame_menu pyinstaller
pyinstaller --onefile --add-data "assets:assets" __main__.py -n trktor
