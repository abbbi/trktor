#!/bin/bash
set -e
pyinstaller --onefile --add-data "assets:assets" __main__.py -n trktor
