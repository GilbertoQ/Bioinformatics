#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os

os.system("cd aces")
os.system("obabel *.mol2 -opdbqt -m")