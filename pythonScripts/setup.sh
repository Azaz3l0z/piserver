python3 -m venv ./venv
. ./venv/bin/activate
pip install pyinstaller
pip install -r requirements.txt
pyinstaller --onefile pyScraper.py
yes | mv ./dist/* .
yes | rm -r ./dist
yes | rm -r ./build
yes | rm pyScraper.spec
deactivate
yes | rm -r ./venv
mv pyScraper pyScraper.sh
