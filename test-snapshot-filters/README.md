You'll want to do something like

PYTHONPATH=/Users/rjose/products/ratchet/modules/python python test.py

The snapshot filters expect a git repo to store their snapshots in. You should
do this to set it up:

    mkdir tmp && cd tmp && git init .

