#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
pip install pygame pygame_menu pyinstaller
pyinstaller --onefile --add-data "assets:assets" __main__.py -n trktor
rm -rf venv
