#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import xmltodict
from engine import Translator
# from ui import Interface

if __name__ == "__main__":

    with open("models/json/example.json", "r") as fl:
        example = json.load(fl)

    with open("models/jflap/eg01.jff", "r") as fl:
        jf = json.dumps(xmltodict.parse(fl))

    with open("models/json/eg02.json", "w+") as fl:
        fl.write(jf.replace("@", ""))

    test = Translator(example)
