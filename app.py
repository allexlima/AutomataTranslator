#!/usr/bin/env python
# -*- coding: utf-8 -*-

from engine import Translator

if __name__ == "__main__":

    with open("models/jflap/eg02.jff", "r") as fl:
        example_jflap = fl.read()

    with open("models/json/example.json", "r") as fl:
        example_json = fl.read()

    test = Translator(example_jflap)
    test.jff2json()
    test.convert()
