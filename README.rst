============
Evascripts
============

-----------------
Some scripts I've written. Mostly for Adafruit related things
-----------------

Notes for how to do things:
===========================

Updating adabot in circuitpython-org:

.. code-block:: shell

    git submodule update --init --recursive
    cd adabot
    git pull origin main
    git checkout main
    cd ..
    git add .
    git commit -m "Updated adabot"
    git push

Test
