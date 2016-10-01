#!/usr/bin/env python
# -*- coding: utf-8 -*-

from engine import Translator

if __name__ == "__main__":

    with open("models/jflap/eg01.jff", "r") as fl:
        # example_jflap = json.loads(json.dumps(xmltodict.parse(fl)))
        example_jflap = fl.read()

    with open("models/json/example.json", "r") as fl:
        # example_json = json.load(fl)
        example_json = fl.read()

    test = Translator(example_json)
    test.jff2json()
    test.convert()

