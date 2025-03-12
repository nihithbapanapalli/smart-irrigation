#!/bin/bash
# Run rainfall.py in the background
python 3 Backend.py & python 3 Rainfall.py & python 3 soil.py & python 3 main.py

