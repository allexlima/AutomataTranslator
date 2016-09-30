#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from engine import Engine
# from ui import Interface

if __name__ == "__main__":

    with open("models/json/example.json", "r") as fl:
        example = json.load(fl)

    test = Engine(example)
    if test.check_syntax() is not True:
        print test.check_syntax()
