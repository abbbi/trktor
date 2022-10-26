irm get.scoop.sh | iex
#irm get.scoop.sh -outfile 'install.ps1'
#.\install.ps1 -RunAsAdmin
scoop install python@3.8.1
git clone http://github.com/abbbi/trktor --depth 1
cd .\trktor
pip install requests pygame pygame_menu pyinstaller
pyinstaller --onefile --add-data "assets;assets" __main__.py -n trktor
