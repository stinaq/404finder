# 404finder

How to set up:

    choco install python3
    choco install pip
    cd [place for github repo]

    pip install virtualenv
    virtualenv .

Every day setup:
---------------
    . venv/bin/activate
    cd App
    python3 process_links.py


Start simple HTTP server:
------------------------
    cd test
    python -m SimpleHTTPServer
